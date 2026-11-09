import json
import os
from unittest import TestCase
from unittest.mock import patch
import httpx
from qa.errors import AppError
from qa.service import select_provider
from qa.llm.nvidia import NvidiaProvider

@patch.dict(os.environ, {"NVIDIA_API_KEY":"test-placeholder", "NVIDIA_MODEL":"test-model", "NVIDIA_JSON_MODE":"false"})
class ProviderTests(TestCase):
    def test_success_request_contract(self):
        response = httpx.Response(200, json={"choices":[{"message":{"content":"{}"}}]})
        with patch("qa.llm.nvidia.httpx.post", return_value=response) as post:
            self.assertEqual(NvidiaProvider().generate("system", "question"), "{}")
            self.assertEqual(post.call_args.kwargs["json"]["model"], "test-model")
            self.assertEqual(post.call_args.kwargs["json"]["temperature"], 0)
            self.assertEqual(post.call_args.kwargs["timeout"], 15.0)
            self.assertNotIn("response_format", post.call_args.kwargs["json"])

    def test_json_mode_when_enabled(self):
        with patch.dict(os.environ, {"NVIDIA_JSON_MODE":"true"}), patch("qa.llm.nvidia.httpx.post", return_value=httpx.Response(200,json={"choices":[{"message":{"content":"{}"}}]})) as post:
            NvidiaProvider().generate("s", "q")
            self.assertEqual(post.call_args.kwargs["json"]["response_format"], {"type":"json_object"})

    def test_http_and_output_errors(self):
        for status, payload, expected in [(429,{},"RATE_LIMIT"),(401,{},"MODEL_UNAVAILABLE"),(500,{},"MODEL_UNAVAILABLE"),(202,{},"MODEL_UNAVAILABLE"),(200,{},"INVALID_MODEL_OUTPUT"),(200,{"choices":[{"message":{"content":None}}]},"INVALID_MODEL_OUTPUT")]:
            with self.subTest(status=status), patch("qa.llm.nvidia.httpx.post", return_value=httpx.Response(status,json=payload)), self.assertRaises(AppError) as error:
                NvidiaProvider().generate("s", "q")
            self.assertEqual(error.exception.code, expected)

    def test_transport_errors(self):
        for failure, expected in [(httpx.ReadTimeout("private"),"TIMEOUT"),(httpx.ConnectError("private"),"MODEL_UNAVAILABLE")]:
            with patch("qa.llm.nvidia.httpx.post", side_effect=failure), self.assertRaises(AppError) as error:
                NvidiaProvider().generate("s","q")
            self.assertEqual(error.exception.code, expected)

    def test_missing_key_and_automatic_mock(self):
        with patch.dict(os.environ, {"NVIDIA_API_KEY":"", "LLM_PROVIDER":"nvidia"}), self.assertRaises(AppError) as error:
            select_provider()
        self.assertEqual(error.exception.code, "MISSING_API_KEY")
        with patch.dict(os.environ, {"NVIDIA_API_KEY":"", "LLM_PROVIDER":""}):
            self.assertEqual(select_provider()[0], "mock")
