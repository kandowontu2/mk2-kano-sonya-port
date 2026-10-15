"""Qualify the actual one Kano/Raiden callback and full ordinary paid recovery.

Full original handoff gates, every observed post field, actual native inputs,
fresh ownership/full-health admission and 500 live intervals. Thirty-three
original screenshots were individually reviewed, not invented from pointers.
This is not full audio, all-victims, all-finishers or whole-port acceptance.
"""
import copy
import gzip
import hashlib
import inspect
import json
import os
import re
from pathlib import Path
import native_process_census_v6647 as census
import verify_native_paired_stumble_handoff as original

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'audit_native_kano_raiden_paired_victim_shared_ram'
OUT = ROOT / 'audit_native_kano_raiden_shared_rejoin_checked'
FRAMES = [1070, 37114, 37117, 37125, 37161, 37200, 37287, 37320, 37440,
          37560, 37585, 37593, 37680, 37800, 37906, 37907, 37920, 37965,
          38040, 38081, 38111, 38160, 38280, 38359, 38360, 38400, 38456,
          38457, 38520, 38640, 38760, 38880, 38956]


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def once(source, before, after):
    need(source.count(before) == 1, 'Whole original handoff: exact observed boundary')
    return source.replace(before, after, 1)


def parse(text, tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line))
            for line in text.splitlines() if line.startswith(tag + ' ')]


