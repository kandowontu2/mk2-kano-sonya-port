"""Actual failed-run reset provenance, not a successful secret/port gate."""
import gzip
import hashlib
import json
import re
import struct
import subprocess
from decimal import Decimal
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT, need = current.ROOT,current.need
FOLDER = ROOT/'audit_natural_smoke_route_sonya_p2_native_uppercut_104_punch_release_reset_trace'
OTHER = ROOT/'audit_natural_smoke_route_sonya_p2_native_uppercut_104_final_round'
OUT = ROOT/'audit_native_secret_graphics_reset_provenance'
off = lambda a:(a-0xff800000)//8


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def inventory(text):
    records = {}
    for line in text.splitlines():
        if line.startswith(('MK2_SECRET_NATIVE_RESET ','MK2_SECRET_RESET_TRACE ',
                            'MK2_STAGE_SECRET_ACCEPT ','MK2_STAGE_SECRET_FIGHT ',
                            'MK2_STAGE_SECRET_PUNCH ','MK2_STAGE_SECRET_RECOVER ')):
            records.setdefault(line.split()[0],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return records


def gate(records,guest,stock):
    reset = records['MK2_SECRET_NATIVE_RESET']
    need(len(reset)==1, 'One directly observed actual native reset')
    reset = reset[0]
    need(reset['writes']=='0' and reset['assistance']=='none' and reset['mode']=='0' and
         reset['pc']=='FF904F90' and reset['watchdogPC']=='FF904F80' and
         Decimal(reset['watchdogSeconds'])==Decimal(3),
         'Actual reset after three seconds since the native graphics-copy watchdog write')
    for lo,hi in ((0xff9037c0,0xff9037f0),(0xff904ee0,0xff905020)):
        need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)], 'Whole original graphics-copy selector/core unchanged')
    # The actual watchdog tap sees the instruction's post-fetch PC F80.
    # The preceding instruction F70 is *A1+ -> *A2+ long copy, NOT the
    # normal explicit watchdog-service routine. Preserve exact stock words.
    need(struct.unpack_from('<H',guest,off(0xff904f70))[0]==0x9a22,
         'Exact native long-copy instruction servicing watchdog address')
    end = Decimal(reset['seconds'])
    begin = end-Decimal(reset['watchdogSeconds'])
    observed = [r for r in records['MK2_SECRET_RESET_TRACE']
                if begin <= Decimal(r['seconds']) < end and r['watchdogPC']=='FF904F80']
    need(len(observed)>=20 and all(r['mode']=='0' and r['pc'] in ('FF904F50','FF904F60','FF904F70','FF904F80','FF904F90')
                                  for r in observed), 'Actual late native copy loop continues until reset')
    accept = records['MK2_STAGE_SECRET_ACCEPT']
    fight = records['MK2_STAGE_SECRET_FIGHT']
    punch = records['MK2_STAGE_SECRET_PUNCH']
    recover = records['MK2_STAGE_SECRET_RECOVER']
    need(len(accept)==len(fight)==len(punch)==len(recover)==1 and
         accept[0]['pc']=='FFA1A470' and accept[0]['taskSide']=='1' and
         fight[0]['id']=='18' and fight[0]['cpu_id']=='14' and fight[0]['arena']=='9' and
         int(accept[0]['frame'])<int(fight[0]['frame'])<int(punch[0]['frame'])<int(recover[0]['frame'])<int(reset['frame']),
         'Actual Sonya18 versus Smoke14 admission, punch and recovery precede the much later reset')
    return dict(actualNativeReset=reset, actualPreResetCopyLoop=observed,
                actualSonyaSecretAdmission=fight[0],actualSonyaPunch=punch[0],actualSonyaRecovery=recover[0],
                sourceCopyServicedWatchdog=True, graphicsSourceAndDestinationRegistersCaptured=False,
                malformedAssetIdentified=False, resetFixed=False,
                fullSecretControlSequenceAccepted=False, fullPortAcceptance=False)


