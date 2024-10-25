import os

from dotenv import load_dotenv

# Load environment variables from the .env file
if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()
class Env:
    # Value should be enum["sandbox","production"]
    environment = os.getenv("ENVIRONMENT")
    admin_email = os.getenv("ADMIN_EMAIL")

    EMAIL_SERVER = os.getenv("EMAIL_SERVER")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    EBAY_INVENTORY_LIMITATION=os.getenv("EBAY_INVENTORY_LIMITATION")