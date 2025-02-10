import wave
import sys

import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

def record():
  # Records 
  with wave.open('audio.wav', 'wb') as wf:
      p = pyaudio.PyAudio()
      wf.setnchannels(CHANNELS)
      wf.setsampwidth(p.get_sample_size(FORMAT))
      wf.setframerate(RATE)

      stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

      print('Recording...')
      for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
          wf.writeframes(stream.read(CHUNK))
      print('Transcribing...')

      stream.close()
      p.terminate()

