from dotenv import load_dotenv

# Load test properties
load_dotenv('test.properties')
# Include all default settings
from app.defaults import *

# Add env specific settings
RUNTIME_ENVIRONMENT = "test"
DEBUG = True
