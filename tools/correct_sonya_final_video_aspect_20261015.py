"""Reuse proven lossless metadata correction; FFmpeg's SAR filter rounded127/150."""
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sp=importlib.util.spec_from_file_location('lossless_aspect',ROOT/'tools/correct_kano_video_aspect_20261015.py')
h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
h.D=ROOT/'video_sonya_final_20261015'
h.VIDEO=h.D/'Sonya_full_playthrough.mp4'
h.TEMP=h.D/'aspect_only.tmp.mp4'
h.RECEIPT=h.D/'aspect_verification.json'

if __name__=='__main__':h.main()
