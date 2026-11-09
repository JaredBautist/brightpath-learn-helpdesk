from django.core.exceptions import RequestDataTooBig, SuspiciousOperation
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from qa.errors import AppError

class JsonErrorsMiddleware(MiddlewareMixin):
    """Keep framework errors credential-free and JSON, even with DEBUG enabled."""
    def process_exception(self, request, exception):
        code = "BAD_REQUEST" if isinstance(exception, (RequestDataTooBig, SuspiciousOperation)) else "INTERNAL_ERROR"
        return self.error_response(code)

    def process_response(self, request, response):
        if response.status_code >= 400 and not response.get("Content-Type", "").startswith("application/json"):
            code = {400: "BAD_REQUEST", 404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED", 500: "INTERNAL_ERROR"}.get(response.status_code, "INTERNAL_ERROR")
            replacement = self.error_response(code)
            if response.has_header("Allow"):
                replacement["Allow"] = response["Allow"]
            return replacement
        response["Cache-Control"] = "no-store"
        return response

    @staticmethod
    def error_response(code: str) -> JsonResponse:
        error = AppError(code)
        return JsonResponse({"ok": False, "errorType": error.code, "message": error.message}, status=error.status)
