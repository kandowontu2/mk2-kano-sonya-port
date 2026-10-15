"""Qualify native hook caller preservation separately from failed visible gate."""
import json
import re
import subprocess
from pathlib import Path
import run_current_stage_palette_pixels_v3602 as stage

ROOT, need, sha = stage.ROOT, stage.need, stage.sha
OUT = ROOT / 'audit_v3609_current_tomb_native_hook_nonmatch_checked'


def run():
    need(not OUT.exists(), 'Fresh native-only proof; never relabel failed visual result')
    folder = stage.CASE
    failed = ROOT / 'audit_v3603_current_tomb_palette_pixels_checked/report.json'
    report = json.loads(failed.read_text())
    result = json.loads((folder / 'result.json').read_text())
    need(not report['passed'] and not result['passed'] and result['exit_code'] == 0 and
         result['actualVisibleFields'] == 537 and len(result['mismatches']) == 502 and
         not result['protocolErrors'], 'Preserve actual failed RGB gate/terminal native capture')
    stage.controls()
    log = (folder / 'run.log').read_text()
    old = (stage.REFERENCE / 'run.log').read_text(encoding='utf-8-sig')
    need(stage.classic(log) == stage.classic(old), 'Every original physical/controller/damage/pose/cleanup record retained')
    provenance = lambda value: [line for line in value.splitlines() if line.startswith('MK2_STAGE_PROVENANCE_')]
    need(provenance(log) == provenance(old), 'Original victim motion, native stores and genuine held random branch retained')
    state = stage.native.check_log(stage.classic(log), 'kano', 1, 1, 'positive', certified_drop_log=stage.classic(old))
    guest, _, payload, _, _ = stage.inventory.current.expected_current()
    need((folder / 'guest_maincpu.bin').read_bytes() == guest and
         (ROOT / stage.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes() == payload, 'Actual whole current guest/payload source-bound')
    entries = stage.tagged(log, 'ALLOC_ENTRY'); resumes = stage.tagged(log, 'ALLOC_RESUME')
    resets = stage.tagged(log, 'RESET_ENTRY'); restored = stage.tagged(log, 'RESET_RESUME')
    terminal = stage.tagged(log, 'RESULT')
    need(len(terminal) == 1 and len(entries) == len(resumes) == 1723 and
         len(resets) == len(restored) == 5 and terminal[0]['matching_allocations'] ==
         terminal[0]['matching_sprites'] == '0', 'Complete nonmatching allocator/reset actual observations')
    for index, (before, after) in enumerate(zip(entries, resumes), 1):
        need(before['serial'] == str(index) and before['request'] == after['request'] and
             before['request'] != 'FECDF710', 'Actual unchanged nonmatching palette request')
        stage.equal_state(before, after)
    for index, (before, after) in enumerate(zip(resets, restored), 1):
        need(before['serial'] == str(index) and before['eligible'] == '0', 'Actual complete native render-list predicate is nonmatching')
        stage.equal_state(before, after)
    need(any(int(row['sprites']) > 0 for row in resets), 'Native reset traversed actual sprites, not only empty boot list')
    faults = []
    for label, before, after, field in (('palette status', entries[0], resumes[0], 0),
                                      ('palette owner A8', entries[-1], resumes[-1], 10),
                                      ('reset status', resets[-1], restored[-1], 0),
                                      ('reset SP', resets[-1], restored[-1], 1)):
        changed = dict(after); words = after['regs'].split(',')
        old_word = words[field]; words[field] = f'{int(words[field],16)^1:08X}'
        changed['regs'] = ','.join(words)
        try: stage.equal_state(before, changed)
        except ValueError as error:
            faults.append(dict(label=label, serial=before['serial'], wordIndex=field,
                               before=old_word, after=words[field], rejectedBy=str(error)))
        else: raise ValueError('Changed actual native hook state accepted')
        stage.equal_state(before, after)
    pins = {}
    def pin(file, wanted=None):
        file = Path(file).resolve(); value = sha(file)
        need(wanted is None or wanted == value, 'Retained actual native source/evidence unchanged')
        pins[str(file)] = value
    before = json.loads((folder / 'input_hashes_before.json').read_text())
    for file, wanted in before.items(): pin(file, wanted)
    snapshots = json.loads((folder / 'source_snapshot_paths.json').read_text())
    for source, captured in snapshots.items():
        pin(captured, before[source])
    reference = json.loads(stage.OLD_REPORT.read_text())
    pin(stage.REFERENCE / 'run.log', reference['inputHashes'][str(stage.REFERENCE / 'run.log')])
    for file in folder.rglob('*'):
        if file.is_file(): pin(file)
    pin(failed); pin(__file__)
    return dict(passed=True, candidate=stage.NAME, nativeScene=state,
                actualNonmatchingPaletteRequests=1723, actualNativePoolResets=5,
                completeCallerStatusSPA0A14StatePairs=1728,
                actualNativeResetListSpriteCounts=[int(row['sprites']) for row in resets],
                actualQualifiedRegisterFaults=faults,
                allOriginalPhysicalHealthPoseBranchNativeStoresAndCleanupUnchanged=True,
                exactTypedFriendshipPaletteOrOwnedBubbleRetirementPathNeverEntered=True,
                nativeSharedHookNonmatchCallerPreservationAccepted=True,
                failedVisibleSceneReport=str(failed), currentVisibleSceneAcceptance=False,
                universalPassThroughOtherScenesOrStageAudioAccepted=False,
                newRuntimeCapturesOrExecutableROMWAVVRAMPixelCopies=0,
                fullPortAcceptance=False, scope=__doc__, inputHashes=pins)


if __name__ == '__main__':
    value = run(); OUT.mkdir(); saved = OUT / 'report.json'
    saved.write_text(json.dumps(value, indent=2) + '\n')
    before = sha(saved); result = subprocess.run(['compact.exe','/C','/I','/Q',str(saved)],capture_output=True,text=True)
    need(result.returncode == 0 and sha(saved) == before, 'Lossless compact native-only proof')
    print(json.dumps({k:v for k,v in value.items() if k not in ('inputHashes','actualQualifiedRegisterFaults')},indent=2))
