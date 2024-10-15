import os
import dotenv
import requests

dotenv.load_dotenv()
phone_id = os.environ.get("PHONE_ID")
phone_number = os.environ.get("PHONE_NUMBER")
whatsapp_token = os.environ.get("WHATSAPP_TOKEN")

def send_message(message_text: str) -> bool:
    # It just sends the request to whatsapp API to send the message passed on the function parameter
    # to the number on the .env file
    requests.post(f'https://graph.facebook.com/v20.0/{phone_id}/messages', headers={
                                                                                        'Authorization': f'Bearer {whatsapp_token}'
                                                                                    },
                                                                                    json={
                                                                                        "messaging_product": "whatsapp",
                                                                                        "recipient_type": "individual",
                                                                                        "to": phone_number,
                                                                                        "type": "text",
                                                                                        "text": {
                                                                                            "preview_url": True,
                                                                                            "body": message_text
                                                                                        }
                                                                                    })
    return True

def audio_file(audio_id: str) -> str:
    #Runs the api to retrieve the audio file URL using the audio id
    url_request = requests.get(f'https://graph.facebook.com/v20.0/{audio_id}/', headers={
                                                                                            'Authorization': f'Bearer {whatsapp_token}', 
                                                                                            'Accept': 'application/json', 
                                                                                            'Content-Disposition': 'attachment; filename=test_audio.ogg'
                                                                                        })
    url_request_clean = url_request.json()['url']

    #Then it sent that URL to another API to return the audio file as a byte text
    audio_request = requests.get(url_request_clean, headers={'Authorization': f'Bearer {whatsapp_token}', 'Accept': 'audio/ogg', 'Content-Disposition': 'attachment; filename=test_audio.ogg'})
    return audio_request.content


if __name__ == "__main__":
    print("Dont work alone")