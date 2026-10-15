"""One real Kano native handoff,20 actual faults; failed full rejoin preserved.

No three-repeat, full victim/finisher/audio/campaign/port acceptance is inferred.
All original rows/images are retained at their actual finite scope and retired.
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
FOLDER = ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_ram'
OUT = ROOT / 'audit_native_kano_raiden_paired_victim_notification_checked'


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def once(source, before, after):
    need(source.count(before) == 1, 'Entire original handoff, only exact observed count/field/character changes')
    return source.replace(before, after, 1)


def qualify_and_retire(ram, viewed_frames):
    need(os.getpid() == 31668 and not OUT.exists() and not census.census(),
         'Same original normal-terminal native/RAM capture, fresh outcome')
    metadata = json.loads((FOLDER / 'result.json').read_text())
    identity = json.loads((FOLDER / 'native_identity.json').read_text())
    terminal = json.loads((FOLDER / 'native_terminal.json').read_text())
    guest_proof = json.loads((FOLDER / 'guest_memory_proof.json').read_text())
    need(metadata == ram['capture']['result'] and metadata['passed'] and terminal['nativeExit'] == 0 and
         metadata['nativeExit'] == 0 and identity == terminal['identity'] and identity['ProcessId'] == 12936 and
         identity['ParentProcessId'] == 31668 and identity['createdUnix'] == 1791701260.6372452 and
         not (FOLDER / 'stderr.log').read_text() and not metadata['nativeCacheOverrunObserved'] and
         not metadata['actualPairedCacheOverrunObserved'] and not metadata['fullPortAcceptance'] and
         guest_proof['everyActualByteComparedInRAM'] and guest_proof['bytes'] == 1048576 and
         hashlib.sha256(ram['guest']).hexdigest().upper() == guest_proof['sha256'] == metadata['guestSHA256'],
         'Actual current whole guest, exact native identity, normal terminal and no decoder corruption')
    text = gzip.open(FOLDER / 'run.log.gz', 'rt', encoding='utf-8').read()
    need(text == ram['capture']['text'] and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation', text, re.I),
         'Entire original native chronology and no ignored runtime errors')
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in text.splitlines()
                         if line.startswith(tag + ' ')]
    rows = parse('MK2_PAIRED_STUMBLE_VICTIM')
    source = inspect.getsource(original.handoffs)
    for before, after in (
        ("len(rows) == 9", "len(rows) == 3"),
        ("All three original native handoffs retained, not a filtered subset", "Entire one actually observed native handoff, all three rows"),
        ("len(grouped) == 3 and min(grouped) == 54865", "len(grouped) == 1 and min(grouped) == 37113"),
        ("Exact previously corrupting native callback and two later repeats", "Exact actual Kano native callback; no repeated-handoff acceptance"),
        ("+ 18 * 4", "+ 17 * 4"),
        ("root == 0xff020000 and group == 0xff031a80", "root == 0xff000000 and group == 0xff0118c0"),
        ("Actual own Sonya main35 fourth composite", "Actual own Kano main35 fourth composite"),
        ("row['victim_id'] == '18'", "row['victim_id'] == '17'")):
        source = once(source, before, after)
    namespace = dict(vars(original))
    exec(compile(source, __file__ + '::entire_original_single_actual_Kano_handoff', 'exec'), namespace)
    gate = namespace['handoffs']
    payload_path = ROOT / metadata['candidate'] / 'roms/mk2ks/mk2ks.mdata'
    need(sha(payload_path) == ram['build']['payload_sha256'], 'Full actual unchanged graphics/script payload')
    payload = payload_path.read_bytes()
    accepted = gate(rows, ram['guest'], payload)
    faults = []

    def reject(bad, description):
        try:
            gate(bad, ram['guest'], payload)
        except ValueError as error:
            faults.append(dict(fault=description, rejectedBy=str(error)))
        else:
            raise ValueError('False actual Kano handoff admitted: ' + description)

    for index in range(3):
        for key, value in (('victim_id', '18'), ('owner_id', '17'), ('packed', '0230B02D'), ('mask', '00FF')):
            bad = copy.deepcopy(rows)
            bad[index][key] = value
            reject(bad, f'row{index} {key}')
    for index, key, value in ((0, 'a0', '0230B02D'), (1, 'a1', '00000600'), (1, 'a9', 'FF006890'),
                              (2, 'pose', 'FEB21730'), (2, 'actor', rows[2]['owner_actor'])):
        bad = copy.deepcopy(rows)
        bad[index][key] = value
        reject(bad, f'row{index} {key}')
    for index in range(3):
        bad = copy.deepcopy(rows)
        bad.pop(index)
        reject(bad, f'missing row{index}')
    counters, stops = parse('MK2_PAIRED_STUMBLE_RESULT'), parse('MK2_KANO_RAIDEN_VICTIM_NO_HANDOFF')
    losses = [row for row in parse('MK2_NAT_CAMPAIGN_LOSS') if row['stage'] == '2']
    need(len(faults) == 20 and len(counters) == len(stops) == 1 and
         counters[0]['frame'] == stops[0]['frame'] == '42030' and stops[0]['real_paid_losses'] == '8' and
         all(counters[0][key] == '1' for key in ('packed_inputs', 'after_lookups', 'after_renders')) and
         len(losses) == 8 and not any(parse(tag) for tag in ('MK2_KANO_RAIDEN_VICTIM_STATE',
            'MK2_KANO_RAIDEN_VICTIM_READMITTED', 'MK2_KANO_RAIDEN_VICTIM_COMPLETE', 'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE')),
         'Actual native callback exists but whole post-notification/rejoin tracker failed; preserve contradictory label')
    names = ['campaign_selection_1_146.png', *['paired_stumble_victim_age' + str(age) + '.png' for age in (1, 4, 12, 48)]]
    frames = [1070, 37114, 37117, 37125, 37161]
    images, raw = ram['scope']['RAM_IMAGES'], ram['scope']['RAM_RAW']
    need(list(images) == list(raw) == names and viewed_frames == frames and set(ram['review_images']) == set(frames),
         'All five original held rasters individually inspected, no target screen invented')
    views = []
    for frame, name in zip(frames, names, strict=True):
        rgb = ram['review_images'][frame]
        need(rgb.shape == (254, 400, 3) and images[name].tobytes() == rgb.tobytes() and len(raw[name]) == 406400 and
             any(row['filename'] == name and row['sha256'] == hashlib.sha256(raw[name]).hexdigest().upper()
                 for row in metadata['actualScenes']), 'Original native BGRX and reviewed decoded RGB bound')
        views.append(dict(frame=frame, filename=name, rawSHA256=hashlib.sha256(raw[name]).hexdigest().upper(),
                          rgbSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(), individuallyViewed=True))
    source_guard = json.loads((ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_source/report.json').read_text())
    pins = dict(metadata['inputHashes'])
    pins.update(source_guard['inputHashes'])
    for path in (Path(__file__).resolve(), Path(original.__file__), ROOT / 'tools/native_ram_raster_review.py',
                 payload_path, *(path for folder in (FOLDER, ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_source',
                    ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_initializer',
                    ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_previous_initializer')
                                for path in folder.rglob('*') if path.is_file())):
        pins[str(path.resolve())] = sha(path)
    need(all(sha(path) == digest for path, digest in pins.items()), 'Whole exact native/source/earlier-failure inputs frozen')
    need(not any(path.suffix.lower() in ('.png', '.wav', '.bin', '.exe', '.zip')
                 for path in FOLDER.rglob('*') if path.is_file()), 'No raw native media/ROM/build copies')
    OUT.mkdir()
    failed = dict(passed=False, originalIntendedKanoVictimAndPaidRejoinAccepted=False,
                  actualTerminalNativeIdentity=identity, actualNativeHandoffRows=rows, actualPairedCounters=counters[0],
                  actualIncorrectNoHandoffLabel=stops[0], actualPostStateFields=0, actualRealRaidenLosses=losses,
                  diagnosis='Source inference: pending snapshot branch executed with the native callback, but chunk signal assignment is not visible to the rawget(_G) consumer; no post-state/admission/completion rows.',
                  normalNativeTerminal=True, nativeCacheCorruptionObserved=False, fullPortAcceptance=False,
                  publicPlayableChanged=False, inputHashes=pins, goalStatus='active')
    failed_path = OUT / 'failed_full_notification_trial.json'
    failed_path.write_text(json.dumps(failed, indent=2) + '\n')
    pins[str(failed_path)] = sha(failed_path)
    port = ram['server'].server_port
    ram['server'].shutdown()
    ram['server'].server_close()
    images.clear()
    raw.clear()
    ram['review_images'].clear()
    ram.clear()
    proof = dict(passed=True, finiteSingleKanoRaidenNativeHandoffAccepted=True,
                 originalIntendedPaidRejoinTrialAccepted=False, failedFullNotificationTrialRetained=True,
                 nativeHandoffs=accepted, completeOriginalHandoffRows=rows, actualSemanticFaultsRejected=faults,
                 individuallyReviewedNativeRasters=views,
                 actualVisualObservations='Dedicated numbered Kano selection and own body; true Kano reaction lifts in front of Raiden, turns native blue and uses native particles. No Liu proxy, invalid descriptor body or selection art covering viewed combat. Visible initial native floor shadow; wider shadow/audio/cinematic clearing remains unverified.',
                 repeatedHandoffsAccepted=False, fullVictimCleanupAccepted=False, fullAudioAccepted=False,
                 fullTowerAccepted=False, allStockFinishersAccepted=False, fullPortAcceptance=False,
                 originalNaturalIntegrationRequirements=source_guard['originalNaturalIntegrationRequirements'],
                 originalRemainingWorkGroups=source_guard['originalRemainingWorkGroups'],
                 originalRawBuffersReleased=5, originalPILBuffersReleased=5, reviewArraysReleased=5,
                 originalCaptureRAMCleared=not ram, reviewServerClosed=True, exactReviewPort=port,
                 exactTerminalNativeIdentity=identity, inputHashes=pins,
                 newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, publicPlayableChanged=False, goalStatus='active')
    (OUT / 'single_handoff_and_failed_notification_ram_retirement.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(dict(singleNativeHandoffAccepted=True, actualFaultsRejected=20, reviewedRastersReleased=5,
                          fullOriginalPaidRejoinTrialAccepted=False, RAMCleared=not ram, output=str(OUT)), indent=2), flush=True)
    return proof