def recovery(states, events):
    need([int(row['frame']) for row in states] == list(range(37114, 38957)),
         'All1843 consecutive original post-callback native fields, not sparse live samples')
    need(all(row['callback'] == '37113' and row['stage'] == '2' and
             row['writes'] == '0' and row['assistance'] == 'none' for row in states),
         'Every actual post field binds the native callback/stage and no assistance')
    rows = {int(row['frame']): row for row in states}
    phases = [(int(row['frame']), row['mode'], row['state1'], row['state2'])
              for i, row in enumerate(states) if not i or
              (row['mode'], row['state1'], row['state2']) !=
              (states[i-1]['mode'], states[i-1]['state1'], states[i-1]['state2'])]
    need(phases == [(37114, '2', '1', '0'), (37287, '5', '1', '0'),
                    (37585, '3', '2', '0'), (37906, '4', '3', '0'),
                    (38081, '4', '4', '0'), (38111, '13', '1', '0'),
                    (38143, '7', '1', '0'), (38359, '6', '1', '0'),
                    (38360, '7', '1', '0'), (38456, '2', '1', '0')],
         'Entire actual KO/continue/selection/lock/ladder/arena/fight phase order')
    need(rows[37114]['actor1'] == '01030EA0' and rows[37114]['id1'] == '17' and
         rows[37114]['hp1'] == '0' and rows[37114]['hp2'] == '161' and
         all(rows[37593][key] == '00000000' for key in ('actor1', 'actor2')) and
         rows[37920]['id1'] == rows[37920]['roster1'] == '1' and
         rows[38040]['id1'] == rows[38040]['roster1'] == '17' and
         all(rows[38143][key] == '00000000' for key in ('actor1', 'actor2')),
         'True old Kano KO, retired actors, actual initialized cursor, selected Kano and native ladder teardown')
    event = lambda name: events[name]
    need(len(event('loss')) == 1 and event('loss')[0]['frame'] == '37593' and
         event('loss')[0]['stage'] == '2' and event('loss')[0]['number'] == '10' and
         len(event('select')) == 1 and event('select')[0]['frame'] == '37907' and
         event('select')[0]['continue'] == '37593' and event('select')[0]['initial'] == '1' and
         event('select')[0]['target'] == '17' and event('select')[0]['number'] == '11' and
         event('select')[0]['path'] == 'Left' and
         len(event('route')) == 1 and event('route')[0]['frame'] == '37963' and
         event('route')[0]['roster'] == '1' and event('route')[0]['path'] == 'Left',
         'Actual earned loss and paid selection, settled initialized cursor route, never assigned roster')
    for button, frames in [('Coin', list(range(37613, 37618)) + list(range(37863, 37868))),
                           ('Start', list(range(37903, 37906))),
                           ('Left', list(range(37963, 37967))),
                           ('High_Punch', list(range(38055, 38063)))]:
        actual = [int(row['frame']) for row in event('input')
                  if row['button'] == button and int(row['frame']) < 38456]
        need(actual == frames, 'Entire actual physical paid/cursor/confirmation input ' + button)
    need([row['frame'] for row in event('select_id')] == ['38037', '38053'] and
         all(row['roster'] == '17' and row['state'] == '3' and row['number'] == '11'
             for row in event('select_id')) and
         len(event('select_exit')) == 1 and event('select_exit')[0]['frame'] == '38111' and
         len(event('fight')) == 1 and event('fight')[0]['frame'] == '38456' and
         event('fight')[0]['human'] == '17:17' and event('fight')[0]['cpu'] == '7:7' and
         event('fight')[0]['actors'] == '01033C00,01033E10' and event('fight')[0]['selection'] == '11',
         'Physical confirmation -> own native ladder -> actual fresh Kano/Raiden fight')
    need(len(event('admit')) == len(event('complete')) == 1 and
         event('admit')[0]['frame'] == '38456' and event('admit')[0]['callback'] == '37113' and
         event('admit')[0]['ids'] == '17,7' and event('admit')[0]['hp'] == '161,161' and
         event('complete')[0]['frame'] == '38956' and event('complete')[0]['admitted'] == '38456' and
         event('complete')[0]['alive_fields'] == '500' and event('complete')[0]['health'] == '63,73',
         'Original full-health admission and whole500-field completion, no shortened endpoint')
    live = states[38456 - 37114:]
    need(len(live) == 501 and live[0]['hp1'] == live[0]['hp2'] == '161' and
         all(row['mode'] == '2' and row['state1'] == '1' and row['state2'] == '0' and
             row['id1'] == row['roster1'] == '17' and row['id2'] == row['roster2'] == '7' and
             row['actor1'] == row['owner1'] == '01033C00' and row['main1'] == '0106E8D0' and
             row['actor2'] == row['owner2'] == '01033E10' and row['main2'] == '0106A370' and
             row['admitted'] == ('-1' if int(row['frame']) == 38456 else '38456') and
             0 < int(row['hp1']) <= 161 and 0 < int(row['hp2']) <= 161 for row in live),
         'Every live field retains true IDs, fresh actors/Main ownership and positive native HP')
    need(len({row['x1'] for row in live}) > 20 and len({row['pose1'] for row in live}) > 10 and
         any(int(row['y1']) < int(row['floor1']) - 8 for row in live) and
         any(row['y1'] == row['floor1'] for row in live),
         'Actual movement, animation, airborne and grounded fields, not frozen ownership')
    live_inputs = [row for row in event('input') if int(row['frame']) >= 38456]
    need(len(live_inputs) == 812 and {row['button'] for row in live_inputs} ==
         {'Left', 'Right', 'Up', 'Down', 'Block', 'High_Punch', 'High_Kick'} and
         all(row['selection'] == '11' for row in live_inputs), 'Whole resumed ordinary input ledger')
    damage = event('damage')
    need(len(damage) == 8 and all(row['pc'] == 'FF836700' and
         row['at'] == ('010602F0' if row['slot'] == '1' else '01060EC0') and
         0 < int(row['after']) < int(row['before']) <= 161 for row in damage) and
         {row['slot'] for row in damage} == {'1', '2'},
         'Eight actual original native damage stores affect both fighters, no HP assistance')
    for slot in ('1', '2'):
        hp = 161
        for row in damage:
            if row['slot'] == slot:
                need(int(row['before']) == hp, 'Complete original health loss chain')
                hp = int(row['after'])
        need(int(live[-1]['hp' + slot]) == hp, 'Native completion health matches full damage ledger')
    need(len(event('special')) == 7 and all(row['move'] == 'knife' and row['id'] == row['roster'] == '17' and
         row['entry'] == 'FFFFB000' and row['at'] == 'FFFFB010' and row['pc'] == 'FFFFB020' and
         row['actor'] == row['a8'] == '01033C00' and row['main'] == row['a13'] == '0106E8D0'
         for row in event('special')), 'Seven actual own knife entries after paid recovery')
    need(all(row['writes'] == '0' and row['assistance'] == 'none'
             for group in events.values() for row in group), 'All original physical/event rows unassisted')
    return dict(consecutivePostCallbackFields=1843, liveStateSamples=501, liveIntervals=500,
                callback=37113, realLoss=37593, selectionOpen=37907, locked=38081,
                selectorTeardown=38143, fullHealthAdmission=38456, completed=38956,
                initialHP=[161, 161], finalHP=[63, 73], nativeDamageStores=damage,
                trueActorIDs=[17, 7], ordinaryInputs=812, actualOwnKnifeEntries=7,
                fullPhaseOrder=phases)


