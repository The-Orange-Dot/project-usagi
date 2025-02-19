from faster_whisper import WhisperModel, BatchedInferencePipeline
import os

def transcribe():
    model_size = "tiny.en"
    # Models
    # tiny.en, tiny, base.en, base, 
    # small.en, small, medium.en, 
    # medium, large-v1, large-v2, large-v3, large, 
    # distil-large-v2, distil-medium.en, distil-small.en, 
    # distil-large-v3, large-v3-turbo, turbo

    # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")
    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    batched_model = BatchedInferencePipeline(model=model)
    segments, info = batched_model.transcribe("./input/audio.wav", beam_size=5, language="en", vad_parameters=dict(min_silence_duration_ms=2000))
    
    # Removes audio file
    os.remove("./input/audio.wav")


    for segment in segments:
        return segment.text.replace("Nacchan", "nah-chan") #Makes Nacchan's name readable
