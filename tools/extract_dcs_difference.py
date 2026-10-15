#!/usr/bin/env python3
"""Isolate one injected DCS command by subtracting a deterministic baseline."""

import argparse
import wave
from pathlib import Path

import numpy as np


def samples(path: Path):
    with wave.open(str(path), "rb") as source:
        params = source.getparams()
        if params.sampwidth != 2:
            raise ValueError(f"Expected signed 16-bit PCM: {path}")
        audio = np.frombuffer(source.readframes(params.nframes), dtype="<i2").astype(np.int32)
    return params, audio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("probe", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start", type=float, default=20.0)
    parser.add_argument("--end", type=float, default=24.0)
    args = parser.parse_args()

    base_params, baseline = samples(args.baseline)
    probe_params, injected = samples(args.probe)
    if base_params != probe_params or len(baseline) != len(injected):
        raise ValueError("Baseline and probe WAV formats/timelines do not match")
    rate = base_params.framerate * base_params.nchannels
    start, end = round(args.start * rate), round(args.end * rate)
    if start < 0 or end > len(baseline) or start >= end:
        raise ValueError("Invalid extraction interval")
    if np.any(baseline[:start] != injected[:start]):
        raise ValueError("Audio differed before the injected command; rerun with stable NVRAM")
    difference = np.clip(injected[start:end] - baseline[start:end], -32768, 32767).astype("<i2")
    with wave.open(str(args.output), "wb") as target:
        target.setparams((base_params.nchannels, 2, base_params.framerate, 0, "NONE", "not compressed"))
        target.writeframes(difference.tobytes())
    print(f"samples={len(difference)} peak={int(np.max(np.abs(difference.astype(np.int32))))}")


if __name__ == "__main__":
    main()
