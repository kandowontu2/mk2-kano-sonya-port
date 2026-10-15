"""Pre-native additive passive queue/RNG transport source qualification."""
import ast,hashlib,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5958_current_pit_queue_rng_source_checked'

def run():
 import run_current_pit_queue_rng_v5956 as host
 current.expected();parentpath=ROOT/'audit_v5953_current_subzero_pit_audio_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Prior native stock-victim audio/owner acceptance and whole goal intact')
 proofpath=host.predecessor.source.OUT/'report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Entire passive native audio transport preflight unchanged')
 observer=(ROOT/host.OBSERVER).read_text();campaign=(ROOT/host.LUA).read_text()
 need(observer.count("dofile('mk2ks_current_subzero_pit_audio_v5941.lua')")==1 and
      campaign.count("dofile('mk2ks_current_subzero_pit_driver_v5940.lua')")==1 and
      campaign.count("dofile('mk2ks_native_stage_failure_deadline_v890.lua')")==1 and
      not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(',observer),
      'Whole original controller/audio retained; additional exact-PC queue/RNG snapshots only read native state')
 fn,digest=host.collector();old,_=host.predecessor.collector();expected=old.source
 for before,after in(('audit_v5947_current_subzero_pit_mix_','audit_v5959_current_pit_queue_rng_'),
                      ("lua='"+host.predecessor.LUA+"'","lua='"+host.LUA+"'"),
                      ('    files.update(ROOT/p for p in '+repr(host.predecessor.EXTRA_INPUTS)+')',
                       '    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')')):
  expected=host.once(expected,before,after)
 need(fn.source==expected and fn.__globals__['source']is host.source and fn.__globals__['state']is host.state and
      fn.__globals__['model']is host.model and host.run.source==host.predecessor.run.source and
      host.run.__globals__['collector']is host.collector and host.run.__globals__['runtime'].state is host.state,
      'Whole original RAM-only native collector/mixer/faults preserve correct actual execution namespaces')
 pins=dict(proof['inputHashes']);pins[str(proofpath)]=sha(proofpath);pins[str(parentpath)]=sha(parentpath)
 for leaf in host.EXTRA_INPUTS:
  path=ROOT/leaf
  if path.suffix=='.py':ast.parse(path.read_text())
  pins[str(path)]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'Every compiled/current/user-dirty/public/executed source byte intact before native boot')
 return dict(passed=True,sourceOnly=True,parentAdditiveJournal=str(parentpath),inputHashes=pins,
             transportSourceSHA256=digest,additionalPassiveQueueRNGObserverSHA256=sha(ROOT/host.OBSERVER),
             whole5945NativeRAMAudioMixerRetained=True,actualNativePriorityRNGAccepted=False,
             fullPortAcceptance=False,newBuilds=0,rawRecordingsWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable passive queue/RNG source preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
