"""Freeze the missing initial RAM inventory and all actually executed sources."""
import gzip,hashlib,json,re
from pathlib import Path
import native_process_census_v6647 as census
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
if __name__=='__main__':
    run=ROOT/'audit_native_sonya_cpu_finisher'
    out=run/'missing_inventory_callback_failure_preserved.json'
    if out.exists() or census.census():raise ValueError('Fresh original failure preservation; actual native game terminal')
    terminal=json.loads((run/'native_terminal.json').read_text())
    pins=json.loads((run/'input_hashes_before.json').read_text())
    text=gzip.open(run/'run.log.gz','rt',encoding='utf-8').read()
    if not(terminal['nativeExit']==0 and (run/'stderr.log').read_text()=='' and
           'MK2_SONYA_CPU_FINISH_OWN_ENTRY ' in text and 'MK2_SONYA_CPU_FINISH_WINNER_HANDOFF ' in text and
           'MK2_CAMPAIGN_GUEST_RAM_DIGEST ' not in text and 'MK2_SONYA_CPU_FINISH_OVERRUN ' not in text and
           all(sha(p)==h for p,h in pins.items())):
        raise ValueError('Actual completed own CPU Sonya finisher; missing required initial inventory, every input frozen')
    sources={p:dict(sha256=h,text=Path(p).read_text()) for p,h in pins.items()
             if Path(p).suffix.lower() in ('.py','.lua','.cpp','.h','.ps1','.cmd')}
    with gzip.open(run/'original_missing_inventory_executed_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    events=[s for s in text.splitlines() if s.startswith(('MK2_SONYA_CPU_FINISH_DISTANCE ',
        'MK2_SONYA_CPU_FINISH_PERFORMER ','MK2_SONYA_CPU_FINISH_OWN_ENTRY ',
        'MK2_SONYA_CPU_FINISH_WINNER_HANDOFF ','MK2_SONYA_CPU_FINISH_RESULT '))]
    out.write_text(json.dumps(dict(passed=False,hostSession=45395,hostExit=1,nativeExit=0,
        nativeGameFailure=False,requiredWholeGuestInventoryMissing=True,
        observedError='ValueError: Actual compiled candidate, complete initialized guest and empty native error stream',
        cause='register_frame_done advances frame before the first register_frame inventory listener; frame==0 never admits it.',
        actualOwnCPUFinisherEvents=events,nativeCacheOverrunObserved=False,
        originalInputHashes=pins,rawNativeFramesLostBeforeVisualReview=True,
        nativeRepairAccepted=False,fullArtAcceptance=False,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(preserved=True,nativeExit=0,actualCPUOwnFinishObserved=True,wholeGuestMissing=True)))
