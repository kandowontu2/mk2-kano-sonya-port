"""Native waited return, facing changes after Square, and normal input latency."""
import inspect,json
from pathlib import Path
import qualify_morph_startup_return_v2 as waited
previous=waited.previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def physical(c):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();a=(0xffa16000-0xff800000)//8;b=(0xffa16410-0xff800000)//8
 need(c['guest'][a:b]==stock[a:b],'Whole original native morph-return scheduler and eligibility instructions')
 source=inspect.getsource(previous.physical)
 changes=[("int(reverse[0]['frame'])==f+512","f+512<=int(reverse[0]['frame'])<=f+900"),
 ("inputs=rows(text,'MK2_HUMAN_SHANG_INPUT');", "for age in range(1100,1110):\n  own_state,other_state=by[first+age,side],by[first+age,3-side]\n  need(own_state['x']!=other_state['x'],'Unambiguous current post-return native facing')\n  expected[age]='Right'if int(own_state['x'])<int(other_state['x'])else'Left'\n inputs=rows(text,'MK2_HUMAN_SHANG_INPUT');"),
 ("for at in range(first+1100,first+1110):need(by[at+1,side]['x']!=by[at,side]['x'],'Restored Shang actually walks under ordinary input')", "need(any(by[at,side]['vx']!='00000000'for at in range(first+1100,first+1130))and by[first+1120,side]['x']!=by[first+1100,side]['x'],'Restored Shang actually walks with original input/IRQ latency')")]
 for before,after in changes:need(source.count(before)==1,'Whole original input/physical contract, only native wait/facing/latency adaptations');source=source.replace(before,after,1)
 scope=dict(vars(previous));exec(compile(source,__file__+'::whole_native_morph_wait_facing_and_input_latency','exec'),scope)
 report,by=scope['physical'](c)
 report.update(returnEntryDeferredFields=report['originalReturnEntries'][0]-report['originalForwardStoreFrame']-512,nativeReturnSchedulingInstructionIntervalUnchanged=True,postReturnDirectionUsesActualFacing=True)
 return report,by

def qualify(c):
 # Record only genuine previous checker failures for previously attempted cases.
 if c['side']==1 or c['move']=='ball':
  out=ROOT/f"audit_morph_startup_return_input_assumption_rejection_{c['move']}_p{c['side']}";need(not out.exists(),'Retain preceding actually executed checker')
  try:waited.physical(c)
  except ValueError as error:
   need(str(error)in('Restored Shang actually walks under ordinary input','Every original morph/ordinary input plus exact late special command'),'Exact preceding frame-latency or fixed-facing assumption failure')
   out.mkdir();(out/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error=str(error),executedSourceSHA256=sha(waited.__file__),newNativeBoots=0),indent=2)+'\n')
  else:raise ValueError('Prior checker failure unexpectedly absent')
 source=inspect.getsource(previous.qualify)
 before='for p in(Path(__file__),Path(original.__file__),';need(source.count(before)==1,'Original and all corrected whole-model pins')
 source=source.replace(before,'for p in(Path(__file__),Path(previous.__file__),Path(waited.__file__),Path(original.__file__),',1)
 scope=dict(vars(previous),__file__=__file__,previous=previous,waited=waited,physical=physical)
 exec(compile(source,__file__+'::whole_same_native_capture_morph_qualification','exec'),scope)
 return scope['qualify'](c)
