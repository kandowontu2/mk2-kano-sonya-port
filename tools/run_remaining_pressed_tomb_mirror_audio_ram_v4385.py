"""Same full native pressed-drop/audio gates, remaining real mirror roles.

Frozen4384 KanoP1 is not rerun. These are earned normal both-Down drop cases,
not unpressed/RNG, whole visible-scene or native DCS full-waveform acceptance.
"""
import json,subprocess,traceback
from pathlib import Path
import run_pressed_tomb_mirror_audio_ram_v4381 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v4386_both_characters_both_slots_pressed_tomb_mirror_audio'
COMPLETED=[]

def main():
    need(not OUT.exists(),'Fresh immutable pressed native mirror matrix')
    first=ROOT/'audit_v4384_pressed_kano_p1_tomb_mirror_audio_checked/report.json'
    previous=json.loads(first.read_text());need(previous['passed']and previous['actualNativeBothDownMirrorDropContexts']==1,'Actual qualified true KanoP1 native pressed drop')
    pins=dict(previous['inputHashes']);pins[str(first)]=sha(first);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'All original executed KanoP1 inputs/captures unchanged')
    capture,proof=runtime.preflight();need(proof==previous['sourcePreflight'],'Every full collector/pair/earned/pressed gate unchanged')
    guest=runtime.runtime.old.expected();COMPLETED.append(previous['case'])
    for fighter,side in (('sonya',1),('kano',2),('sonya',2)):
        case=runtime.pair(fighter,side,guest,capture)
        text=(ROOT/case['capture']/'run.log').read_text()
        pressed=runtime.state.qualify_pressed_drop(text,fighter,side,1,'positive',guest)
        need(case['lateOwnedMirrorVictimScreams']==1,'Exactly one genuine owned late victim scream for actual drop')
        case['nativePressedBranch']=pressed;case['actualNativePhaseFaultsRejected']=runtime.state.pressed_phase_faults(text,fighter,side,guest)
        COMPLETED.append(case)
        print(json.dumps(dict(qualified=fighter,side=side,actualNativeDropBranch=pressed['actualBothDownBranchFrame'],
          actualDCSDeliveredBytes=len(case['nativeDCSDeliveredBytes']),lateOwnedScreams=case['lateOwnedMirrorVictimScreams'],
          sourceQualifiedNativeMotion=pressed['phase'],fullPortAcceptance=False)),flush=True)
        for name in (case['capture'],case['baseline']):
            leaf=ROOT/name;meta=json.loads((leaf/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'All actual matrix input bytes consistent');pins[p]=h
            for p in leaf.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
    need({(c['fighter'],c['side'],c['victim'])for c in COMPLETED}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)},'All actual real-character/physical-slot mirrors')
    need(all(sha(p)==h for p,h in pins.items()),'All actual original/new source/log/result bytes unchanged')
    return dict(passed=True,candidate=runtime.runtime.old.NAME,cases=COMPLETED,inputHashes=pins,sourcePreflight=proof,
      actualNativeBothDownMirrorDropContexts=4,actualPairedCaptures=8,
      current3836BothCharactersBothSlotsNativePressedMirrorTombDropPhaseCleanupLateVictimRouteDCSDeliveryWinnerMixAccepted=True,
      unpressedNativeRandomMirrorDropContextsAccepted=False,fullTombRasterAndFloorShadowAccepted=False,
      nativeDCSStageVictimFullWaveformAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite partial/complete native pressed matrix');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Matrix compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
