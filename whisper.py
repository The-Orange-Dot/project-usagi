from faster_whisper import WhisperModel, BatchedInferencePipeline

def transcribe():
    model_size = "small.en"
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
    segments, info = batched_model.transcribe("audio.wav", beam_size=5, language="en", vad_parameters=dict(min_silence_duration_ms=2000))

    # print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        return segment.text

