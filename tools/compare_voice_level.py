"""Read-only rough voice-level comparison around traced MKII sound commands.

The output reports band-limited energy above a short preceding background.
It is an A/B aid, not an isolated DCS sample or a perceptual loudness claim.
"""
import math
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfiltfilt


def load(path):
    with wave.open(path, "rb") as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        samples = np.frombuffer(source.readframes(source.getnframes()), "<i2")
    return rate, samples.reshape(-1, channels).astype(np.float64).mean(axis=1) / 32768


def energy(samples, rate, start, duration):
    window = samples[round(start * rate) : round((start + duration) * rate)]
    return float(np.mean(window * window))


for spec in sys.argv[1:]:
    label, path, frame = spec.split("|", 2)
    rate, samples = load(path)
    samples = sosfiltfilt(butter(4, (300, 3000), btype="bandpass", fs=rate, output="sos"), samples)
    when = int(frame) / 54.706840
    background = energy(samples, rate, when - 0.6, 0.5)
    active = energy(samples, rate, when + 0.05, 1.1)
    above = math.sqrt(max(active - background, 0))
    print(f"{label} command={when:.3f}s background={math.sqrt(background):.5f} "
          f"active={math.sqrt(active):.5f} excess={above:.5f}")
