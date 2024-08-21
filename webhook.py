from flask import Flask, request, jsonify
import os

whatsapp_token = os.environ.get("WHATSAPP_TOKEN")
verify_token = os.environ.get("VERIFY_TOKEN")

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json  # Get the JSON data from the incoming request
    # Process the data and perform actions based on the event
    print("Received webhook data:", data)
    return jsonify({'message': 'Webhook received successfully'}), 200

@app.route('/webhook', methods=['GET'])
def verify():
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == verify_token:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        print("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)