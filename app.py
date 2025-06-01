import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")

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

        # Send reply using WhatsApp API
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": sender_id,
            "type": "text",
            "text": {"body": reply_text}
        }
        response = requests.post("https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages", headers=headers, json=payload)
        print("Reply sent:", response.json())

    return "Webhook received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

