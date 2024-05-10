import os
from .logger import DataDogLogger
from .dreambooth import DreamBoothAPI


REPLICATE_TOKEN = os.getenv("REPLICATE_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "test_pass")
DOCS_USERNAME = os.getenv("DOCS_USERNAME", "test_name")
DATADOG_SERVICE_NAME = os.getenv("DATADOG_SERVICE_NAME", "replicate-api")
API_KEY = os.getenv("API_KEY")
logger = DataDogLogger(DATADOG_SERVICE_NAME)
api = DreamBoothAPI(api_token=REPLICATE_TOKEN)
