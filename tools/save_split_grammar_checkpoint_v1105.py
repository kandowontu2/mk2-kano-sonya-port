"""Freeze current regressions, correct original split grammar and draft art."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'audit_v1105_split_grammar_checkpoint'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUT.exists():
        raise ValueError('Preserve checkpoints')
    prior_path = ROOT/'audit_v1090_arm_palette_checkpoint/checkpoint.json'
    prior = json.loads(prior_path.read_text())
    pins = dict(prior['inputHashes'])
    for filename, wanted in pins.items():
        assert digest(Path(filename)) == wanted, filename
    prior_count = len(pins)
    proof_paths = [ROOT/name for name in (
        'audit_v1092_native_regressions_checked/report.json',
        'audit_v1100_native_split_grammar_checked/report.json')]
    proofs = [json.loads(path.read_text()) for path in proof_paths]
    assert all(p['passed'] and not p['errors'] and not p['fullPortAccepted'] for p in proofs)
    assert len(proofs[0]['cases']) == 20 and len(proofs[1]['cases']) == 2
    assert proofs[1]['main0IsConstructorSeedNotSplitAnimation'] and proofs[1]['sameHalfStreamMirroredByNativeActor']
    assert not proofs[1]['kanoSonyaSplitAccepted'] and not proofs[1]['replacementMain0Required']
    for proof in proofs:
        for filename, wanted in proof['inputHashes'].items():
            assert digest(Path(filename)) == wanted, filename
            if filename in pins:
                assert pins[filename] == wanted, filename
            pins[filename] = wanted
    units_paths = [ROOT/name for name in (
        'audit_v1097_native_regression_proof_units/unit-results.json',
        'audit_v1102_native_split_grammar_units/unit-results.json')]
    units = [json.loads(path.read_text()) for path in units_paths]
    assert all(u['passed'] and u['corruptionChecks'] == 3 and not u['fullPortAccepted'] for u in units)
    review_path = ROOT/'audit_v1103_native_split_control_visual_review/manual-review.json'
    review = json.loads(review_path.read_text())
    assert review['actualScenesManuallyReviewed'] == 4 and len(review['inputHashes']) == 4 and not review['kanoSonyaSplitAccepted']
    for filename, wanted in review['inputHashes'].items():
        assert digest(Path(filename)) == wanted, filename
        pins[filename] = wanted
    art = json.loads((ROOT/'art_native_split_v1104/prompts-and-review.json').read_text())
    assert art['tool'] == 'built-in image_gen' and art['draft'] and not art['encoded'] and not art['installed'] and not art['nativeRuntimeAccepted']
    assert len(art['assets']) == 2
    for asset in art['assets'].values():
        assert digest(Path(asset['source'])) == asset['sha256']
        assert digest(ROOT/'art_native_split_v1104'/asset['file']) == asset['sha256']
        pins[asset['source']] = asset['sha256']
    assert digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp') == '1DF1D1217776DBC3830F00ED078589A925A81F7C356F8EADE117907711A68CF6'
    assert digest(ROOT/'mame-mkp/mkport.exe') == '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    folders = ('audit_v1092_native_regressions_checked','audit_v1097_native_regression_proof_units',
        'audit_v1094_native_split_opposite_references','audit_v1095_kung_lao_liu_kang_p2_split_native_trace',
        'audit_v1096_kung_lao_liu_kang_p2_split_native_trace','audit_v1100_native_split_grammar_checked',
        'audit_v1102_native_split_grammar_units','audit_v1103_native_split_control_visual_review',
        'art_native_split_v1093','art_native_split_v1104')
    folders += tuple(proofs[0]['cases'])+tuple(proofs[1]['cases'])
    for folder in folders:
        for path in (ROOT/folder).rglob('*'):
            if path.is_file():
                pins[str(path)] = digest(path)
    for path in proof_paths+units_paths+[prior_path,review_path]:
        pins[str(path)] = digest(path)
    sources = ('tools/run_native_regressions_v1091.ps1','tools/verify_native_regressions_v1092.py',
        'tools/test_native_regressions_v1097.py','tools/audit_native_split_opposite_v1094.py',
        'tools/run_native_split_trace_v1095.ps1','mk2ks_native_split_trace_v1095.lua',
        'tools/run_native_split_trace_v1096.ps1','tools/run_native_split_trace_v1098.ps1',
        'mk2ks_native_split_trace_v1098.lua','tools/verify_native_split_grammar_v1100.py',
        'tools/test_native_split_grammar_v1102.py','tools/save_split_grammar_checkpoint_v1105.py',
        'STATUS_2026-10-03_CURRENT_SPLIT_GRAMMAR.md')
    OUT.mkdir()
    for filename in sources:
        path = ROOT/filename
        frozen = OUT/'input_sources'/filename
        frozen.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, frozen)
        pins[str(path)] = digest(path)
        pins[str(frozen)] = digest(frozen)
    pngs = {}
    for killer in ('jax','baraka','cage','kitana','reptile'):
        cases = [ROOT/c for c,data in proofs[0]['cases'].items() if data['killer'] == killer]
        assert len(cases) == 4
        pngs[killer] = sum(len(list((case/'snap').rglob('*.png'))) for case in cases)
    data = {'candidate': prior['candidate'], 'historicalPinsRevalidated': prior_count,
        'establishedTwentyRegressionsOnThisCandidateAccepted': True,
        'currentRegressionCases': 20, 'currentRegressionActualPNGs': pngs,
        'regressionCorruptionChecks': 3, 'originalSplitControlCases': 2,
        'originalSplitMirroredHalfPosesPerControl': 7, 'pairedZeroSentinelsVerified': 2,
        'main0MustRemainNormalStance': True, 'originalSplitCorruptionChecks': 3,
        'actualOriginalSplitScenesManuallyReviewed': 4, 'newHalfBodyDraftAtlases': 2,
        'failed1094StanceAsOppositeHalfInferenceRejected': True,
        'failed1095AutobootArgumentPreserved': True,
        'missing1096UnretainedHooksNotAcceptedAsTrace': True,
        'kanoSonyaSplitAccepted': False, 'draftArtworkInstalled': False,
        'gameDriverAndPayloadUnchangedThisTurn': True, 'installedExecutableUnchanged': True,
        'existingLaunchersNotUpdated': True, 'releaseZipNotUpdated': True,
        'noDeletionOccurred': True, 'naturalAlternateSelectionAccepted': False,
        'allStockFatalitiesAccepted': False, 'allArenasAccepted': False,
        'fullTowerAccepted': False, 'finalCombinedGameplayAndUIAccepted': False,
        'fullPortAccepted': False, 'evidencePins': len(pins), 'inputHashes': pins}
    (OUT/'checkpoint.json').write_text(json.dumps(data, indent=2)+'\n')
    for filename, wanted in pins.items():
        assert digest(Path(filename)) == wanted, filename
    print(json.dumps({k:v for k,v in data.items() if k != 'inputHashes'}, indent=2))


if __name__ == '__main__':
    main()
