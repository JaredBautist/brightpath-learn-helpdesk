ERRORS = {
    "BAD_REQUEST": (400, "Send a JSON question containing 1 to 500 characters."),
    "RATE_LIMIT": (429, "The model rate limit was reached. Please try again later."),
    "INVALID_MODEL_OUTPUT": (502, "The model returned an invalid answer. Please try again."),
    "MODEL_UNAVAILABLE": (503, "The model is unavailable. Please try again later."),
    "MISSING_API_KEY": (503, "The selected model provider is missing its API key."),
    "TIMEOUT": (504, "The model request timed out. Please try again."),
    "NOT_FOUND": (404, "API route not found."),
    "METHOD_NOT_ALLOWED": (405, "Use POST for this endpoint."),
    "INTERNAL_ERROR": (500, "An unexpected server error occurred."),
}

class AppError(Exception):
    """Application failure identified by a public, credential-free error code."""
    def __init__(self, code: str):
        self.code = code
        self.status, self.message = ERRORS[code]
        super().__init__(code)
