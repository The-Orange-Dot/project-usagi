import record_voice
import whisper
import ollama_input
import os
import json
import time

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

while True:
  # Records the voice of the user and transcribes it
  record_voice.record()
  transcribed_text = whisper.transcribe()
  
  if transcribed_text:
    print(transcribed_text)

    # Calls Deepseek to respond to transcribed text
    ollama_response = ollama_input.ollama_chat(message_data, transcribed_text)

    # Concats the user's transcribed text and the ollamas
    concat.concat_text(file_name, "user", transcribed_text)
    concat.concat_text(file_name, "assistant", ollama_response["answer"])

    print("")
    print(f"\033[96m[YOU]: {transcribed_text}") # For Cyan colored text: \033[96m
    print(f"\033[92m[MOCCHAN]: " + ollama_response["answer"]) # For Green colored text: \033[92m
    print("\033[37m") # Resets the color of text back to white

    time.sleep(2)
  else:
    print("NO TEXT!!")

    if counter == 5:
      print("Ending Listener")
      break
    else:
      # counter+=1
      print(f"Keeing an ear out. Retrying {6 - counter} more times.")


# Removes audio file
os.remove("./audio.wav")