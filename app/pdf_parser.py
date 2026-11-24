import re
import io
import requests
from typing import Dict, Any, Optional
from pypdf import PdfReader

class GovtNotificationPDFParser:
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        """Extracts text from PDF bytes using pypdf."""
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        # Read up to first 10 pages where job circular terms are usually stated
        max_pages = min(10, len(reader.pages))
        for i in range(max_pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    @classmethod
    def extract_from_url(cls, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return cls.extract_text_from_bytes(resp.content)

    @classmethod
    def parse_notice_text(cls, text: str) -> Dict[str, Any]:
        """Analyzes text of a recruitment gazette and extracts key parameters."""
        extracted: Dict[str, Any] = {
            "title": "Medical Officer Recruitment",
            "qualification": "MBBS",
            "total_posts": 1,
            "min_age": 21,
            "max_age": 35,
            "bond_years": 0,
            "bond_penalty_amount": "No Bond",
            "selection_mode": "Written Exam + Interview",
            "category_seats": {},
            "application_fee": "As per notification",
            "key_clauses": []
        }

        # 1. Total Posts Detection
        posts_match = re.search(r'(?:total\s*(?:no\.?\s*of)?\s*(?:posts?|vacanc(?:y|ies)|seats?))\s*[:=-]?\s*(\d+)', text, re.IGNORECASE)
        if not posts_match:
            posts_match = re.search(r'(\d+)\s*(?:posts?|vacancies|seats?)\s*of\s*(?:medical officer|gdmo|doctor)', text, re.IGNORECASE)
        if posts_match:
            extracted["total_posts"] = int(posts_match.group(1))

        # 2. Qualification
        if re.search(r'\b(?:MD|MS|DNB|Specialist)\b', text, re.IGNORECASE):
            extracted["qualification"] = "MD/MS"
        elif re.search(r'\b(?:BAMS|BHMS|BUMS|AYUSH)\b', text, re.IGNORECASE):
            extracted["qualification"] = "AYUSH"
        elif re.search(r'\b(?:BDS|Dental)\b', text, re.IGNORECASE):
            extracted["qualification"] = "BDS"
        else:
            extracted["qualification"] = "MBBS"

        # 3. Upper Age Limit
        age_match = re.search(r'(?:upper\s*age\s*limit|maximum\s*age|not\s*exceeding|age\s*not\s*more\s*than)\s*[:=-]?\s*(\d{2})\s*years?', text, re.IGNORECASE)
        if age_match:
            extracted["max_age"] = int(age_match.group(1))

        # 4. Mandatory Service / Rural Bond
        bond_match = re.search(r'(?:bond|service\s*agreement|compulsory\s*(?:rural)?\s*service).*?(?:period\s*of|for)\s*(\d+)\s*years?', text, re.IGNORECASE | re.DOTALL)
        if bond_match:
            extracted["bond_years"] = int(bond_match.group(1))
            extracted["bond_penalty_amount"] = f"{extracted['bond_years']} Year(s) Mandatory Service Bond"

        penalty_match = re.search(r'(?:penalty|bond\s*amount|liquidated\s*damages|sum\s*of)\s*(?:Rs\.?|INR|₹)\s*([\d,]+(?:\s*lakh(?:s)?)?)', text, re.IGNORECASE)
        if penalty_match:
            penalty_val = penalty_match.group(1)
            extracted["bond_penalty_amount"] = f"{extracted['bond_years'] or 1} Year Bond (Penalty: ₹{penalty_val})"

        # 5. Selection Mode
        if re.search(r'walk[-\s]?in\s*interview', text, re.IGNORECASE):
            extracted["selection_mode"] = "Direct Walk-in Interview"
        elif re.search(r'computer\s*based\s*(?:test|examination)|cbt|online\s*exam', text, re.IGNORECASE):
            extracted["selection_mode"] = "Computer Based Test (CBT) + Interview"
        elif re.search(r'written\s*(?:examination|test)', text, re.IGNORECASE):
            extracted["selection_mode"] = "Written Examination + Interview"
        elif re.search(r'merit\s*(?:based|list)|academic\s*merit', text, re.IGNORECASE):
            extracted["selection_mode"] = "Merit Based (Marks in MBBS)"

        # 6. Category Seat Breakdown
        categories = ["UR", "OBC", "SC", "ST", "EWS"]
        seats_dict = {}
        for cat in categories:
            cat_match = re.search(rf'\b{cat}\b\s*[:=-]?\s*(\d+)', text, re.IGNORECASE)
            if cat_match:
                seats_dict[cat] = int(cat_match.group(1))
        if seats_dict:
            extracted["category_seats"] = seats_dict

        # 7. Application Fee
        fee_match = re.search(r'(?:application\s*fee|prescribed\s*fee)\s*[:=-]?\s*(?:Rs\.?|INR|₹)\s*(\d+)', text, re.IGNORECASE)
        if fee_match:
            extracted["application_fee"] = f"₹{fee_match.group(1)}"

        return extracted
