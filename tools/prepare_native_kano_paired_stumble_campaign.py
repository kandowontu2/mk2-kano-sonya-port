"""Current-build Kano full tower capture, queued behind the same live Sonya run.

Keep every original Kano normal-input policy and5900-second deadline.
New wrappers observe actual packed-victim handoffs and global cache failure.
Source preflight alone does NOT boot a game or qualify runtime/art/audio.
"""
import argparse
import code
import gzip
import inspect
import json
import re
import traceback
from pathlib import Path
import run_current_kano_p1_campaign_v5195 as original
import capture_native_paired_stumble_campaign as repaired
import native_process_census_v6647 as census

ROOT, need, sha = repaired.ROOT, repaired.need, repaired.sha
OUT = ROOT / 'audit_native_kano_paired_stumble_campaign'
SOURCE = ROOT / 'audit_native_kano_paired_stumble_campaign_source'
INIT = ROOT / 'audit_native_kano_paired_stumble_campaign_initializer'
OLD_INIT = ROOT / 'audit_native_kano_paired_stumble_campaign_previous_initializer'
LUA = 'mk2ks_native_kano_paired_stumble_campaign.lua'
CONTROLLERS = [LUA,'mk2ks_native_kano_paired_stumble_cache_guard.lua',
    'mk2ks_native_paired_stumble_campaign.lua','mk2ks_native_kano_laser_sonya_postending.lua',*original.CONTROLLERS]
RAM = {}


def once(text,before,after):
    need(text.count(before)==1, 'Exactly one whole original transport boundary: '+before[:80])
    return text.replace(before,after)


