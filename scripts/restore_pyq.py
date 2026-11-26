"""Batch-restore scanned UPSC CMS question PDFs into app/pyq_papers.json using Gemini Vision.

Usage:
    GEMINI_API_KEY=... ./venv/bin/python scripts/restore_pyq.py --paper upsc-cms-2025-paper-2-authentic
    GEMINI_API_KEY=... ./venv/bin/python scripts/restore_pyq.py --all-scanned
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types

REPO_ROOT = Path(__file__).resolve().parent.parent
PYQ_PATH = REPO_ROOT / "app" / "pyq_papers.json"
DOWNLOADS = Path.home() / "Downloads"
REVIEW_QUEUE_PATH = REPO_ROOT / "review_queue.json"

SCANNED_PDF_MAP = {
    "upsc-cms-2009-paper-1-authentic": DOWNLOADS / "UPSC CMS 2009 PAPER I QUESTIONS.pdf",
    "upsc-cms-2009-paper-2-authentic": DOWNLOADS / "UPSC CMS 2009 PAPER II QUESTIONS.pdf",
    "upsc-cms-2010-paper-1-authentic": DOWNLOADS / "UPSC CMS 2010 PAPER I QUESTIONS.pdf",
    "upsc-cms-2010-paper-2-authentic": DOWNLOADS / "UPSC CMS 2010 PAPER II QUESTIONS.pdf",
    "upsc-cms-2011-paper-1-authentic": DOWNLOADS / "UPSC CMS 2011 PAPER I QUESTIONS.pdf",
    "upsc-cms-2011-paper-2-authentic": DOWNLOADS / "UPSC CMS 2011 PAPER II QUESTIONS.pdf",
    "upsc-cms-2012-paper-1-authentic": DOWNLOADS / "UPSC CMS 2012 PAPER I QUESTIONS.pdf",
    "upsc-cms-2012-paper-2-authentic": DOWNLOADS / "UPSC CMS 2012 PAPER II QUESTIONS.pdf",
    "upsc-cms-2013-paper-1-authentic": DOWNLOADS / "UPSC CMS 2013 PAPER I QUESTIONS.pdf",
    "upsc-cms-2013-paper-2-authentic": DOWNLOADS / "UPSC CMS 2013 PAPER II QUESTIONS.pdf",
    "upsc-cms-2021-paper-1-authentic": DOWNLOADS / "UPSC CMS 2021 PAPER I QUESTIONS.pdf",
    "upsc-cms-2021-paper-2-authentic": DOWNLOADS / "UPSC CMS 2021 PAPER II QUESTIONS.pdf",
    "upsc-cms-2022-paper-1-authentic": DOWNLOADS / "UPSC CMS 2022 PAPER I QUESTIONS.pdf",
    "upsc-cms-2022-paper-2-authentic": DOWNLOADS / "UPSC CMS 2022 PAPER II QUESTIONS.pdf",
    "upsc-cms-2023-paper-2-authentic": DOWNLOADS / "UPSC CMS 2023 PAPER II QUESTIONS.pdf",
    "upsc-cms-2024-paper-1-authentic": DOWNLOADS / "UPSC CMS 2024 PAPER I QUESTIONS.pdf",
    "upsc-cms-2024-paper-2-authentic": DOWNLOADS / "UPSC CMS 2024 PAPER II QUESTIONS.pdf",
    "upsc-cms-2025-paper-1-authentic": DOWNLOADS / "UPSC CMS 2025 PAPER I QUESTIONS.pdf",
    "upsc-cms-2025-paper-2-authentic": DOWNLOADS / "UPSC CMS 2025 PAPER II QUESTIONS.pdf",
}

PROMPT = """
You are an expert UPSC CMS (Combined Medical Services) exam-content restoration specialist.
Read EVERY page of the attached UPSC CMS Question Booklet PDF visually and extract all 120 questions verbatim.

