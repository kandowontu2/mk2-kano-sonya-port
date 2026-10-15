"""Current native table/delta inventory, not new runtime or full-port acceptance.

Reconstruct the whole guest/payload in RAM. Inspect the actual compiled source
graph, not the restored user's checkout. Historical report bindings remain
historical; unchanged tables alone never promote their gameplay/visual results.
"""
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path

import verify_current_cpu_square_v3280 as current

ROOT = current.ROOT
OUT = ROOT / 'audit_v3591_current_native_feature_coverage'
PREVIOUS = ROOT / 'audit_v3583_current_friendship_visible_full_scope_checkpoint/checkpoint.json'
need, sha = current.need, current.assembly.sha
NAME = current.current.CANDIDATE


def digest(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def addr(at):
    return 0xff800000 + at * 8


def at(address):
    return (address - 0xff800000) // 8


def u32(raw, offset):
    return struct.unpack_from('<I', raw, offset)[0]


def delta_contract(guest, old, payload, old_payload, ranges):
    need(len(guest) == len(old) == 0x100000 and len(payload) == len(old_payload) == 0x200000,
         'Whole native guest and payload lengths')
    changes = [i for i, (a, b) in enumerate(zip(old, guest)) if a != b]
    need(changes and all(any(lo <= i < hi for lo, hi in ranges) for i in changes),
         'Only independently assembled palette/router guest ranges differ from1836')
    allowed = {current.morph.FRAMES + index * 20 + field
               for index in range(12) for field in range(8, 14)}
    asset_changes = [i for i, (a, b) in enumerate(zip(old_payload, payload)) if a != b]
    need(asset_changes and set(asset_changes) <= allowed,
         'Only twelve source/format morph descriptors differ from1836 payload')
    return changes, asset_changes


def table_contract(raw, original, name, offset, rows, stride, original_address,
                   consumers=(), stock_rows=17, additions=None):
    start = at(original_address)
    need(raw[offset:offset + stock_rows * stride] ==
         original[start:start + stock_rows * stride], name + ': exact original rows')
    for consumer in consumers:
        need(u32(raw, at(consumer)) == addr(offset), name + ': actual native operand')
    if additions is not None:
        actual = [u32(raw, offset + i * stride) for i in range(stock_rows, rows)]
        need(actual == additions, name + ': explicit correctly typed appended rows')
    return dict(name=name, storage='guest', byteOffset=offset,
                nativeAddress=f'{addr(offset):08X}', rows=rows, strideBytes=stride,
                preservedOriginalRows=stock_rows,
                originalTableAddress=f'{original_address:08X}',
                nativeConsumers=[f'{c:08X}' for c in consumers],
                appendedRowsHex=raw[offset + stock_rows * stride:offset + rows * stride].hex().upper(),
                sha256=digest(raw[offset:offset + rows * stride]))


def run():
    need(not OUT.exists(), 'Fresh immutable small coverage inventory')
    state = json.loads(PREVIOUS.read_text())
    need(state['goalStatus'] == 'active' and len(state['remaining']) == 5 and
         not state['fullPortAcceptance'], 'Preserve unfinished complete objective')
    pins = {}

    def pin(path):
        path = Path(path).resolve()
        pins[str(path)] = sha(path)
        return path

    guest, old, payload, ends, ranges = current.expected_current()
    old_payload_path = pin(ROOT / 'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata')
    old_payload = old_payload_path.read_bytes()
    changes, asset_changes = delta_contract(guest, old, payload, old_payload, ranges)
    case = pin(ROOT / 'audit_v3580_current_sonya_friendship_visible_p2/guest_maincpu.bin')
    need(case.read_bytes() == guest, 'Actual current whole initialized guest equals independent assembly')
    playable = ROOT / NAME
    need(sha(pin(playable / 'mkport_candidate.exe')) == current.current.EXE and
         pin(playable / 'roms/mk2ks/mk2ks.mdata').read_bytes() == payload,
         'Existing actual current playable pair; no new copies')
    build = json.loads(pin(playable / 'build-info.json').read_text(encoding='utf-8-sig'))
    need(build['metadata_only_source_rebuild'] and build['prior_candidate'] ==
         'diagnostic_v2753_native_friendship_palette', 'Actual build declaration')
    machine_rel = 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    machine = pin(playable / machine_rel)
    prior_machine = pin(ROOT / 'diagnostic_v2753_native_friendship_palette' / machine_rel)
    need(machine.read_bytes() == prior_machine.read_bytes() and
         sha(machine) == current.assembly.SOURCE_SHA, 'Entire compiled machine unchanged from2753')
    current.assembly.source_check()
    driver_rel = 'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    driver = pin(playable / driver_rel)
    previous_driver = pin(ROOT / 'diagnostic_v2753_native_friendship_palette' / driver_rel)
    before = 'CRC(4a606b51) SHA1(36a54a06e295ea08f1ce9bda9bfbce6353731ca9)'
    after = 'CRC(a65205cf) SHA1(b8f9602b0c1a620df3f7e13bd7f659185cc40afa)'
    text = previous_driver.read_text()
    need(text.count(before) == 1 and driver.read_text() == text.replace(before, after),
         'Entire driver differs only in payload metadata, not CPU/scanner changes')
    prior_build = json.loads(pin(ROOT / 'diagnostic_v2753_native_friendship_palette/build-info.json').read_text(encoding='utf-8-sig'))
    compiled = []
    for relative in ('src/devices/cpu/tms34010/tms34010.cpp',
                     'src/mame/midway/midtunit_v.cpp'):
        suffix = '/input_sources/mame-mkp/' + relative
        matches = [(Path(p), h) for p, h in build['input_hashes'].items()
                   if str(p).replace('\\', '/').endswith(suffix)]
        need(matches and len({h for _, h in matches}) == 1, 'Unambiguous actual compiled source ' + relative)
        selected, wanted = min(matches, key=lambda item: len(str(item[0])))
        pin(selected)
        need(sha(selected) == wanted, 'Actual selected compiled source digest')
        prior_matches = [(Path(p), h) for p, h in prior_build['input_hashes'].items()
                         if str(p).replace('\\', '/').endswith(suffix)]
        need(prior_matches and len({h for _, h in prior_matches}) == 1,
             'Resolve prior actual compiled graph, not an invented direct path ' + relative)
        prior, prior_wanted = min(prior_matches, key=lambda item: len(str(item[0])))
        pin(prior)
        need(sha(prior) == prior_wanted and wanted == prior_wanted and selected.read_bytes() == prior.read_bytes(),
             'Whole CPU/renderer source unchanged ' + relative)
        compiled.append(dict(file=relative, selected=str(selected), sha256=wanted, identicalTo2753=True))
    for relative in ('src/devices/cpu/tms34010/34010gfx.hxx',
                     'src/devices/cpu/tms34010/34010ops.hxx'):
        selected = pin(playable / 'input_sources/mame-mkp' / relative)
        wanted = build['input_hashes'][str(selected)]
        need(sha(selected) == wanted, 'Actual current compiled included header digest')
        compiled.append(dict(file=relative, selected=str(selected), sha256=wanted,
                             exactCurrentCompileBinding=True, prior2753DirectHeaderSnapshotAvailable=False,
                             directByteComparisonTo2753Claimed=False))
    original = pin(ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    tables = []

    def table(*args, **kwargs):
        value = table_contract(guest, original, *args, **kwargs)
        lo, size = value['byteOffset'], value['rows'] * value['strideBytes']
        need(guest[lo:lo + size] == old[lo:lo + size], value['name'] + ': byte-identical to1836')
        value['byteIdenticalTo1836'] = True
        tables.append(value)

    table('P1 lifebar name', 0xfdc00, 19, 8, 0xff806480, (0xff805a70,))
    table('P2 lifebar name', 0xfdd00, 19, 8, 0xff8068c0, (0xff805bf0,))
    table('winner name', 0xfdf00, 19, 4, 0xff822280, (0xff829680,))
    table('fighter damage callback', 0xfe100, 19, 4, 0xff8367b0,
          (0xff836750,), additions=[0, 0])
    table('fighter AI decision callback', 0xf4400, 19, 4, 0xff9b1db0,
          (0xff9b1d60,), additions=[0xff9b20d0] * 2)
    table('fighter AI round callback', 0xf4500, 19, 4, 0xff9b2210,
          (0xff9b21c0,), additions=[0xff9b91b0] * 2)
    table('AI special ACTION callback (not fighter ID)', 0xf4800, 24, 4, 0xff9b76d0,
          (0xff9b7680,), additions=[0xff9b91b0] * 7)
    table('AI special ACTION dispatch (not fighter ID)', 0xf4480, 24, 4, 0xff8a5960,
          (0xff8a5920,), stock_rows=22, additions=[addr(0xf7800), addr(0xf7840)])
    table('Babality direction commands', 0xf97a0, 19, 4, 0xff87e3a0,
          (0xff87e250,), additions=[addr(0xf97f0), addr(0xf9810)])
    table('Friendship commands', 0xf98a0, 19, 4, 0xff880a70,
          (0xff8808a0,), additions=[addr(0xf9940), addr(0xf9960)])
    table('Friendship actions', 0xf98f0, 19, 4, 0xff880d90,
          (0xff880d40,), additions=[addr(0xf9a00), addr(0xf9c00)])
    table('Reptile victim position', 0xfa800, 19, 8, 0xff8c9900, (0xff8c8a70,))
    table('Jax head-clap victim position', 0xfb600, 19, 4, 0xff8c7ff0, (0xff8c7b50,))
    for name, offset, source, consumer in (
        ('Kitana inflation victim sequence', 0xfac40, 0xff9ed0f0, 0xff9ec840),
        ('Kitana inflation first palette', 0xfac90, 0xff9eca40, 0xff9ec8b0),
        ('Kitana inflation second palette', 0xface0, 0xff9ecc30, 0xff9ecbd0),
        ('Kung Lao vertical-split victim', 0xfbf40, 0xff8cf110, 0xff8cea70)):
        table(name, offset, 19, 4, source, (consumer,))
    pit_start = at(0xff85e6b0)
    need(payload[0x130100:0x130100 + 17 * 4] == original[pit_start:pit_start + 17 * 4] and
         payload[0x130100:0x130100 + 19 * 4] == old_payload[0x130100:0x130100 + 19 * 4] and
         all(u32(guest, at(c)) == 0xff180800 for c in (0xff85c330, 0xff85c4a0)),
         'Pit victim sequence is a19row payload table, not a guest offset or12row extension')
    tables.append(dict(name='Pit victim fall/impact', storage='payload', byteOffset=0x130100,
                       nativeAddress='FF180800', rows=19, strideBytes=4,
                       preservedOriginalRows=17, byteIdenticalTo1836=True,
                       sha256=digest(payload[0x130100:0x130100 + 76])))
    commands = []
    for name, offset, words in (
        ('Kano stage U,U,B+LK', 0xf5400, (0x38,7,5,5,0,0,0,8,5,5,0,0,0)),
        ('Sonya stage F,F,D+HP', 0xf5420, (0x38,6,8,8,0,0,0,6,7,7,0,0,0)),
        ('Kano skeleton B,D,F+HK', 0xf54c0, (0x38,8,6,7,0,0,0,7,6,8,0,0,0)),
        ('Sonya kiss B,F,D,D+LP', 0xf54e0, (0x38,6,6,8,7,0,0,6,6,7,8,0,0))):
        need(struct.unpack_from('<13H', guest, offset) == words and
             guest[offset:offset + 26] == old[offset:offset + 26], 'Explicit native command ' + name)
        commands.append(dict(name=name, nativeAddress=f'{addr(offset):08X}', newestFirstFacingPair=list(words)))
    cpu_branches = []
    for fighter, offset, destinations in (
        ('kano', 0xf7800, (0xff600, 0xffbc0, 0xf1980)),
        ('sonya', 0xf7840, (0xff680, 0xff940, 0xf3480))):
        words = [0x09c0,0xfa,0x0d5f,0xec20,0xff80,0xc80c,
                 0x09c0,0x190,0x0d5f,0xec20,0xff80,0xc803]
        for destination in destinations:
            words.extend((0xc080, addr(destination) & 65535, addr(destination) >> 16))
        encoded = struct.pack('<' + 'H' * len(words), *words)
        need(guest[offset:offset + len(encoded)] == encoded == old[offset:offset + len(encoded)],
             'Actual final CPU variety opcode/branch targets ' + fighter)
        cpu_branches.append(dict(fighter=fighter, entry=f'{addr(offset):08X}',
                                 nativeRandomHelper='FF80EC20',
                                 branchTargets=[f'{addr(d):08X}' for d in destinations],
                                 branchNames=['knife', 'ball', 'blade'] if fighter == 'kano' else ['ring', 'square', 'bicycle'],
                                 everyBranchRuntimeAutomaticallyAccepted=False))
    # These are final event bindings AFTER all parser wrappers. In particular,
    # Sonya's individual finisher LP press is not her Friendship LP release.
    event_rows = []
    for name, table_at, fighter, parser in (
        ('Kano HP blade/knife', 0xff180, 17, 0xf1900),
        ('Kano LP choke', 0xff1d0, 17, 0xf2200),
        ('Kano HK Friendship -> skeleton', 0xff270, 17, 0xf9980),
        ('Kano LK Babality -> stage', 0xff2c0, 17, 0xf9840),
        ('Sonya HP stage -> square', 0xff180, 18, 0xf5480),
        ('Sonya LP press individual kiss', 0xff1d0, 18, 0xf5560),
        ('Sonya LP release Friendship -> leg', 0xff220, 18, 0xf99a0),
        ('Sonya HK bicycle', 0xff270, 18, 0xf3400),
        ('Sonya LK Babality', 0xff2c0, 18, 0xf9860)):
        need(u32(guest, table_at + fighter * 4) == addr(parser), 'Actual final event row ' + name)
        event_rows.append(dict(name=name, fighterID=fighter, rowOffset=table_at + fighter * 4,
                               parser=f'{addr(parser):08X}'))
    coverage = []
    selected_reports = (
        ('selection/ladder/first-match names', 'currentNativeMorphShadowUIReport', NAME,
         'both physical slots; blink/player number, stance, backdrop, teardown, own ladder icons, true ID/name shadow; not combined audio'),
        ('morph repeated/cancel/KO/reset', 'currentNativeMorphAdversityReport', NAME,
         '24 physical cases; not all morph CPU/raster/arena/audio contexts'),
        ('Square CPU hit', 'candidateUnderTestNativeSquareHitRenderEraseReport', NAME,
         'specific natural CPU hit; native phase art, shadow and erase'),
        ('Bicycle CPU hit', 'currentNativeBicycleRenderEraseReport', NAME,
         'specific natural CPU hit; native phase art, shadow and erase'),
        ('Bicycle blocked', 'currentNativeBicycleBlockedRenderEraseReport', NAME,
         'both physical slots blocked; specific native phase art/shadow/erase'),
        ('Ring CPU hit', 'current3172NativeCPURingSceneReport', NAME,
         'specific native CPU hit versus Kano; not all repeats/KO/arenas'),
        ('Ring CPU blocked mirror', 'current3172NativeCPUBlockedMirrorRingReport', NAME,
         'specific blocked Sonya mirror; not all contexts'),
        ('Knife actual boss contact', 'currentKnifeBossOwnedContactReport', NAME,
         'actual earned Shao contact/blocked/KO/retirement; not complete phase art/audio'),
        ('Kano natural campaign', 'current3172KanoNaturalCampaignReport', NAME,
         'true-ID P1 natural Kintaro/Shao clears, own ending and attract'),
        ('Sonya natural campaign', 'current3172SonyaNaturalCampaignReport', NAME,
         'true-ID P1 natural Kintaro/Shao clears, own ending and attract'),
        ('Friendship full retained audio', 'current3172FriendshipAudioReport', NAME,
         'both characters/human slots; cue tails/overlap/ownership/cleanup'),
        ('Friendship full visible sequence', 'current3172FriendshipVisibleSceneReport', NAME,
         '6400visible fields; three reused captures explicitly lack standalone exit-code metadata; no hidden-VRAM promotion'))
    for feature, key, candidate, scope in selected_reports:
        path = pin(state[key]); report = json.loads(path.read_text())
        need(report['passed'] and report.get('candidate', candidate) == candidate, 'Actual accepted bounded report ' + feature)
        coverage.append(dict(feature=feature, report=str(path), build=candidate,
                             status='current-bounded-runtime', scope=scope,
                             historicalUnderlyingGraphRevalidatedThisTurn=False))
    for feature, path in (
        ('Tomb representative scenes', 'audit_v2080_current_kano_p1_tomb_matrix_checked/report.json'),
        ('Pit representative full movie', 'audit_v2100_current_kano_p1_pit_movie_checked/report.json')):
        report_path = pin(ROOT / path); report = json.loads(report_path.read_text())
        need(report['passed'] and report['candidate'] == 'diagnostic_v1836_ball_register_boundary',
             'Do not mislabel older stage runtime')
        coverage.append(dict(feature=feature, report=str(report_path), build=report['candidate'],
                             status='older-bounded-runtime/current-table-invariant-only',
                             scope=report['scope'], currentRuntimeAutomaticallyPromoted=False,
                             historicalUnderlyingGraphRevalidatedThisTurn=False))
    faults = []
    for label, kind, location in (('unrelated guest opcode', 'guest', 0x100),
                                   ('unrelated payload pixel', 'payload', 0x134000),
                                   ('own damage callback', 'table', 0xfe100 + 17 * 4)):
        altered = bytearray(guest if kind != 'payload' else payload)
        altered[location] ^= 1
        try:
            if kind == 'table':
                table_contract(altered, original, 'damage fault', 0xfe100, 19, 4,
                               0xff8367b0, (0xff836750,), additions=[0, 0])
            else:
                delta_contract(altered if kind == 'guest' else guest, old,
                               altered if kind == 'payload' else payload, old_payload, ranges)
        except ValueError as error:
            faults.append(dict(label=label, byteOffset=location, before=(guest if kind != 'payload' else payload)[location],
                               after=altered[location], rejectedBy=str(error)))
        else:
            raise ValueError('Qualified inventory counterexample accepted: ' + label)
    pin(PREVIOUS)
    pin(ROOT / 'tools/build_native_morph_shadow_v3171.ps1')
    pin(ROOT / 'mk3/mk3-maincpu.bin')
    for module in tuple(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(ROOT / 'tools'):
            pin(filename)
    rejected_tool = pin(ROOT / 'tools/map_current_native_feature_coverage_v3584.py')
    rejected_table_tool = pin(ROOT / 'tools/map_current_native_feature_coverage_v3586.py')
    pin(ROOT / 'tools/map_current_native_feature_coverage_v3588.py')
    pin(ROOT / 'audit_v3589_current_native_feature_coverage/report.json')
    pin(__file__)
    for file, wanted in pins.items():
        need(sha(file) == wanted, 'Relevant actual inputs unchanged')
    return dict(passed=True, candidate=NAME, wholeCurrentGuestIndependentlyReconstructed=True,
                wholeCurrentPayloadIndependentlyReconstructed=True,
                guestSHA256=digest(guest), payloadSHA256=digest(payload),
                compiledMachineAndCPURendererUnchangedFrom2753=True,
                completeIncludedHeaderGraphDirectlyComparedTo2753=False,
                driverDeltaOnlyPayloadCRCAndSHA1=True, compiledSourceBindings=compiled,
                guestDeltaFrom1836=dict(changedBytes=len(changes), allowedByteRanges=ranges, assemblyEnds=ends,
                    sharedGlobalEntryHooks=['FF80CF60 palette allocator', 'FF83F060 sprite-pool reset'],
                    paletteMatch='FECDF710 exact request, NOT taskID1320',
                    retirementMatch='FE9D2610..FE9D2790 pose AND FFFE2800 owned palette source AND positive reference count',
                    nonmatch='original status/registers restored and original stolen prologues/tails retained',
                    universalRuntimePassThroughProven=False),
                payloadDeltaFrom1836=dict(changedBytes=len(asset_changes), descriptors=12,
                    descriptorStride=20, firstDescriptor=current.morph.FRAMES,
                    changedFields='original compressed source pointer and format only; fields8..13',
                    allOtherPayloadBytesUnchanged=True),
                tables=tables, explicitOwnCommands=commands, finalPhysicalEventBindings=event_rows,
                actualFinalCPUVarietyBranches=cpu_branches,
                finisherSetInventoryExhaustive=False,
                dedicatedIndividualCommandTuplesObservedPerAddedFighter=1,
                secondIndividualFatalityRequirementInferred=False,
                coverage=coverage, actualQualifiedInventoryFaults=faults,
                rejectedPriorInventoryAttempt=dict(tool=str(rejected_tool), terminalExitCode=1,
                    error='FileNotFoundError: invented direct2753 34010gfx.hxx path; no inventory report produced',
                    accepted=False, correction='resolve exact original compiled source graph from both build manifests'),
                rejectedPriorTableInventoryAttempt=dict(tool=str(rejected_table_tool), terminalExitCode=1,
                    error='ValueError: AI special ACTION dispatch appended rows do not equal early initialization addresses',
                    accepted=False, correction='inventory final appended action rows without assuming early initialization values'),
                newRuntimeCaptures=0, newExecutableROMWAVPixelImageCopies=0,
                gameOrPublicBytesChanged=False, fullPortAcceptance=False,
                nextPriority='Current shared palette/reset pass-through in a representative non-Friendship full stage scene. Then consolidate explicit remaining branch/move/victim gates and combined current UI/audio release regression; do not rerun completed natural P1 endings or Friendship sequences.',
                remainingOriginalGroups=state['remaining'], inputHashes=pins)


if __name__ == '__main__':
    report = run()
    OUT.mkdir()
    path = OUT / 'report.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    before = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == before, 'Lossless compact small coverage report')
    print(json.dumps(dict(saved=str(path), passed=report['passed'], nativeTables=len(report['tables']),
                         boundedFeatureRows=len(report['coverage']), guestDeltaBytes=report['guestDeltaFrom1836']['changedBytes'],
                         payloadDeltaBytes=report['payloadDeltaFrom1836']['changedBytes'],
                         newRuntimeOrPlayableCopies=0, fullPortAcceptance=False), indent=2))
