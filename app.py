import os
import json
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")

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
    """Handles incoming messages from WhatsApp."""
    data = request.get_json()

    # Log incoming message for debugging
    print(json.dumps(data, indent=2))

    return "Webhook received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
