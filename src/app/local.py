from dotenv import load_dotenv

# load secrets to ENV
load_dotenv('secrets.properties')

# Include all default settings
from app.defaults import *

# Add env specific settings
RUNTIME_ENVIRONMENT = "local"
DEBUG = False

# add Security Setup
CORS_EXPOSE_HEADERS = ["session-id", "content-type", "content-length"]
CORS_ALLOW_HEADERS = CORS_EXPOSE_HEADERS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:4200',
]
ALLOWED_HOSTS = ['localhost','127.0.0.1']
CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
)
