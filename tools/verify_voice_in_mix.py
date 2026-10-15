"""Locate a voice sample in a recorded MAME stereo mix (read-only audit)."""
import sys
import wave

import numpy as np
from scipy.signal import fftconvolve, resample_poly


def audio(path):
    with wave.open(path, "rb") as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        if source.getsampwidth() != 2:
            raise ValueError(f"Expected 16-bit PCM: {path}")
        values = np.frombuffer(source.readframes(source.getnframes()), "<i2")
    return rate, values.reshape(-1, channels).astype(np.float64).mean(axis=1) / 32768.0


mix_rate, mix = audio(sys.argv[1])
voice_rate, voice = audio(sys.argv[2])
if mix_rate % voice_rate:
    raise ValueError("Mix rate must be an integer multiple of sample rate")
mix = resample_poly(mix, 1, mix_rate // voice_rate)
start = int(float(sys.argv[3]) * voice_rate)
end = int(float(sys.argv[4]) * voice_rate)
region = mix[start : end + len(voice)]
correlation = fftconvolve(region, voice[::-1], mode="valid")
energies = np.r_[0, np.cumsum(region * region)]
window_energy = energies[len(voice) :] - energies[: -len(voice)]
normalized = correlation / np.sqrt(np.maximum(window_energy, 1e-12) * np.sum(voice * voice))
peak = int(np.argmax(np.abs(normalized)))
offset = start + peak
gain = correlation[peak] / np.sum(voice * voice)
print(f"time={offset / voice_rate:.4f}s correlation={normalized[peak]:.4f} gain={gain:.4f}")
