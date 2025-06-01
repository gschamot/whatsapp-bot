import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Environment variables (hardcoded token)
VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
PHONE_NUMBER_ID = "670463136150869"
ACCESS_TOKEN = "EAAcSzUCVS8gBO7ZBpN9xkoronm81hTjHgUIFc5MFlN9rstsCc8L2ngRSKe34xDefDRV0S1S6ZAuLCQal8j1LONWCvhHvi61tGZC6rpqO8rtZBSZATr9YlCDkYs2fBSD7VbTQ8M1ZCMt4lSWZCw2mWhux64XwQadLW13e96xq0tbNkB1d4YwBo7nHYasJLpvbtbaqbJgGJdyK1oPmZBwvubyaZCP7ZB3JTXk64fDqAZD"

@app.route("/webhook", methods=["GET"])
def verify():
    """Handles the verification handshake from Meta."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handles incoming messages and sends auto-replies."""
    data = request.get_json()
    print(json.dumps(data, indent=2))

    # Extract sender ID and message
    messages = data.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])
    if messages:
        sender_id = messages[0]["from"]
        message_text = messages[0]["text"]["body"]

        # Auto-reply message
        reply_text = f"Hey {sender_id}, thanks for your message: '{message_text}'."

