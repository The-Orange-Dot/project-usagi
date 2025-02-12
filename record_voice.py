import wave
import sys

import pyaudio
import numpy as np

# Hides errors from pyaudio
from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 16000
SILENCE_THRESHOLD = 800  # Adjust based on your environment (Decrease for a more sensative )
SILENCE_TIMEOUT = 1.5    # Seconds of silence before stopping

def record():
    with wave.open('./tmp/audio.wav', 'wb') as wf:
        with noalsaerr():
            p = pyaudio.PyAudio()
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

            consecutive_silent = 0
            max_silent_chunks = int(SILENCE_TIMEOUT * RATE / CHUNK)

            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                wf.writeframes(data)
                
                # Handle stereo channels properly
                audio_data = np.frombuffer(data, dtype=np.int16)
                if CHANNELS > 1:
                    # Reshape to separate channels
                    audio_data = audio_data.reshape(-1, CHANNELS)
                    # Calculate RMS per channel and take the maximum
                    rms = np.max(np.sqrt(np.mean(audio_data**2, axis=0) + 1e-7))
                else:
                    # Mono channel calculation with epsilon to prevent sqrt(0)
                    rms = np.sqrt(np.mean(audio_data**2) + 1e-7)

                # print(f"Current RMS: {rms:.2f}")  # Debug output

                # Reset counter when voice is detected
                if rms > SILENCE_THRESHOLD or np.isnan(rms):
                    consecutive_silent = 0
                else:
                    consecutive_silent += 1

                # Stop recording if silence persists
                if consecutive_silent > max_silent_chunks:
                    # print('Stopped recording.')
                    break

            stream.close()
            p.terminate()
