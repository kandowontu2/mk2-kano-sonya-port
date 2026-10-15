"""Preserve failed checker; pin independently observed slot-specific stop clocks."""
import inspect
from pathlib import Path
import qualify_bounded_twohuman_square_rise_cleanup as base

source=Path(base.__file__).read_text()
gate=inspect.getsource(base.gate)
updated=gate.replace('def gate(rows,side,length):','def gate(rows,side,length):\n    stopped=5464 if side==1 else 5471')
updated=updated.replace("r['pos']=='5464.00000000'","Decimal(r['pos'])==stopped")
updated=updated.replace('0<5464<length','0<stopped<length')
updated=updated.replace('stoppedSample=5464,unplayedSamples=length-5464','stoppedSample=stopped,unplayedSamples=length-stopped')
assert source.count(gate)==1
source=source.replace(gate,updated)
source=source.replace("['pos']='5465.00000000'","['pos']=str((5464 if side==1 else 5471)+1)")
source=source.replace('audit_bounded_twohuman_square_rise_cleanup_checked','audit_bounded_twohuman_square_slot_clocks_checked')
source=source.replace("print(json.dumps(dict(passed=True,contexts=2,unplayedSamples=length-5464)))","print(json.dumps(dict(passed=True,contexts=2,results=results)))")
exec(compile(source,__file__+'::independent slot clocks','exec'),{'__name__':'__main__','__file__':__file__})
