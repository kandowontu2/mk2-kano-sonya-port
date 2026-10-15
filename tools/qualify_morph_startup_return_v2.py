"""Allow original return scheduling to wait for a late native special.

The idle-morph checker required the return entry exactly at512. Preserve that
executed rejection. Require the original unmodified scheduling instructions,
finite entry after512, and the genuine12-field return after that entry.
"""
import inspect,json
from pathlib import Path
import qualify_morph_startup_return as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def physical(c):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();a=(0xffa16000-0xff800000)//8;b=(0xffa16410-0xff800000)//8
 need(c['guest'][a:b]==stock[a:b],'Whole original morph-return scheduling/eligibility instructions before dedicated lookup operand')
 source=inspect.getsource(previous.physical)
 before="int(reverse[0]['frame'])==f+512";need(source.count(before)==1,'Exact prior idle-only deadline assumption')
 source=source.replace(before,"f+512<=int(reverse[0]['frame'])<=f+900",1)
 scope=dict(vars(previous));exec(compile(source,__file__+'::whole_native_waited_return_physical_contract','exec'),scope)
 report,by=scope['physical'](c)
 report['returnEntryDeferredFields']=report['originalReturnEntries'][0]-report['originalForwardStoreFrame']-512
 report['nativeReturnSchedulingInstructionIntervalUnchanged']=True
 return report,by

def qualify(c):
 out=ROOT/f"audit_morph_startup_return_idle_deadline_rejection_{c['move']}_p{c['side']}"
 need(not out.exists(),'Retain actual prior checker rejection')
 try:previous.physical(c)
 except ValueError as error:
  need(str(error)=='Original timed return starts at512 and genuine final return completes after12 fields; retries retained','Only actual idle deadline rejection is adapted')
  out.mkdir();(out/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error=str(error),executedSourceSHA256=sha(previous.__file__),newNativeBoots=0),indent=2)+'\n')
 else:raise ValueError('Prior idle deadline did not reject this finite late-special context')
 source=inspect.getsource(previous.qualify)
 before='for p in(Path(__file__),Path(original.__file__),';need(source.count(before)==1,'Whole original qualifier and exact executed source pin')
 source=source.replace(before,'for p in(Path(__file__),Path(previous.__file__),Path(original.__file__),',1)
 scope=dict(vars(previous),__file__=__file__,previous=previous,physical=physical)
 exec(compile(source,__file__+'::whole_same_terminal_morph_return_qualification','exec'),scope)
 return scope['qualify'](c)
