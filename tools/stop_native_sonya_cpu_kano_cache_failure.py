"""Stop exact live diagnostic only after observed native global-state corruption."""
import ctypes as c,gzip,json,re
from ctypes import wintypes as w
from pathlib import Path
import native_process_census_v6647 as native
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_native_sonya_p1_postending_kano_anchors_checked'
def need(v,m):
    if not v:raise ValueError(m)
if __name__=='__main__':
    receipt=OUT/'explicit_confirmed_cache_failure_stop.json'
    need(not receipt.exists(),'Fresh immutable exact native stop receipt')
    expected=json.loads((OUT/'native_identity.json').read_text())
    actual=next((p for p in native.census() if p['ProcessId']==161288),None)
    need(actual==expected and actual['ParentProcessId']==158136,'Same native PID/parent/path/creation/full command')
    events=[];last=None
    try:
        with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8') as stream:
            for line in stream:
                if line.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN '):events.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_LIVE '):last=line.strip()
    except EOFError:pass
    parsed=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in events]
    need(parsed and all(r['pc']=='FF838860' and r['id']=='17' and r['frame']=='36314' and
                        r['mask']=='FFFF' and r['writes']=='0' and r['assistance']=='none' for r in parsed) and
         any(r['at']=='01061B00' and r['data']=='FFFF' for r in parsed),
         'Real native cache code overwrote actual winner/game-state memory, not an observation timeout')
    k=native.k
    k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];k.GetExitCodeProcess.restype=w.BOOL
    k.TerminateProcess.argtypes=[w.HANDLE,w.UINT];k.TerminateProcess.restype=w.BOOL
    k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];k.WaitForSingleObject.restype=w.DWORD
    handle=k.OpenProcess(0x101001,False,actual['ProcessId']);need(handle,'Exact identified native kernel handle')
    try:
        created,ended,kernel,user=(w.FILETIME() for _ in range(4))
        need(k.GetProcessTimes(handle,c.byref(created),c.byref(ended),c.byref(kernel),c.byref(user)) and
             ((created.dwHighDateTime<<32)|created.dwLowDateTime)/10**7-11644473600==actual['createdUnix'],'Never stop recycled PID')
        code=w.DWORD();need(k.GetExitCodeProcess(handle,c.byref(code)) and code.value==259,'Same actual native still live')
        need(k.TerminateProcess(handle,0xffffffff) and k.WaitForSingleObject(handle,5000)==0 and
             k.GetExitCodeProcess(handle,c.byref(code)) and code.value==0xffffffff,'Authoritative explicit diagnostic exit')
    finally:k.CloseHandle(handle)
    receipt.write_text(json.dumps(dict(passed=False,explicitlyStoppedAfterConfirmedCacheFailure=True,
        nativeExit=code.value,nativeIdentity=actual,actualGlobalOverrunEvents=events,lastObservedNativeField=last,
        fullPortAcceptance=False,goalStatus='active',reason='Confirmed native imported CPU Kano cache decoder wrote into global game state.'),indent=2)+'\n')
    print(json.dumps(dict(stopped=True,nativeExit=code.value,confirmedOverrunEvents=len(events))),flush=True)
