
# Step 1)
# required deps
from app.settings import *


# Step 2)
# set test properties
load_dotenv('test.properties', override=True)
# BASE_DIR = Path(__file__).resolve().parent.parent
TEST_RUNNER = 'app.test.runner.NoDbTestRunner'

# Step 3)
# test settings
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME')
    }
}
