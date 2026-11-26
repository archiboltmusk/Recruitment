import re
import io
import os
import shutil
import socket
import subprocess
import tempfile
import ipaddress
import requests
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
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
            if 2015 <= dt.year <= 2030:
                return dt
        except ValueError:
            continue
    return None


def _parse_pdf_meta_date(raw: Any) -> Optional[datetime]:
    s = str(raw or "").strip()
    m = re.search(r"D:(\d{4})(\d{2})(\d{2})", s)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
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
        """Best-effort OCR fallback for scanned WB govt PDFs via local tesseract or optional cloud Vision/OCR API."""
        if shutil.which("pdftoppm") and shutil.which("tesseract"):
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
                    avail_langs = set()
                    try:
                        lang_res = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True, timeout=5)
                        avail_langs = {ln.strip() for ln in (lang_res.stdout or "").splitlines() if ln.strip() and not ln.startswith("List of")}
                    except Exception:
                        avail_langs = {"eng"}
                    lang_arg = "+".join([l for l in ("eng", "hin", "ben") if l in avail_langs]) or "eng"
                    ocr_chunks: List[str] = []
                    for fname in sorted(os.listdir(tmpdir)):
                        if fname.endswith(".png"):
                            res = subprocess.run(
                                ["tesseract", os.path.join(tmpdir, fname), "stdout", "-l", lang_arg],
                                capture_output=True,
                                text=True,
                                timeout=15,
                            )
                            if res.stdout:
                                ocr_chunks.append(res.stdout)
                    if ocr_chunks:
                        return "\n".join(ocr_chunks)
            except Exception:
                pass

        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        if gemini_key and len(pdf_bytes) <= 4 * 1024 * 1024:
            try:
                import base64
                b64 = base64.b64encode(pdf_bytes).decode("ascii")
                res = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
                    json={
                        "contents": [{
                            "parts": [
                                {"text": "Extract all text verbatim from this Indian government medical recruitment PDF notice (memo number, posts, age limit, pay, walk-in/last date)."},
                                {"inline_data": {"mime_type": "application/pdf", "data": b64}},
                            ]
                        }]
                    },
                    timeout=15,
                )
                if res.ok:
                    cands = res.json().get("candidates") or []
                    if cands:
                        parts = (cands[0].get("content") or {}).get("parts") or []
                        txt = "\n".join(p.get("text", "") for p in parts if p.get("text"))
                        if txt.strip():
                            return txt
            except Exception:
                pass

        ocr_space_key = os.getenv("OCR_SPACE_API_KEY", "").strip()
        if ocr_space_key and len(pdf_bytes) <= 1024 * 1024:
            try:
                res = requests.post(
                    "https://api.ocr.space/parse/image",
                    data={"apikey": ocr_space_key, "language": "eng", "filetype": "PDF"},
                    files={"file": ("notice.pdf", pdf_bytes, "application/pdf")},
                    timeout=15,
                )
                if res.ok:
                    parsed = res.json().get("ParsedResults") or []
                    txt = "\n".join(p.get("ParsedText", "") for p in parsed)
                    if txt.strip():
                        return txt
            except Exception:
                pass
        return ""

    @classmethod
    def extract_text_and_meta_from_bytes(cls, pdf_bytes: bytes) -> Dict[str, Any]:
        """Extracts text and PDF CreationDate/ModDate metadata from PDF bytes."""
        reader = PdfReader(io.BytesIO(pdf_bytes))
        meta = reader.metadata or {}
        pdf_creation_date = _parse_pdf_meta_date(meta.get("/CreationDate")) or _parse_pdf_meta_date(meta.get("/ModDate"))
        text = ""
        max_pages = min(10, len(reader.pages))
        for i in range(max_pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
        if len(re.sub(r"\s+", "", text)) < 60:
            ocr_text = cls._ocr_pdf_bytes(pdf_bytes)
            if len(ocr_text.strip()) > len(text.strip()):
                text = ocr_text
        return {"text": text, "pdf_creation_date": pdf_creation_date}

    @classmethod
    def extract_text_from_bytes(cls, pdf_bytes: bytes) -> str:
        """Extracts text from PDF bytes using pypdf, with OCR fallback for scanned notices."""
        return cls.extract_text_and_meta_from_bytes(pdf_bytes)["text"]

    @staticmethod
    def normalize_pdf_url(url: str) -> str:
        u = (url or "").strip()
        m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=)([A-Za-z0-9_-]{15,})", u)
        if m:
            return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
        return u

    @staticmethod
    def _is_trusted_indian_portal(url: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        return host.endswith((".gov.in", ".nic.in", ".edu.in", ".ac.in", ".org.in"))

    @classmethod
    def extract_from_url_with_meta(cls, url: str) -> Dict[str, Any]:
        url = cls.normalize_pdf_url(url)
        if not cls.is_safe_url(url):
            raise ValueError("Invalid or restricted URL. Access to local, private, or non-HTTP addresses is blocked.")

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
        current_url = url
        verify_tls = True
        for _ in range(5):
            try:
                resp_cm = requests.get(current_url, headers=headers, stream=True, timeout=14, allow_redirects=False, verify=verify_tls)
            except requests.exceptions.SSLError:
                if verify_tls and cls._is_trusted_indian_portal(current_url):
                    import urllib3
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    verify_tls = False
                    resp_cm = requests.get(current_url, headers=headers, stream=True, timeout=14, allow_redirects=False, verify=False)
                else:
                    raise
            with resp_cm as resp:
                if resp.is_redirect or resp.status_code in (301, 302, 303, 307, 308):
                    loc = resp.headers.get("Location", "")
                    from urllib.parse import urljoin
                    next_url = urljoin(current_url, loc)
                    if not cls.is_safe_url(next_url):
                        raise ValueError("Redirect target blocked by SSRF policy.")
                    current_url = next_url
                    continue
                resp.raise_for_status()
                cl = resp.headers.get("Content-Length")
                if cl and int(cl) > MAX_PDF_SIZE_BYTES:
                    raise ValueError("PDF file size exceeds maximum permitted limit (15 MB).")

                last_modified = None
                lm_raw = resp.headers.get("Last-Modified")
                if lm_raw:
                    try:
                        lm_dt = parsedate_to_datetime(lm_raw)
                        last_modified = lm_dt.replace(tzinfo=None) if lm_dt else None
                    except Exception:
                        last_modified = None

                ctype = (resp.headers.get("Content-Type") or "").lower()
                if "text/html" in ctype and "drive.google.com" in current_url:
                    return {"text": "", "pdf_creation_date": None, "last_modified": last_modified}

                pdf_bytes = io.BytesIO()
                downloaded = 0
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        downloaded += len(chunk)
                        if downloaded > MAX_PDF_SIZE_BYTES:
                            raise ValueError("PDF stream exceeded 15 MB limit.")
                        pdf_bytes.write(chunk)

                res = cls.extract_text_and_meta_from_bytes(pdf_bytes.getvalue())
                res["last_modified"] = last_modified
                return res
        raise ValueError("Too many redirects while fetching PDF URL.")

    @classmethod
    def extract_from_url(cls, url: str) -> str:
        return cls.extract_from_url_with_meta(url)["text"]

    @classmethod
    def parse_notice_text(cls, text: str) -> Dict[str, Any]:
        """Analyzes text of a recruitment gazette (including WB & scanned notices) and extracts key parameters."""
        extracted: Dict[str, Any] = {
            "title": "Medical Officer Recruitment",
            "qualification": "MBBS",
            "total_posts": None,
            "min_age": 21,
            "max_age": 35,
            "age_cutoff_date": None,
            "experience_years_required": 0,
            "pay_scale": None,
            "last_date": None,
            "exam_date": None,
            "memo_number": None,
            "bond_years": 0,
            "bond_penalty_amount": "No Bond",
            "selection_mode": "Written Exam + Interview",
            "category_seats": {},
            "cadre_breakdown": [],
            "application_fee": "As per notification",
            "key_clauses": [],
            "parsed_confident": False,
            "is_scanned": len(re.sub(r"\s+", "", text or "")) < 60,
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

        # 1. Total Posts Detection (handles "Total -37", "Total Number of post :- 04", "No. of Posts: 01(One)", etc.)
        posts_match = re.search(
            r"(?:total\s*(?:no\.?\s*of)?\s*(?:posts?|vacanc(?:y|ies)|seats?)?|(?:total\s*)?no\.?\s*of\s*(?:posts?|vacanc(?:y|ies)|seats?)|total\s*[-–:=])\s*[:=-]?\s*(\d+)",
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

        # 2. Qualification (header + Essential Qualification section aware so MD/MS/DNB isn't mislabeled MBBS)
        header_text = text[:1200]
        qual_sec_m = re.search(r"(?:essential\s+)?qualifications?\s*[:\-].{0,350}", text, re.IGNORECASE | re.DOTALL)
        qual_scope = f"{header_text}\n{qual_sec_m.group(0) if qual_sec_m else ''}"
        is_acad_jr = bool(re.search(r"\b(?:academic\s+(?:jr\.?|junior\s+resident)|(?:jr\.?|junior\s+resident)\s*\(?\s*academic\s*\)?)\b", qual_scope, re.IGNORECASE)) and not re.search(r"\bnon[-\s]*academic\b", qual_scope, re.IGNORECASE)
        has_pg_header = is_acad_jr or bool(re.search(r"\b(?:MD/MS|M\.?D\.?|M\.?S\.?|DNB|DrNB|D\.?M\.?|M\.?Ch\.?|PG\s+Degree|PG\s+Diploma|DGO|DCH|DMRD|Specialist|Senior\s+Resident|Sr\.?\s*Resident|Consultant)\b", qual_scope, re.IGNORECASE))
        has_mbbs_header = (not is_acad_jr) and bool(re.search(r"\b(?:MBBS|GDMO|CGDMO|Junior\s+Resident|Jr\.?\s*Resident|\bJR\b|Non[-\s]*Academic|House\s*Staff|RMO|Clinical\s+Tutor|Tutor|Demonstrator)\b", qual_scope, re.IGNORECASE))
        if has_pg_header and not has_mbbs_header:
            extracted["qualification"] = "MD/MS"
        elif has_mbbs_header and not has_pg_header:
            extracted["qualification"] = "MBBS"
        elif has_pg_header and has_mbbs_header:
            # If Essential Qualification mentions "MBBS with MD/MS/DNB", it requires PG
            if qual_sec_m and re.search(r"\b(?:with\s+(?:MD|MS|DNB|DrNB|PG)|MD/MS|DNB|DrNB)\b", qual_sec_m.group(0), re.IGNORECASE) and not re.search(r"\b(?:or\s+MBBS|GDMO|Junior\s+Resident)\b", qual_sec_m.group(0), re.IGNORECASE):
                extracted["qualification"] = "MD/MS"
            else:
                extracted["qualification"] = "MBBS / MD/MS" if re.search(r"\b(?:GDMO|CGDMO|Junior\s+Resident|Medical\s+Officer)\b", qual_scope, re.IGNORECASE) else "MD/MS"
        elif re.search(r"\b(?:MD|MS|DNB|DrNB|DGO|DCH|DMRD|Specialist|Senior\s+Resident|Sr\.?\s*Resident|Consultant)\b", text, re.IGNORECASE):
            extracted["qualification"] = "MD/MS"
        elif re.search(r"\b(?:BAMS|BHMS|BUMS|BSMS|BNYS|AYUSH)\b", text, re.IGNORECASE):
            extracted["qualification"] = "AYUSH"
        elif re.search(r"\b(?:BDS|MDS|Dental)\b", text, re.IGNORECASE):
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

        cutoff_m = re.search(
            r"(?:age\s+(?:limit|as\s+on|reckoned\s+as\s+on)|as\s+on)\s*[:=-]?\s*" + DATE_TOKEN_RE.pattern,
            text,
            re.IGNORECASE,
        )
        if cutoff_m:
            dt = _parse_indian_date(cutoff_m.group(1))
            if dt:
                extracted["age_cutoff_date"] = dt.strftime("%Y-%m-%d")

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

        # 5. Dates (Walk-in / Interview windows & Application Last Dates)
        walkin_block = re.search(
            r"(?:walk[-\s]?in[-\s]?interview|date\s+of\s+interview|interview\s+(?:date|schedule|will\s+be\s+held(?:\s+on)?)|reporting\s+date|date\s+of\s+counsell?ing|document\s+verification).{0,240}",
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
                r"(?:last\s*date(?:\s*of\s*(?:full\s*)?(?:submission|registration|application))?|closing\s*date|submit(?:ted)?\s*(?:up\s*to|on\s*or\s*before))\s*[:=-]?\s*(?:midnight\s*of\s*)?([\s\S]{5,240})",
                text,
                re.IGNORECASE,
            )
            if last_date_ctx:
                found_dates = [d for tok in DATE_TOKEN_RE.findall(last_date_ctx.group(1)) if (d := _parse_indian_date(tok))]
                if found_dates:
                    extracted["last_date"] = max(found_dates).strftime("%Y-%m-%d")
                    signals += 1

        if not extracted["last_date"]:
            window_ctx = re.search(
                r"(?:between|from)\s+[^\n]{0,40}?" + DATE_TOKEN_RE.pattern + r"[^\n]{0,40}?\bto\b[^\n]{0,20}?" + DATE_TOKEN_RE.pattern,
                text,
                re.IGNORECASE,
            )
            if window_ctx:
                d_end = _parse_indian_date(window_ctx.group(2))
                if d_end:
                    extracted["last_date"] = d_end.strftime("%Y-%m-%d")
                    signals += 1

        all_doc_dates = [d for tok in DATE_TOKEN_RE.findall(text or "") if (d := _parse_indian_date(tok))]
        latest_doc_date = max(all_doc_dates) if all_doc_dates else None
        extracted["latest_document_date"] = latest_doc_date.strftime("%Y-%m-%d") if latest_doc_date else None
        now_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
        extracted["is_stale_document"] = bool(
            not extracted["last_date"]
            and not extracted["exam_date"]
            and latest_doc_date is not None
            and latest_doc_date < (now_ist - timedelta(days=30))
        )

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

        # 9. Application Fee (supports Application Fee / Demand Draft / Bank Transfer)
        fee_match = re.search(
            r"(?:application\s*fees?|prescribed\s*fee|demand\s*draft(?:\s*of)?|dd\s*(?:of|for)|bank\s*transfer\s*(?:of)?)\s*(?:of|:=-)?\s*(?:Rs\.?|INR|₹)\s*(\d{2,5})/?-?",
            text,
            re.IGNORECASE,
        )
        if not fee_match:
            fee_match = re.search(r"(?:application\s*fees?|prescribed\s*fee)\s*(?:of|:=-)?\s*(\d{2,4})/-?", text, re.IGNORECASE)
        if fee_match:
            extracted["application_fee"] = f"₹{fee_match.group(1)}"
        elif re.search(r"zero\s*(?:application\s*)?fee|no\s*application\s*fee", text, re.IGNORECASE):
            extracted["application_fee"] = "Zero Application Fee"

        # 10. Post-qualification Experience
        exp_m = re.search(
            r"(\d+)\s*(?:\+\s*)?(?:years?|yrs?)\s*(?:of\s*)?(?:post[-\s]*(?:pg|qualification|mbbs)\s*)?experience",
            text,
            re.IGNORECASE,
        )
        if exp_m:
            yrs = int(exp_m.group(1))
            if 0 < yrs <= 25:
                extracted["experience_years_required"] = yrs

        # 11. Multi-Cadre Seat Breakdown (splits GDMO vs Specialist vs Junior Resident vs AYUSH)
        cadre_patterns = [
            ("GDMO / Medical Officer", "MBBS", r"(?:General\s+Duty\s+Medical\s+Officer|GDMO|Medical\s+Officer\s*(?:\(MBBS\))?)\s*[-–:=]+\s*(\d+)"),
            ("Senior Resident / Specialist", "MD/MS", r"(?:Senior\s+Resident|Sr\.?\s*Resident|Specialist(?:\s+Medical\s+Officer)?)\s*[-–:=]+\s*(\d+)"),
            ("Junior Resident", "MBBS", r"(?:Junior\s+Resident|Jr\.?\s*Resident|House\s*Staff)\s*[-–:=]+\s*(\d+)"),
            ("AYUSH Medical Officer", "AYUSH", r"(?:AYUSH\s*(?:Medical\s+Officer|MO)|BAMS|BHMS)\s*[-–:=]+\s*(\d+)"),
        ]
        cadres: List[Dict[str, Any]] = []
        for label, c_qual, pat in cadre_patterns:
            cm = re.search(pat, text, re.IGNORECASE)
            if cm:
                cnt = int(cm.group(1))
                if 0 < cnt <= 2000:
                    cadres.append({"cadre": label, "qualification": c_qual, "posts": cnt})
        if cadres:
            extracted["cadre_breakdown"] = cadres

        extracted["parsed_confident"] = signals >= 2
        return extracted
