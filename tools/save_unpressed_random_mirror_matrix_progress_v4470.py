"""Record four actual rare mirror scenes; preserve all five full-port groups."""
import ctypes, json, subprocess
from pathlib import Path
import assemble_unpressed_random_mirror_tomb_matrix_v4468 as matrix
ROOT, need, sha = matrix.ROOT, matrix.need, matrix.sha
PARENT = ROOT / 'audit_v4464_tomb_mirror_random_drop_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v4471_unpressed_random_mirror_full_scope_checkpoint'

def main():
    need(not OUT.exists(), 'Fresh full-scope checkpoint')
    state = json.loads(PARENT.read_text()); original_remaining = list(state['remaining'])
    pins = dict(state['inputHashes'])
    need(all(sha(p) == h for p,h in pins.items()), 'Every inherited full-goal requirement/evidence unchanged')
    def pin(path, wanted=None):
        path = Path(path).resolve(); key = str(path); actual = sha(path)
        need((wanted is None or actual == wanted) and (key not in pins or pins[key] == actual),
             'Consistent actually executed original and new evidence bytes')
        pins[key] = actual
    pin(PARENT); pin(__file__)
    path = matrix.OUT / 'report.json'; proof = json.loads(path.read_text()); pin(path)
    need(proof['passed'] and proof['current3836BothCharactersBothSlotsUnpressedRareMirrorTombWholeRenderPaletteShadowEraseAccepted'] and
         proof['actualTrueMirrorRenderContexts'] == 4 and proof['actualWholeVisibleFields'] == 2148 and
         proof['actualExactVisibleRGBPixels'] == 218236800 and proof['actualRenderCounterexamplesRejected'] == 8 and
         proof['priorCompletedNativeScenesNotRerun'] and not proof['fullPortAcceptance'] and
         not proof['completeStageVictimAudioAccepted'] and not proof['broaderPitTombVictimsAccepted'],
         'Four terminal native rare mirror scenes, strict original phase/art/shadow/erase gates and exclusions')
    for p,h in proof['inputHashes'].items(): pin(p,h)
    earlier = []
    for folder,key in (
        ('audit_v4369_both_characters_both_slots_true_mirror_tomb_render',
         'current3836BothCharactersBothPhysicalSlotsTrueMirrorTombWholeRenderPaletteShadowEraseAccepted'),
        ('audit_v4409_both_characters_both_slots_pressed_mirror_tomb_render',
         'current3836BothCharactersBothPhysicalSlotsPressedMirrorTombWholeRenderPaletteShadowEraseAccepted')):
        oldpath = ROOT / folder / 'report.json'; old = json.loads(oldpath.read_text()); pin(oldpath)
        need(old['passed'] and old[key] and old['actualTrueMirrorRenderContexts'] == 4 and
             old['actualWholeVisibleFields'] == 2148 and old['actualExactVisibleRGBPixels'] == 218236800 and
             not old['fullPortAcceptance'] and not old['allStageVictimAudioAccepted'],
             'Reuse only actually completed held/pressed mirror scenes, no broader audio claim')
        for p,h in old['inputHashes'].items(): pin(p,h)
        earlier.append(str(oldpath))
    query = "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'find_tomb_mirror_native_random_drop_v4455.py|qualify_tomb_mirror_random_drop_v4458.py|run_remaining_random_drop_mirror_render_ram_v4465.py|audit_v4466_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    live = subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(live.returncode == 0 and not live.stdout.strip(), 'Actual search/state/render jobs terminal')
    files = set()
    for fighter,side,delay in matrix.CONTEXTS:
        if (fighter,side) == ('kano',1): continue
        folder,output = matrix.remaining.paths(fighter,side)
        leaves = [folder,output,ROOT / f'audit_v4459_tomb_mirror_random_drop_checked/{fighter}_p{side}_delay{delay:02d}']
        if side == 2:
            leaves += sorted((ROOT / 'audit_v4456_tomb_mirror_random_timing_search').glob(f'{fighter}_p2_delay*'))
            files.add(ROOT / f'audit_v4456_tomb_mirror_random_timing_search/search_{fighter}_p2_01_20.json')
        for leaf in leaves: files.update(p for p in leaf.rglob('*') if p.is_file())
    files.update(p for p in matrix.OUT.rglob('*') if p.is_file())
    alloc = ctypes.windll.kernel32.GetCompressedFileSizeW
    alloc.argtypes = [ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)]; alloc.restype = ctypes.c_uint32
    allocated = 0
    for p in files:
        pin(p); hi = ctypes.c_uint32(); lo = alloc(str(p),ctypes.byref(hi))
        need(lo != 0xffffffff, 'Exact current diagnostic allocated bytes')
        allocated += (hi.value << 32) | lo
    next_action = (
        'Both genuine identities now have actual native unpressed rare Tomb mirror drops in both physical slots, '
        'complete earned/native branch/269callback phase/801field cleanup and source-perfect whole537field scenes '
        'through retirement+30. Normal P1/alternate P2 mirror palettes, original floor/native compressed owned '
        'shadows/continuous CPU/FIFO/DMA/shift/VRAM/RGB/erase gates and actual counterexamples all passed. '
        'Reuse these four scenes and the already completed held/pressed mirror matrices; do not rerun accepted '
        'SonyaP2 natural tower. No forced RNG, guest, health, AI, IDs, positions or palette writes. '
        'Next inspect and close complete native stage/victim DCS waveform or broader Pit/Tomb stock-victim '
        'combinations using actual native input and RAM-only observers, not donor/proxy identities. '
        'Full move-phase/ground/shadows/CPU/repeat/KO/overlap across arenas, other finishers/victims/morphs/'
        'secrets/cinematics, missing current-build character/slot natural tower and full ending transitions/audio, '
        'and final combined selection/ladder/names/audio/dependency-aware cleanup/refreshed release remain open. '
        'All five original groups retained. Public1836 is still an unchanged playtest, not finished release. '
        'No new builds, raw native media/ROM copies or deletion; no historical savings recounted.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
        inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
            mergeRule='All original full-goal groups/evidence/exclusions retained; four actual rare mirror render/state contexts added.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual P2 native rare RNG6/40 branches qualified, SonyaP1/KanoP2/SonyaP2 whole native scenes verified; aggregate original earned/branch/phase/art/palette/ground/shadow/erase/fault gates pass for all four mirror contexts.',
        current3836UnpressedRandomTombMirrorDropContexts=proof['cases'],
        current3836BothCharactersBothSlotsUnpressedRandomTombMirrorStateRenderAccepted=True,
        current3836SonyaP1UnpressedRandomTombMirrorWholeRenderAccepted=True,
        current3836P2UnpressedRandomTombMirrorCoverageAccepted=True,
        current3836TrueMirrorTombAllDropAndPressedBranchesAccepted=True,
        current3836UnpressedRandomTombMirrorMatrixReport=str(path),
        retainedHeldAndPressedMirrorReports=earlier,
        completeStageVictimAudioAccepted=False,broaderPitTombVictimCoverageAccepted=False,
        currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
        currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,
        currentTurnReclaimedAllocatedBytes=0,
        cleanupAccounting='New compressed source/text/digest evidence only; native guest/VRAM/RGB RAM-only. No deletion or historical saving counted again.',
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining'] == original_remaining and len(original_remaining) == 5, 'Full objective and all five requirement groups intact')
    need(all(sha(p) == h for p,h in pins.items()), 'All inherited/current source and public evidence unchanged')
    OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode == 0,
         'Checkpoint compressed before writes')
    (OUT / 'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT / 'checkpoint.json'),inputPins=len(pins),
        actualRareMirrorNativeStateRenderContexts=4,wholeVisibleFields=2148,
        currentEvidenceAllocatedBytes=allocated,originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__ == '__main__': main()
