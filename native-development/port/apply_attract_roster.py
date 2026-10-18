"""Mechanical application of the native fourteen-fighter attract roster."""
from pathlib import Path
from drone_source import integrate_attract
p=Path(__file__).resolve().parent.parent/'baseline/mk2-rebuild-main/srcp/MKAMODE.ASM'
p.write_text(integrate_attract(p.read_text()))
