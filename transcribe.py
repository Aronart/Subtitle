from faster_whisper import WhisperModel


def transcribe(video, whisper_model):
    print("Loading Faster-Whisper model...")
    model = WhisperModel(whisper_model, compute_type="int8_float32")

    print("Transcribing...")
    segments, info = model.transcribe(video, beam_size=5, word_timestamps=True)

    results = {"segments": []}
    for seg in segments:
        results["segments"].append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text,
            "words": [{"start": w.start, "end": w.end, "word": w.word} for w in seg.words]
        })

    print("Transcribtion Finished")
    return results

