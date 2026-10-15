"""Whole original collision gate, all three original fireball animation boxes."""
import inspect,json
from pathlib import Path
import qualify_bicycle_launch_ko_round_v2 as previous
original=previous.original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.projectile_gate)
# Obtain the whole constructed original gate, not a truncated backing module.
before="source=inspect.getsource(projectile.projectile_gate)"
after="""source=inspect.getsource(projectile.projectile_gate)
 source=source.replace('(0xff8f3760,0xff8f37f0)','(0xff8f3760,0xff8f3910)',1)
 source=source.replace("entry['a0']=='FF8F3760'", "entry['a0']in('FF8F3760','FF8F37F0','FF8F3880')",1)
 source=source.replace("    fields={(int(r['frame']),int(r['slot'])):r", "    need(struct.unpack_from('<9H',guest,at(0xff8f37f0))==(112,25,100,20,0x1110,0x1605,0,0,1)and struct.unpack_from('<9H',guest,at(0xff8f3880))==(148,25,125,20,0x1110,0x1605,0,0,1), 'Both additional whole original fireball animation rectangles/reaction17/damage22')\\n    fields={(int(r['frame']),int(r['slot'])):r",1)"""
need(source.count(before)==1,'Whole existing projectile source construction')
scope=dict(vars(original));exec(compile(source.replace(before,after),__file__+'::all_three_original_fireball_descriptors','exec'),scope)
projectile_gate=scope['projectile_gate']
source=inspect.getsource(original.source_events)
need(source.count("'FFF9A690'")==1,'Exact second native Bicycle source port PC')
scope=dict(vars(original));exec(compile(source.replace("'FFF9A690'","'FFF9A520'"),__file__+'::actual_compiled_cry_marker_PC','exec'),scope)
source_events=scope['source_events']
source=inspect.getsource(original.qualify)
source=source.replace('Path(__file__),Path(square.__file__)','Path(__file__),Path(previous.__file__),Path(original.__file__),Path(square.__file__)')
scope=dict(vars(original),__file__=__file__,previous=previous,original=original,physical=previous.physical,projectile_gate=projectile_gate,source_events=source_events)
exec(compile(source,__file__+'::whole_same_terminal_Bicycle_KO_qualifier','exec'),scope)
qualify=scope['qualify']

def preserve_descriptor_failure(c):
 out=ROOT/'audit_bicycle_ko_high_only_descriptor_rejection';need(not out.exists(),'Fresh original high-only descriptor rejection')
 report=dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error='Every original high-fireball descriptor and full branch outcome',
  cause='Longer native trajectory also observes unchanged original second/third fireball animation rectangles; original high-only checker retained.',
  inputHashes={str(Path(original.__file__)):sha(original.__file__),str(Path(previous.__file__)):sha(previous.__file__)},fullPortAcceptance=False,newNativeBoots=0)
 out.mkdir();(out/'failure.json').write_text(json.dumps(report,indent=2)+'\n')