RULES:
- Do NOT include question numbers (like "1." or "19-") at the start of question_text.
- For "Match List I with List II" questions, format question_text cleanly with:
  Match List I with List II and select the correct answer using the code given below the lists:
  List I (...)
  List II (...)
  A. ...
  1. ...
  B. ...
  2. ...
  C. ...
  3. ...
  D. ...
  4. ...
  Code: A B C D
  and format each option as 4 space-separated digits (e.g. "2 3 4 1").
- For multi-statement questions (1./2./3./4. or I./II./III./IV.), put each statement on its own line with its exact marker, followed by "Select the correct answer using the code given below:".
- Strip all watermarks ("Prepp", "Your Personal Exams Guide", page headers/footers).
- ANTI-HALLUCINATION GUARDRAIL: If a medical term, drug name, dose, lab value, or number is unreadable in the scan, output it as [UNREADABLE] and set needs_manual_review: true — do NOT guess.
- Keep options in exact (a), (b), (c), (d) order without "(a)"/"(b)"/"(c)"/"(d)" prefixes.

Return ONLY a valid JSON array of 120 objects:
[
  {
    "question_number": 1,
    "question_text": "...",
    "options": ["opt A", "opt B", "opt C", "opt D"],
    "confidence": "high | medium | low",
    "needs_manual_review": false
  }
]
"""


def restore_paper(client: genai.Client, paper_id: str, pdf_path: Path, model_name: str) -> tuple[int, list[dict]]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Missing PDF: {pdf_path}")
    print(f"Uploading {pdf_path.name} for {paper_id}...")
    uploaded = client.files.upload(file=str(pdf_path))
    try:
        resp = client.models.generate_content(
            model=model_name,
            contents=[uploaded, PROMPT],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )
    finally:
        try:
            client.files.delete(name=uploaded.name)
        except Exception:
            pass

    items = json.loads(resp.text)
    by_num = {int(item["question_number"]): item for item in items if "question_number" in item}

    data = json.loads(PYQ_PATH.read_text(encoding="utf-8"))
    questions = data["questions"][paper_id]
    updated = 0
    review_items = []
    for idx, q in enumerate(questions, 1):
        item = by_num.get(idx)
        if not item:
            review_items.append({"paper_id": paper_id, "question_id": q["id"], "reason": "missing_in_extraction"})
            continue
        if item.get("needs_manual_review") or "[UNREADABLE]" in item.get("question_text", ""):
            review_items.append({"paper_id": paper_id, "question_id": q["id"], **item})
            continue
        opts = [str(o).strip() for o in (item.get("options") or [])]
        if len(opts) == 4 and all(opts) and item.get("question_text"):
            q["text"] = item["question_text"].strip()
            q["options"] = opts
            updated += 1
        else:
            review_items.append({"paper_id": paper_id, "question_id": q["id"], **item})

    PYQ_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return updated, review_items


def main():
    parser = argparse.ArgumentParser(description="Restore scanned UPSC CMS PDFs into app/pyq_papers.json")
    parser.add_argument("--paper", help="Single paper ID (e.g. upsc-cms-2025-paper-2-authentic)")
    parser.add_argument("--all-scanned", action="store_true", help="Process all 19 scanned UPSC CMS papers")
    parser.add_argument("--model", default="gemini-2.5-pro", help="Gemini model name (default: gemini-2.5-pro)")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY in your environment before running this script.")

    client = genai.Client(api_key=api_key)
    targets = list(SCANNED_PDF_MAP.keys()) if args.all_scanned else ([args.paper] if args.paper else [])
    if not targets:
        raise SystemExit("Pass --paper <id> or --all-scanned")

    all_reviews = []
    for pid in targets:
        updated, reviews = restore_paper(client, pid, SCANNED_PDF_MAP[pid], args.model)
        print(f"  {pid}: updated {updated}/120 questions, {len(reviews)} flagged for review")
        all_reviews.extend(reviews)
        time.sleep(1.5)

    if all_reviews:
        REVIEW_QUEUE_PATH.write_text(json.dumps(all_reviews, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {len(all_reviews)} review items to {REVIEW_QUEUE_PATH}")


if __name__ == "__main__":
    main()
