"""Qualified actual Knife-controller/observer source faults, positive control."""
import json,subprocess
from pathlib import Path
from unittest.mock import patch
import current_shao_knife_source_v3512 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
OUT=ROOT/'audit_v3514_current_shao_knife_source_checked'
def main():
    need(not OUT.exists(),'Immutable source evidence')
    original=native.source_boundary();native.runner_boundary();driver=(ROOT/native.DRIVER).resolve()
    saved=Path.read_text;faults=[]
    variants=[('wrong_Knife_attack',original.replace("if age>=8 and age<12 then press('High Punch')end","if age>=8 and age<12 then press('Low Punch')end",1),native.DECLARED_ERROR),
      ('changed_true_Kano_ID',original.replace('{kano=17,sonya=18}','{kano=1,sonya=18}',1),native.SOURCE_ERROR),
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
    observer=(ROOT/native.OBSERVER).resolve();real=native.observer_boundary()
    bad=real.replace('p:read_u32(m+0x230)==p:read_u32(slots[side].actor)',
       'p:read_u32(m+0x230)==p:read_u32(slots[opponent].actor)',1)
    need(bad!=real,'Non-vacuous original parent-link observer fault')
    def read(path,*args,**kwargs):return bad if path.resolve()==observer else saved(path,*args,**kwargs)
    with patch.object(Path,'read_text',read):
        try:native.observer_boundary()
        except ValueError as error:
            need('Entire read-only observer differs only'in str(error),'Specific read-only native-owner invariant')
            faults.append('wrong_observed_child_parent')
        else:raise ValueError('Wrong observer owner accepted')
    need(native.observer_boundary()==real,'Same-path unchanged observer positive')
    pins={str(p.resolve()):sha(p)for p in (driver,observer,ROOT/native.BASELINE,ROOT/native.RUNNER,
       ROOT/'tools/run_current_campaign_shao_ring_retreat_v3486.ps1',ROOT/'mk2ks_campaign_shao_ring_observer_v3499.lua',
       Path(__file__),Path(native.__file__),ROOT/'audit_v3412_current_kano_natural_lowkick_campaign_checked/report.json',
       ROOT/'audit_v3494_current_sonya_ring_campaign_checked/report.json',ROOT/'audit_v3505_current_ring_native_deciding_route_outcomes/report.json')}
    value=dict(passed=True,ordinaryAndKintaroControlsAndNativeObserversExact=True,entireRunnerOtherwiseExact=True,
       actualQualifiedSourceFaults=faults,samePathSourcePositiveAccepted=True,campaignAcceptancePending=True,
       noGamePowerDifficultyAIRNGOrHealthChanges=True,rawAudioFilesWritten=0,newBuildsOrROMCopies=0,
       readOnlyChildParentGuardDamageObserverPrepared=True,observerRuntimeNotYetAccepted=True,
       fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless compact source proof')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
