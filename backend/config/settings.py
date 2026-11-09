import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "local-development-only-not-for-production")
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",") if host.strip()]
if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(os.environ["RENDER_EXTERNAL_HOSTNAME"])
if os.getenv("RENDER") and SECRET_KEY == "local-development-only-not-for-production":
    raise RuntimeError("Set SECRET_KEY for Render")
INSTALLED_APPS = ["qa"]
MIDDLEWARE = ["qa.middleware.JsonErrorsMiddleware", "django.middleware.security.SecurityMiddleware"]
DATABASES = {}
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DATA_UPLOAD_MAX_MEMORY_SIZE = 16_384
SECURE_CONTENT_TYPE_NOSNIFF = True
if os.getenv("RENDER"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
