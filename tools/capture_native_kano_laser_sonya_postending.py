"""Established entire Sonya campaign and fresh Kano join, current candidate.

Whole original physical policies are unchanged. Independent expected guest
and original current payload/source hashes bind this actual changed native
build. RAM-only critical rasters, lossless compressed chronology, no audio or
whole-port acceptance from terminal transport. Preserve failures, same handle.
"""
import code
import gzip
import hashlib
import inspect
import json
import os
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_sonya_p1_postending_kano as old
import capture_native_kano_laser_ui as current_ui
import capture_native_kano_laser_audio as audio
import native_process_census_v6647 as census

ROOT,need,sha=audio.ROOT,audio.need,audio.sha
NAME=audio.NAME
OUT=ROOT/'audit_native_kano_laser_sonya_postending'
INIT=ROOT/'audit_native_kano_laser_sonya_postending_initializer_source'
SOURCE=ROOT/'audit_native_kano_laser_sonya_postending_source'
LUA='mk2ks_native_kano_laser_sonya_postending.lua'
CONTROLLERS=[LUA,*old.CONTROLLERS]
RAM={}


def expectation():
    source=inspect.getsource(current_ui.expectation)
    scope=dict(vars(current_ui),__file__=__file__,INIT=INIT)
    exec(compile(source,__file__+'::whole_current_source_initializer','exec'),scope)
    guest,gfx,build=scope['expectation']()
    need(build['executable_sha256']=='186BF4D724F4426157001C5795E2FC589AA59E1BB605694E310A7695B38BCED3' and
         hashlib.sha256(guest).hexdigest().upper()=='AB1A0AEAE5BBE6457D591C8B9491E439E4DCA8F08A2E37A3710A3FA67769EF6E',
         'Actual current candidate, not an old campaign executable')
    provider=SimpleNamespace(ROOT=ROOT,NAME=NAME,EXE_SHA=build['executable_sha256'],
        GUEST_SHA=build['expected_guest_sha256'],PAYLOAD_SHA=build['payload_sha256'],
        __file__=__file__,expected=lambda:guest,expected_gfx=lambda:gfx)
    return guest,gfx,build,provider


def source_guard():
    need(not SOURCE.exists(),'Fresh exact campaign source qualification')
    accepted=json.loads((ROOT/'audit_v5214_extended_sonya_p1_whole_campaign_checked/report.json').read_text())
    rejected=json.loads((ROOT/'audit_native_sonya_p1_postending_kano_anchors_checked/cache_failure_preserved.json').read_text())
    need(accepted['passed'] and accepted['case']['unassisted_clear_proven'] and
         rejected['confirmedNativeGraphicsCorruption'] and rejected['observedGlobalStores']==146,
         'Original successful physical controller and later true cache failure retained, not treated as current success')
    for name in old.original.CONTROLLERS:
        p=ROOT/name
        need(accepted['case'].get('inputHashes',accepted.get('inputHashes',{})).get(str(p))==sha(p),
             'Whole previously earned tower physical controller unchanged: '+name)
    for name in old.CONTROLLERS:
        p=ROOT/name
        need(rejected['originalInputHashes'].get(str(p))==sha(p),'Whole later original ending/join loader unchanged: '+name)
    for name in CONTROLLERS:
        text=(ROOT/name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',text),
             'Every transitive physical controller/passive observer free of guest writes: '+name)
    wrapper=(ROOT/LUA).read_text()
    need(wrapper.count("dofile('mk2ks_native_sonya_p1_postending_kano.lua')")==1 and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and
         wrapper.count('manager.machine:exit()')==1 and 'if pending then' in wrapper,
         'New wrapper adds only passive real-overrun termination; no changed physical policy')
    parent=json.loads((ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json').read_text())
    need(len(parent['originalNaturalIntegrationRequirements'])==14 and len(parent['originalRemainingWorkGroups'])==6,
         'Full natural-game integration objective retained')
    paths=[Path(__file__),ROOT/'audit_v5214_extended_sonya_p1_whole_campaign_checked/report.json',
           ROOT/'audit_native_sonya_p1_postending_kano_anchors_checked/cache_failure_preserved.json',
           ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json',*[ROOT/n for n in CONTROLLERS]]
    SOURCE.mkdir()
    report=dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,
        wholeOriginalPhysicalCampaignAndEndingJoinControllersUnchanged=True,
        earlierRealCacheCorruptionNotRelabeledAsSuccess=True,originalObservationDeadlineSeconds=18000,
        newObserverOnlyStopsAfterRealCacheGlobalStores=True,originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        fullPortAcceptance=False,goalStatus='active')
    (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def functions(provider):
    source=old.capture_source()
    changes=[
        ("'-samplerate','48000'","'-samplerate','48000','-wavwrite','NUL'"),
        ('return dict(result=result,images=images,text=chronology,guest=guest)',
         'return dict(result=result,images=images,text=chronology,guest=guest,rawImages=raw_images)'),
        ('guestproof=None;scenes=[];', 'raw_images=RAM_RAW;guestproof=None;scenes=[];'),
        ('images={};preview_seen=set();', 'images=RAM_IMAGES;preview_seen=set();'),
        ('preview_seen.add(fields[\'sha256\']);images[name]=image',
         "preview_seen.add(fields['sha256']);images[name]=image;raw_images[name]=raw"),
        ('Actual terminal current4992 transport and native callbacks; inspect immutable failure',
         'Actual terminal current candidate transport and native callbacks; inspect immutable failure'),
        ("or line.startswith('MK2_CAMPAIGN_HOST_DEADLINE ')",
         "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_'))"),
    ]
    # The old adapter already wrote native_terminal after process.wait;
    # the identity is observed live, with an explicit current native provider.
    for before,after in changes:
        need(source.count(before)==1,'Exact whole original current host adaptation: '+before)
        source=source.replace(before,after,1)
    def metadata_clean(errors,proof):
        need(errors=='' and proof and proof['sha256']==provider.GUEST_SHA and proof['everyActualByteComparedInRAM'],
             'Completely empty current native error stream and whole independent guest')
        return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,releaseMetadataCorrectionStillRequired=False)
    scope=dict(vars(old.original),__file__=__file__,native=provider,census=census,OUT=OUT,LUA=LUA,
               CONTROLLERS=CONTROLLERS,qualify_payload_metadata_warning=metadata_clean,RAM_RAW={},RAM_IMAGES={})
    exec(compile(source,__file__+'::entire_original_physical_campaign_current_guest_host','exec'),scope)
    return scope,source


def run():
    need(not OUT.exists() and not INIT.exists() and not SOURCE.exists() and not census.census(),
         'One fresh current full campaign; never replay a live handle')
    guard=source_guard()
    guest,gfx,build,provider=expectation()
    scope,source=functions(provider)
    RAM.update(scope=scope,guest=guest,gfx=gfx,build=build)
    captured=scope['capture']()
    RAM['capture']=captured
    need(not census.census(),'Actual original native producer terminal, no replay')
    with gzip.open(OUT/'executed_current_postending_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(host=source,files={str(ROOT/n):(ROOT/n).read_text() for n in CONTROLLERS}),stream)
    need(all(sha(p)==h for p,h in guard['inputHashes'].items()),'Whole original campaign/ending/join physical sources intact after actual game')
    return captured


if __name__=='__main__':
    try: captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else SOURCE
        if folder.exists():
            p=folder/'current_capture_failure.json';need(not p.exists(),'Preserve actual original current failure')
            p.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual current campaign; no ending/join acceptance from transport alone.',local=dict(RAM=RAM))