def qualify_and_retire(ram, viewed_frames):
    need(os.getpid() == 26952 and not OUT.exists() and not census.census(),
         'Same original RAM parent, normal terminal native and fresh finite proof')
    metadata = json.loads((FOLDER / 'result.json').read_text())
    identity = json.loads((FOLDER / 'native_identity.json').read_text())
    terminal = json.loads((FOLDER / 'native_terminal.json').read_text())
    guest_proof = json.loads((FOLDER / 'guest_memory_proof.json').read_text())
    need(metadata == ram['capture']['result'] and metadata['passed'] and metadata['nativeExit'] == 0 and
         terminal['nativeExit'] == 0 and terminal['identity'] == identity and
         identity['ProcessId'] == 25124 and identity['ParentProcessId'] == 26952 and
         identity['createdUnix'] == 1791702215.4636784 and
         str(FOLDER) in identity['CommandLine'] and '-nocheat' in identity['CommandLine'] and
         '-wavwrite NUL' in identity['CommandLine'] and
         sha(identity['ExecutablePath']) == metadata['executableSHA256'] == ram['build']['executable_sha256'] and
         not (FOLDER / 'stderr.log').read_text() and not metadata['nativeCacheOverrunObserved'] and
         not metadata['actualPairedCacheOverrunObserved'] and not metadata['fullPortAcceptance'] and
         guest_proof['everyActualByteComparedInRAM'] and guest_proof['bytes'] == 1048576 and
         hashlib.sha256(ram['guest']).hexdigest().upper() == guest_proof['sha256'] == metadata['guestSHA256'],
         'Exact native birth/path/parent/command, full compiled guest, no ignored native/cache failure')
    text = gzip.open(FOLDER / 'run.log.gz', 'rt', encoding='utf-8').read()
    need(text == ram['capture']['text'] and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation', text, re.I),
         'Whole original native chronology, not a truncated or filtered reconstruction')
    rows = parse(text, 'MK2_PAIRED_STUMBLE_VICTIM')
    body = inspect.getsource(original.handoffs)
    for before, after in [("len(rows) == 9", "len(rows) == 3"),
        ("len(grouped) == 3 and min(grouped) == 54865", "len(grouped) == 1 and min(grouped) == 37113"),
        ("+ 18 * 4", "+ 17 * 4"),
        ("root == 0xff020000 and group == 0xff031a80", "root == 0xff000000 and group == 0xff0118c0"),
        ("row['victim_id'] == '18'", "row['victim_id'] == '17'")]:
        body = once(body, before, after)
    namespace = dict(vars(original))
    exec(compile(body, __file__ + '::whole_original_actual_single_Kano_handoff', 'exec'), namespace)
    handoff_gate = namespace['handoffs']
    payload_path = ROOT / metadata['candidate'] / 'roms/mk2ks/mk2ks.mdata'
    need(sha(payload_path) == ram['build']['payload_sha256'], 'Whole unchanged current graphics/script payload')
    payload = payload_path.read_bytes()
    handoff = handoff_gate(rows, ram['guest'], payload)
    states = parse(text, 'MK2_KANO_RAIDEN_VICTIM_STATE')
    tags = dict(loss='LOSS', select='SELECT', route='SETTLED_ROUTE', select_id='SELECT_ID',
                select_exit='SELECT_EXIT', fight='FIGHT', input='INPUT', special='SPECIAL')
    events = {key: [row for row in parse(text, 'MK2_NAT_CAMPAIGN_' + tag)
                    if 37593 <= int(row['frame']) <= 38956] for key, tag in tags.items()}
    events['admit'] = parse(text, 'MK2_KANO_RAIDEN_VICTIM_READMITTED')
    events['complete'] = parse(text, 'MK2_KANO_RAIDEN_VICTIM_COMPLETE')
    events['damage'] = [row for row in parse(text, 'MK2_NAT_CAMPAIGN_HEALTH')
                        if int(row['frame']) >= 38456 and int(row['after']) < int(row['before'])]
    recovered = recovery(states, events)
    counters = parse(text, 'MK2_PAIRED_STUMBLE_RESULT')
    need(len(counters) == 1 and counters[0]['frame'] == '38956' and
         all(counters[0][key] == '1' for key in ('packed_inputs', 'after_lookups', 'after_renders')) and
         not any(parse(text, tag) for tag in ('MK2_KANO_RAIDEN_VICTIM_NO_HANDOFF',
           'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE', 'MK2_MILEENA_CAMPAIGN_OVERRUN',
           'MK2_NAT_CAMPAIGN_ENDING_COMPLETED')), 'Correct native terminal, finite target, no invented tower/ending')
    faults = []

    def reject(thunk, description):
        try:
            thunk()
        except ValueError as error:
            faults.append(dict(fault=description, rejectedBy=str(error)))
        else:
            raise ValueError('False recovery/handoff accepted: ' + description)

    for index in range(3):
        for key, value in [('victim_id', '18'), ('owner_id', '17'), ('packed', '0230B02D'), ('mask', '00FF')]:
            bad = copy.deepcopy(rows); bad[index][key] = value
            reject(lambda: handoff_gate(bad, ram['guest'], payload), f'handoff{index} {key}')
    for index, key, value in [(0, 'a0', '0230B02D'), (1, 'a1', '00000600'), (1, 'a9', 'FF006890'),
                              (2, 'pose', 'FEB21730'), (2, 'actor', rows[2]['owner_actor'])]:
        bad = copy.deepcopy(rows); bad[index][key] = value
        reject(lambda: handoff_gate(bad, ram['guest'], payload), f'handoff{index} {key}')
    for index in range(3):
        bad = copy.deepcopy(rows); bad.pop(index)
        reject(lambda: handoff_gate(bad, ram['guest'], payload), f'missing handoff{index}')
    for frame, key, value in [(37114, 'callback', '0'), (37593, 'actor1', '01030EA0'),
         (37920, 'roster1', '17'), (38040, 'id1', '1'), (38143, 'actor1', '01036330'),
         (38456, 'hp1', '160'), (38456, 'hp2', '160'), (38457, 'admitted', '-1'),
         (38640, 'mode', '4'), (38640, 'stage', '3'), (38640, 'state1', '3'),
         (38640, 'state2', '1'), (38640, 'id1', '1'), (38640, 'roster1', '1'),
         (38640, 'id2', '17'), (38640, 'roster2', '17'), (38640, 'owner1', '01030EA0'),
         (38640, 'owner2', '010310B0'), (38640, 'main1', '0106BF30'),
         (38640, 'hp1', '0'), (38640, 'writes', '1'), (38640, 'assistance', 'health')]:
        bad = copy.deepcopy(states); bad[frame-37114][key] = value
        reject(lambda: recovery(bad, events), f'native state{frame} {key}')
    for index in (0, 1342, len(states)-1):
        bad = copy.deepcopy(states); bad.pop(index)
        reject(lambda: recovery(bad, events), f'missing consecutive field{index}')
    for name in ('loss', 'select', 'route', 'select_id', 'select_exit', 'fight', 'admit', 'complete', 'damage', 'special'):
        bad = copy.deepcopy(events); bad[name] = []
        reject(lambda: recovery(states, bad), 'missing entire native event ' + name)
    for button in ('Coin', 'Start', 'Left', 'High_Punch', 'Block'):
        bad = copy.deepcopy(events); bad['input'] = [row for row in bad['input'] if row['button'] != button]
        reject(lambda: recovery(states, bad), 'missing actual physical ' + button)
    need(len(faults) == 60, 'All20 handoff and40 full-state/paid-input/damage/activation faults actually rejected')
    images, raw = ram['scope']['RAM_IMAGES'], ram['scope']['RAM_RAW']
    need(viewed_frames == FRAMES and list(images) == list(raw) and len(images) == 33 and
         set(ram['review_images']) == set(FRAMES), 'Every original held screenshot individually viewed')
    names = ['campaign_selection_1_146.png', *['paired_stumble_victim_age' + str(age) + '.png' for age in (1, 4, 12, 48)],
             *['kano_raiden_paired_frame' + str(frame) + '.png' for frame in FRAMES[5:]]]
    need(list(images) == names, 'Actual observed names and frames, no synthesized clearing screenshot')
    views = []
    for frame, name in zip(FRAMES, names, strict=True):
        rgb = ram['review_images'][frame]
        raw_digest = hashlib.sha256(raw[name]).hexdigest().upper()
        need(rgb.shape == (254, 400, 3) and images[name].tobytes() == rgb.tobytes() and len(raw[name]) == 406400 and
             any(row['filename'] == name and row['sha256'] == raw_digest for row in metadata['actualScenes']),
             'Individually reviewed pixels bound to original native BGRX snapshot transport')
        views.append(dict(frame=frame, filename=name, nativeBGRXSHA256=raw_digest,
                          reviewedRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(), individuallyViewed=True))
    source = json.loads((ROOT / 'audit_native_kano_raiden_paired_victim_shared_source/report.json').read_text())
    pins = dict(metadata['inputHashes']); pins.update(source['inputHashes'])
    for path in (Path(__file__).resolve(), Path(original.__file__), ROOT / 'tools/native_ram_raster_review.py', payload_path,
                 *(path for folder in (FOLDER, ROOT / 'audit_native_kano_raiden_paired_victim_shared_source',
                    ROOT / 'audit_native_kano_raiden_paired_victim_shared_initializer',
                    ROOT / 'audit_native_kano_raiden_paired_victim_shared_previous_initializer')
                   for path in folder.rglob('*') if path.is_file())):
        pins[str(path.resolve())] = sha(path)
    need(all(sha(path) == digest for path, digest in pins.items()), 'Every native/source/prior-failure input still frozen')
    need(not any(path.suffix.lower() in ('.png', '.wav', '.bin', '.exe', '.zip')
                 for path in FOLDER.rglob('*') if path.is_file()), 'No raw media or duplicate builds/ROM')
    proof = dict(passed=True, finiteSingleKanoRaidenVictimAndOrdinaryPaidRecoveryAccepted=True,
                 nativeHandoffs=handoff, entireNativeRecovery=recovered, actualFaultsRejected=faults,
                 individuallyReviewedScreens=views, exactTerminalNativeIdentity=identity,
                 snapshotEvidenceOnly=True, independentContinuousDisplayModelAccepted=False,
                 visualObservations='Native Kano electrocution/lift/blue particles and fatality; original scene persists while continue panels slide in, then clears. Initialized Liu cursor precedes actual Kano choice. Confirmed dedicated numbered Kano icon and own locked pose clear before the own ladder portrait; black transition and subsequent Portal arena show no selection artwork. Fresh own Kano body, visible floor shadow, black-shadowed name, movement/airborne/hit/recovery and both fighters taking native damage. The38360 snapshot catches native transition palette/redraw; it is not claimed to be clean stable combat. State and scanout may differ at an individual snapshot boundary.',
                 repeatedHandoffsAccepted=False, bothCharactersBothSlotsAccepted=False,
                 fullFinisherVictimMatrixAccepted=False, audioAccepted=False, allStageShadowAccepted=False,
                 fullTowerAccepted=False, allSecretMorphAccepted=False, fullPortAcceptance=False,
                 originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
                 originalRemainingWorkGroups=source['originalRemainingWorkGroups'], inputHashes=pins,
                 newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, publicPlayableChanged=False, goalStatus='active')
    OUT.mkdir()
    port = ram['server'].server_port
    ram['server'].shutdown(); ram['server'].server_close()
    images.clear(); raw.clear(); ram['review_images'].clear(); ram.clear()
    proof.update(originalRawBuffersReleased=33, originalPILBuffersReleased=33, reviewArraysReleased=33,
                 originalCaptureRAMCleared=not ram, exactClosedReviewPort=port, reviewServerClosed=True)
    (OUT / 'report.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(dict(passed=True, nativePostFields=1843, liveIntervals=500, actualFaultsRejected=60,
                          originalScreensReviewedReleased=33, RAMCleared=not ram, output=str(OUT)), indent=2), flush=True)
    return proof
