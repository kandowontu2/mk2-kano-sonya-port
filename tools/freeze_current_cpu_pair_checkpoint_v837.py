"""Pin current CPU displayed grabs with prior current integration evidence.

This bounded checkpoint is not complete CPU, choreography/audio or port approval.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def need(condition,message):
    if not condition:raise ValueError(message)


def main():
    out=ROOT/'audit_v837_current_cpu_pair_checkpoint'
    need(not out.exists(),'Refusing to overwrite evidence')
    inputs={};reports={}
    def track(path,wanted=None):
        path=Path(path).resolve();actual=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or actual==wanted,'Pinned input changed: '+str(path))
        need(str(path)not in inputs or inputs[str(path)]==actual,'Inconsistent evidence hash')
        inputs[str(path)]=actual
    track(__file__)
    names=('audit_v830_current_roster_checkpoint','audit_v834_current_cpu_profile_diagnosis',
           'audit_v835_current_cpu_pair_display_checked','audit_v833_current_cpu_pair_display_units',
           'audit_v836_current_cpu_pair_state_units')
    for name in names:
        path=ROOT/name/'verification.json';track(path)
        proof=json.loads(path.read_text());reports[name]=proof
        need(proof['fullPortAcceptance']is False,'Whole-port approval remains open')
        for path,wanted in proof.get('checked_inputs',proof.get('inputHashes',{})).items():track(path,wanted)
    diagnosis=reports[names[1]];display=reports[names[2]]
    need(diagnosis['passed']is False,'Do not hide the failed historical move expectation')
    mirror=diagnosis['cases']['audit_v831_cpu_queue_sonya_mirror']
    need(mirror['declared_profile']=='bicycle'and not mirror['declared_result']['passed']
         and mirror['strict_square_result']['passed'],'Actual strict mirror diagnosis preserved')
    need(display['passed']and not display['CPU_acceptance']and len(display['cases'])==5,
         'All five bounded display paths pass without complete CPU claim')
    frames=pixels=body_pixels=paired_fields=0
    for name,case in display['cases'].items():
        need(name.startswith('audit_v831_')and case['passed']and case['paired']['passed'],
             'Actual current captures and complete declared native contracts')
        need(all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in case['records']),
             'No replay/display mismatch waived')
        need(all(b['mismatches']==0 and b['pixels']>100 for r in case['records']for b in r['body'].values()),
             'Both bodies actually visible and exact')
        frames+=case['sampled_frames'];pixels+=case['exact_screen_pixels']
        body_pixels+=case['exact_body_pixels'];paired_fields+=case['paired']['paired_fields']
    need((frames,pixels,body_pixels,paired_fields)==(425,43180000,2476717,565),'Actual complete evidence totals')
    for name,count in ((names[3],37),(names[4],22)):
        units=reports[name]
        need(units['passed']and units['methods']==count and units['baseline_cases']==5,'Actual checker suite passes')
        path=ROOT/name/'unit-tests.log';track(path);log=path.read_text()
        need(f'Ran {count} tests'in log and log.rstrip().endswith('OK'),'Actual successful test output')
    track(ROOT/'PLAY_LATEST_TEST_BUILD.cmd','54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784')
    track(ROOT/'mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    proof={'candidate':display['candidate'],'checked_inputs':inputs,'checked_input_count':len(inputs),
           'currentCpuDisplayedGrabPathsAcceptance':True,'currentCpuDisplayedGrabCases':5,
           'sampledFrames':frames,'exactDisplayedPixels':pixels,'exactBodyPixels':body_pixels,
           'pairedFields':paired_fields,'newCheckerUnitMethods':59,
           'allSelectableHumanContactOutcomesAcceptance':True,
           'fullPortAcceptance':False,'fullCpuAcceptance':False,
           'fullMoveArtAudioChoreographyAcceptance':False,'allArenaFloorAcceptance':False,
           'fullFinisherAcceptance':False,'unassistedTowerClearAcceptance':False,'release_promoted':False,
           'limits':['five P1 CPU choke/leg paths and genuine first ordinary/square follow-ups only',
                     '425 sampled drawing passes; unsampled rendered fields and inter-pass erasure excluded',
                     'native held choreography proven, not artistic/audio judgement for every move',
                     'failed historical bicycle expectation retained; actual mirror square fully checked'],
           'remaining':['wider CPU moves/victims/slots/interruption/KO and full move art/audio',
                        'remaining finisher/cinematic variants, arena/camera grounding and UI timing paths',
                        'genuine complete towers through both bosses and complete endings',
                        'final whole-port regression and matching production CMD/release ZIP']}
    out.mkdir();(out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({k:proof[k]for k in('checked_input_count','currentCpuDisplayedGrabCases','sampledFrames',
                                      'exactDisplayedPixels','newCheckerUnitMethods','fullPortAcceptance')},indent=2))


if __name__=='__main__':main()
