"""Fit concurrent donor effects in a recorded MKII stereo mix (read-only)."""
import sys
import wave

import numpy as np
from scipy.signal import resample_poly


def pcm(path):
    with wave.open(path, "rb") as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        assert source.getsampwidth() == 2
        data = np.frombuffer(source.readframes(source.getnframes()), "<i2")
    return rate, data.reshape(-1, channels).astype(np.float64).mean(axis=1)


mix_rate, mix = pcm(sys.argv[1])
kiss_at, burn_at = float(sys.argv[2]), float(sys.argv[3])
samples = [pcm(path) for path in sys.argv[4:7]]
assert len(samples) == 3 and len({rate for rate, _ in samples}) == 1
sample_rate = samples[0][0]
assert mix_rate % sample_rate == 0
mix = resample_poly(mix, 1, mix_rate // sample_rate)
start = round(kiss_at * sample_rate)
offsets = [0, round((burn_at - kiss_at) * sample_rate),
           round((burn_at - kiss_at) * sample_rate)]
length = max(offset + len(sample) for offset, (_, sample) in zip(offsets, samples))
region = mix[start:start + length]
assert len(region) == length
columns = []
for offset, (_, sample) in zip(offsets, samples):
    column = np.zeros(length)
    column[offset:offset + len(sample)] = sample
    columns.append(column)
matrix = np.column_stack(columns)
gains, _, _, _ = np.linalg.lstsq(matrix, region, rcond=None)
for name, gain in zip(("kiss", "fire", "victim"), gains):
    print(f"{name}_gain={gain:.4f}")
residual = region - matrix @ gains
print(f"residual_rms={np.sqrt(np.mean(residual ** 2)):.2f}")
