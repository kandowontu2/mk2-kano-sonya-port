"""Mechanical application of reviewed back-break table bounds extension."""
from pathlib import Path
from throw_source import extend_back_break_alignment
p=Path(__file__).resolve().parent.parent/'baseline/mk2-rebuild-main/srcp/MKSLAM.ASM'
p.write_text(extend_back_break_alignment(p.read_text()))
