import suppress
# suppress.suppress_jack_errors()

import record_voice
import whisper
import ollama_input
import os
import json
import time
import librosa
import speech

import helpers.concat_files as concat

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

counter = 0

print()
print("========================================")
print("Starting up Mocchan")
print("========================================")
print()

print("You're now talking to Mocchan...")


while True:
  # Records the voice of the user and transcribes it
  record_voice.record()

  sound_file_duration = librosa.get_duration(path="./tmp/audio.wav")
  
  if sound_file_duration > 1.6:
    print("Transcribing....")
    transcribed_text = whisper.transcribe()
    
    if transcribed_text:
      # Calls Deepseek to respond to transcribed text
      ollama_response = ollama_input.ollama_chat(message_data, transcribed_text)

      # Allows Mocchan to speak
      speech.speak(ollama_response["answer"])

      # Concats the user's transcribed text and the ollamas
      concat.concat_text(file_name, "user", transcribed_text)
      concat.concat_text(file_name, "assistant", ollama_response["answer"])

      print("")
      print(f"\033[96m[YOU]: {transcribed_text}") # For Cyan colored text: \033[96m
      print(f"\033[92m[MOCCHAN]: " + ollama_response["answer"]) # For Green colored text: \033[92m
      print("\033[37m") # Resets the color of text back to white

      counter = 0
      time.sleep(2)
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

