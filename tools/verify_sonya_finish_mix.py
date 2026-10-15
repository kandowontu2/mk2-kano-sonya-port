"""Fit Sonya's three simultaneous donor cues in an actual MAME stereo mix."""

import argparse
import wave
from pathlib import Path

import numpy as np
from scipy.signal import fftconvolve, resample_poly


def audio(path: Path) -> tuple[int, np.ndarray]:
    with wave.open(str(path), "rb") as source:
        if source.getsampwidth() != 2:
            raise ValueError(f"Expected 16-bit PCM: {path}")
        rate = source.getframerate()
        channels = source.getnchannels()
        samples = np.frombuffer(source.readframes(source.getnframes()), "<i2")
    return rate, samples.reshape(-1, channels).astype(np.float64).mean(axis=1) / 32768.0


def locate(mix: np.ndarray, sample: np.ndarray, rate: int,
           start_seconds: float, end_seconds: float) -> int:
    start, end = int(start_seconds * rate), int(end_seconds * rate)
    region = mix[start:end + len(sample)]
    scores = fftconvolve(region, sample[::-1], mode="valid")
    return start + int(np.argmax(scores))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mix", type=Path)
    parser.add_argument("--samples", type=Path,
                        default=Path(__file__).resolve().parent.parent / "samples" / "mk2ks")
    args = parser.parse_args()
    mix_rate, mix = audio(args.mix)
    names = ("sonya_kiss", "sonya_burn_fire", "sonya_burn_victim")
    clips = {}
    for name in names:
        rate, clip = audio(args.samples / f"{name}.wav")
        if mix_rate % rate:
            raise ValueError("Mix rate is not an integer multiple of sample rate")
        clips[name] = clip
    sample_rate = rate
    mix = resample_poly(mix, 1, mix_rate // sample_rate)
    offsets = {name: locate(mix, clips[name], sample_rate, 58, 68) for name in names}
    left = min(offsets.values())
    right = max(offsets[name] + len(clips[name]) for name in names)
    target = mix[left:right]
    matrix = np.zeros((len(target), len(names)), dtype=np.float64)
    for index, name in enumerate(names):
        begin = offsets[name] - left
        matrix[begin:begin + len(clips[name]), index] = clips[name]
    gains, *_ = np.linalg.lstsq(matrix, target, rcond=None)
    full_error = np.sum((target - matrix @ gains) ** 2)
    for index, name in enumerate(names):
        reduced = np.delete(matrix, index, axis=1)
        reduced_gains, *_ = np.linalg.lstsq(reduced, target, rcond=None)
        reduced_error = np.sum((target - reduced @ reduced_gains) ** 2)
        improvement = (reduced_error - full_error) / reduced_error
        print(f"{name} time={offsets[name] / sample_rate:.4f}s "
              f"gain={gains[index]:.4f} unique_error_reduction={improvement:.5f}")
        if gains[index] < 0.25 or improvement < 0.005:
            raise SystemExit(f"{name} was not independently audible in the mix")


if __name__ == "__main__":
    main()
