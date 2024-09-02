
# Step 1)
# required deps
import os
from dotenv import load_dotenv

# Step 2)
# set test properties
load_dotenv('test.properties')

# Step 3)
# test settings
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
