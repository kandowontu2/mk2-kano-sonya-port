"""Exact measured-controller delta, qualified source faults, no gameplay acceptance."""
import json,subprocess,sys
from pathlib import Path
from unittest.mock import patch
import verify_current_campaign_shao_guarded_highkick_v3461 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
OUT=ROOT/'audit_v3464_guarded_highkick_source_boundary'

def main():
    need(not OUT.exists(),'Immutable source boundary proof')
    positive=native.source_boundary();driver=(ROOT/native.DRIVER).resolve()
    original_read=Path.read_text;tests=[]
    source_error='Only stage16 physical decisions and policy labels differ; whole ordinary/Kintaro/selection/health/win/ending source exact'
    declared_error='Exact declared physical high-kick policy; no game/register/health/RNG writes'
    variants=[('wrong_guard_release_threshold',positive.replace('if gap<=105 and cpu_height<20 then','if gap<=125 and cpu_height<20 then',1),declared_error),
        ('changed_true_Sonya_identity',positive.replace('{kano=17,sonya=18}','{kano=17,sonya=1}',1),source_error),
        ('changed_original_Kintaro_window',positive.replace('cpu_height>160 and cpu_height<=240','cpu_height>150 and cpu_height<=240',1),source_error),
        ('injected_guest_health_write',positive.replace('     if gap<=105 and cpu_height<20 then','     p:write_u16(0x010602f0,161)\n     if gap<=105 and cpu_height<20 then',1),declared_error)]
    for label,changed,message in variants:
        need(changed!=positive,'Non-vacuous actual driver source fault')
        def read(path,*args,**kwargs):
            return changed if path.resolve()==driver else original_read(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            try:native.source_boundary()
            except ValueError as error:
                need(message in str(error),'Specific intended whole-source/declared-input invariant')
                tests.append(dict(name=label,rejectedBy=message))
            else:raise ValueError('Corrupted controller source accepted')
    need(native.source_boundary()==positive,'Same-path unchanged source positive')
    runner=(ROOT/native.RUNNER).read_text()
    restored=runner.replace('mk2ks_natural_campaign_shao_highkick_v3419.lua',
        'mk2ks_natural_campaign_shao_lowkick_v3406.lua').replace(native.DRIVER,
        'mk2ks_natural_campaign_shao_highkick_v3419.lua').replace('shao_guarded_highkick','shao_crouch_highkick')
    baseline=ROOT/'tools/run_current_campaign_shao_highkick_v3420.ps1'
    need(restored==baseline.read_text(),'Entire actual runner differs only in exact policy/driver/baseline paths')
    evidence=ROOT/'audit_v3446_current_sonya_defensive_leg_campaign_checked/report.json'
    proof=json.loads(evidence.read_text())
    hashes={str(Path(k).resolve()).casefold():v for k,v in proof['inputHashes'].items()}
    need(hashes[str(baseline.resolve()).casefold()]==sha(baseline),'Bound previously accepted entire runner')
    pins={str(p.resolve()):sha(p)for p in (driver,ROOT/native.BASELINE,ROOT/native.RUNNER,baseline,
        evidence,ROOT/'audit_v3456_current_highkick_incoming_exposure/report.json',
        ROOT/'audit_v3452_current_highkick_damage_model_checked/report.json',Path(__file__))}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py' and Path(file).resolve().is_relative_to(ROOT/'tools'):
            pins[str(Path(file).resolve())]=sha(file)
    for file,digest in pins.items():need(sha(file)==digest,'Actual source/evidence bytes unchanged')
    value=dict(passed=True,exactShaoOnlyGuardThresholdChangeAccepted=True,previousThreshold=125,currentThreshold=105,
        ordinaryAndKintaroControlsAndObserversUnchanged=True,actualRunnerInputsAndOptionsOtherwiseUnchanged=True,
        actualQualifiedSourceFaults=tests,samePathSourcePositiveAccepted=True,actualCaptureOrGameChanged=False,
        campaignAcceptancePending=True,controllerImprovementAccepted=False,rawAudioFilesWritten=0,newBuildsOrROMCopies=0,
        fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless source-boundary report compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
