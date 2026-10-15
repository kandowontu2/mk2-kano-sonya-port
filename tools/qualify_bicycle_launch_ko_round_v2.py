"""Retain the original checker; bind the entire inherited physical namespace."""
import inspect,json
from pathlib import Path
import qualify_bicycle_launch_ko_round as original
ROOT,need,sha=original.ROOT,original.need,original.sha
scope=dict(vars(original.square.prior));scope.update(vars(original.square));scope['projectile']=original.projectile
exec(compile(original.source,__file__+'::whole_physical_with_original_inherited_globals','exec'),scope)
physical=scope['physical']
source=inspect.getsource(original.qualify)
source=source.replace('Path(__file__),Path(square.__file__)','Path(__file__),Path(original.__file__),Path(square.__file__)')
scope=dict(vars(original),__file__=__file__,original=original,physical=physical)
exec(compile(source,__file__+'::whole_same_terminal_Bicycle_qualifier','exec'),scope)
qualify=scope['qualify']

def preserve_context_failure(c):
 out=ROOT/'audit_bicycle_ko_original_context_failure';need(not out.exists(),'Fresh original context failure receipt')
 report=dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error="NameError: name 'one' is not defined",
  cause='The constructed physical checker omitted the inherited native namespace; no captured state is changed.',
  inputHashes={str(Path(original.__file__)):sha(original.__file__)},fullPortAcceptance=False,newNativeBoots=0)
 out.mkdir();(out/'failure.json').write_text(json.dumps(report,indent=2)+'\n')
