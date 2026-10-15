"""Stop only the exact owned diagnostic after verified repeated policy losses.

Not a timeout, game defect, failed continue or successful ending. Preserve all
actual input sources and native outcomes before changing ordinary test inputs.
"""
import ctypes as c
import gzip
import json
import re
from ctypes import wintypes as w
from pathlib import Path
import native_process_census_v6647 as census
import capture_native_kano_laser_sonya_postending as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=original.OUT
PARENT,GAME=168996,191216


def run():
    receipt=OUT/'explicit_unsuccessful_physical_policy_stop.json'
    need(not receipt.exists(),'Fresh exact diagnostic stop receipt')
    expected=json.loads((OUT/'native_identity.json').read_text())
    actual=next((p for p in census.census() if p['ProcessId']==GAME),None)
    need(actual==expected and actual['ParentProcessId']==PARENT and
         Path(actual['ExecutablePath']).resolve()==(ROOT/original.NAME/'mkport_candidate.exe').resolve(),
         'Exact actual original native PID/parent/path/birth/whole command still live')
    pins=json.loads((OUT/'input_hashes_before.json').read_text())
    proof=json.loads((OUT/'guest_memory_proof.json').read_text())
    need(all(sha(p)==h for p,h in pins.items()) and proof['everyActualByteComparedInRAM'] and
         proof['sha256']=='AB1A0AEAE5BBE6457D591C8B9491E439E4DCA8F08A2E37A3710A3FA67769EF6E',
         'Actual independently source-bound current guest and all original executed inputs unchanged')
    losses=[];wins=[];stages=[];selected=[];last=None;overruns=[]
    with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8') as stream:
        try:
            for line in stream:
                if line.startswith('MK2_NAT_CAMPAIGN_LOSS '): losses.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_WIN '): wins.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_STAGE '): stages.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_SELECT_ID '): selected.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_LIVE '): last=line.strip()
                if line.startswith(('MK2_MILEENA_CAMPAIGN_OVERRUN ','MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ')): overruns.append(line.strip())
        except EOFError: pass  # Trailer is absent only for this confirmed live original writer.
    parsed=lambda lines:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines]
    lrows,wrows,srows,cs=map(parsed,(losses,wins,stages,selected))
    live=parsed([last])[0]
    need(len(lrows)>=16 and [int(q['number']) for q in lrows]==list(range(1,len(lrows)+1)) and
         all(q['stage']=='0' and q['human_slot']=='1' and q['fighter']=='sonya' for q in lrows) and
         len(wrows)>=2*len(lrows) and all(q['slot']=='2' for q in wrows) and
         {q['stage'] for q in srows}=={'0'} and live['human']=='18:18' and live['cpu']=='17:17' and
         int(live['frame'])>36314 and all(q['roster']=='18' and q['state']=='3' for q in cs) and not overruns,
         'Sixteen actual complete paid losses, zero human round wins, repeated real Sonya selection and live Kano; not a timeout/softlock')
    k=census.k
    k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];k.GetExitCodeProcess.restype=w.BOOL
    k.TerminateProcess.argtypes=[w.HANDLE,w.UINT];k.TerminateProcess.restype=w.BOOL
    k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];k.WaitForSingleObject.restype=w.DWORD
    handle=k.OpenProcess(0x101001,False,GAME);need(handle,'Exact identified private diagnostic process handle')
    try:
        created,ended,kernel,user=(w.FILETIME() for _ in range(4))
        need(k.GetProcessTimes(handle,c.byref(created),c.byref(ended),c.byref(kernel),c.byref(user)) and
             ((created.dwHighDateTime<<32)|created.dwLowDateTime)/10**7-11644473600==actual['createdUnix'],
             'Never terminate a recycled process identity')
        exit_code=w.DWORD()
        need(k.GetExitCodeProcess(handle,c.byref(exit_code)) and exit_code.value==259,'Same original diagnostic still live')
        need(k.TerminateProcess(handle,0xffffffff) and k.WaitForSingleObject(handle,5000)==0 and
             k.GetExitCodeProcess(handle,c.byref(exit_code)) and exit_code.value==0xffffffff,
             'Authoritative explicit unsuccessful controller trial exit')
    finally: k.CloseHandle(handle)
    receipt.write_text(json.dumps(dict(passed=False,testIntentionallyStopped=True,nativeExit=exit_code.value,
        actualNativeIdentity=actual,observedPaidContinueLosses=len(losses),actualCPURoundWinReads=len(wins),
        actualHumanRoundWinReads=0,actualStage=0,observedGlobalCacheOverruns=0,lastObservedNativeField=last,
        originalGuestProof=proof,originalInputHashes=pins,actualLossEvents=losses,
        endingReached=False,postEndingJoinAccepted=False,fullPortAcceptance=False,goalStatus='active',
        reason='Established generic zoning input policy consistently loses to current true CPU Kano; preserve failure before changing physical test tactics, not gameplay.'),indent=2)+'\n')
    print(json.dumps(dict(stopped=True,nativeExit=exit_code.value,actualPaidLosses=len(losses),cacheOverruns=0,postEndingJoinAccepted=False)),flush=True)


if __name__=='__main__': run()