def visual(c):
    need(c['folder']==FOLDER and c['terminal']['nativeExit']==0, 'Same actually reviewed original failed run')
    headers=[]
    for i,name in ((37,'secret_fight.png'),(38,'secret_recovered.png')):
        frame=c['rgbFrames'][i]
        need(frame['header']['stage']==name and
             hashlib.sha256(frame['pixels']).hexdigest().upper()==frame['header']['sha256'],
             'Whole actual viewed native screen bytes')
        headers.append(frame['header'])
    path=FOLDER/'finite_secret_visual_review.json'
    need(not path.exists(), 'Fresh finite review; original failed report unchanged')
    result=dict(actuallyViewedNativeFrames=headers,
                observation='Native Sonya versus gray Smoke, matching names and floor shadows; no selector artwork. Recovery shows the real Sonya body with low health. This does not accept subsequent survival or the late reset.',
                completeSecretControlSequenceAccepted=False,fullPortAcceptance=False,newRawMedia=0)
    path.write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    need(not OUT.exists() and not native.census(), 'Fresh provenance; original games terminal')
    transport = json.loads((FOLDER/'report.json').read_text())
    need(not transport['passed'] and transport['nativeTerminal']['nativeExit']==0,
         'Original failed transport and actual exit retained; no full-pass relabelling')
    for folder in (FOLDER,OTHER):
        report = json.loads((folder/'report.json').read_text())
        with gzip.open(folder/'executed_sources.json.gz','rt',encoding='utf-8') as f:
            sources = json.load(f)
        for path,digest in report['inputHashes'].items():
            if path in sources:
                need(digest==sources[path]['sha256']==hashlib.sha256(sources[path]['text'].encode()).hexdigest().upper(),
                     'Whole originally executed sources remain archived')
            else:
                need(sha(path)==digest, 'Original compiled/native/reference inputs unchanged')
        handle = native.k.OpenProcess(0x1000,False,report['nativeTerminal']['actualWindowsIdentity']['ParentProcessId'])
        if handle:
            native.k.CloseHandle(handle)
            raise ValueError('Original RAM review collector still live')
    with gzip.open(FOLDER/'run.log.gz','rt',encoding='utf-8') as f:
        records = inventory(f.read())
    guest,stock = current.expected(),(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    result = gate(records,guest,stock)
    reviewed=json.loads((FOLDER/'finite_secret_visual_review.json').read_text())
    need(len(reviewed['actuallyViewedNativeFrames'])==2 and not reviewed['completeSecretControlSequenceAccepted'],
         'Finite visual review never replaces whole secret/control/reset acceptance')
    faults = []
    for label,key,value in (('wrong reset PC','pc','FF811D20'),
                            ('wrong watchdog writer','watchdogPC','FF814E90'),
                            ('wrong elapsed watchdog time','watchdogSeconds','2.8')):
        changed = dict(records)
        changed['MK2_SECRET_NATIVE_RESET']=[dict(records['MK2_SECRET_NATIVE_RESET'][0],**{key:value})]
        try:
            gate(changed,guest,stock)
        except ValueError as error:
            faults.append(dict(fault=label,rejected=str(error)))
        else:
            raise ValueError('Altered actual reset provenance accepted')
    altered = bytearray(guest)
    altered[off(0xff904f70)]^=1
    try:
        gate(records,altered,stock)
    except ValueError as error:
        faults.append(dict(fault='native graphics-copy instruction',rejected=str(error)))
    else:
        raise ValueError('Altered actual copy source accepted')
    need(len(faults)==4 and gate(records,guest,stock)==result, 'Four actual evidence/source corruptions reject, positive restored')
    files = {p for folder in (FOLDER,OTHER) for p in folder.rglob('*') if p.is_file()}
    files.update((Path(__file__).resolve(),ROOT/'tools/preserve_incomplete_secret_capture.py',ROOT/'tools/check_rearmed_secret_faults.py',ROOT/'mk2ks_natural_smoke_route.lua'))
    storage=[]
    for path in sorted(files):
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink() and
             path.suffix.lower() not in ('.exe','.zip','.bin','.wav','.png','.pcm','.rgb','.mdata'), 'Exact finite text/evidence leaves only')
        digest,before=sha(path),allocated(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
        need(sha(path)==digest, 'Lossless bounded failed-run evidence compression')
        storage.append(dict(path=str(path),sha256=digest,beforeAllocatedBytes=before,allocatedBytes=allocated(path)))
    parent = ROOT/'audit_native_dual_roll_progress_storage/report.json'
    scope = json.loads(parent.read_text())['remaining']
    need(len(scope)==6, 'Original entire integration/release scope retained')
    result.update(provenanceCheckPassed=True,actualSourceRecordFaultsRejected=faults,
                  goalStatus='active', candidate=current.NAME, originalRemainingScope=scope,
                  previousGoalTurnClassification='progress: Sonya native slot rotations and unchanged sound-queue exposure checked',
                  thisGoalTurnClassification='progress: native Sonya Smoke admission/controls reproduced; held-punch controller corrected; genuine later watchdog reset localized to original graphics copy, not falsely accepted as a complete secret run',
                  originalFailedNativeRunsPreserved=2,allRAMHostsReleased=True,
                  exactCompressedTargets=storage,allocatedBytes=sum(r['allocatedBytes'] for r in storage),
                  nextAction='Capture decoder A/B registers, source/destination/header and return-PC ancestry at the first graphics-copy watchdog write. Identify and fix the offending record/table route; preserve the original failed runs. Separately use away-walking/finite punch pulses for actual same-round Smoke controls. No forced health/RNG; then complete combined current UI/audio/gameplay and matching public CMD/ZIP.',
                  publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(provenanceCheckPassed=True,actualLateGraphicsCopyWatchdogReset=True,
                         actualFaultsRejected=4,resetFixed=False,allocatedBytes=result['allocatedBytes'],allRAMHostsReleased=True)))


if __name__=='__main__':
    main()
