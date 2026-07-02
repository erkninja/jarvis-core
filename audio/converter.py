def raw_to_wav(raw_path, wav_path, sample_rate=16000):
    import wave

    with open(raw_path, "rb") as f:
        raw_data = f.read()

    with wave.open(wav_path, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(raw_data)
