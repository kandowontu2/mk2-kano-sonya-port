"""Whole original Kano native/boss/ending gate on this exact repaired game.

Run inside the actual retained RAM parent after genuine native completion.
No reconstructed guest/raster files, no control changes, and no inherited
art/audio/finisher/fresh-join acceptance from a successful campaign.
"""
import hashlib
import inspect
import json
import os
from pathlib import Path
from types import SimpleNamespace
import verify_current_kano_p1_whole_campaign_v5199 as original
import prepare_native_kano_paired_stumble_host_checked as capture
import prepare_native_kano_paired_stumble_campaign as prepared
import native_process_census_v6647 as census

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_kano_repaired_whole_campaign_checked'


def verify(ram):
    need(not OUT.exists(), 'Fresh whole current native campaign qualification')
    folder = capture.OUT
    identity = json.loads((folder/'native_identity.json').read_text())
    terminal = json.loads((folder/'native_terminal.json').read_text())
    proof = json.loads((folder/'guest_memory_proof.json').read_text())
    source = json.loads((capture.SOURCE/'report.json').read_text())
    metadata = json.loads((folder/'result.json').read_text())
    need(os.getpid()==identity['ParentProcessId'] and terminal['identity']==identity and terminal['nativeExit']==0 and
         identity not in census.census() and source['passed'] and source['wholePythonHostCompiled'] and
         hashlib.sha256(ram['executedHost'].encode()).hexdigest().upper()==source['hostSourceSHA256'] and
         all(sha(p)==h for p,h in source['inputHashes'].items()),
         'Same exact original RAM parent, executed entire host and actual successful native terminal')
    guest = ram['guest']
    build = ram['build']
    provider = SimpleNamespace(NAME=prepared.repaired.NAME,ROOT=ROOT,EXE_SHA=build['executable_sha256'],
        GUEST_SHA=build['expected_guest_sha256'],PAYLOAD_SHA=build['payload_sha256'],expected=lambda:guest)

    def metadata_clean(errors,actual):
        need(errors=='' and actual==proof and actual['everyActualByteComparedInRAM'] and
             actual['sha256']==provider.GUEST_SHA and actual['executableSHA256']==provider.EXE_SHA and
             actual['payloadSHA256']==provider.PAYLOAD_SHA, 'Empty actual native stderr and full original guest proof')
        return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,releaseMetadataCorrectionStillRequired=False)

    transport = SimpleNamespace(OUT=folder,CONTROLLERS=prepared.CONTROLLERS,LUA=prepared.LUA,
        __file__=capture.__file__,qualify_payload_metadata_warning=metadata_clean)
    scope = dict(vars(original),__file__=__file__,OUT=OUT,current=provider,capture=transport)

    def matched(actual_folder,pins):
        before = json.loads((folder/'input_hashes_before.json').read_text())
        need(actual_folder==folder and metadata['passed'] and metadata['nativeExit']==0 and metadata['fighter']=='kano' and
             metadata['physicalSlot']==1 and metadata['identity']==17 and metadata['inputHashes']==before and
             metadata['candidate']==provider.NAME and metadata['executableSHA256']==provider.EXE_SHA and
             metadata['guestSHA256']==provider.GUEST_SHA and metadata['rawMediaGuestAudioFilesWritten']==metadata['newBuilds']==0 and
             not metadata['nativeCacheOverrunObserved'] and not metadata['actualPairedCacheOverrunObserved'] and
             all(sha(p)==h for p,h in before.items()) and
             all(before.get(p)==h for p,h in build['input_hashes'].items()),
             'Entire actually executed current guest/build/control inputs and zero observed cache overruns')
        need(metadata_clean((folder/'stderr.log').read_text(),proof)==metadata['qualifiedTestCandidateMetadataWarning'],
             'No older candidate metadata-warning exemption inherited')
        text='\n'.join((ROOT/name).read_text() for name in prepared.CONTROLLERS)
        need(not original.re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',text),
             'Every transitive physical controller and passive observer unchanged and free of guest writes')
        command=identity['CommandLine']
        need('-nocheat' in command and '-noautoframeskip' in command and '-frameskip 0' in command and
             "MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'" in ram['executedHost'] and
             "MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'" in ram['executedHost'],
             'Actual native command and complete executed original ordinary Kano physical policy')
        need(not any(p.suffix.lower() in ('.png','.wav','.bin') for p in folder.rglob('*') if p.is_file()),
             'No guest/raster/audio dumps created')
        pins.update(before)
        original.original.original.knife.source_boundary()

    scope['matched'] = matched
    for function in (original.read_log,original.campaign_meta,original.ram_guest,original.ram_guest_checked,
                     original.adapt_transport,original.make_native,original.run):
        exec(compile(inspect.getsource(function),__file__+'::entire_original_'+function.__name__,'exec'),scope)
    report = scope['run']()
    need(report['passed'] and report['actualNaturalCurrentKanoP1BossesOwnEndingAttractAccepted'] and
         not report['fullPortAcceptance'], 'Entire original all-opponent/boss/native-ending gate, never whole-port acceptance')
    need(not original.re.search(r'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE |MK2_MILEENA_CAMPAIGN_OVERRUN |LUA ERROR|stack traceback',
                               scope['read_log'](folder)), 'Entire actual chronology remains free of observed corruption/callback failure')
    report.update(actualNativeIdentity=identity,actualNativeTerminal=terminal,
        fullCurrentNativeKanoTowerEndingReturnAccepted=True,freshJoinAccepted=False,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    for p in (Path(__file__),Path(original.__file__),Path(capture.__file__),Path(prepared.__file__),
              capture.SOURCE/'report.json',folder/'native_identity.json',folder/'native_terminal.json'):
        report['inputHashes'][str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in report['inputHashes'].items()), 'All original current inputs remain bound after full campaign/fault gate')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,fullCurrentNativeKanoTowerEndingReturnAccepted=True,
        actualNativePID=identity['ProcessId'],stages=report['case']['stages_reached'],
        semanticFaultsRejected=len(report['actualNativeAndRAMProofFaultsRejected']),
        freshJoinAccepted=False,fullPortAcceptance=False)),flush=True)
    return report
