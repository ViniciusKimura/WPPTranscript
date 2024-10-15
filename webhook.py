from flask import Flask, request, jsonify
import os
import dotenv
import openai_api
import meta_api

dotenv.load_dotenv()
list_id = [] #List containing the messages IDs
waiting_response = False #Used to when the is already a audio waiting a user response
transcripted_text = None #Store the audio transcripted waiting for a response

verify_token = os.environ.get("VERIFY_TOKEN")

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    global waiting_response
    global transcripted_text

    data = request.json  # Get the JSON data from the incoming request
    #print("Received webhook data:", data)
    #print("\n")
    #Fist tests if the message is a message, if not, it would throw an error
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]        
    except:
        return jsonify({'message': 'Message not found'}), 404
    #Then it checks if the message is audio and if the message already got processed to prevent duplicates
    print("Received webhook data:", data)
    #Checks if its a audio and then if there is already an audio waiting for a response
    if(message["type"] == "audio" and transcripted_text == None and waiting_response == False):
        audio_id = message["audio"]["id"]
        if(audio_id not in list_id):
            #print(audio_id)
            list_id.append(audio_id) #Puts the message id on the list so it does not run again the same message
            # Sends the audio id to a function that will return the audio byte data
            audio_request = meta_api.audio_file(audio_id)
            meta_api.send_message("Sending audio to ")
            #With said byte information, we send it to my othor code to handle the OpenAI request
            transcripted_text = openai_api.transcript(audio_request)
            waiting_response = True
            meta_api.send_message("Send the number reference to the action. \n\n" +
                                  "1. Just transcript the audio \n" +
                                  "2. Send the audio to Chat GPT \n")
        else:
            return jsonify({'message': 'Audio already processed'}), 200
    #If theres a audio waiting for a response, it will check for text messages containing some available option
    elif (message["type"] == "text" and transcripted_text != None and waiting_response == True):
        if(message["text"]["body"] == '1'): #1 will just send the transcription and reset the global variables so another audio could be sent
            meta_api.send_message("Transcription:")
            meta_api.send_message(transcripted_text)
            transcripted_text = None
            waiting_response = False
        elif(message["text"]["body"] == '2'): #2 will just send the transcription and use it as a prompt on CHAT-GPT, and then reset the global variables
            meta_api.send_message("Transcription:")
            meta_api.send_message(transcripted_text)
            meta_api.send_message("Sending audio to Chat GPT")
            meta_api.send_message(openai_api.gpt_prompt(transcripted_text))
            transcripted_text = None
            waiting_response = False
        else:
            meta_api.send_message("Chose a valid option.")
        
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