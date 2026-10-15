"""Current actual failed chain forensic replay; original inputs exactly retained.

Just ten passive animation/root/descriptor/global-store taps. Same private
candidate, physical buttons and observation deadline; no test state writes.
"""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_kano_laser_sonya_postending_leg_guard_late as prior
import preserve_native_sonya_raiden_cache_failure as failure

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_sonya_raiden_cache_cause'
INIT=ROOT/'audit_native_sonya_raiden_cache_cause_initializer_source'
SOURCE=ROOT/'audit_native_sonya_raiden_cache_cause_source'
LUA='mk2ks_native_sonya_raiden_cache_cause.lua'
CONTROLLERS=[LUA,*prior.CONTROLLERS]
RAM={}


def source_guard():
    need(not SOURCE.exists(),'Fresh exact passive failure-cause source proof')
    original=json.loads((failure.OUT/'report.json').read_text())
    retired=json.loads((failure.RETIRED/'report.json').read_text())
    parent=json.loads((prior.SOURCE/'report.json').read_text())
    need(not original['passed'] and original['preservationPassed'] and
         original['confirmedCurrentNativeGraphicsCacheCorruption'] and original['actualGlobalCacheStores']==146 and
         retired['passed'] and parent['passed'] and all(sha(p)==h for p,h in original['inputHashes'].items()) and
         all(sha(p)==h for p,h in parent['inputHashes'].items()),
         'Actual failed original current process terminal/preserved before targeted provenance replay')
    observer=(ROOT/LUA).read_text()
    need(observer.count("dofile('mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua')")==1 and
         ':set_value(' not in observer and ':clear_value(' not in observer and
         'manager.machine:exit()' not in observer and 'cpu.PC.value~=0xff838860' in observer and
         'p:read_u16(actor+0x1f0)==18' in observer and 'p:read_u16(other+0x1f0)==7' in observer,
         'Passive true paired-victim identity/role trace only, no changed input or terminal policy')
    need(observer.count('install_read_tap')==1 and observer.count('install_write_tap')==1 and
         "assert(#taps==10" in observer and "ring_size=1800" in observer,
         'Exactly nine native read locations plus one passive first-store ring, bounded trace')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',(ROOT/name).read_text()),
             'All actual physical sources and observers contain no guest/ID/CPU/health/RNG edits')
    paths=[Path(__file__),Path(prior.__file__),Path(failure.__file__),failure.OUT/'report.json',
           failure.RETIRED/'report.json',prior.SOURCE/'report.json',*[ROOT/n for n in CONTROLLERS]]
    SOURCE.mkdir()
    report=dict(passed=True,sourceOnlyAccepted=True,nativeCauseAccepted=False,
        wholePriorPhysicalCampaignEndingJoinBytesUnchanged=True,passiveReadLocations=9,passiveFirstGlobalStoreTap=1,
        maximumRetainedProvenanceRows=1800,originalObservationDeadlineSeconds=18000,
        originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        fullPortAcceptance=False,goalStatus='active')
    (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    base=prior.prior.prior
    scope=dict(vars(base),__file__=__file__,OUT=OUT,INIT=INIT,SOURCE=SOURCE,LUA=LUA,
               CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (base.expectation,base.functions,base.run):
        exec(compile(inspect.getsource(function),__file__+'::entire_current_passive_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else SOURCE
        if folder.exists():
            p=folder/'current_capture_failure.json';need(not p.exists(),'Preserve actual terminal provenance trial failure')
            p.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual Sonya-victim/Raiden failure-cause trial; source fix/full goal remain open.',local=dict(RAM=RAM))
