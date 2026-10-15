"""Preserve the real unsuccessful physical-controller trial before retrying."""
import gzip
import json
import subprocess
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def main():
    folder=ROOT/'audit_native_postending_kano_p2_sonya_join'
    out=folder/'stopped_controller_trial_preserved.json'
    need(not out.exists() and not native.census(),'Original host/native terminal before any new native test')
    result=json.loads((folder/'result.json').read_text())
    stopped=json.loads((folder/'explicit_unsuccessful_controller_stop.json').read_text())
    need(not result['passed'] and result['nativeExit']==stopped['nativeExit']==4294967295 and
         stopped['testIntentionallyStopped'] and stopped['observedPaidContinueLosses']==53 and
         result['actualStages']==[0,1] and not result['nativeCacheOverrunObserved'], 'Actual incomplete test remains a failure')
    pins=json.loads((folder/'input_hashes_before.json').read_text())
    need(all(sha(p)==h for p,h in pins.items()),'All original actual executed inputs unchanged')
    sources={p:dict(sha256=h,text=Path(p).read_text()) for p,h in pins.items() if Path(p).suffix in ('.lua','.py')}
    with gzip.open(folder/'stopped_executed_sources.json.gz','wt',encoding='utf-8') as stream:json.dump(sources,stream)
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream:text=stream.read()
    need('MK2_POSTENDING_BEGIN ' not in text and 'MK2_NAT_CAMPAIGN_ENDING_COMPLETED ' not in text and
         'LUA ERROR' not in text and not (folder/'stderr.log').read_text(), 'No earned ending/join or game script error falsely credited')
    files=[p for p in folder.rglob('*') if p.is_file()]
    storage=[]
    for p in files:
        need(p.resolve().is_relative_to(ROOT) and not p.is_symlink(),'Exact bounded evidence target')
        digest=sha(p)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
        need(sha(p)==digest,'Original source/evidence bytes preserved')
        storage.append(dict(path=str(p),sha256=digest,allocatedBytes=allocated(p)))
    receipt=dict(passed=True,failedNativeTrialPreserved=True,actualNativeExit=4294967295,
                 actualLosses=53,postEndingJoinAccepted=False,softlockClaim=False,gameBugClaim=False,
                 fullPortAcceptance=False,goalStatus='active',originalActualInputHashes=pins,files=storage,
                 nextAction='Fresh current native run, only ordinary Subzero-specific approach/jump-kick buttons changed; same earned tower and post-ending Sonya join requirement.',
                 newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(preserved=True,actualFailedExit=4294967295,losses=53,allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage))),flush=True)

if __name__=='__main__':main()
