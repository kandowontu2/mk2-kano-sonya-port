#!/usr/bin/env python3
"""Summarize time-aligned audio differences from isolated DCS command probes."""

import argparse
import hashlib
import wave
from pathlib import Path

import numpy as np


def read(path: Path):
    with wave.open(str(path), "rb") as source:
        params = source.getparams()
        audio = np.frombuffer(source.readframes(params.nframes), dtype="<i2").astype(np.int32)
    return params, audio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    params, baseline = read(args.directory / "baseline2.wav")
    rate = params.framerate * params.nchannels
    print("command  pre19s  20s  21s  22s  23s  24s  25s  26s  delta_sha8")
    for path in sorted(args.directory.glob("probe_*.wav")):
        probe_params, probe = read(path)
        if probe_params != params or len(probe) != len(baseline):
            raise ValueError(f"Timeline mismatch: {path}")
        values = []
        for second in range(19, 27):
            difference = probe[second * rate:(second + 1) * rate] - baseline[second * rate:(second + 1) * rate]
            values.append(float(np.sqrt(np.mean(np.square(difference.astype(np.float64))))))
        delta_hash = hashlib.sha256((probe - baseline)[20 * rate:].astype("<i4").tobytes()).hexdigest()[:8]
        print(f"{path.stem[6:]:>7} " + " ".join(f"{value:5.1f}" for value in values) +
              f"  {delta_hash}")


if __name__ == "__main__":
    main()
