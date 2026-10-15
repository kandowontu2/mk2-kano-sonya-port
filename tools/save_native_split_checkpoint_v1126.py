"""Freeze normal split scope; resolve intentional historic source exactly."""
import hashlib,json,shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'audit_v1126_owned_split_checkpoint'
PREVIOUS = ROOT/'audit_v1105_split_grammar_checkpoint/checkpoint.json'
SOURCE = ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
ARCHIVED = ROOT/'audit_v1108_split_source_transition/input_sources/midtunit_m.cpp'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

if OUT.exists():
    raise ValueError('Never overwrite a checkpoint')
previous = json.loads(PREVIOUS.read_text())
pins,resolutions = {},[]
for filename,wanted in previous['inputHashes'].items():
    path = Path(filename)
    if path==SOURCE and digest(path)!=wanted:
        assert digest(ARCHIVED)==wanted
        pins[str(ARCHIVED)] = wanted
        resolutions.append(dict(canonical=filename,historicalSource=str(ARCHIVED),SHA256=wanted))
    else:
        assert path.is_file() and digest(path)==wanted, 'Historical evidence changed '+filename
        pins[filename] = wanted
pins[str(PREVIOUS)] = digest(PREVIOUS)
reports = (
    ROOT/'audit_v1124_owned_native_split_checked/report.json',
    ROOT/'audit_v1121_original_split_controls_checked/report.json',
    ROOT/'audit_v1125_owned_split_corruption_checks/report.json',
    ROOT/'audit_v1119_owned_split_actual_visual_review/review.json',
)
data = [json.loads(path.read_text()) for path in reports]
assert data[0]['passed'] and len(data[0]['cases'])==4 and not data[0]['fullPortAccepted']
assert data[1]['passed'] and len(data[1]['cases'])==2 and not data[1]['fullPortAccepted']
assert data[2]['passed'] and len(data[2]['checks'])==10 and data[2]['runtimeEvidenceModified'] is False
assert data[3]['normalObservedVisualReviewPassed'] and data[3]['sceneCount']==68
for path,report in zip(reports,data):
    pins[str(path)] = digest(path)
    for filename,wanted in report.get('inputHashes',{}).items():
        assert digest(Path(filename))==wanted, 'Current evidence changed '+filename
        assert filename not in pins or pins[filename]==wanted, 'Conflicting evidence pin '+filename
        pins[filename] = wanted
info_path = ROOT/'diagnostic_v1110_owned_native_split/build-info.json'
info = json.loads(info_path.read_text(encoding='utf-8-sig'))
for filename,wanted in info['input_hashes'].items():
    assert digest(Path(filename))==wanted
    assert filename not in pins or pins[filename]==wanted
    pins[filename] = wanted
for path in (
    info_path,ROOT/'diagnostic_v1110_owned_native_split/mkport_candidate.exe',
    ROOT/'STATUS_2026-10-03_CURRENT_OWNED_SPLIT.md',ROOT/'mame-mkp/mkport.exe',
    ROOT/'PLAY_CURRENT_V786_TEST_BUILD.cmd',ROOT/'PLAY_LATEST_TEST_BUILD.cmd',ROOT/'PLAY_MK2_KANO_SONYA.cmd',
):
    pins[str(path)] = digest(path)
assert digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
for folder in ('audit_v1112_verifier_draft_failure','audit_v1113_verifier_palette_failure',
               'audit_v1117_corruption_harness_failure','audit_v1118_original_split_controls_checked',
               'audit_v1122_owned_native_split_checked','audit_v1123_lookup_phase_diagnosis',
               'audit_v1115_owned_native_split_checked','audit_v1116_owned_split_actual_scene_contacts'):
    for path in (ROOT/folder).rglob('*'):
        if path.is_file():
            pins[str(path)] = digest(path)
tools = [ROOT/'mk2ks_native_split_display_v1111.lua',ROOT/'tools/run_native_split_v1111.ps1',
         ROOT/'tools/build_native_split_v1107.py',ROOT/'mk2ks_native_split_trace_v1098.lua',Path(__file__)]
tools += [ROOT/f'tools/verify_native_split_v{n}.py' for n in (1112,1113,1115,1122,1124)]
tools += [ROOT/f'tools/test_native_split_v{n}.py' for n in (1117,1120,1125)]
tools += [ROOT/f'tools/verify_native_split_controls_v{n}.py' for n in (1118,1121)]
tools += [ROOT/'tools/render_native_split_review_v1116.py',ROOT/'tools/save_native_split_visual_review_v1119.py']
OUT.mkdir()
for path in tools:
    pins[str(path)] = digest(path)
    target = OUT/'input_sources'/path.relative_to(ROOT)
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(path,target)
    pins[str(target)] = digest(target)
record = dict(candidate=info['name'],executableSHA256=info['executable_sha256'],payloadSHA256=info['payload_sha256'],
    historicalPinsRevalidated=len(previous['inputHashes']),resolvedHistoricalCompiledSources=resolutions,
    currentOwnNormalSplitCases=4,currentOriginalControlCases=2,actualOwnScenesReviewed=68,
    corruptionChecks=9,previousNativeRegressionsNotPromotedToCurrent=True,
    scope='Normal Dead Pool own split and original control regression only',
    alternateCostumesAccepted=False,bloodCostumeInvarianceAccepted=False,
    currentOtherFatalityRegressionsAccepted=False,allArenasAccepted=False,
    fullPortAccepted=False,goalComplete=False,launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='inputHashes'},indent=2))
print('Pinned files:',len(pins))