def source_guard():
    nine_path = ROOT / 'audit_native_sonya_first_nine_ladder_fights_checked/report.json'
    nine = json.loads(nine_path.read_text())
    kano_path = ROOT / 'audit_v5200_current_kano_p1_whole_campaign_checked/report.json'
    kano = json.loads(kano_path.read_text())
    need(nine['passed'] and not nine['fullPortAcceptance'] and kano['passed'],
         'Current finite repaired-game evidence and old actual Kano campaign proof, not inherited current acceptance')
    need(all(sha(p)==h for p,h in nine['inputHashes'].items()), 'Every current repaired-source/native evidence input unchanged')
    old_pins = kano.get('case',{}).get('inputHashes',kano.get('inputHashes',{}))
    for name in original.CONTROLLERS:
        need(old_pins.get(str(ROOT/name))==sha(ROOT/name), 'All previously qualified ordinary Kano controls unchanged: '+name)
    for name in CONTROLLERS:
        text = (ROOT/name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',text),
             'Every loaded controller uses ordinary buttons and passive observations only')
    wrapper = (ROOT/LUA).read_text()
    need(wrapper.count("once(")==3 and
         wrapper.count("id==17 and p:read_u16(owner+0x1f0)==7")==1 and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'Two exact observer-route substitutions; no changed physical inputs or game exits')
    driver = (ROOT/'mk2ks_kano_current_p2_campaign_ram_v4472.lua').read_text()
    need("assert(limit==5900,'Declared finite observation window only')" in driver,
         'Entire original finite Kano observation deadline retained')
    need(len(nine['originalNaturalIntegrationRequirements'])==14 and len(nine['originalRemainingWorkGroups'])==6,
         'Full natural-character integration scope retained')
    paths = [Path(__file__),Path(original.__file__),Path(repaired.__file__),nine_path,kano_path,
             repaired.GUARD,*[ROOT/n for n in CONTROLLERS]]
    pins = {str(p.resolve()):sha(p) for p in paths}
    report = dict(passed=True,sourceOnlyAccepted=True,ordinaryKanoControlsByteIdentical=True,
        physicalInputChanges=0,passiveVictimRasterTarget=17,passiveVictimOwner=7,
        originalObservationDeadlineSeconds=5900,wholeOriginalKanoTowerAndEndingReturnRetained=True,
        additionalFreshJoinNotInThisOriginalController=True,currentCandidate=repaired.NAME,
        originalNaturalIntegrationRequirements=nine['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=nine['originalRemainingWorkGroups'],inputHashes=pins,
        nativeParserAccepted=False,nativeGameplayAccepted=False,fullTowerAccepted=False,
        endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,fullPortAcceptance=False,
        newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    if SOURCE.exists():
        need(json.loads((SOURCE/'report.json').read_text())==report, 'Existing full source preflight remains exactly unchanged')
    else:
        SOURCE.mkdir(); (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def functions(provider):
    text = inspect.getsource(original.capture)
    changes = (
        ("need(not OUT.exists(),'Fresh immutable campaign; never restart a live run')",
         "need(not OUT.exists() and not census.census(),'Fresh actual Kano run only after previous exact native terminal')"),
        ("'-samplepath',str(ROOT/'samples')", "'-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples')"),
        ("'-samplerate','48000'", "'-samplerate','48000','-wavwrite','NUL'"),
        ("stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:",
         "stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict',creationflags=subprocess.CREATE_NO_WINDOW)as process:"),
        ("  (OUT/'process.json').write_text(",
         "  identity=next((q for q in census.census() if q['ProcessId']==process.pid),None)\n"
         "  need(identity and identity['ParentProcessId']==os.getpid() and identity['createdUnix']>=started-1 and Path(identity['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve() and str(OUT) in identity['CommandLine'],'Same actual native child birth/path/parent/command')\n"
         "  (OUT/'native_identity.json').write_text(json.dumps(identity,indent=2)+'\\n')\n"
         "  (OUT/'process.json').write_text("),
        ('  code=process.wait()', "  code=process.wait()\n (OUT/'native_terminal.json').write_text(json.dumps(dict(nativeExit=code,identity=identity),indent=2)+'\\n')"),
        ('guestproof=None;scenes=[];', 'raw_images=RAM_RAW;guestproof=None;scenes=[];'),
        ('images={};preview_seen=set();', 'images=RAM_IMAGES;preview_seen=set();'),
        ("preview_seen.add(fields['sha256']);images[name]=image", "preview_seen.add(fields['sha256']);images[name]=image;raw_images[name]=raw"),
        ("      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+\n       base64.b64encode(preview.getvalue()).decode(),flush=True)",
         '      # Entire original native screen pixels retained only in RAM.'),
        ("name.startswith('ending_page') or name=='ending_return_to_attract.png')",
         "name.startswith('paired_stumble_victim_') or name.startswith('ending_page') or name=='ending_return_to_attract.png')"),
        ("or line.startswith('MK2_CAMPAIGN_HOST_DEADLINE ')",
         "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_','MK2_PAIRED_STUMBLE_'))"),
        ('  actualNaturalTowerClearAccepted=False,',
         "  actualNaturalTowerClearAccepted=False,actualPairedCacheOverrunObserved='MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ' in chronology,"),
        (" need(not overruns,'No original cache writes into global state')",
         " need(not overruns and 'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ' not in chronology,'No observed original cache writes into global state')"),
        (' return result\n', ' return dict(result=result,images=images,rawImages=raw_images,text=chronology,guest=guest)\n'))
    for before,after in changes: text = once(text,before,after)
    def metadata_clean(errors,proof):
        need(errors=='' and proof and proof['sha256']==provider.GUEST_SHA and proof['everyActualByteComparedInRAM'] and
             proof['executableSHA256']==provider.EXE_SHA and proof['payloadSHA256']==provider.PAYLOAD_SHA,
             'Completely empty current native error stream and full independent actual guest, no warning waiver')
        return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,releaseMetadataCorrectionStillRequired=False)
    scope = dict(vars(original),__file__=__file__,native=provider,census=census,OUT=OUT,LUA=LUA,
        CONTROLLERS=CONTROLLERS,qualify_payload_metadata_warning=metadata_clean,RAM_RAW={},RAM_IMAGES={})
    exec(compile(text,__file__+'::whole_original_Kano_capture_and_passive_identity_RAM_handoffs','exec'),scope)
    return scope,text


def run():
    need(not OUT.exists() and not census.census() and not (ROOT/'mame-mkp/build/mingw-gcc').exists(),
         'Wait for same Sonya run terminal/retirement; never replay solely for observation timeout')
    guard = source_guard()
    scope = dict(vars(repaired),__file__=__file__,OLD_INIT=OLD_INIT,INIT=INIT)
    exec(compile(inspect.getsource(repaired.expectation),__file__+'::whole_current_source_initializer','exec'),scope)
    guest,gfx,build,provider = scope['expectation']()
    host,executed = functions(provider)
    RAM.update(scope=host,guest=guest,gfx=gfx,build=build,executedHost=executed)
    captured = host['capture'](); RAM['capture'] = captured
    need(not any(q['ExecutablePath']==str(ROOT/repaired.NAME/'mkport_candidate.exe') for q in census.census()),
         'Actual native terminal, not observation timeout')
    need(all(sha(p)==h for p,h in guard['inputHashes'].items()), 'Whole prepared controls remain unchanged after native terminal')
    return captured


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--source-only',action='store_true'); args=parser.parse_args()
    if args.source_only:
        report=source_guard()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,nativeBoots=0,emulatorBuilds=0,
                             nativeGameplayAccepted=False,fullPortAcceptance=False)),flush=True)
    else:
        try: captured=run()
        except Exception as error:
            folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
            if folder.exists():
                path=folder/'current_capture_failure.json'; need(not path.exists(),'Preserve actual original preparation/capture failure')
                path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual current Kano native buffers; no whole-port acceptance from transport.',local=dict(RAM=RAM))
