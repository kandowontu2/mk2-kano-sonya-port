"""Intentional cancellation of the identified second unsuccessful bot trial."""
import ctypes as c
from ctypes import wintypes as w
import gzip,json
from pathlib import Path
import native_process_census_v6647 as native
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_native_postending_kano_p2_sonya_reactive'
def need(v,m):
    if not v:raise ValueError(m)
def main():
    receipt=OUT/'explicit_unsuccessful_controller_stop.json'
    need(not receipt.exists(),'Fresh actual stop record')
    expected=json.loads((OUT/'native_identity.json').read_text())
    live=next((r for r in native.census() if r['ProcessId']==174412),None)
    need(live==expected and live['ParentProcessId']==125744,'Exact native trial creation/command/parent')
    losses=[];endings=[];last=None
    try:
        with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8') as stream:
            for line in stream:
                if line.startswith('MK2_NAT_CAMPAIGN_LOSS '):losses.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_ENDING_'):endings.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_LIVE '):last=line.strip()
    except EOFError:pass
    need(len(losses)>=20 and not endings and last and 'stage=1 ' in last and 'cpu=8:8' in last,
         'Actual repeated unsuccessful attempts, not expired observation')
    k=native.k
    k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];k.GetExitCodeProcess.restype=w.BOOL
    k.TerminateProcess.argtypes=[w.HANDLE,w.UINT];k.TerminateProcess.restype=w.BOOL
    k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];k.WaitForSingleObject.restype=w.DWORD
    handle=k.OpenProcess(0x101001,False,live['ProcessId']);need(handle,'Exact native handle')
    try:
        created,ended,kernel,user=(w.FILETIME() for _ in range(4))
        need(k.GetProcessTimes(handle,c.byref(created),c.byref(ended),c.byref(kernel),c.byref(user)) and
             ((created.dwHighDateTime<<32)|created.dwLowDateTime)/10**7-11644473600==live['createdUnix'],'No recycled PID')
        code=w.DWORD()
        need(k.GetExitCodeProcess(handle,c.byref(code)) and code.value==259,'Same actual job live')
        need(k.TerminateProcess(handle,0xffffffff) and k.WaitForSingleObject(handle,5000)==0 and
             k.GetExitCodeProcess(handle,c.byref(code)) and code.value==0xffffffff,'Authoritative deliberate native exit')
    finally:k.CloseHandle(handle)
    receipt.write_text(json.dumps(dict(passed=False,testIntentionallyStopped=True,nativeExit=code.value,nativeIdentity=live,
        observedPaidContinueLosses=len(losses),lastOwnedNativeField=last,postEndingJoinAccepted=False,
        reason='Subzero-only approach/jump-kick physical policy did not clear stage1.',softlockClaim=False,gameBugClaim=False,
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(explicitlyStopped=True,nativeExit=code.value,actualLosses=len(losses))),flush=True)
if __name__=='__main__':main()
