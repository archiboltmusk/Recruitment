import re
import io
import os
import shutil
import socket
import subprocess
import tempfile
import ipaddress
import requests
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Any, Optional, List
from pypdf import PdfReader

MAX_PDF_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit to prevent DoS

DATE_TOKEN_RE = re.compile(
    r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[,\s]+\d{4})\b",
    re.IGNORECASE,
)


def _parse_indian_date(raw: str) -> Optional[datetime]:
    cleaned = re.sub(r"(\d{1,2})(?:st|nd|rd|th)\b", r"\1", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned.replace(",", " ")).strip()
    for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%y", "%d/%m/%y", "%d-%m-%y", "%d %b %Y", "%d %B %Y"):
        try:
            dt = datetime.strptime(cleaned, fmt)
            if 2024 <= dt.year <= 2030:
                return dt
        except ValueError:
            continue
    return None


class GovtNotificationPDFParser:
    @staticmethod
    def is_safe_url(url: str) -> bool:
        """Validates that a URL does not point to internal, private, or loopback network addresses (SSRF Protection)."""
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                return False

            hostname = parsed.hostname
            if not hostname:
                return False

            if hostname.lower() in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
                return False

            addr_info = socket.getaddrinfo(hostname, None)
            for family, _, _, _, sockaddr in addr_info:
                ip_str = sockaddr[0]
                ip_obj = ipaddress.ip_address(ip_str)
                if (
                    ip_obj.is_private
                    or ip_obj.is_loopback
                    or ip_obj.is_link_local
                    or ip_obj.is_multicast
                    or ip_obj.is_reserved
                ):
                    return False
            return True
        except Exception:
            return False

    @staticmethod
    def _ocr_pdf_bytes(pdf_bytes: bytes) -> str:
        """Best-effort OCR fallback for scanned WB govt PDFs when pdftoppm + tesseract are installed."""
        if not (shutil.which("pdftoppm") and shutil.which("tesseract")):
            return ""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                pdf_path = os.path.join(tmpdir, "notice.pdf")
                with open(pdf_path, "wb") as f:
                    f.write(pdf_bytes)
                subprocess.run(
                    ["pdftoppm", "-png", "-r", "200", "-f", "1", "-l", "4", pdf_path, os.path.join(tmpdir, "page")],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=20,
                )
                ocr_chunks: List[str] = []
                for fname in sorted(os.listdir(tmpdir)):
                    if fname.endswith(".png"):
                        res = subprocess.run(
                            ["tesseract", os.path.join(tmpdir, fname), "stdout", "-l", "eng"],
                            capture_output=True,
                            text=True,
                            timeout=15,
                        )
                        if res.stdout:
                            ocr_chunks.append(res.stdout)
                return "\n".join(ocr_chunks)
        except Exception:
            return ""

    @classmethod
    def extract_text_from_bytes(cls, pdf_bytes: bytes) -> str:
        """Extracts text from PDF bytes using pypdf, with OCR fallback for scanned notices."""
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        max_pages = min(10, len(reader.pages))
        for i in range(max_pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
        if len(re.sub(r"\s+", "", text)) < 60:
            ocr_text = cls._ocr_pdf_bytes(pdf_bytes)
            if len(ocr_text.strip()) > len(text.strip()):
                return ocr_text
        return text

    @classmethod
    def extract_from_url(cls, url: str) -> str:
        if not cls.is_safe_url(url):
            raise ValueError("Invalid or restricted URL. Access to local, private, or non-HTTP addresses is blocked.")

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"}
        with requests.get(url, headers=headers, stream=True, timeout=12) as resp:
            resp.raise_for_status()
            cl = resp.headers.get("Content-Length")
            if cl and int(cl) > MAX_PDF_SIZE_BYTES:
                raise ValueError("PDF file size exceeds maximum permitted limit (15 MB).")

            pdf_bytes = io.BytesIO()
            downloaded = 0
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    downloaded += len(chunk)
                    if downloaded > MAX_PDF_SIZE_BYTES:
                        raise ValueError("PDF stream exceeded 15 MB limit.")
                    pdf_bytes.write(chunk)

            return cls.extract_text_from_bytes(pdf_bytes.getvalue())

    @classmethod
    def parse_notice_text(cls, text: str) -> Dict[str, Any]:
        """Analyzes text of a recruitment gazette (including WB & scanned notices) and extracts key parameters."""
        extracted: Dict[str, Any] = {
            "title": "Medical Officer Recruitment",
            "qualification": "MBBS",
            "total_posts": None,
            "min_age": 21,
            "max_age": 35,
            "pay_scale": None,
            "last_date": None,
            "exam_date": None,
            "memo_number": None,
            "bond_years": 0,
            "bond_penalty_amount": "No Bond",
            "selection_mode": "Written Exam + Interview",
            "category_seats": {},
            "application_fee": "As per notification",
            "key_clauses": [],
            "parsed_confident": False,
        }

        signals = 0

        # 0. Memo / Advertisement Number
        memo_match = re.search(
            r"(?:Memo(?:randum)?\s*(?:No\.?|#)?|Advt\.?\s*No\.?)\s*[:=-]?\s*([A-Za-z0-9/_().-]{5,60})",
            text,
            re.IGNORECASE,
        )
        if memo_match:
            memo_val = memo_match.group(1).strip(" .,:;")
            memo_date_m = re.search(r"Date[d]?\s*[:=-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", text[memo_match.end():memo_match.end() + 120], re.IGNORECASE)
            extracted["memo_number"] = f"{memo_val} ({memo_date_m.group(1)})" if memo_date_m else memo_val
            signals += 1

        # 1. Total Posts Detection (handles "Total -37", "Total Number of post :- 04", etc.)
        posts_match = re.search(
            r"(?:total\s*(?:no\.?\s*of)?\s*(?:posts?|vacanc(?:y|ies)|seats?)?|total\s*[-–:=])\s*[:=-]?\s*(\d+)",
            text,
            re.IGNORECASE,
        )
        if not posts_match:
            posts_match = re.search(
                r"(\d+)\s*(?:nos?\.?\s*of\s*)?(?:posts?|vacancies|seats?)\s*(?:of\s*(?:medical officer|gdmo|cgdmo|doctor))?",
                text,
                re.IGNORECASE,
            )
        if posts_match:
            post_num = int(posts_match.group(1))
            if 0 < post_num <= 5000:
                extracted["total_posts"] = post_num
                signals += 1

        # 2. Qualification (header-aware so footnotes don't overwrite MBBS GDMO notices)
        header_text = text[:800]
        has_pg_header = bool(re.search(r"\b(?:MD/MS|MD|MS|DNB|Specialist|Senior\s+Resident|Sr\.?\s*Resident)\b", header_text, re.IGNORECASE))
        has_mbbs_header = bool(re.search(r"\b(?:MBBS|GDMO|CGDMO|Junior\s+Resident|Jr\.?\s*Resident|House\s*Staff)\b", header_text, re.IGNORECASE))
        if has_pg_header and not has_mbbs_header:
            extracted["qualification"] = "MD/MS"
        elif has_mbbs_header and not has_pg_header:
            extracted["qualification"] = "MBBS"
        elif has_pg_header and has_mbbs_header:
            extracted["qualification"] = "MBBS / MD/MS" if re.search(r"\b(?:GDMO|CGDMO|Junior\s+Resident|Medical\s+Officer)\b", header_text, re.IGNORECASE) else "MD/MS"
        elif re.search(r"\b(?:MD|MS|DNB|Specialist|Senior\s+Resident|Sr\.?\s*Resident)\b", text, re.IGNORECASE):
            extracted["qualification"] = "MD/MS"
        elif re.search(r"\b(?:BAMS|BHMS|BUMS|AYUSH)\b", text, re.IGNORECASE):
            extracted["qualification"] = "AYUSH"
        elif re.search(r"\b(?:BDS|Dental)\b", text, re.IGNORECASE):
            extracted["qualification"] = "BDS"
        else:
            extracted["qualification"] = "MBBS"

        # 3. Age Limit (handles "Below 64 years", "21 to 40 years", "upper age limit 37 years")
        below_age = re.search(r"\bbelow\s+(\d{2})\s+years?\b", text, re.IGNORECASE)
        range_age = re.search(r"\b(?:minimum\s+)?(\d{2})\s*(?:years?|yrs?)?\s*(?:to|[-–])\s*(?:maximum\s+)?(\d{2})\s*(?:years?|yrs?)\b", text, re.IGNORECASE)
        upper_age = re.search(
            r"(?:upper\s*age\s*limit|maximum\s*age(?:\s*limit)?|not\s*exceeding|age\s*not\s*more\s*than)\s*[:=-]?\s*(\d{2})\s*(?:years?|yrs?)",
            text,
            re.IGNORECASE,
        )
        if below_age:
            extracted["max_age"] = int(below_age.group(1)) - 1
        elif range_age:
            extracted["min_age"] = int(range_age.group(1))
            extracted["max_age"] = int(range_age.group(2))
        elif upper_age:
            extracted["max_age"] = int(upper_age.group(1))

        # 4. Pay Scale / Consolidated Remuneration ("Rs. 60,000/-", "60000.00 per month", "Level-16")
        pay_match = re.search(
            r"(?:Rs\.?|INR|₹)\s*([\d,]{4,10})(?:\.\d{2})?\s*/?-?\s*(?:per\s*month|p\.?m\.?|consolidated)?",
            text,
            re.IGNORECASE,
        )
        level_match = re.search(r"(?:Pay\s*Matrix\s*)?Level[-\s]*(10B|10|11|16)\b", text, re.IGNORECASE)
        if pay_match:
            amt = pay_match.group(1).replace(",", "")
            if amt.isdigit() and int(amt) >= 15000:
                extracted["pay_scale"] = f"₹{int(amt):,}/month (Consolidated)"
                signals += 1
        elif level_match:
            extracted["pay_scale"] = f"Pay Level {level_match.group(1)}"
            signals += 1

        # 5. Dates (Walk-in windows & Application Last Dates)
        walkin_block = re.search(
            r"walk[-\s]?in[-\s]?interview.{0,160}",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if walkin_block:
            walkin_dates = [d for tok in DATE_TOKEN_RE.findall(walkin_block.group(0)) if (d := _parse_indian_date(tok))]
            if walkin_dates:
                extracted["exam_date"] = min(walkin_dates).strftime("%Y-%m-%d")
                extracted["last_date"] = max(walkin_dates).strftime("%Y-%m-%d")
                signals += 1

        if not extracted["last_date"]:
            last_date_ctx = re.search(
                r"(?:last\s*date(?:\s*of\s*(?:full\s*)?(?:submission|registration|application))?|closing\s*date|submit(?:ted)?\s*(?:up\s*to|on\s*or\s*before))\s*[:=-]?\s*(?:midnight\s*of\s*)?([^\n]{5,60})",
                text,
                re.IGNORECASE,
            )
            if last_date_ctx:
                found_dates = [d for tok in DATE_TOKEN_RE.findall(last_date_ctx.group(1)) if (d := _parse_indian_date(tok))]
                if found_dates:
                    extracted["last_date"] = max(found_dates).strftime("%Y-%m-%d")
                    signals += 1

        # 6. Mandatory Service / Rural Bond
        bond_match = re.search(r"(?:bond|service\s*agreement|compulsory\s*(?:rural)?\s*service).*?(?:period\s*of|for)\s*(\d+)\s*years?", text, re.IGNORECASE | re.DOTALL)
        if bond_match:
            extracted["bond_years"] = int(bond_match.group(1))
            extracted["bond_penalty_amount"] = f"{extracted['bond_years']} Year(s) Mandatory Service Bond"

        penalty_match = re.search(r"(?:penalty|bond\s*amount|liquidated\s*damages|sum\s*of)\s*(?:Rs\.?|INR|₹)\s*([\d,]+(?:\s*lakh(?:s)?)?)", text, re.IGNORECASE)
        if penalty_match:
            penalty_val = penalty_match.group(1)
            extracted["bond_penalty_amount"] = f"{extracted['bond_years'] or 1} Year Bond (Penalty: ₹{penalty_val})"

        # 7. Selection Mode
        if re.search(r"walk[-\s]?in[-\s]?interview", text, re.IGNORECASE):
            extracted["selection_mode"] = "Direct Walk-in Interview"
        elif re.search(r"computer\s*based\s*(?:test|examination)|cbt|online\s*exam", text, re.IGNORECASE):
            extracted["selection_mode"] = "Computer Based Test (CBT) + Interview"
        elif re.search(r"written\s*(?:examination|test)", text, re.IGNORECASE):
            extracted["selection_mode"] = "Written Examination + Interview"
        elif re.search(r"merit\s*(?:based|list)|academic\s*merit", text, re.IGNORECASE):
            extracted["selection_mode"] = "Merit Based (Marks in MBBS)"

        # 8. Category Seat Breakdown (supports "UR - 20", "SC - 07", "OBC - 10", "UR(EC)-2")
        categories = ["UR", "OBC", "SC", "ST", "EWS"]
        seats_dict: Dict[str, int] = {}
        for cat in categories:
            cat_match = re.search(rf"\b{cat}\b\s*[-–:=]+\s*(\d+)", text, re.IGNORECASE)
            if cat_match:
                seats_dict[cat] = int(cat_match.group(1))
        if seats_dict:
            extracted["category_seats"] = seats_dict

        # 9. Application Fee
        fee_match = re.search(r"(?:application\s*fees?|prescribed\s*fee)\s*(?:of|:=-)?\s*(?:Rs\.?|INR|₹)?\s*(\d{2,4})/-?", text, re.IGNORECASE)
        if fee_match:
            extracted["application_fee"] = f"₹{fee_match.group(1)}"
        elif re.search(r"zero\s*(?:application\s*)?fee|no\s*application\s*fee", text, re.IGNORECASE):
            extracted["application_fee"] = "Zero Application Fee"

        extracted["parsed_confident"] = signals >= 2
        return extracted
