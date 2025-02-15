import suppress
suppress.suppress_jack_errors()

import asyncio
import record_voice
import whisper
import os
import json
from send_transcription import send_transcription
import librosa
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv('API_ENDPOINT')
server_ip = os.getenv('SERVER_IP')
port = os.getenv('SERVER_PORT')

# Loads json data of chat history
with open('mocchan/data.json', "r") as file:
  folder_path = "./mocchan"
  file_name = "data.json"
  file_path = os.path.join(folder_path, file_name)
  with open(file_path, 'r+') as file:
    message_data = json.load(file)

# Creates folder for storing history
history_folder = 'mocchan'
if not os.path.exists(history_folder):
  os.mkdir('./mocchan')
file_name = f"./mocchan/data.json"

print()
print("========================================")
print("Starting up Mocchan")
print("========================================")
print()

print("You're now talking to Mocchan...")

if os.path.exists("./tmp/output.wav"):
  os.remove("./tmp/output.wav")

counter = 0

while True:
  # Create tmp directory if needed
  os.makedirs('./input', exist_ok=True)

  # Records the voice of the user and transcribes it
  record_voice.record()

  if os.path.exists("./input/audio.wav"):
    sound_file_duration = librosa.get_duration(path="./input/audio.wav")
  else:
    sound_file_duration = 1
  
  if 'sound_file_duration' in locals() and sound_file_duration > 1.6:
    print("Transcribing....")    
    transcribed_text = whisper.transcribe()    
    counter = 0

    if transcribed_text:
        result = send_transcription(transcribed_text)
        if result:
            print("Audio file saved successfully!")
        else:
            print("Failed to save audio file")
    else:
      print("No text to transcribe...")
  else:
    if counter == 50:
      print("Mocchan was left alone for too long. She's going to sleep.")
      break
    elif counter == 10 or counter == 20:
      print('Listening...')
      counter+=1
    elif counter == 30:
      print("Mocchan is still waiting here...")
      counter+=1
    elif counter == 40:
      print("Mocchan's about to leave...")
      counter+=1
    else:
      counter+=1