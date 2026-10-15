"""Complete true17/17 and18/18 Tomb contexts in both physical slots, RAM audio.

Reuse the qualified complete4350 controller/collector and native1731 gates.
Never replay the frozen KanoP1 context, overwrite a capture or persist PCM.
This extends earned mirror/cleanup/winner audio evidence, not full raster or
complete stock DCS waveform/stage/mirror-branch acceptance.
"""
import json,subprocess,traceback
from pathlib import Path
import run_tomb_mirror_audio_ram_v4350 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v4354_both_characters_both_slots_tomb_mirrors'
COMPLETED=[]

def main():
    need(not OUT.exists(),'Fresh bounded complete mirror matrix')
    first=ROOT/'audit_v4352_tomb_mirror_audio_ram_observed/report.json'
    old=json.loads(first.read_text());need(old['passed']and old['actualTrueMirrorContexts']==1,'Actual qualified KanoP1 context')
    pins=dict(old['inputHashes']);pins[str(first)]=sha(first);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(path)==h for path,h in pins.items()),'All frozen original KanoP1 inputs/evidence unchanged')
    capture,proof=runtime.preflight();need(proof==old['sourcePreflight'],'Exact same original full contracts and RAM collector')
    guest=runtime.old.expected();COMPLETED.append(old['case'])
    for fighter,side in (('sonya',1),('kano',2),('sonya',2)):
        case=runtime.pair(fighter,side,guest,capture);COMPLETED.append(case)
        print(json.dumps(dict(qualified=fighter,side=side,actionFrame=case['inputContract']['action_frame'],
          actualDeliveredDCSBytes=len(case['nativeDCSDeliveredBytes']),lateMirrorScreams=case['lateOwnedMirrorVictimScreams'],
          winnerMix=case['originalWinnerMix'],fullPortAcceptance=False)),flush=True)
        for name in (case['capture'],case['baseline']):
            leaf=ROOT/name;meta=json.loads((leaf/'result.json').read_text())
            for path,h in meta['input_hashes'].items():need(path not in pins or pins[path]==h,'Every paired matrix source byte consistent');pins[path]=h
            for path in leaf.rglob('*'):
                if path.is_file():pins[str(path)]=sha(path)
    need({(c['fighter'],c['side'],c['victim'])for c in COMPLETED}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)},'All four real physical mirror contexts')
    need(all(sha(path)==h for path,h in pins.items()),'All actual frozen native inputs/captures/report bytes unchanged')
    return dict(passed=True,candidate=runtime.old.NAME,cases=COMPLETED,inputHashes=pins,sourcePreflight=proof,
      actualTrueMirrorContexts=4,actualPairedCaptures=8,
      current3836NativeTombBothTrueMirrorCharactersBothSlotsEarnedStateCleanupDCSDeliveryWinnerMixAccepted=True,
      fullTombRasterAndFloorShadowAccepted=False,nativeDCSStageVictimFullWaveformAccepted=False,
      allStageMirrorBranchesAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite actual partial or complete mirror observations');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
