import base64
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from app.database import Base
from app.models import Vacancy, CorrigendumLog, PushSubscription
from app.pdf_parser import GovtNotificationPDFParser
from app.main import (
    analyze_pdf_file,
    PDFAnalyzeFileRequest,
    rss_feed,
    sitemap_xml,
    save_push_subscription,
    PushSubscribeRequest,
    list_recent_corrigenda,
    check_eligibility,
    DoctorProfile,
)


class MedAlertsSmokeTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()
        self.db.add(
            Vacancy(
                id="smoke-vac-1",
                title="WBHRB GDMO Recruitment 2026",
                organization="WBHRB",
                category="State PSC",
                state="West Bengal",
                designation="General Duty Medical Officer",
                qualification="MBBS",
                total_posts=1200,
                min_age=21,
                max_age=36,
                is_active=True,
            )
        )
        self.db.add(
            CorrigendumLog(
                vacancy_id="smoke-vac-1",
                title="WBHRB GDMO Recruitment 2026",
                field_changed="last_date",
                old_value="2026-11-30",
                new_value="2026-12-15",
            )
        )
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_pdf_parser_text(self):
        parsed = GovtNotificationPDFParser.parse_notice_text(
            "Memo No: WBHRB/2026/99. Total 450 posts of Medical Officer (MBBS). Max age 36 years. Last date 31-12-2026."
        )
        self.assertEqual(parsed["total_posts"], 450)
        self.assertEqual(parsed["qualification"], "MBBS")

    def test_rss_and_sitemap(self):
        rss = rss_feed(db=self.db)
        self.assertEqual(rss.media_type, "application/rss+xml")
        self.assertIn(b"WBHRB GDMO Recruitment 2026", rss.body)

        sm = sitemap_xml(db=self.db)
        self.assertEqual(sm.media_type, "application/xml")
        self.assertIn(b"/?job=smoke-vac-1</loc>", sm.body)

    def test_push_subscribe_and_corrigenda(self):
        req = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 12345)})
        res = save_push_subscription(
            PushSubscribeRequest(endpoint="https://push.example.com/sub/abc", qualification_filter="MBBS"),
            req,
            self.db,
        )
        self.assertTrue(res["ok"])
        self.assertEqual(self.db.query(PushSubscription).count(), 1)

        corrigenda = list_recent_corrigenda(limit=10, db=self.db)
        self.assertEqual(len(corrigenda), 1)
        self.assertEqual(corrigenda[0]["field_changed"], "last_date")

    def test_eligibility_engine(self):
        profile = DoctorProfile(
            name="Dr. Test",
            qualification="MBBS",
            college_name="Medical College Kolkata",
            passing_year=2024,
            internship_status="completed",
            age=26,
            category="UR",
            home_state="West Bengal",
            registered_with_smc=True,
        )
        out = check_eligibility(profile, self.db)
        self.assertEqual(out["summary"]["fully_eligible"], 1)

    def test_analyze_pdf_file_mocked(self):
        orig = GovtNotificationPDFParser.extract_text_from_bytes
        GovtNotificationPDFParser.extract_text_from_bytes = staticmethod(
            lambda b: "Total 200 posts for MBBS Medical Officer. Pay Level 10."
        )
        try:
            req = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 12345)})
            payload = PDFAnalyzeFileRequest(
                filename="test.pdf",
                content_base64=base64.b64encode(b"%PDF-1.4 mock").decode(),
            )
            out = analyze_pdf_file(payload, req)
            self.assertTrue(out["success"])
            self.assertEqual(out["data"]["total_posts"], 200)
        finally:
            GovtNotificationPDFParser.extract_text_from_bytes = orig


    def test_ssrf_redirect_blocked(self):
        import requests
        from unittest.mock import patch, MagicMock
        fake_resp = MagicMock()
        fake_resp.is_redirect = True
        fake_resp.status_code = 302
        fake_resp.headers = {"Location": "http://localhost/admin"}
        fake_resp.__enter__ = lambda s: s
        fake_resp.__exit__ = lambda s, *a: False
        with patch.object(GovtNotificationPDFParser, "is_safe_url", side_effect=[True, False]):
            with patch.object(requests, "get", return_value=fake_resp):
                with self.assertRaises(ValueError):
                    GovtNotificationPDFParser.extract_from_url("https://example.com/redirect.pdf")

    def test_exam_history_candidate_filter_and_corrigendum_broadcast(self):
        from app.models import ExamAttempt, Subscription, NotificationLog
        from app.main import list_exam_attempts
        from app.notifier import Notifier
        self.db.add(ExamAttempt(exam_id="e1", exam_title="CMS", candidate_name="Dr. Alice", final_score=80.0, accuracy_pct=80.0))
        self.db.add(ExamAttempt(exam_id="e1", exam_title="CMS", candidate_name="Dr. Bob", final_score=60.0, accuracy_pct=60.0))
        self.db.add(Subscription(channel="telegram", target="123456789", is_active=True))
        self.db.commit()

        alice_rows = list_exam_attempts(limit=5, candidate_name="Dr. Alice", db=self.db)
        self.assertEqual(len(alice_rows), 1)
        self.assertEqual(alice_rows[0]["candidate_name"], "Dr. Alice")

        vac = self.db.query(Vacancy).first()
        Notifier.broadcast_corrigendum(self.db, vac, [{"field": "last_date", "old": "2026-11-30", "new": "2026-12-15"}])
        self.assertEqual(self.db.query(NotificationLog).count(), 1)


if __name__ == "__main__":
    unittest.main()
