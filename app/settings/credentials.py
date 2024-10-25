import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Security:
    clientId = os.getenv("APP_CLIENT_ID")
    clientSecret = os.getenv("APP_CLIENT_SECRET")

class Connector:
    clientId = os.getenv("CONNECTOR_CLIENT_ID")
    clientSecret = os.getenv("CONNECTOR_CLIENT_SECRET")
    endpoint = os.getenv("CONNECOTR_END_POINT")