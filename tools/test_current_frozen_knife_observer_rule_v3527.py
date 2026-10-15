"""Narrow literal observer exception; original dynamic/write protection remains."""
import inspect,json,re,subprocess
from pathlib import Path
from unittest.mock import patch
import verify_current_campaign_shao_knife_observer_v3526 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
OUT=ROOT/'audit_v3528_current_frozen_knife_observer_rule_checked'
def main():
    need(not OUT.exists(),'Immutable narrow observer rule proof')
    original=native.source_boundary();clean=native.strip_checked_observer(original)
    need(clean==original[:-len(native.policy.LOAD)],'Exact one EOF load removed; every control byte remains')
    rule="need(not re.search(r':write_|\\bload\\s*\\(|\\bdofile\\s*\\(|\\beval\\b',source),'No guest writes/dynamic delegated code')"
    need(inspect.getsource(native.old.verify).count(rule)==1,'Original full-verifier rule bound exactly')
    def check_controls(source):
        need(not re.search(r':write_|\bload\s*\(|\bdofile\s*\(|\beval\b',native.strip_checked_observer(source)),
             'Original no guest writes/dynamic delegated code retained on all controls')
    check_controls(original);faults=[]
    variants=[('unknown_observer_path',original.replace(native.policy.LOAD,"dofile('unknown.lua')\n"),
       'Exactly one frozen literal read-only observer load'),
      ('duplicate_observer_load',original+native.policy.LOAD,'Exactly one frozen literal read-only observer load'),
      ('controller_guest_health_write',"p:write_u16(0x010602f0,161)\n"+original,'Original no guest writes/dynamic delegated code'),
      ('controller_dynamic_eval',"eval('guest write')\n"+original,'Original no guest writes/dynamic delegated code')]
    for name,changed,message in variants:
        need(changed!=original,'Non-vacuous actual loader/control source fault')
        try:check_controls(changed)
        except ValueError as error:
            need(message in str(error),'Specific narrow-loader or original dynamic/write rejection');faults.append(name)
        else:raise ValueError('Corrupted loader/write protection accepted')
    path=(ROOT/native.policy.OBSERVER).resolve();before=path.read_text();saved=Path.read_text
    altered=before+"p:write_u16(0x010602f0,161)\n"
    def read(p,*args,**kwargs):return altered if p.resolve()==path else saved(p,*args,**kwargs)
    with patch.object(Path,'read_text',read):
        try:native.strip_checked_observer(original)
        except ValueError as error:
            need('Entire read-only observer differs only'in str(error),'Entire observer source gate, not blanket relaxation')
            faults.append('observer_guest_health_write')
        else:raise ValueError('Observer guest write accepted')
    check_controls(original);need(native.strip_checked_observer(original)==clean,'Same-path original literal observer positive')
    pins={str(p.resolve()):sha(p)for p in(Path(__file__),Path(native.__file__),Path(native.policy.__file__),
       Path(native.old.__file__),ROOT/native.DRIVER,path,ROOT/'audit_v3514_current_shao_knife_source_checked/report.json')}
    value=dict(passed=True,onlyOneFrozenReadOnlyObserverLoadAllowed=True,originalDynamicCodeAndGuestWriteGateRetained=True,
       actualQualifiedSourceFaults=faults,samePathOriginalPositiveAccepted=True,actualCaptureOrGameChanged=False,
       wholeCampaignAcceptanceNotImpliedBySourceRules=True,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(value,indent=2)+'\n');digest=sha(p)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(p)],capture_output=True,text=True)
    need(result.returncode==0 and sha(p)==digest,'Lossless compact narrow-rule proof')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
