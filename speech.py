import torch
import pyaudio
import wave
import os
import time

from dotenv import load_dotenv 
load_dotenv() 

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

def speak(text):
  print("Voice generated....IF I HAD ONE!!!")

  F5_CONNECT = os.getenv("F5_CONNECT")
  F5_PATH = os.getenv("F5_PATH")
  F5_DESTINATION = os.getenv("F5_DESTINATION")
  RETRIEVE_FILE = os.getenv("RETRIEVE_FILE")

  f5_command = f"""
  {F5_CONNECT} {F5_PATH}\\f5-tts_infer-cli \
  --model \\"F5-TTS\\" \
  --output_dir \\"{F5_DESTINATION}\\" \
  --output_file \\"output.wav\\" \
  --speed 1.6 \
  --gen_text \\"{text}\\"
  """

  os.system(f5_command)
  time.sleep(0.5) # Ensures the file is updated before being moved
  os.system(f"{F5_CONNECT} {RETRIEVE_FILE}")

## ============ UNCOMMENT BELOW TO ADD SPEECH WHEN YOU GET A SPEAKER ============================

# def speak(text):
#   tts.tts_to_file(text, speaker_wav="./voice-sample/nimi-sample-voice.mp3", file_path="./tmp/output.wav")

#   try:
#       with wave.open("./tmp/output.wav", 'rb') as wf:
#           # Initialize PyAudio
#           p = pyaudio.PyAudio()
          
#           # Open audio stream
#           stream = p.open(
#               format=p.get_format_from_width(wf.getsampwidth()),
#               channels=wf.getnchannels(),
#               rate=wf.getframerate(),
#               output=True
#           )
          
#           # Play audio
#           data = wf.readframes(1024)
#           while data:
#               stream.write(data)
#               data = wf.readframes(1024)

#   except Exception as e:
#       # Catch any error during playback/PyAudio setup
#       print("There's an error with the output device")
#       # Optional: Log the actual error for debugging
#       print(f"Error details: {str(e)}")

#   finally:
#       # Cleanup resources (even if an error occurs)

#       # Removes audio file
#       os.remove("./tmp/output.wav")

#       if stream is not None:
#           stream.stop_stream()
#           stream.close()
#       if p is not None:
#           p.terminate()

speak("test")