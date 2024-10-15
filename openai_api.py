import os
from openai import OpenAI
import dotenv
import datetime
import time

dotenv.load_dotenv()

client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

def transcript(audio_byte: str) -> str:
    # First we give it a name to the temp file that will be created
    file_name = 'whatsapp_audio_{0}.ogg'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S'))
    # Then we create it using the byte data passed as a function parameter
    with open(file_name, 'wb') as audio_file:
        audio_file.write(audio_byte)
    # And then we read said file, and with the file stored localy we can sent it to OpenAI whisper that will 
    # return a transcription of the audio 
    with open(file_name, 'rb') as audio_file:
        transcripted_text = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    # Remove the file
    os.remove(file_name)
    return transcripted_text.text

def gpt_prompt(prompt: str) -> str:
    #Sends the prompt to gpt-3.5-turbo and return the response.
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print("Dont work alone")