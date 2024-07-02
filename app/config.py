import sys
import os
from env import *
import logging

def load_configurations(app):
    app.config["ACCESS_TOKEN"] = ACCESS_TOKEN
    app.config["YOUR_PHONE_NUMBER"] = "9039971486"
    app.config["APP_ID"] = APP_ID
    app.config["APP_SECRET"] = APP_SECRET
    app.config["RECIPIENT_WAID"] = RECIPIENT_WAID
    app.config["VERSION"] = VERSION
    app.config["PHONE_NUMBER_ID"] = PHONE_NUMBER_ID
    app.config["VERIFY_TOKEN"] = VERIFY_TOKEN


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
