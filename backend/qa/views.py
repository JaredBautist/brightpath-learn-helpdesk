import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from qa.errors import AppError
from qa.service import ask_question

@csrf_exempt
@require_POST
def ask(request: HttpRequest) -> JsonResponse:
    """Accept a bounded JSON question and return a sourced answer or JSON error."""
    try:
        if request.content_type != "application/json":
            raise AppError("BAD_REQUEST")
        try:
            payload = json.loads(request.body)
        except (ValueError, UnicodeError) as exc:
            raise AppError("BAD_REQUEST") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("question"), str):
            raise AppError("BAD_REQUEST")
        question = payload["question"].strip()
        if not question or len(payload["question"]) > 500:
            raise AppError("BAD_REQUEST")
        provider, answer = ask_question(question, request.GET.get("simulate") == "failure")
        return JsonResponse({"ok": True, "provider": provider, **answer})
    except AppError as error:
        return JsonResponse({"ok": False, "errorType": error.code, "message": error.message}, status=error.status)
