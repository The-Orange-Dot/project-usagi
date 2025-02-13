import torch
import pyaudio
import wave
import os
import time
from play_audio import play

from dotenv import load_dotenv 
load_dotenv() 

F5_CONNECT = os.getenv("F5_CONNECT")
F5_PATH = os.getenv("F5_PATH")
F5_DESTINATION = os.getenv("F5_DESTINATION")
RETRIEVE_FILE = os.getenv("RETRIEVE_FILE")
INIT_AUDIO = os.getenv("INIT_AUDIO")

def speak(text):

  f5_command = f"""
  {INIT_AUDIO} | {F5_CONNECT} {F5_PATH}f5-tts_infer-cli \
  --model \\"F5-TTS\\" \
  --output_dir \\"{F5_DESTINATION}\\" \
  --output_file \\"output.wav\\" \
  --speed 1.5 \
  --gen_text \\"{text}\\"
  """

  os.system(f5_command) # Sends cmd to generate audio speech for generated text

  if os.path.exists("./tmp/output.wav"):
    os.remove("./tmp/output.wav")

  os.system(RETRIEVE_FILE) # Sends the audio from the remote server to here to play

  play("./tmp/output.wav", device_index=1)
