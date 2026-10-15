"""Same complete unassisted physical campaign on the native coordinate repair.

Keep all earlier fights, bosses, paid continues, deadlines and fresh-join policy.
Read all initialized windows and native raster callbacks; media remains in RAM.
No proxy/cheats/forced outcome/new ROM copy or public promotion.
"""
import code
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_shang_owned_drain_campaign as original
import verify_native_shang_drain_anchors_startup as startup

ROOT,need,sha=original.ROOT,original.need,original.sha
NAME=startup.NAME
OUT=ROOT/'audit_native_shang_drain_anchors_campaign'
SOURCE=ROOT/'audit_native_shang_drain_anchors_campaign_source'
INIT=ROOT/'audit_native_shang_drain_anchors_campaign_initializer'
LUA=original.LUA
CONTROLLERS=original.CONTROLLERS
RAM={}

def functions(provider):
    scope,host=original.functions(provider)
    scope.update(OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,RAM_HANDLE=RAM,__file__=__file__)
    before='metadataOwnedModelCorrectionRequired=True'
    need(host.count(before)==1,'Unique inherited corrected complete LOW-model label')
    host=host.replace(before,'metadataOwnedModelCorrectionRequired=False',1)
    exec(compile(host,__file__+'::same_whole_original_physical_campaign_on_coordinate_successor','exec'),scope)
    return scope,host

def run():
    need(not OUT.exists() and not SOURCE.exists() and not INIT.exists() and
         not startup.initial.identity.census() and not(ROOT/'mame-mkp/build/mingw-gcc').exists(),
         'Fresh replay only after original compiler/startup terminal and generated cache retirement')
    proof_paths=[ROOT/'audit_native_shang_repair_terminal_sampled_checked/report.json',
                 ROOT/'audit_native_shang_drain_anchors_source/report.json',
                 startup.BUILD_GUARD,startup.OUT/'report.json']
    prior,anchors,guard,cold=[json.loads(p.read_text(encoding='utf-8-sig'))for p in proof_paths]
    need(all(p['passed']for p in (prior,anchors,guard,cold)) and
         prior['finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted'] and
         anchors['changedHighBytes']==18 and cold['actualNativeInitializedWindowsAccepted'] and
         len(guard['originalNaturalIntegrationRequirements'])==14 and len(guard['originalRemainingWorkGroups'])==6,
         'Actual preceding recovery, coordinate-only conservation, full cold native windows and entire original scope')
    meta_path=ROOT/NAME/'build-info.json'
    meta=json.loads(meta_path.read_text(encoding='utf-8-sig'))
    need(not meta['public_build_promoted'] and not meta['native_runtime_accepted'] and not meta['full_port_accepted'] and
         sha(ROOT/NAME/'mkport_candidate.exe')==meta['executable_sha256'], 'Exact unpromoted compiled candidate')
    pins={}
    for proof in (prior,anchors,guard,cold):
        need(not proof['fullPortAcceptance'],'Finite predecessor proofs do not establish complete port')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and(p not in pins or pins[p]==h),'Every original immutable reviewed source: '+p)
            pins[p]=h
    for name in CONTROLLERS:
        source=(ROOT/name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',source),
             'Actual controller remains physical-input/passive-read only: '+name)
    provider=SimpleNamespace(ROOT=ROOT,NAME=NAME,EXE_SHA=meta['executable_sha256'],
        GUEST_SHA=meta['expected_guest_sha256'],PAYLOAD_SHA=meta['payload_sha256'],__file__=__file__)
    scope,host=functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'"in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'"in host and "'-str','18100'"in host and
         "'-nocheat'"in host and "'-wavwrite','NUL'"in host and 'len(images)<=64'in host,
         'Unchanged entire original selection/tower/ending/fresh-join strategy and deadlines; bounded RAM media')
    for path in (Path(__file__),Path(original.__file__),Path(startup.__file__),meta_path,*proof_paths,
                 *(ROOT/name for name in CONTROLLERS)):
        pins[str(path.resolve())]=sha(path)
    source_report=dict(passed=True,sourceOnlyAccepted=True,currentCandidate=NAME,
        unchangedWholeOriginalPhysicalInputs=True,allThirteenEarlierOpponentsRetained=True,
        inputHashes=pins,wholeGeneratedHostSHA256=startup.initial.digest(host.encode()),
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],fullPortAcceptance=False,
        actualFatalityArtworkAccepted=False,fullTowerAccepted=False,audioAccepted=False,goalStatus='active')
    SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(source_report,indent=2)+'\n')
    INIT.mkdir();wanted=startup.expected(INIT)
    need({k:startup.initial.digest(v)for k,v in wanted.items()}==cold['actualWindowHashes'],
         'Complete independent initialization matches actual cold native successor')
    provider.expected=lambda:wanted['high']
    provider.expected_windows=lambda:wanted
    provider.expected_gfx=lambda:wanted['graphics']
    RAM.update(scope=scope,wanted=wanted,build=meta,executedHost=host,guard=source_report)
    captured=scope['capture']();RAM['capture']=captured
    return captured

if __name__=='__main__':
    try:run()
    except Exception as error:
        folder=OUT if OUT.exists()else(INIT if INIT.exists()else SOURCE)
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if folder.exists():
            path=folder/'current_capture_failure.json';need(not path.exists(),'Never overwrite original campaign failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Original coordinate-repair native handle and complete evidence retained in RAM.',local=dict(RAM=RAM))
