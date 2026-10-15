"""Whole5957 preflight plus explicit corrected inline deadline and failures."""
import ast,json
from pathlib import Path
import qualify_current_pit_queue_rng_v5957 as original_source
ROOT,need,sha=original_source.ROOT,original_source.need,original_source.sha
OUT=ROOT/'audit_v5963_current_pit_queue_rng_source_checked'

def run():
 import run_current_pit_queue_rng_v5961 as host
 proofpath=original_source.OUT/'report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual executed5954/5955/5956/5957 preflight remains unchanged')
 prior=original_source.run();pins=dict(prior['inputHashes']);pins[str(proofpath)]=sha(proofpath)
 old=(ROOT/'mk2ks_current_subzero_pit_campaign_v5942.lua').read_text()
 deadline=old[old.index('local frame=0'):]
 campaign=(ROOT/host.LUA).read_text()
 need(campaign[campaign.index('local frame=0'):]==deadline and
      campaign.count("dofile('mk2ks_current_subzero_pit_driver_v5940.lua')")==1 and
      campaign.count("dofile('mk2ks_current_pit_queue_rng_v5954.lua')")==1,
      'Whole exact actual5942 inline failure-only deadline; controller and observer unchanged')
 fn,digest=host.collector();old_fn,_=host.failed_host.collector();expected=old_fn.source
 for before,after in(('audit_v5959_current_pit_queue_rng_','audit_v5964_current_pit_queue_rng_'),
                      ("lua='"+host.failed_host.LUA+"'","lua='"+host.LUA+"'"),
                      ('    files.update(ROOT/p for p in '+repr(host.failed_host.EXTRA_INPUTS)+')',
                       '    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')')):
  expected=host.once(expected,before,after)
 need(fn.source==expected and fn.__globals__['source']is host.source and fn.__globals__['state']is host.state and
      host.run.source==host.failed_host.run.source and host.run.__globals__['collector']is host.collector,
      'Whole failed-host RAM-only native collector/mixer corrected only by fresh campaign/output/source namespace')
 failures=[]
 for fighter in('kano','sonya'):
  for side in(1,2):
   folder=ROOT/f'audit_v5959_current_pit_queue_rng_{fighter}_p{side}_samples'
   meta=json.loads((folder/'result.json').read_text());error=(folder/'stderr.log').read_text()
   need(meta['exit_code']!=0 and 'cannot open mk2ks_native_stage_failure_deadline_v890.lua'in error,
        'Preserve all actual terminal boot failures; no gameplay/audio/RNG acceptance')
   for p in folder.rglob('*'):
    if p.is_file():pins[str(p)]=sha(p)
   failures.append(dict(fighter=fighter,physicalSlot=side,capture=str(folder),exitCode=meta['exit_code'],reason='Nonexistent boot deadline file; before gameplay'))
 for leaf in host.EXTRA_INPUTS:
  path=ROOT/leaf
  if path.suffix=='.py':ast.parse(path.read_text())
  pins[str(path)]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All failed/prior/current/compiled/user-dirty/source evidence intact before corrected boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,retainedActualFailedBoots=failures,
             entirePreviousNativeRAMAudioAlgorithmsRetained=True,actualNativePriorityRNGAccepted=False,
             fullPortAcceptance=False,newBuilds=0,rawRecordingsWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable corrected boot source preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
