import os
from openai import OpenAI
import dotenv
import datetime
import time

dotenv.load_dotenv()
verify_token = os.environ.get("VERIFY_TOKEN")

client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

def initClient():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

def transcript(openai_client, audio_byte):
    # First we give it a name to the temp file that will be created
    file_name = 'whatsapp_audio_{0}.ogg'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S'))
    # Then we create it using the byte data passed as a function parameter
    with open(file_name, 'wb') as audio_file:
        audio_file.write(audio_byte)
    # And then we read said file, and with the file stored localy we can sent it to OpenAI whisper that will 
    # return a transcription of the audio 
    with open(file_name, 'rb') as audio_file:
        transcripted_text = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    #print(transcripted_text.text)
    # Remove the file
    os.remove(file_name)
    return transcripted_text.text

def transcript_demo():
    with open('whatsapp_audio.ogg', 'rb') as audio_file:
            #audio_file.write(audio_byte)
            transcripted_text = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
    return transcripted_text

if __name__ == "__main__":
    print(transcript_demo())