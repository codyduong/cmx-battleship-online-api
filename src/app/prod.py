# Production Deployment Settings

from app.settings import *

from socket import gethostbyname, gethostname

# Add env specific settings
RUNTIME_ENVIRONMENT = "prod"
DEBUG = False

# Step 5.1)
# Security Setup
CORS_EXPOSE_HEADERS = ["session-id", "content-type", "content-length"]
CORS_ALLOW_HEADERS = CORS_EXPOSE_HEADERS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:4200',
    'https://www.morriswa.org',
]
ALLOWED_HOSTS = [
    'www.morriswa.org',
    gethostbyname(gethostname())
]
CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
)
