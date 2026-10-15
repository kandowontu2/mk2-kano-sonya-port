"""Established normal P2 UI fixture, followed by naturally earned CPU Sonya finish."""
import code,gzip,json,re
from pathlib import Path
import capture_native_postending_join as host
import native_cpu_finisher_spacing_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_native_sonya_cpu_finisher'
LUA='mk2ks_native_sonya_cpu_finisher.lua'
CONTROLLERS=[LUA,'mk2ks_native_ui_flow_v2_probe.lua']
def metadata_clean(errors,proof):
    need(errors=='' and proof and proof['sha256']==native.GUEST_SHA and
         proof['executableSHA256']==native.EXE_SHA and proof['payloadSHA256']==native.PAYLOAD_SHA and
         proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten']==0,
         'Actual compiled candidate, complete initialized guest and empty native error stream')
    return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,releaseMetadataCorrectionStillRequired=False)
def capture_source():
    source=host.capture_source()
    before="MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='2',"
    after=before+"MK2KS_UI_FIGHTER='kano',MK2KS_UI_SIDE='2',MK2KS_UI_BOOT='604',"
    need(source.count(before)==1,'Exact host environment for unchanged original604frame UI input fixture')
    source=source.replace(before,after)
    before='  code=process.wait()'
    after=before+"\n (OUT/'native_terminal.json').write_text(json.dumps(dict(nativeExit=code,identity=identity),indent=2)+'\\n')"
    need(source.count(before)==1,'Exact actual child terminal provenance boundary')
    return source.replace(before,after)
def run():
    need(not OUT.exists() and not host.census.census(),'Fresh actual game process, no live-test restart')
    native.expected()
    prior=json.loads((ROOT/'audit_native_current_ui_ram/kano_p2/result.json').read_text())
    accepted=json.loads((ROOT/'audit_native_current_ui_owned_checked/report.json').read_text())
    case=next(r for r in accepted['cases'] if r['fighter']=='kano' and r['side']==2)
    ui=ROOT/CONTROLLERS[1]
    need(accepted['passed'] and case['sameActualCompleteStatePixelAndOwnerGatesAccepted'] and
         case['nativeTerminal']['nativeExit']==0 and prior['candidate']==accepted['candidate'] and
         prior['inputHashes'][str(ui)]==accepted['inputHashes'][str(ui)]==sha(ui) and
         all(sha(p)==h for p,h in accepted['inputHashes'].items()),
         'Entire actually accepted original P2 selection/ladder/first-combat input fixture unchanged')
    source=capture_source()
    need(all(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',(ROOT/p).read_text())
             for p in CONTROLLERS),'Only physical inputs and passive geometry/health/lookup observations')
    scope=dict(vars(host.original),__file__=__file__,native=native,census=host.census,
               OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,qualify_payload_metadata_warning=metadata_clean)
    exec(compile(source,__file__+'::whole_existing_native_RAM_host','exec'),scope)
    captured=scope['capture']()
    with gzip.open(OUT/'executed_host_and_controller_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(host=source,files={str(ROOT/p):(ROOT/p).read_text() for p in CONTROLLERS}),stream)
    return captured
if __name__=='__main__':
    try:capture=run()
    except Exception as e:
        if OUT.exists():
            path=OUT/'capture_failure.json';need(not path.exists(),'Preserve actual first failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(e),fullPortAcceptance=False),indent=2)+'\n')
        raise
    code.interact(banner='Actual CPU Sonya finisher test terminal; native frames remain in RAM.',local=dict(capture=capture))
