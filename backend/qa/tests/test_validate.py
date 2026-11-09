import json
from unittest import TestCase
from qa.validate import validate
from qa.errors import AppError

class ValidationTests(TestCase):
    def payload(self, quote="A group coaching session takes place every Tuesday at 16:00 UTC.", doc="DOC2"):
        return json.dumps({"answerable": True, "answer": "Tuesday", "sources": [{"docId": doc, "quote": quote}]})

    def test_verified_quote_and_metadata(self):
        result = validate(self.payload())
        self.assertTrue(result["answerable"])
        self.assertEqual(result["sources"][0]["file"], "02-coaching-and-feedback.md")

    def test_invalid_sources_abstain(self):
        for quote, doc in [("invented", "DOC2"), ("", "DOC2"), ("Tuesday", "DOC99")]:
            with self.subTest(quote=quote, doc=doc):
                result = validate(self.payload(quote, doc))
                self.assertFalse(result["answerable"])
                self.assertEqual(result["sources"], [])

    def test_normalization_and_fences(self):
        self.assertTrue(validate("```json\n" + self.payload("EVERY   TUESDAY") + "\n```")["answerable"])

    def test_bad_json_or_schema(self):
        for raw in ['no json', '[]', '{}', '{"answerable": 1,"answer":"x","sources":[]}', '{"answerable":true,"answer":"","sources":[]}', '{"answerable":true,"answer":"x","sources":[{}]}']:
            with self.subTest(raw=raw), self.assertRaises(AppError) as error:
                validate(raw)
            self.assertEqual(error.exception.code, "INVALID_MODEL_OUTPUT")

    def test_negative_output_is_standardized(self):
        result = validate(json.dumps({"answerable":False,"answer":"invented price","sources":[]}), "How much does it cost?")
        self.assertIn("not available in the supplied documents", result["answer"])
        self.assertIn("support@brightpath.example", result["answer"])
