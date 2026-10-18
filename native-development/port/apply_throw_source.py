"""Mechanical live-source application of canonical own throw integration."""
from pathlib import Path
from throw_source import integrate
PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline/mk2-rebuild-main/srcp'
p=BASE/'MKSLAM.ASM'
p.write_text(integrate(p.read_text()))
# Keep TI's32-character symbol limit, without changing any data records.
for filename in ('KSTHANI.ASM','KSTHVIC.ASM'):
    p=PORT/'generated_throw'/filename
    text=p.read_text()
    for owner in ('kano','sonya'):
        for actor in ('kano','sonya'):
            text=text.replace(f'ks_throw_{owner}_victim_{actor}',f'ks_th_{owner}_v_{actor}')
    p.write_text(text)
