"""Preserve exact normal-terminal eight-loss no-handoff trial; no positive proof."""
import gzip
import hashlib
import json
import os
import re
from pathlib import Path
import native_process_census_v6647 as census

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'audit_native_kano_raiden_paired_victim_ram'
OUTPUT = ROOT / 'audit_native_kano_raiden_paired_victim_checked'


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def preserve(ram, viewed_frames):
    need(os.getpid() == 3792 and not OUTPUT.exists() and not census.census(),
         'Same original terminal native/RAM trial and fresh failed-outcome preservation')
    metadata = json.loads((FOLDER / 'result.json').read_text())
    terminal = json.loads((FOLDER / 'native_terminal.json').read_text())
    identity = json.loads((FOLDER / 'native_identity.json').read_text())
    guest_proof = json.loads((FOLDER / 'guest_memory_proof.json').read_text())
    need(terminal['nativeExit'] == metadata['nativeExit'] == 0 and metadata['passed'] and
         terminal['identity'] == identity and identity['ProcessId'] == 33824 and identity['ParentProcessId'] == 3792 and
         identity['createdUnix'] == 1791700623.8304558 and not (FOLDER / 'stderr.log').read_text() and
         not metadata['nativeCacheOverrunObserved'] and not metadata['actualPairedCacheOverrunObserved'] and
         not metadata['actualNaturalTowerClearAccepted'] and not metadata['fullPortAcceptance'],
         'Normal transport terminal is not intended victim/campaign acceptance')
    text = gzip.open(FOLDER / 'run.log.gz', 'rt', encoding='utf-8').read()
    need(text == ram['capture']['text'] and metadata == ram['capture']['result'] and
         hashlib.sha256(ram['guest']).hexdigest().upper() == guest_proof['sha256'] == metadata['guestSHA256'] and
         guest_proof['everyActualByteComparedInRAM'] and guest_proof['bytes'] == 1048576,
         'Exact original entire guest and complete native chronology still held')
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in text.splitlines()
                         if line.startswith(tag + ' ')]
    losses = [row for row in parse('MK2_NAT_CAMPAIGN_LOSS') if row['stage'] == '2']
    stop, counters = parse('MK2_KANO_RAIDEN_VICTIM_NO_HANDOFF'), parse('MK2_PAIRED_STUMBLE_RESULT')
    need(len(losses) == 8 and len(stop) == len(counters) == 1 and
         stop[0]['frame'] == counters[0]['frame'] == losses[-1]['frame'] == '43357' and
         stop[0]['real_paid_losses'] == '8' and all(counters[0][key] == '0'
         for key in ('packed_inputs', 'after_lookups', 'after_renders')) and
         not any(parse(tag) for tag in ('MK2_PAIRED_STUMBLE_VICTIM', 'MK2_KANO_RAIDEN_VICTIM_STATE',
                                       'MK2_KANO_RAIDEN_VICTIM_READMITTED', 'MK2_KANO_RAIDEN_VICTIM_COMPLETE',
                                       'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE')) and
         not re.search(r'LUA ERROR|stack traceback|fatal error|access violation', text, re.I),
         'Entire actual bounded miss, zero target callbacks and no observed runtime/decoder failure')
    images, raw = ram['scope']['RAM_IMAGES'], ram['scope']['RAM_RAW']
    name = 'campaign_selection_1_146.png'
    need(list(images) == list(raw) == [name] and viewed_frames == [1070] and
         set(ram['review_images']) == {1070} and len(raw[name]) == 406400 and
         images[name].tobytes() == ram['review_images'][1070].tobytes() and
         any(row['filename'] == name and row['sha256'] == hashlib.sha256(raw[name]).hexdigest().upper()
             for row in metadata['actualScenes']),
         'Only original held dedicated Kano selection raster individually reviewed; no victim raster exists')
    pins = dict(metadata['inputHashes'])
    for path in (Path(__file__).resolve(), ROOT / 'tools/native_ram_raster_review.py',
                 *(path for folder in (FOLDER, ROOT / 'audit_native_kano_raiden_paired_victim_source',
                                       ROOT / 'audit_native_kano_raiden_paired_victim_initializer',
                                       ROOT / 'audit_native_kano_raiden_paired_victim_previous_initializer')
                   for path in folder.rglob('*') if path.is_file())):
        pins[str(path.resolve())] = sha(path)
    need(all(sha(path) == digest for path, digest in pins.items()), 'Exact frozen native/source/negative-result inputs')
    need(not any(path.suffix.lower() in ('.png', '.wav', '.bin', '.exe', '.zip')
                 for path in FOLDER.rglob('*') if path.is_file()), 'No raw/native build/media copies in failed trial')
    OUTPUT.mkdir()
    failure_path = OUTPUT / 'report.json'
    failure = dict(passed=False, intendedKanoRaidenVictimRuntimeAccepted=False,
                   reason='Eight genuine Raiden losses reached no actual paired-victim callback.',
                   normalNativeTransportTerminal=True, actualTerminalNativeIdentity=identity,
                   actualEightNativeLosses=losses, actualZeroPairedCounters=counters[0],
                   nativeExit=0, cacheCorruptionObserved=False, guestProof=guest_proof,
                   individuallyReviewedSelectionFrame=1070, victimRastersObserved=0,
                   fullPortAcceptance=False, publicPlayableChanged=False, inputHashes=pins, goalStatus='active')
    failure_path.write_text(json.dumps(failure, indent=2) + '\n')
    pins[str(failure_path)] = sha(failure_path)
    port = ram['server'].server_port
    ram['server'].shutdown()
    ram['server'].server_close()
    images.clear()
    raw.clear()
    ram['review_images'].clear()
    ram.clear()
    receipt = dict(passed=True, preservationOnly=True, originalIntendedVictimTrialAccepted=False,
                   normalNativeTransportTerminal=True, originalTrialFailureRetained=True,
                   individuallyViewedFrame=1070,
                   actualViewedSelection='Dedicated Kano top-row numbered icon and own body; no victim art was captured.',
                   originalRawBufferReleased=1, originalPILBufferReleased=1, reviewArrayReleased=1,
                   originalRAMDictionaryCleared=not ram, reviewServerClosed=True, exactReviewPort=port,
                   inputHashes=pins, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                   fullPortAcceptance=False, publicPlayableChanged=False, goalStatus='active')
    (OUTPUT / 'no_handoff_preservation_and_ram_retirement.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(preserved=True, intendedVictimTrialAccepted=False, RAMCleared=not ram,
                          originalHeldImagesReleased=1, receipt=str(OUTPUT)), indent=2), flush=True)
    return receipt
