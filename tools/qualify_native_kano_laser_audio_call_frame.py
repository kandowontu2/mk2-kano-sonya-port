"""Successor: furnish a real caller return frame for emitted RETS helpers.

The failed qualification and staged game sources remain immutable. This is
only a synthetic source test, never native gameplay or audio acceptance.
"""
from pathlib import Path
import qualify_native_kano_laser_audio as failed

source = Path(failed.__file__).read_text()
changes = [
    ("OUT=ROOT/'audit_native_kano_laser_audio_source'",
     "OUT=ROOT/'audit_native_kano_laser_audio_call_frame_source'"),
    ('cpu=CPU(guest,offset);cpu.store(cpu.regs[8]+0x1f0,ident,16)',
     'cpu=CPU(guest,offset);cpu.store(cpu.regs[8]+0x1f0,ident,16)\n'
     '            for reg in (*range(8),9,10,11,14):cpu.regs[reg]=0x12340000+reg\n'
     '            saved=cpu.regs.copy();cpu.push(15,0x12345678)'),
    ('saved=cpu.regs.copy();before=dict(cpu.mem);cpu.execute()',
     'before=dict(cpu.mem);cpu.execute()'),
    ('paths=[Path(__file__),Path(prior.__file__),',
     'paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_audio.py",'
     'ROOT/"audit_native_kano_laser_audio_source/failure.txt",Path(prior.__file__),'),
]
for old, new in changes:
    failed.need(source.count(old) == 1, 'Exact retained failed-source boundary')
    source = source.replace(old, new)
exec(compile(source, str(Path(__file__).resolve()), 'exec'),
     dict(__name__='__main__', __file__=str(Path(__file__).resolve())))
