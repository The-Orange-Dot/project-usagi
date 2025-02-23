import wave
import sys
import pyaudio
import numpy as np
from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, c_char_p, cdll
import os

# Error suppression setup
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
SILENCE_THRESHOLD = 1000
SILENCE_TIMEOUT = 2

def record():
    with noalsaerr():
        p = pyaudio.PyAudio()
        device_info = p.get_default_input_device_info()
        device_index = device_info['index']
        CHANNELS = int(device_info['maxInputChannels'])
        
        # Dynamically determine sample rate
        RATE = 16000  # Default
        try:
            # Test if 16000 Hz is supported
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK
            )
            stream.close()
        except:
            # Fallback to 44100 Hz
            RATE = 44100

        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=CHUNK
        )

        frames = []
        consecutive_silent = 0
        max_silent_chunks = int(SILENCE_TIMEOUT * RATE / CHUNK)

        print("Recording...")
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            
            audio_data = np.frombuffer(data, dtype=np.int16)
            if CHANNELS > 1:
                audio_data = audio_data.reshape(-1, CHANNELS)
                rms = np.max(np.sqrt(np.mean(audio_data**2, axis=0) + 1e-7))
            else:
                rms = np.sqrt(np.mean(audio_data**2) + 1e-7)

            if rms > SILENCE_THRESHOLD or np.isnan(rms):
                consecutive_silent = 0
            else:
                consecutive_silent += 1

            if consecutive_silent > max_silent_chunks:
                break

        stream.close()
        
        # Generate 1-second silence buffers
        samples_per_buffer = RATE * CHANNELS
        front_silence = np.zeros(samples_per_buffer, dtype=np.int16).tobytes()
        back_silence = np.zeros(samples_per_buffer, dtype=np.int16).tobytes()
        
        # Combine audio with buffers
        combined_data = front_silence + b''.join(frames) + back_silence

        # Save to file
        os.makedirs("./input", exist_ok=True)
        with wave.open('./input/audio.wav', 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(combined_data)

        p.terminate()
