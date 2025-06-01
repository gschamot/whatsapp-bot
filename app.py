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
        response = requests.post(f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages", headers=headers, json=payload)
        
        print("Reply sent:", response.json())

        # ✅ Fix: Always return a response to Meta
        return json.dumps({"status": "message sent"}), 200

    return json.dumps({"status": "no message found"}), 200
