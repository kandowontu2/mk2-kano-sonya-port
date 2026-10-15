"""Finite native Sonya/Raiden handoff fix; unsuccessful tower remains false.

Three real native handoffs, full guest binding, physical loss/continue fields,
and five individually inspected original rasters. No broader victim, sound,
whole campaign, ending, join or full-port acceptance is inferred.
"""
import copy
import gzip
import hashlib
import json
import os
import re
import struct
from pathlib import Path
import capture_native_paired_stumble_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT / 'audit_native_paired_stumble_handoff_checked'
GAME, PARENT = 129056, 64112


def handoffs(rows, guest, payload):
    need(len(rows) == 9, 'All three original native handoffs retained, not a filtered subset')
    grouped = {}
    for row in rows:
        grouped.setdefault(int(row['frame']), []).append(row)
    need(len(grouped) == 3 and min(grouped) == 54865, 'Exact previously corrupting native callback and two later repeats')
    outer = struct.unpack_from('<I', guest, (0xff9060a0 - 0xff800000) // 8)[0]
    root = struct.unpack_from('<I', guest, (outer - 0xff800000) // 8 + 18 * 4)[0]
    stream = struct.unpack_from('<I', payload, (root - 0xfe800000) // 8 + 35 * 4)[0]
    group = struct.unpack_from('<I', payload, (stream - 0xfe800000) // 8 + 3 * 4)[0]
    need(root == 0xff020000 and group == 0xff031a80, 'Actual own Sonya main35 fourth composite')
    accepted = []
    for frame, items in sorted(grouped.items()):
        need([r['kind'] for r in items] == ['packed_input', 'after_lookup', 'after_render'],
             'Original native instruction order and complete handoff')
        entry, lookup, rendered = items
        for row, pc, at, data in zip(items, ('FF875300','FF8753D0','FF842340'),
                                    ('FF8752F0','FF8753C0','FF842330'), ('4C09','0D5F','09AF')):
            need(row['pc'] == pc and row['at'] == at and row['data'] == data and row['mask'] == 'FFFF' and
                 row['owner_id'] == '7' and row['victim_id'] == '18' and row['stage'] == '2' and
                 row['action'] == '0303' and row['packed'] == '2303BCE0' and
                 row['writes'] == '0' and row['assistance'] == 'none' and row['health'].split(',')[0] == '0',
                 'Actual native instructions, full width, owned identities, KO context and repaired parameter')
            need(all(row[k] == entry[k] for k in ('owner_actor','victim_actor','main','victim_main','cache','health')) and
                 row['owner_actor'] != row['victim_actor'] and row['main'] != row['victim_main'] and
                 all(0x01000000 <= int(row[k],16) < 0x01100000
                     for k in ('owner_actor','victim_actor','main','victim_main','cache')),
                 'Complete original actor/Main/cache context across each actual handoff')
        need(entry['actor'] == lookup['actor'] == entry['owner_actor'] and
             rendered['actor'] == entry['victim_actor'] and entry['a0'] == '2303BCE0' and
             entry['a1'] == 'FFFEBD00' and lookup['a0'] == f'{root:08X}' and
             lookup['a1'] == '00000060' and lookup['a9'] == f'{stream + 3*32:08X}' and
             rendered['a9'] == f'{stream + 4*32:08X}' and rendered['pose'] == f'{group:08X}',
             'Native packed row -> true own animation -> correct pose offset -> actual own composite copied')
        accepted.append(dict(callback=frame, actualVictimActor=entry['victim_actor'],
            actualOwnerActor=entry['owner_actor'], actualVictimMain=entry['victim_main'],
            actualOwnerMain=entry['main'], actualOwnedComposite=f'{group:08X}', health=entry['health']))
    return accepted


def verify(ram, carrier, server):
    need(os.getpid() == PARENT and not OUT.exists(), 'Exact retained original native parent; fresh finite proof')
    folder = capture.OUT
    terminal = json.loads((folder / 'native_terminal.json').read_text())
    metadata = json.loads((folder / 'result.json').read_text())
    failure = json.loads((folder / 'current_capture_failure.json').read_text())
    stop = json.loads((folder / 'explicit_unsuccessful_physical_policy_stop.json').read_text())
    proof = json.loads((folder / 'guest_memory_proof.json').read_text())
    before = json.loads((folder / 'input_hashes_before.json').read_text())
    need(terminal['nativeExit'] == 4294967295 and terminal['identity']['ProcessId'] == GAME and
         terminal['identity']['ParentProcessId'] == PARENT and not metadata['passed'] and
         not failure['passed'] and stop['physicalPolicyUnsuccessful'] and
         stop['observedLossesByStage']['2'] == 43 and not stop['stoppedSolelyForObservationTimeout'] and
         not metadata['nativeCacheOverrunObserved'] and not capture.base.census.census(),
         'Original unsuccessful-policy stop preserved; not mislabelled as successful tower/native zero exit')
    need(proof['everyActualByteComparedInRAM'] and proof['bytes'] == 1048576 and
         hashlib.sha256(ram['guest']).hexdigest().upper() == proof['sha256'] == metadata['guestSHA256'] and
         proof['executableSHA256'] == ram['build']['executable_sha256'] and
         all(sha(p) == h for p, h in before.items()) and not (folder / 'stderr.log').read_text().strip(),
         'Entire actual native guest, actual compiled executable, all original sources and empty stderr')
    payload_path = ROOT / capture.NAME / 'roms/mk2ks/mk2ks.mdata'
    need(sha(payload_path) == ram['build']['payload_sha256'], 'Exact whole current graphics/script payload')
    payload = payload_path.read_bytes()
    text = gzip.open(folder / 'run.log.gz','rt',encoding='utf-8').read()
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line))
        for line in text.splitlines() if line.startswith(tag + ' ')]
    rows = parse('MK2_PAIRED_STUMBLE_VICTIM')
    accepted = handoffs(rows, ram['guest'], payload)
    live, losses, selected = map(parse, ('MK2_NAT_CAMPAIGN_LIVE','MK2_NAT_CAMPAIGN_LOSS','MK2_NAT_CAMPAIGN_SELECT_ID'))
    after = [r for r in live if int(r['frame']) > 54865]
    need(len(after) > 1000 and int(after[-1]['frame']) > 160000 and
         all(r['human'] == '18:18' and r['cpu'] == '7:7' and r['stage'] == '2' and
             r['writes'] == '0' and r['assistance'] == 'none' for r in after) and
         any(int(r['frame']) == 55345 for r in losses) and
         any(r['frame'] == '55789' and r['roster'] == '18' and r['state'] == '3' for r in selected) and
         any(int(r['frame']) > 55805 and int(r['health'].split(',')[0]) > 0 for r in after),
         'Real loss, physical paid reselect and resumed combat; over1000 native fields after old corruption point')
    need(not parse('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE') and not parse('MK2_MILEENA_CAMPAIGN_OVERRUN') and
         not parse('MK2_NAT_CAMPAIGN_ENDING_COMPLETED') and not parse('MK2_POSTENDING_COMPLETE'),
         'No observed decoder corruption; missing ending/join remains unaccepted')
    faults = []
    for index, row in enumerate(rows):
        for key, value in [('victim_id','17'),('owner_id','18'),('packed','0230B02D'),('mask','00FF')]:
            bad = copy.deepcopy(rows); bad[index][key] = value
            try:
                handoffs(bad, ram['guest'], payload)
            except ValueError as error:
                faults.append(dict(row=index, field=key, rejectedBy=str(error)))
            else:
                raise ValueError('False native handoff admitted')
    for index, key, value in [(0,'a0','0230B02D'),(1,'a1','00000600'),(1,'a9','FF0216C0'),
                              (2,'pose','FEB21730'),(2,'actor',rows[2]['owner_actor'])]:
        bad = copy.deepcopy(rows); bad[index][key] = value
        try:
            handoffs(bad, ram['guest'], payload)
        except ValueError as error:
            faults.append(dict(row=index, field=key, rejectedBy=str(error)))
        else:
            raise ValueError('Original wrong animation/pose/actor accepted')
    for index in range(9):
        bad = copy.deepcopy(rows); bad.pop(index)
        try:
            handoffs(bad, ram['guest'], payload)
        except ValueError as error:
            faults.append(dict(row=index, field='missing', rejectedBy=str(error)))
        else:
            raise ValueError('Missing original handoff field admitted')
    raw, images = ram['scope']['RAM_RAW'], ram['scope']['RAM_IMAGES']
    expected = ['campaign_selection_1_146.png', *['paired_stumble_victim_age'+str(age)+'.png' for age in (1,4,12,48)]]
    need(list(raw) == list(images) == expected and len(carrier['rgbFrames']) == 5 and server.server_port == 57808,
         'Exactly five original individually inspected native rasters, no new image files')
    for name, record in zip(expected, carrier['rgbFrames']):
        need(record['pixels'] is raw[name] and len(raw[name]) == 406400 and
             hashlib.sha256(raw[name]).hexdigest().upper() == record['header']['sha256'] and
             record['header'] in [dict(r,width='400',height='254') for r in metadata['actualScenes']],
             'Original host/native raster digests and zero-copy alias binding')
    OUT.mkdir()
    with gzip.open(OUT / 'original_executed_host_and_controllers.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=ram['executedHost'],
                       controllers={str(ROOT/n):(ROOT/n).read_text() for n in capture.CONTROLLERS}), stream)
    pins = dict(before)
    for path in [Path(__file__), *folder.rglob('*'), *capture.SOURCE.rglob('*'), *capture.INIT.rglob('*'),
                 OUT / 'original_executed_host_and_controllers.json.gz']:
        if path.is_file(): pins[str(path.resolve())] = sha(path)
    source = json.loads((capture.SOURCE / 'report.json').read_text())
    report = dict(passed=True, finiteNativeSonyaRaidenHandoffAccepted=True,
        originalCampaignTransportPassed=False, originalLosingPolicyFailurePreserved=True,
        fullTowerAccepted=False, endingAccepted=False, freshJoinAccepted=False,
        exactNativeGame=GAME, exactRAMParent=PARENT, exactReviewPort=server.server_port,
        actualNativeExit=terminal['nativeExit'], nativeHandoffs=accepted, completeNativeHandoffRows=rows,
        observedLaterNativeFields=len(after), lastObservedNativeField=after[-1],
        observedGlobalCacheCorruptionRows=0, semanticFaultsRejected=faults,
        individuallyViewedOriginalRasters=[r['header'] for r in carrier['rgbFrames']],
        visualObservations=['True Sonya own reaction body, not Liu or a descriptor artifact.',
          'Native Raiden lift/electrocution coloration and particles visible in the original reaction frames.',
          'No selection portraits/poses cover the viewed combat frames; first reaction includes the native floor shadow.',
          'Locked selection uses dedicated top-row portrait and actual Sonya body; full UI regressions remain separate.'],
        currentGuestProof=proof, inputHashes=pins,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
        KanoVictimRuntimeAccepted=False, allStockFinishersAccepted=False, audioAccepted=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,
        fullPortAcceptance=False,goalStatus='active',
        nextAction='Retire the original RAM; use ordinary improved Raiden tactics on the same repaired private candidate. No additional emulator build required.')
    (OUT / 'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(finiteNativeSonyaRaidenHandoffAccepted=True,actualHandoffs=len(accepted),
        semanticFaultsRejected=len(faults),laterNativeFields=len(after),viewedNativeRasters=5,
        fullTowerAccepted=False,originalCampaignTransportPassed=False)),flush=True)
