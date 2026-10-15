"""Preserve actual zero-exit repaired run rejected by stale host metadata oracle."""
import gzip,hashlib,json,subprocess
from pathlib import Path
import native_cpu_finisher_dispatch_context as fixed
import native_ai_response_context as old
import native_process_census_v6647 as census
ROOT,need,sha=fixed.ROOT,fixed.need,fixed.sha
if __name__=='__main__':
    folder=ROOT/'audit_native_cpu_finisher_repair_regression'
    out=folder/'stale_host_metadata_failure_preserved.json'
    need(not out.exists() and not census.census(),'Fresh preservation; actual native terminal')
    terminal=json.loads((folder/'native_terminal.json').read_text())
    pins=json.loads((folder/'input_hashes_before.json').read_text())
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    need(terminal['nativeExit']==0 and (folder/'stderr.log').read_text()=='' and
         proof['sha256']==fixed.GUEST_SHA!=hashlib.sha256(old.expected()).hexdigest().upper(),
         'Actual new guest/zero exit/empty native error stream, not a game failure')
    oldmeta=json.loads((ROOT/old.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(proof['sha256']!=oldmeta['expected_guest_sha256'] and all(sha(p)==h for p,h in pins.items()),
         'Actually executed inputs unchanged; old imported metadata function expects previous guest')
    text=gzip.open(folder/'run.log.gz','rt',encoding='utf-8').read()
    need('MK2_FINISH_DISPATCH_REGRESSION_WINNER_HANDOFF frame=36401 'in text and
         'global_cache_stores=0'in text and 'MK2_MILEENA_CAMPAIGN_OVERRUN 'not in text,
         'Actual owned native finisher handoff and no native cache overrun preserved')
    sources={p:dict(sha256=h,text=Path(p).read_text())for p,h in pins.items()
             if Path(p).suffix.lower()in('.py','.lua','.cpp','.h','.ps1','.cmd')}
    with gzip.open(folder/'original_stale_metadata_executed_sources.json.gz','wt',encoding='utf-8')as s:json.dump(sources,s)
    out.write_text(json.dumps(dict(passed=False,hostOracleFailure=True,nativeExit=0,
        actualNewGuest=proof['sha256'],incorrectExpectedOldGuest=oldmeta['expected_guest_sha256'],
        originalInputHashes=pins,actualOwnFinisherHandoffFrame=36401,
        noCacheOverrunObserved=True,rawVisualsLostBeforeRAMReview=True,
        nativeArtAccepted=False,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    for p in folder.iterdir():
        if p.is_file():subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    print(json.dumps(dict(preserved=True,nativeExit=0,staleHostOracle=True,gameFailureClaim=False)))
