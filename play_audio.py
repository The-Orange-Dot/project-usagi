import wave
import pyaudio
import librosa
import soundfile as sf
import time

def get_supported_rates(device_index):
    p = pyaudio.PyAudio()
    rates = [8000, 16000, 44100, 48000]
    supported_rates = []
    
    for rate in rates:
        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=2,
                rate=rate,
                output=True,
                output_device_index=device_index
            )
            stream.close()
            supported_rates.append(rate)
        except:
            pass
            
    p.terminate()
    return supported_rates

def resample_audio(input_path, output_path, target_rate):
    y, sr = librosa.load(input_path, sr=None)
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_rate)
    sf.write(output_path, y_resampled, target_rate)

def play(file_path, device_index = 1):
    # Check file's current sample rate
    with wave.open(file_path, 'rb') as wf:
        file_rate = wf.getframerate()

    # Get supported rates for the USB speaker
    supported_rates = get_supported_rates(device_index)
    
    # Resample if needed
    if file_rate not in supported_rates:
        # print(f"Resampling from {file_rate} Hz to {supported_rates[0]} Hz")
        resample_audio(file_path, "./output/output.wav", supported_rates[0])
        file_path = "./output/output.wav"
    
    # Play the audio
    with wave.open(file_path, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            output_device_index=device_index
        )
        
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        # Calculate duration
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        # print(f"Audio duration: {duration:.2f} seconds ({int(duration//60)}:{int(duration%60):02d})")
        
        print("Listening...")

        # SET AUDIO VOLUME WITH amixer -c 3 set 'PCM' 70%
        stream.stop_stream()
        stream.close()
        p.terminate()

