"""Qualified actual Ring-controller source faults and same-path positive."""
import json,subprocess
from pathlib import Path
from unittest.mock import patch
import current_shao_ring_source_v3487 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
OUT=ROOT/'audit_v3489_current_shao_ring_source_checked'
def main():
    need(not OUT.exists(),'Immutable source evidence')
    original=native.source_boundary();native.runner_boundary();driver=(ROOT/native.DRIVER).resolve()
    saved=Path.read_text;faults=[]
    variants=[('wrong_Ring_attack',original.replace("press('Low Punch')end","press('High Punch')end",1),native.DECLARED_ERROR),
      ('changed_true_Sonya_ID',original.replace('{kano=17,sonya=18}','{kano=17,sonya=1}',1),native.SOURCE_ERROR),
      ('changed_original_Kintaro_window',original.replace('cpu_height>160 and cpu_height<=240','cpu_height>150 and cpu_height<=240',1),native.SOURCE_ERROR),
      ('injected_guest_health',original.replace('     elseif gap<140 then','     p:write_u16(0x010602f0,161)\n     elseif gap<140 then',1),native.DECLARED_ERROR)]
    for name,changed,message in variants:
        need(changed!=original,'Non-vacuous actual controller fault')
        def read(path,*args,**kwargs):return changed if path.resolve()==driver else saved(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            try:native.source_boundary()
            except ValueError as error:
                need(message in str(error),'Intended source/button invariant rejected');faults.append(name)
            else:raise ValueError('Changed source accepted')
    need(native.source_boundary()==original,'Same-path actual source positive')
    pins={str(p.resolve()):sha(p)for p in (driver,ROOT/native.BASELINE,ROOT/native.RUNNER,ROOT/native.base.RUNNER,
       Path(__file__),Path(native.__file__),ROOT/'audit_v3474_current_sonya_guarded_highkick_campaign_checked/report.json',
       ROOT/'audit_v3480_current_guarded_highkick_incoming_exposure/report.json',ROOT/'audit_v3482_current_ring_boss_frontgate_checked/report.json')}
    value=dict(passed=True,ordinaryAndKintaroControlsAndNativeObserversExact=True,entireRunnerOtherwiseExact=True,
       actualQualifiedSourceFaults=faults,samePathSourcePositiveAccepted=True,campaignAcceptancePending=True,
       noGamePowerDifficultyAIRNGOrHealthChanges=True,rawAudioFilesWritten=0,newBuildsOrROMCopies=0,
       fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless compact source proof')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
