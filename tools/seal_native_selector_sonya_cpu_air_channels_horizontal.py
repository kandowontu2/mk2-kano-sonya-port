"""Seal current same-run channel/packet and both-actor movement evidence.

Keeps the original contact/display/audio receipt and all rejected checker
sources unchanged. Compress only this small metadata/source addition, never
make a ROM, raw-media, build or ZIP copy. Full objective remains active.
"""
import json, subprocess
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_horizontal as horizontal
import seal_native_selector_sonya_cpu_air as previous

ROOT, need, sha = horizontal.ROOT, horizontal.need, horizontal.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_channels_horizontal_sealed.json'


def execute():
    need(not OUT.exists(),'Fresh immutable integrated movement/channel receipt')
    old=ROOT/'audit_native_selector_sonya_cpu_air_sealed.json'
    need(sha(old)=='F460BE9CE888CBAFDB506B9D698554283E5763BAB4B02F2DE1761FE0CD1E9C12',
         'Whole original contact/display/audio finite receipt unchanged')
    paths=[old,horizontal.audio.OUT/'report.json',horizontal.OUT/'report.json']
    reports=[json.loads(p.read_text()) for p in paths]
    capture=horizontal.contact.control.capture; held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in previous.census.census_hosts() if r['ProcessId']==38752)
    need(held['process'].poll()==0 and (host['ParentProcessId'],host['createdUnix'])==
         (40316,1791734919.6266766) and not previous.census.identity.census() and
         all(r['passed'] and r['actualNativeIdentity']==held['identity'] for r in reports),
         'All finite proofs on actual50372 terminal and same original host; no pending native game')
    channels=reports[1]; movement=reports[2]
    need(channels['completeRecorded19ChannelClocksAccepted'] and
         channels['wholeRecordedNativePacketsAccepted'] and
         channels['all19ChannelClocks']['exactPreciseChannelStates']==31274 and
         channels['all19ChannelClocks']['exactVideoChannelStates']==34219 and
         channels['wholeNativePacketADSPChronology']['packets']==133 and
         len(channels['effectiveFaultsRejected'])==18 and
         movement['pairedHorizontal']['actualWordStores']==721 and
         movement['pairedHorizontal']['physicalNextFieldComparisons']==166 and
         movement['pairedHorizontal']['releasedHorizontalPushReplayAccepted'] and
         len(movement['effectiveFaultsRejected'])==19,
         'Complete recorded channel/packet and both-actor contact/recovery movement scopes')
    need(not channels['privateOwnerRetirementAccepted'] and
         not channels['allOverlapPriorityContextsAccepted'] and
         not movement['allContactsArenasAccepted'] and
         all(not r['fullPortAcceptance'] for r in reports),
         'Owner lifetime/priority, wider arena coverage and full objective not inferred')
    pins={}
    for report in reports:
        for p,h in report['inputHashes'].items():
            need(p not in pins or pins[p]==h,'No differing whole source/evidence pin replaced'); pins[p]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every entire historical/current evidence input intact')
    sources=[ROOT/'tools'/name for name in (
        'qualify_native_selector_sonya_cpu_air_channels.py',
        'qualify_native_selector_sonya_cpu_air_channels_assets.py',
        'qualify_native_selector_sonya_cpu_air_horizontal.py')]
    failure=ROOT/'audit_native_selector_sonya_cpu_air_channels_checked/failure.json'
    need(json.loads(failure.read_text())['error']=="NameError(\"name 'qualified' is not defined\")",
         'Original actual asset-prefix checker rejection preserved')
    files={Path(__file__).resolve(),failure.resolve(),*(p.resolve() for p in sources),
           *(p.resolve() for p in paths[1:])}
    for p in paths:
        key=str(p.resolve()); h=sha(p)
        need(key not in pins or pins[key]==h,'Original full receipt/checker reports not overwritten'); pins[key]=h
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve()) and p.suffix in ('.py','.json'),
             'Only exact new small metadata/source files, no folder wildcard or raw media')
        key=str(p); h=sha(p)
        need(key not in pins or pins[key]==h,'No executed source/failed or passing evidence rewritten'); pins[key]=h
        logical=p.stat().st_size; before=previous.storage.stored(p)
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',key],capture_output=True)
        need(call.returncode==0 and sha(p)==h,'Whole metadata bytes preserved after exact LZX')
        entries.append(dict(path=key,sha256=h,logicalBytes=logical,storedBefore=before,
                            storedAfter=previous.storage.stored(p)))
    sync=previous.storage.source.verify()
    need(sync['passed'] and all(sha(p)==h for p,h in pins.items()),
         'All15 compiled sources, fixed CMD/ZIP/private endpoints and whole evidence pins unchanged')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        previousReceipt=str(old),previousReceiptSHA256=sha(old),
        all19ChannelClocks=channels['all19ChannelClocks'],
        wholeNativePacketADSPChronology=channels['wholeNativePacketADSPChronology'],
        pairedHorizontal=movement['pairedHorizontal'],effectiveChannelFaultsRejected=18,
        effectiveHorizontalFaultsRejected=19,originalAssetProofPrefixFailurePreserved=True,
        sourceSyncPassed=True,fullInputPins=len(pins),inputMismatches=0,inputHashes=pins,
        exactNewSmallFileCompression=entries,logicalNewMetadataBytes=sum(r['logicalBytes'] for r in entries),
        storedNewMetadataBytes=sum(r['storedAfter'] for r in entries),
        requirements=reports[0]['requirements'],remainingGroups=reports[0]['remainingGroups'],
        privateOwnerRetirementAccepted=False,allHitGruntProducersIndividuallyAccepted=False,
        allOverlapPriorityContextsAccepted=False,heardAudioQualityAccepted=False,
        directContactInstructionTapAccepted=False,allUnsavedErasureAccepted=False,
        allEffectOwnershipAccepted=False,allContactsArenasAccepted=False,
        wholeObjectiveStillActive=True,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0)
    OUT.write_text(json.dumps(result,indent=2)+'\n'); h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole final immutable integrated receipt unchanged after LZX')
    print('PASS all19 channels/133 packets/721 paired stores; full scope active, public unchanged',flush=True)
    return result
