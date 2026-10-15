"""Stop only the identified unsuccessful headless zoning-controller test.

This is an intentional test cancellation after actual repeated losses, not an
observation timeout or a claim of a game softlock. Preserve its real exit/log.
"""
import ctypes as c
from ctypes import wintypes as w
import gzip
import json
from pathlib import Path
import native_process_census_v6647 as native

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_native_postending_kano_p2_sonya_join'

def need(value,message):
    if not value: raise ValueError(message)

def main():
    receipt=OUT/'explicit_unsuccessful_controller_stop.json'
    need(not receipt.exists(),'Fresh explicit cancellation record')
    expected=json.loads((OUT/'native_identity.json').read_text())
    live=next((r for r in native.census() if r['ProcessId']==expected['ProcessId']),None)
    need(live==expected and live['ProcessId']==141900 and live['ParentProcessId']==174832 and
         'mk2ks_native_kano_p2_postending_sonya.lua' in live['CommandLine'], 'Exact known automated test, never another game process')
    losses=[]; stages=set(); ending=[]; last=None
    try:
        with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8') as stream:
            for line in stream:
                if line.startswith('MK2_NAT_CAMPAIGN_LOSS '): losses.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_STAGE '): stages.add(int(line.split(' stage=')[1].split()[0]))
                if line.startswith('MK2_NAT_CAMPAIGN_ENDING_'): ending.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_LIVE '): last=line.strip()
    except EOFError: pass
    need(len(losses)>=40 and stages=={0,1} and not ending and last and 'cpu=8:8' in last,
         'Actual repeatedly unsuccessful zoning plan, not mere missing output')
    k=native.k
    k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)]; k.GetExitCodeProcess.restype=w.BOOL
    k.TerminateProcess.argtypes=[w.HANDLE,w.UINT]; k.TerminateProcess.restype=w.BOOL
    k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD]; k.WaitForSingleObject.restype=w.DWORD
    handle=k.OpenProcess(0x100001|0x1000,False,live['ProcessId'])
    need(handle,'Open exact native test handle')
    try:
        creation,exit_time,kernel,user=(w.FILETIME() for _ in range(4))
        need(k.GetProcessTimes(handle,c.byref(creation),c.byref(exit_time),c.byref(kernel),c.byref(user)), 'Actual handle creation identity')
        born=((creation.dwHighDateTime<<32)|creation.dwLowDateTime)/10**7-11644473600
        need(born==live['createdUnix'],'No recycled PID or replacement native run')
        code=w.DWORD()
        need(k.GetExitCodeProcess(handle,c.byref(code)) and code.value==259,'Same native test still running before intentional stop')
        need(k.TerminateProcess(handle,0xffffffff),'Explicit stop of exact unsuccessful automated test')
        need(k.WaitForSingleObject(handle,5000)==0 and k.GetExitCodeProcess(handle,c.byref(code)) and code.value==0xffffffff,
             'Authoritative actual native terminal exit, never handle existence alone')
    finally: k.CloseHandle(handle)
    result=dict(passed=False,testIntentionallyStopped=True,nativeExit=code.value,nativeIdentity=live,
                reason='Existing physical zoning controller repeatedly lost against native Subzero8 on stage1; ending and fresh join were never reached.',
                observedPaidContinueLosses=len(losses),observedStages=sorted(stages),lastOwnedNativeField=last,
                softlockClaim=False,gameBugClaim=False,postEndingJoinAccepted=False,fullPortAcceptance=False,goalStatus='active',
                nextAction='After the original host is terminal, use a fresh test changing only ordinary controller strategy against Subzero8. Keep game health/difficulty/RNG/actors and public launcher unchanged.')
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(explicitlyStopped=True,nativePID=live['ProcessId'],nativeExit=code.value,actualLosses=len(losses))),flush=True)

if __name__=='__main__':main()
