"""Read the retained exact dynamic predictor source instead of inspect linenos."""
import inspect,json
from pathlib import Path
import qualify_sonya_launch_ko_round as original
ROOT,need,sha=original.ROOT,original.need,original.sha

def predict(carrier,events,pins):
 source=original.prior.mirror.old.source
 start=source.index('def predict(carrier,pins):');source=source[start:]
 before='events=source_events(carrier,pins);voice=';need(source.count(before)==1,'Whole exact retained original source predictor body')
 source=source.replace('def predict(carrier,pins):','def predict(carrier,pins,events):',1).replace(before,'voice=',1)
 scope=dict(vars(original.prior.mirror.old));exec(compile(source,__file__+'::whole_retained_predictor_source_without_lineno_lookup','exec'),scope)
 return scope['predict'](carrier,pins,events)

source=inspect.getsource(original.qualify)
source=source.replace('Path(__file__),Path(prior.__file__)','Path(__file__),Path(original_adapter.__file__),Path(prior.__file__)')
scope=dict(vars(original),__file__=__file__,predict=predict,original_adapter=original)
exec(compile(source,__file__+'::whole_Sonya_same_terminal_qualifier','exec'),scope)
qualify=scope['qualify']

def preserve_retrieval_failure(carrier):
 out=ROOT/'audit_sonya_ko_predictor_source_retrieval_failure';need(not out.exists(),'Fresh preserved old predictor retrieval failure')
 report=dict(passed=False,nativeTerminal=carrier['terminal'],error="OSError('lineno is out of bounds')",nativeGameFailure=False,
             cause='inspect.getsource cannot recover the dynamically compiled lexical adapter from its shorter backing file.',
             wholeDynamicSourceRemainsPreserved=True,fullPortAcceptance=False,inputHashes={str(Path(original.__file__)):sha(original.__file__)},newNativeBoots=0)
 out.mkdir();(out/'failure.json').write_text(json.dumps(report,indent=2)+'\n')
