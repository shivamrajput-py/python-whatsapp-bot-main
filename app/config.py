import sys
import os
import logging


ACCESS_TOKEN="EABo5ekpspDMBOwKRqwgYhTa8ZAd6ZCRJDh8J86RhCQ03R4ZBDgIBjPRZAI8viNS2BJ9pVxfCVIGvVBntKcU9NCNQ2iENgPo58U4ANRXaLHUKt0nAXt6e9nNZCYbefmwG8ipxfp9f218rAXRdHtrudgZAI2gx8KZBsskEeZCDLKNdyAt33IMtIpdvNzZAzQZCymT8NE37XiI0zgZCZBOn8ZBUbMyAZD"

APP_ID="7381546791904307"
APP_SECRET="aa2bbe8eb68d27b916d29ed79b219e2a"
RECIPIENT_WAID="+919039971486" # Your WhatsApp number with country code (e.g., +31612345678)
VERSION="v18.0"
PHONE_NUMBER_ID="253194004550261"

VERIFY_TOKEN="12345"


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
