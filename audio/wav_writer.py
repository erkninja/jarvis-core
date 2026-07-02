import wave
import os

os.makedirs("/app/data", exist_ok=True)


def write_wav(filename, pcm_bytes, sample_rate=16000):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)
