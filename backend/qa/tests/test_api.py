import json
import os
from unittest.mock import patch
from django.test import SimpleTestCase

@patch.dict(os.environ, {"LLM_PROVIDER": "mock", "SIMULATE_FAILURE": "false"})
class ApiTests(SimpleTestCase):
    def post(self, question, suffix=""):
        return self.client.post("/api/ask" + suffix, data=json.dumps({"question":question}), content_type="application/json")

    def test_coaching_and_sources(self):
        response = self.post("How often is the group coaching session and where do I find the link?")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("Tuesday at 16:00 UTC", payload["answer"])
        self.assertIn("30 minutes", payload["answer"])
        self.assertEqual(payload["sources"][0]["docId"], "DOC2")

    def test_price_abstains(self):
        payload = self.post("How much does BrightPath Learn cost and can I get a refund?").json()
        self.assertFalse(payload["answerable"])
        self.assertIn("support@brightpath.example", payload["answer"])
        self.assertEqual(payload["sources"], [])

    def test_both_simulation_switches(self):
        for suffix, env in [("?simulate=failure", "false"), ("", "true")]:
            with patch.dict(os.environ, {"SIMULATE_FAILURE":env}):
                response = self.post("coaching link", suffix)
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.json()["errorType"], "MODEL_UNAVAILABLE")
                self.assertNotIn("answer", response.json())

    def test_bad_input(self):
        for question in ["", "   ", "x" * 501, 12, None]:
            self.assertEqual(self.post(question).status_code, 400)
        for raw in ['{', '[]']:
            self.assertEqual(self.client.post("/api/ask", raw, content_type="application/json").status_code, 400)
        self.assertEqual(self.client.post("/api/ask", {"question":"x"}).status_code, 400)

    def test_json_framework_errors(self):
        for response, status in [(self.client.get("/api/ask"), 405), (self.client.get("/missing"), 404)]:
            self.assertEqual(response.status_code, status)
            self.assertFalse(response.json()["ok"])
        self.client.raise_request_exception = False
        with patch("qa.views.ask_question", side_effect=RuntimeError("private diagnostic")):
            response = self.post("coaching link")
            self.assertEqual(response.status_code, 500)
            self.assertNotIn("private diagnostic", response.content.decode())
            self.assertEqual(response.json()["errorType"], "INTERNAL_ERROR")

    def test_production_https_and_nosniff(self):
        with self.settings(SECURE_SSL_REDIRECT=True):
            response = self.post("coaching link")
            self.assertEqual(response.status_code, 301)
            self.assertTrue(response["Location"].startswith("https://"))
            response = self.client.post("/api/ask", data=json.dumps({"question":"coaching link"}), content_type="application/json", secure=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["ok"])
            self.assertEqual(response["X-Content-Type-Options"], "nosniff")
