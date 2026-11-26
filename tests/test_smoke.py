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
        self.engine.dispose()

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

    def test_exam_catalog_and_images_integrity(self):
        from pathlib import Path
        from app.exam_data import EXAMS_CATALOG, EXAM_QUESTIONS

        static_root = Path(__file__).resolve().parent.parent / "app"
        self.assertGreaterEqual(len(EXAMS_CATALOG), 10)
        image_count = 0
        for exam in EXAMS_CATALOG:
            eid = exam["id"]
            self.assertIn(eid, EXAM_QUESTIONS)
            qs = EXAM_QUESTIONS[eid]
            self.assertGreater(len(qs), 0)
            for q in qs:
                self.assertEqual(len(q["options"]), 4)
                self.assertIn(q["correct_option"], (0, 1, 2, 3))
                if "image_url" in q:
                    image_count += 1
                    rel = q["image_url"].lstrip("/")
                    self.assertTrue((static_root / rel).is_file(), f"Missing image: {rel}")
        self.assertEqual(image_count, 15)

    def test_portal_sources_and_link_extractor(self):
        from bs4 import BeautifulSoup
        from app.scraper import PORTAL_SOURCES, LiveGazetteScraper

        self.assertGreaterEqual(len(PORTAL_SOURCES), 75)
        names = [s["name"] for s in PORTAL_SOURCES]
        urls = [s["url"] for s in PORTAL_SOURCES]
        self.assertEqual(len(names), len(set(names)), "Duplicate portal names found")
        self.assertEqual(len(urls), len(set(urls)), "Duplicate portal URLs found")
        for s in PORTAL_SOURCES:
            for key in ("name", "organization", "url", "category", "state", "pay_scale"):
                self.assertTrue(s.get(key), f"Missing {key} in {s.get('name')}")

        html = """
        <table>
          <tr><td>Engagement of 12 GDMO under NHM Purulia</td><td><a href="/files/gdmo.pdf">Download PDF</a></td></tr>
        </table>
        <script>window.__DATA__ = {"subject": "Walk-in Interview for Junior Resident at AIIMS", "file": "/docs/jr_2026.pdf"};</script>
        """
        soup = BeautifulSoup(html, "html.parser")
        links = LiveGazetteScraper._extract_candidate_links(soup, html, "https://example.gov.in/")
        self.assertTrue(any("Engagement of 12 GDMO" in t and u.endswith("/files/gdmo.pdf") for t, u in links))
        self.assertTrue(any("Walk-in Interview for Junior Resident" in t and u.endswith("/docs/jr_2026.pdf") for t, u in links))

    def test_scanned_pdf_fuzzy_dedup_and_subscription_filters(self):
        from app.scraper import _sig_tokens, _is_fuzzy_duplicate
        from app.models import Subscription
        from app.notifier import Notifier

        scanned = GovtNotificationPDFParser.parse_notice_text("   ")
        self.assertTrue(scanned["is_scanned"])

        t1 = _sig_tokens("Engagement of 12 GDMO under NHM Purulia Sadar Hospital")
        t2 = _sig_tokens("Notice for Engagement of 12 GDMO under NHM Purulia Sadar Hospital")
        self.assertTrue(_is_fuzzy_duplicate("West Bengal", t2, [("West Bengal", t1)]))
        self.assertFalse(_is_fuzzy_duplicate("Odisha", t2, [("West Bengal", t1)]))

        vac_wb_bond = Vacancy(
            id="v-bond",
            title="State MO",
            organization="WB",
            category="State PSC",
            state="West Bengal",
            designation="MO",
            qualification="MBBS",
            bond_years=2,
        )
        sub = Subscription(
            channel="telegram",
            target="12345",
            qualification_filter="MBBS",
            state_filter="West Bengal",
            category_filter="ALL",
            zero_bond_only=True,
        )
        self.assertFalse(Notifier._matches_subscription(sub, vac_wb_bond))
        vac_wb_bond.bond_years = 0
        self.assertTrue(Notifier._matches_subscription(sub, vac_wb_bond))

    def test_seo_jobposting_and_paper_split_exams(self):
        from app.main import serve_index, serve_seo_job_track, _resolve_exam_and_questions

        res_job = serve_index(job="smoke-vac-1", db=self.db)
        self.assertIn(b'"@type": "JobPosting"', res_job.body)
        self.assertIn(b'WBHRB GDMO Recruitment 2026', res_job.body)

        res_track = serve_seo_job_track("west-bengal")
        self.assertIn(b"West Bengal Medical Officer", res_track.body)

        sm = sitemap_xml(db=self.db)
        self.assertIn(b"/jobs/west-bengal</loc>", sm.body)

        m1, q1 = _resolve_exam_and_questions("cms-paper-1")
        m2, q2 = _resolve_exam_and_questions("cms-paper-2")
        self.assertIsNotNone(m1)
        self.assertIsNotNone(m2)
        self.assertGreater(len(q1), 0)
        self.assertGreater(len(q2), 0)

    def test_api_routes_weak_drill_vapid_and_suggest_update(self):
        from unittest.mock import patch
        from app.main import (
            get_stats,
            get_vapid_public_key,
            get_weak_drill_questions,
            suggest_vacancy_update,
            SuggestUpdateRequest,
            list_corrigendum_suggestions,
            resolve_corrigendum_suggestion,
        )

        st = get_stats(db=self.db)
        self.assertEqual(st["active_notices"], 1)

        vk = get_vapid_public_key(db=self.db)
        self.assertIn("public_key", vk)

        rss_wb = rss_feed(state="West Bengal", qualification="MBBS", db=self.db)
        self.assertIn(b"WBHRB GDMO Recruitment 2026", rss_wb.body)
        rss_empty = rss_feed(state="Kerala", qualification="MBBS", db=self.db)
        self.assertNotIn(b"WBHRB GDMO Recruitment 2026", rss_empty.body)

        drill = get_weak_drill_questions(subjects="Medicine,Surgery", limit=10)
        self.assertEqual(len(drill["questions"]), 10)

        req = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 12345)})
        with patch("app.main.check_rate_limit"), patch("app.pdf_parser.GovtNotificationPDFParser.is_safe_url", return_value=True):
            sug = suggest_vacancy_update(
                "smoke-vac-1",
                SuggestUpdateRequest(suggested_url="https://www.hrb.wb.gov.in/notice", note="Date extended to 20 Dec 2026"),
                req,
                self.db,
            )
        self.assertTrue(sug["ok"])

        pending = list_corrigendum_suggestions(status_filter="PENDING", db=self.db)
        self.assertEqual(len(pending), 1)

        resolved = resolve_corrigendum_suggestion(pending[0]["id"], decision="APPROVED", db=self.db)
        self.assertEqual(resolved["status"], "APPROVED")

    def test_robots_txt_and_multilang_ocr(self):
        from unittest.mock import patch, MagicMock
        from app.main import robots_txt

        rob = robots_txt()
        self.assertEqual(rob.media_type, "text/plain")
        self.assertIn(b"Sitemap:", rob.body)
        self.assertIn(b"/sitemap.xml", rob.body)

        with patch("shutil.which", return_value="/usr/bin/mock"), \
             patch("subprocess.run") as mock_run:
            lang_proc = MagicMock(stdout="List of available languages in \"/usr/share/tesseract-ocr/5/tessdata/\" (3):\nben\neng\nhin\n")
            tess_proc = MagicMock(stdout="Memo No: 123\nTotal 10 posts")
            mock_run.side_effect = [MagicMock(), lang_proc, tess_proc]
            with patch("os.listdir", return_value=["page-1.png"]):
                txt = GovtNotificationPDFParser._ocr_pdf_bytes(b"%PDF-1.4")
                self.assertIn("Memo No: 123", txt)
                tess_cmd = mock_run.call_args_list[2][0][0]
                self.assertEqual(tess_cmd[-1], "eng+hin+ben")

    def test_exam_search_report_and_full_day_simulator(self):
        from unittest.mock import patch
        from app.main import (
            _resolve_exam_and_questions,
            search_exam_questions,
            report_exam_question,
            QuestionReportRequest,
            list_question_reports,
        )

        meta, qs = _resolve_exam_and_questions("cms-full-day")
        self.assertIsNotNone(meta)
        self.assertEqual(meta["total_marks"], 500)
        self.assertEqual(len(qs), 240)

        res = search_exam_questions(q="diabetes", limit=15)
        self.assertGreater(len(res["questions"]), 0)
        self.assertLessEqual(len(res["questions"]), 15)

        req = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 12345)})
        with patch("app.main.check_rate_limit"):
            rep = report_exam_question(
                QuestionReportRequest(question_id=res["questions"][0]["id"], reason="OCR typo", note="Check option B"),
                req,
                self.db,
            )
        self.assertTrue(rep["ok"])
        reports = list_question_reports(db=self.db)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["reason"], "OCR typo")

    def test_admin_password_and_question_correction(self):
        import os
        from unittest.mock import patch
        from fastapi import HTTPException
        from app.main import (
            admin_login,
            AdminLoginRequest,
            admin_search_questions,
            admin_ai_fix_question,
            QuestionAIFixRequest,
            admin_update_question,
            QuestionUpdateRequest,
            _find_question_in_memory,
            _apply_question_overrides,
        )

        req = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 12345)})
        with patch.dict(os.environ, {"ADMIN_PASSWORD": "test-secret-pw"}, clear=False), \
             patch("app.main.check_rate_limit"):
            with self.assertRaises(HTTPException) as ctx:
                admin_login(AdminLoginRequest(password="wrong"), req)
            self.assertEqual(ctx.exception.status_code, 403)

            ok = admin_login(AdminLoginRequest(password="test-secret-pw"), req)
            self.assertTrue(ok["ok"])

        found = admin_search_questions(q="cms16-p1-003", limit=5, db=self.db)
        self.assertEqual(len(found["results"]), 1)

        with patch("app.main.check_rate_limit"):
            ai_res = admin_ai_fix_question(
                "cms16-p1-003",
                QuestionAIFixRequest(provider="local", text="Test stem 1. First 2. Second", options=["2 a nd 3 only", "1, 2 and 3", "1 and 3 only", "1 and 2 only"]),
                req,
            )
            self.assertTrue(ai_res["ok"])
            self.assertEqual(ai_res["suggestion"]["options"][0], "2 and 3 only")

        q_orig = dict(_find_question_in_memory("cms16-p1-003"))
        try:
            with patch("app.main._persist_question_to_pyq_json", return_value=True):
                upd = admin_update_question(
                    "cms16-p1-003",
                    QuestionUpdateRequest(
                        subject=q_orig["subject"],
                        text=q_orig["text"],
                        options=q_orig["options"],
                        correct_option=q_orig["correct_option"],
                        explanation="Verified manual edit",
                        citation=q_orig.get("citation", ""),
                    ),
                    db=self.db,
                )
            self.assertTrue(upd["ok"])
            _find_question_in_memory("cms16-p1-003")["explanation"] = "stale"
            _apply_question_overrides(self.db)
            self.assertEqual(_find_question_in_memory("cms16-p1-003")["explanation"], "Verified manual edit")
        finally:
            _find_question_in_memory("cms16-p1-003").update(q_orig)

    def test_stale_siliguri_table_pdf_and_link_filtering(self):
        from datetime import datetime, timedelta
        from bs4 import BeautifulSoup
        from app.scraper import LiveGazetteScraper
        from app.main import _is_vacancy_expired

        siliguri_ocr_text = (
            "SILIGURI MUNICIPAL CORPORATION\n"
            "Memo no 836 Estt./SMC Date 10/2/2026\n"
            "Applications are invited online for engagement of Health Officer on contract basis\n"
            "Name of the Post No. of post Remuneration Age Limit Last date of application\n"
            "1\nHealth Officer (Contractual)\n1 (one)\nRs. 62,000/-\n"
            "Not more than 62 years as on 01/01/2025\n"
            "25/02/2026 by 4:30 pm\n"
        )
        parsed = GovtNotificationPDFParser.parse_notice_text(siliguri_ocr_text)
        self.assertEqual(parsed["last_date"], "2026-02-25")

        stale_only_text = "SILIGURI MUNICIPAL CORPORATION\nMemo no 123 Date 10/01/2025\nWalk-in details in annexure."
        parsed_stale = GovtNotificationPDFParser.parse_notice_text(stale_only_text)
        self.assertIsNone(parsed_stale["last_date"])
        self.assertTrue(parsed_stale["is_stale_document"])

        html = """
        <a href="news-announcement.php?">Online applications are invited for Health Officer at Siliguri Municipal Corporation</a>
        <a href="userfiles/file/836_Estt_SMC.pdf">Online applications are invited for Health Officer at Siliguri Municipal Corporation</a>
        """
        soup = BeautifulSoup(html, "html.parser")
        links = LiveGazetteScraper._extract_candidate_links(soup, html, "https://www.siligurismc.in/recruitments.php")
        self.assertEqual(len(links), 1)
        self.assertTrue(links[0][1].endswith(".pdf"))

        now_ist = datetime(2026, 11, 26, 15, 0)
        v_old_verified = Vacancy(
            id="v-old-ver",
            title="Old Verified PDF Without Date",
            organization="SMC",
            category="Contractual",
            designation="Health Officer",
            verification_status="VERIFIED_PDF",
            last_date=None,
            exam_date=None,
            is_active=True,
            created_at=datetime(2026, 11, 10, 10, 0),
        )
        self.assertTrue(_is_vacancy_expired(v_old_verified, now_ist))

        v_dead_ticker = Vacancy(
            id="v-dead-ticker",
            title="Ticker Notice",
            organization="SMC",
            category="Contractual",
            designation="Health Officer",
            notification_url="https://www.siligurismc.in/news-announcement.php?",
            is_active=True,
            created_at=now_ist - timedelta(hours=6),
        )
        self.assertTrue(_is_vacancy_expired(v_dead_ticker, now_ist))


if __name__ == "__main__":
    unittest.main()
