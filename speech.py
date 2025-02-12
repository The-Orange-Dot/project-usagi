import torch
from TTS.api import TTS
import simpleaudio as sa

def speak(text):
  # Get device
  device = "cuda" if torch.cuda.is_available() else "cpu"

  # # Init TTS with the target model name
  tts = TTS(model_name="tts_models/en/jenny/jenny").to(device)

  tts.tts_to_file(text, speaker_wav="./voice-sample/nimi-sample-voice.mp3", file_path="output.wav")

  wave_obj = sa.WaveObject.from_wave_file("./output.wav")
  play_obj = wave_obj.play()
  play_obj.wait_done()

