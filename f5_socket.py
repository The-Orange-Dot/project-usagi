import socket
import numpy as np
import asyncio
import pyaudio
import os
import time

def save_audio_for_debuging(full_audio):
    # Generate WAV header and save as WAV
    timestamp = int(time.time() * 1000)
    filename = f"./output/audio_{timestamp}.wav"
    
    num_channels = 1
    sample_width = 4  # 32-bit float (4 bytes)
    sample_rate = 48000
    audio_format = 3  # WAVE_FORMAT_IEEE_FLOAT
    data_size = len(full_audio)
    riff_chunk_size = 36 + data_size  # 36 is header size excluding 'RIFF' and riff size

    wav_header = (
        b'RIFF' +
        riff_chunk_size.to_bytes(4, 'little') +
        b'WAVE' +
        b'fmt ' +
        (16).to_bytes(4, 'little') +  # fmt chunk size (16 bytes)
        audio_format.to_bytes(2, 'little') +
        num_channels.to_bytes(2, 'little') +
        sample_rate.to_bytes(4, 'little') +
        (sample_rate * num_channels * sample_width).to_bytes(4, 'little') +  # byte rate
        (num_channels * sample_width).to_bytes(2, 'little') +  # block align
        (sample_width * 8).to_bytes(2, 'little') +  # bits per sample
        b'data' +
        data_size.to_bytes(4, 'little')
    )

    with open(filename, 'wb') as f:
        f.write(wav_header)
        f.write(full_audio)

    print(f"Audio saved to {filename}")

async def listen_to_voice(text, server_ip='192.168.86.27', server_port=9998):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    async def play_audio_stream():
        silent_duration = 0.5  # seconds
        silent_samples = int(silent_duration * 48000)
        silent_buffer = np.zeros(silent_samples, dtype=np.float32).tobytes()
        
        buffer = silent_buffer
        full_audio = b''
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                         channels=1,
                         rate=48000,
                         output=True,
                         frames_per_buffer=2048)
        
        os.makedirs("./output", exist_ok=True)

        try:
            while True:
                chunk = await asyncio.get_event_loop().run_in_executor(None, client_socket.recv, 1024)
                if not chunk:
                    break
                if b"END_OF_AUDIO" in chunk:
                    buffer += chunk.replace(b"END_OF_AUDIO", b"")
                    if buffer:
                        audio_array = np.frombuffer(buffer, dtype=np.float32).copy()
                        stream.write(audio_array.tobytes())
                        full_audio += buffer
                    break
                buffer += chunk
                while len(buffer) >= 4096:
                    audio_chunk = buffer[:4096]
                    audio_array = np.frombuffer(audio_chunk, dtype=np.float32).copy()
                    stream.write(audio_array.tobytes())
                    full_audio += audio_chunk
                    buffer = buffer[4096:]
            

            # COMMENT THIS OUT WHEN NOT DEBUGGING!!
            save_audio_for_debuging(full_audio)

        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    try:
        await asyncio.get_event_loop().run_in_executor(None, client_socket.sendall, text.encode('utf-8'))
        await play_audio_stream()
        print("Audio playback finished.")

    except Exception as e:
        print(f"Error in listen_to_voice: {e}")

    finally:
        client_socket.close()

async def main(text):
    await listen_to_voice(text, server_ip='192.168.86.27', server_port=9998)