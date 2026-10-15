"""Successor: native idle excludes motion bits, not normal body flags."""
from pathlib import Path
from types import FunctionType
import qualify_bounded_twohuman_idle_probe as prior

source=Path(prior.__file__).read_text()
old="for key in ('vx','vy','gravity','flags','body','trail'):assert int(r[key],16)==0"
assert source.count(old)==1
source=source.replace(old,"for key in ('vx','vy','gravity','trail'):assert int(r[key],16)==0\n            assert int(r['flags'],16)&0x1c==0 and int(r['body'],16)&0x0c==0")
scope=dict(prior.__dict__)
scope['__name__']='qualified_successor'
scope['__file__']=__file__
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
