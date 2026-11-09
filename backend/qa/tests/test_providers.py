import json
import os
from unittest import TestCase
from unittest.mock import patch
import httpx
from qa.errors import AppError
from qa.service import select_provider
from qa.llm.nvidia import NvidiaProvider

@patch.dict(os.environ, {"NVIDIA_API_KEY":"test-placeholder", "NVIDIA_MODEL":"test-model", "NVIDIA_JSON_MODE":"false", "NVIDIA_TIMEOUT_SECONDS":"15"})
class ProviderTests(TestCase):
    def test_success_request_contract(self):
        response = httpx.Response(200, json={"choices":[{"message":{"content":"{}"}}]})
        with patch("qa.llm.nvidia.httpx.post", return_value=response) as post:
            self.assertEqual(NvidiaProvider().generate("system", "question"), "{}")
            self.assertEqual(post.call_args.kwargs["json"]["model"], "test-model")
            self.assertEqual(post.call_args.kwargs["json"]["temperature"], 0)
            self.assertEqual(post.call_args.kwargs["timeout"].read, 15.0)
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

    def test_timeout_default_when_variable_absent(self):
        with patch.dict(os.environ):
            os.environ.pop("NVIDIA_TIMEOUT_SECONDS", None)
            self.assertEqual(NvidiaProvider().timeout.read, 15.0)

    def test_timeout_override_and_connection_budgets(self):
        for seconds in (10, 45):
            with self.subTest(seconds=seconds), patch.dict(os.environ, {"NVIDIA_TIMEOUT_SECONDS":str(seconds)}), patch("qa.llm.nvidia.httpx.post", return_value=httpx.Response(200,json={"choices":[{"message":{"content":"{}"}}]})) as post:
                NvidiaProvider().generate("s", "q")
                timeout = post.call_args.kwargs["timeout"]
                self.assertEqual(timeout.read, float(seconds))
                self.assertEqual((timeout.connect, timeout.write, timeout.pool), (5.0, 5.0, 5.0))

    def test_invalid_timeout_never_calls_provider(self):
        for configured in ["", "invalid", "nan", "inf", "0", "-1", "4.9", "60.1"]:
            with self.subTest(configured=configured), patch.dict(os.environ, {"NVIDIA_TIMEOUT_SECONDS":configured}), patch("qa.llm.nvidia.httpx.post") as post, self.assertRaises(AppError) as error:
                NvidiaProvider().generate("s", "q")
            self.assertEqual(error.exception.code, "MODEL_UNAVAILABLE")
            post.assert_not_called()

    def test_timeout_logging_does_not_expose_private_content(self):
        for failure in [httpx.ConnectTimeout, httpx.ReadTimeout, httpx.WriteTimeout, httpx.PoolTimeout]:
            with self.subTest(phase=failure.__name__), patch("qa.llm.nvidia.httpx.post", side_effect=failure("private upstream diagnostic")), self.assertLogs("qa.llm.nvidia", level="WARNING") as logs, self.assertRaises(AppError) as error:
                NvidiaProvider().generate("private system prompt", "private question")
            self.assertEqual(error.exception.code, "TIMEOUT")
            self.assertEqual(error.exception.status, 504)
            self.assertNotIn("15 seconds", error.exception.message)
            logged = " ".join(logs.output)
            self.assertIn(failure.__name__, logged)
            self.assertIn("elapsed_seconds=", logged)
            self.assertIn("test-model", logged)
            self.assertNotIn("private", logged)
            self.assertNotIn("test-placeholder", logged)
