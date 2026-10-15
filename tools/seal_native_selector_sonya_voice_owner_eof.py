"""Preserve rejected input run and accepted independent quiet EOF observations.

No retained-host execution or new native process. Exact metadata compression
only. Corrected IN2 controller is prepared, not claimed executed or accepted.
"""
import ast,ctypes,hashlib,json,subprocess
from pathlib import Path
import verify_native_source_sync as sync

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_sealed.json'
need,sha=sync.need,sync.sha
BASE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_ram/ordinary_Kano_walk_lowkick_native_Sonya_CPU_actual_voice_owners'
FAILURE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_capture_checked/failure.json'
PROOF=ROOT/'audit_native_selector_sonya_voice_owner_eof_boundary_faults_checked/report.json'


def stored(path):
    fn=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
    fn.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)];fn.restype=ctypes.c_ulong
    high=ctypes.c_ulong();low=fn(str(path),ctypes.byref(high))
    need(low!=0xffffffff or ctypes.get_last_error()==0,'Exact Windows stored-size read')
    return low+(high.value<<32)


def execute():
    need(not OUT.exists(),'Fresh immutable quiet ownership/storage receipt')
    proof=json.loads(PROOF.read_text()); failed=json.loads(FAILURE.read_text())
    need(proof['passed'] and not failed['passed'] and
         proof['actualNativeIdentity']==failed['actualNativeIdentity'] and
         proof['nativeExit']==failed['nativeExit']==0 and
         proof['recordedQuietEOFOwnership']['actualSavedOwnerSnapshots']==13850 and
         proof['totalEffectiveFaultsRejected']==17 and proof['actualOriginalLuaErrors']==19 and
         not proof['physicalLowkickGameplayAccepted'] and not proof['allOwnerLifetimeTransitionsAccepted'],
         'Actual input failure retained, independent finite EOF observations not promoted to gameplay')
    census=json.loads(subprocess.check_output(['powershell','-NoProfile','-Command',
        "@(Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,ParentProcessId) | ConvertTo-Json -Compress"],text=True) or '[]')
    need(not census,'No pending native game; do not replace an observation timeout')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Entire original/current source/evidence inventory unchanged')
    folders=(
        'audit_native_selector_sonya_cpu_lowkick_owners_capture_checked',
        'audit_native_selector_sonya_voice_owner_eof_checked',
        'audit_native_selector_sonya_voice_owner_eof_errors_checked',
        'audit_native_selector_sonya_voice_owner_eof_boundary_checked',
        'audit_native_selector_sonya_voice_owner_eof_boundary_faults_checked')
    files={Path(__file__).resolve()}
    for folder in folders:
        at=(ROOT/folder).resolve();need(at.is_relative_to(ROOT.resolve()) and at.is_dir(),'Exact new metadata directory')
        files.update(p.resolve() for p in at.rglob('*') if p.is_file())
    files.update(p.resolve() for p in BASE.rglob('*') if p.is_file())
    for name in (
        'capture_native_selector_sonya_cpu_lowkick_owners.py',
        'capture_native_selector_sonya_cpu_lowkick_owners_bound.py',
        'read_native_selector_lowkick_live.py','read_native_selector_lowkick_live_remote.py',
        'qualify_native_selector_sonya_voice_owner_eof.py',
        'qualify_native_selector_sonya_voice_owner_eof_errors.py',
        'qualify_native_selector_sonya_voice_owner_eof_boundary.py',
        'qualify_native_selector_sonya_voice_owner_eof_boundary_faults.py'):
        files.add((ROOT/'tools'/name).resolve())
    for name in ('mk2ks_native_selector_sonya_cpu_lowkick_owners.lua','mk2ks_native_selector_sonya_cpu_lowkick_owners_bound.lua'):
        files.add((ROOT/name).resolve())
    pending=ROOT/'tools/capture_native_selector_sonya_cpu_lowkick_owners_bound.py'
    ast.parse(pending.read_text())
    wrapper=(ROOT/'mk2ks_native_selector_sonya_cpu_lowkick_owners_bound.lua').read_text()
    need("manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']" in wrapper and
         "high['P1 Down'],high['P1 Block']}" in wrapper,
         'Prepared actual IN2 input/release binding only, no executed-game acceptance')
    entries=[]
    for p in sorted(files):
        cmos=p.name=='nvram' and p.parent.name=='mk2ks' and p.parent.parent.name=='nvram' and p.stat().st_size==16384
        need(p.is_relative_to(ROOT.resolve()) and (p.suffix.lower() in ('.py','.lua','.json','.gz','.log','.cfg') or cmos),
             'Only exact small source/metadata/normal16KiB CMOS, no raw-media/build/ROM/ZIP')
        key=str(p);h=sha(p);need(key not in pins or pins[key]==h,'Executed sources and actual failures never overwritten');pins[key]=h
        before=stored(p);logical=p.stat().st_size
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',key],capture_output=True)
        need(call.returncode==0 and sha(p)==h,'Whole original bytes unchanged after exact LZX')
        entries.append(dict(path=key,sha256=h,logicalBytes=logical,storedBefore=before,storedAfter=stored(p)))
    need(sync.verify()['passed'] and all(sha(p)==h for p,h in pins.items()),
         'All15 compiled sources/fixed public endpoints and every original/current input hash intact')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=proof['actualNativeIdentity'],nativeExit=0,
        recordedQuietEOFOwnership=proof['recordedQuietEOFOwnership'],effectiveOwnerFaultsRejected=17,
        failedControllerPreserved=True,actualOriginalLuaErrors=19,physicalLowkickGameplayAccepted=False,
        preparedIN2CorrectionNotExecuted=True,terminalInputCurrentlyDenied=True,
        originalHostStillRetained=True,allOwnerLifetimeTransitionsAccepted=False,
        hitKOResetMorphOwnerCleanupAccepted=False,allArenaCPUContextsAccepted=False,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,sourceSyncPassed=True,
        exactNewMetadataCompression=entries,logicalNewBytes=sum(r['logicalBytes'] for r in entries),
        storedNewBytes=sum(r['storedAfter'] for r in entries),
        wholeObjectiveStillActive=True,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGamesThisTurn=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0)
    OUT.write_text(json.dumps(result,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole final finite receipt unchanged after LZX')
    print(json.dumps(dict(passed=True,inputPins=len(pins),mismatches=0,logicalNewBytes=result['logicalNewBytes'],
        storedNewBytes=result['storedNewBytes'],receiptSHA256=h,fullPortAcceptance=False)),flush=True)
    return result


if __name__=='__main__':execute()
