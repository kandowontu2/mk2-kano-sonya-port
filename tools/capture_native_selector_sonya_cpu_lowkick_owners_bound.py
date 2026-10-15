"""Retain actual IN0 Low Kick errors; same full collector with correct IN2.

Only run after exact original49084 is genuinely terminal. No restart on
observation timeout. Reject Lua callback errors even if transport passes.
"""
import json
from pathlib import Path
import capture_native_selector_sonya_cpu_lowkick_owners as rejected

ROOT,need,sha=rejected.ROOT,rejected.need,rejected.sha
REJECTION=ROOT/'audit_native_selector_sonya_cpu_lowkick_input_rejected/report.json'


def preserve_rejection():
    held=rejected.NATIVE_HANDLES[rejected.KEY]
    need(held['process'].poll()==0 and held['identity']['ProcessId']==49084,
         'Exact original failed-controller run terminal0; never restart an active run')
    original=rejected.OUT/'failure.json'
    folder,text,images=rejected.RAM_CASES[rejected.KEY]
    stderr=folder/'stderr.log'; errors=stderr.read_text()
    marker="attempt to index a nil value (field 'P1 Low Kick')"
    need('[LUA ERROR]' in errors and marker in errors,
         'Actual original missing-IN2 controller failure, not a timeout or game softlock')
    pins={str(p.resolve()):sha(p) for p in (original,stderr,Path(rejected.__file__),rejected.LUA,
                                          folder/'result.json',folder/'process.json')}
    value=dict(passed=False,preservationPassed=True,goalStatus='active',actualNativeIdentity=held['identity'],
        nativeExit=0,reason='Original IN0 controller lookup omitted actual IN2 P1 Low Kick',
        actualLuaErrorCount=errors.count(marker),wholeOriginalTransportReceiptPreserved=True,
        physicalLowkickGameplayAccepted=False,privateOwnerRetirementAccepted=False,inputHashes=pins,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    if REJECTION.exists():
        need(json.loads(REJECTION.read_text())==value,'Preserved original actual rejection unchanged')
    else:
        REJECTION.parent.mkdir(); REJECTION.write_text(json.dumps(value,indent=2)+'\n')
    return value


original_source=Path(rejected.__file__).read_text()
source=original_source
for before,after in (
    ("BASE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_ram'",
     "BASE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_bound_ram'"),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_capture_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_bound_capture_checked'"),
    ("LUA=ROOT/'mk2ks_native_selector_sonya_cpu_lowkick_owners.lua'",
     "LUA=ROOT/'mk2ks_native_selector_sonya_cpu_lowkick_owners_bound.lua'"),
    ("KEY='ordinary_Kano_walk_lowkick_native_Sonya_CPU_actual_voice_owners'",
     "KEY='ordinary_Kano_actual_IN2_lowkick_native_Sonya_CPU_actual_voice_owners'"),
    ("old=previous.NATIVE_HANDLES[previous.KEY]", "old=rejected.NATIVE_HANDLES[rejected.KEY]"),
    ("old['identity']['ProcessId']==50372", "old['identity']['ProcessId']==49084"),
    ("for p in (Path(__file__),LUA,parent.OUT,Path(previous.__file__),Path(parent.__file__),",
     "for p in (Path(__file__),Path(rejected.__file__),rejected.LUA,rejected.OUT/'failure.json',REJECTION,LUA,parent.OUT,Path(previous.__file__),Path(parent.__file__),"),
    ("lua=LUA.read_text()",
     "lua=rejected.LUA.read_text(); wrapper=LUA.read_text()\n    need(\"manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']\" in wrapper and \"high['P1 Down'],high['P1 Block']}\" in wrapper, 'Actual compiled IN2 lookup and original per-frame release list')"),
    ("held=NATIVE_HANDLES[KEY]\n    need(held['process'].poll()==report['nativeExit']",
     "held=NATIVE_HANDLES[KEY]\n    need('[LUA ERROR]' not in (BASE/KEY/'stderr.log').read_text(), 'Every actual Lua controller/observer callback completed without error')\n    need(held['process'].poll()==report['nativeExit']")):
    need(source.count(before)==1,'Only actual input binding, error admission and source-preservation boundaries')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_original_collector_actual_IN2_input_and_release','exec'))


original_execute=execute
def execute(state,preflight=False):
    failure=preserve_rejection()
    need(all(sha(p)==h for p,h in failure['inputHashes'].items()),'Whole original actual failed controller evidence intact')
    return original_execute(state,preflight)
