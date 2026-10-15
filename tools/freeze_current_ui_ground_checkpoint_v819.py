"""Freeze current bounded UI/ground/native-shadow proofs, not a release gate."""
import argparse
import hashlib
import json
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();root,output=args.root.resolve(),args.output.resolve()
    need(not output.exists(),'Do not overwrite checkpoint')
    tracked={}
    def track(path,wanted=None):
        path=Path(path);actual=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or actual==wanted,'Changed accepted proof input: '+str(path))
        tracked[str(path.resolve())]=actual
    track(Path(__file__))
    reports={}
    for name in ('audit_v809_native_stage_checkpoint','audit_v816_current_ui_ground_checked',
                 'audit_v817_current_native_ui_units','audit_v818_current_ground_shadow_units'):
        path=root/name/'verification.json';track(path);report=json.loads(path.read_text());reports[name]=report
        for target,wanted in report['checked_inputs'].items():track(target,wanted)
        need(report['fullPortAcceptance']is False,'Scope must remain bounded')
    current=reports['audit_v816_current_ui_ground_checked']
    need(current['passed']and current['boundedCurrentGroundShadowAcceptance']and current['boundedCurrentUiFlowAcceptance']
         and len(current['ground_cases'])==len(current['ui_cases'])==4
         and current['sampled_ground_frames']==148 and current['native_owned_shadow_copies']==120162
         and current['allArenaFloorAcceptance']is False,'Exact current runtime scope')
    for name,count in (('audit_v817_current_native_ui_units',46),('audit_v818_current_ground_shadow_units',13)):
        need(reports[name]['passed']and reports[name]['methods']==count,'Unit proof not successful')
        path=root/name/'unit-tests.log';track(path);text=path.read_text()
        need(f'Ran {count} tests'in text and text.rstrip().endswith('OK'),'Actual successful unit output required')
    track(root/'PLAY_LATEST_TEST_BUILD.cmd','54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784')
    track(root/'mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    output.mkdir()
    report={'candidate':current['candidate'],'checked_inputs':tracked,'checked_input_count':len(tracked),
        'boundedCurrentUiFlowAcceptance':True,'boundedCurrentGroundShadowAcceptance':True,
        'sampled_ground_frames':148,'ground_display_pixels':148*400*254,'ground_indexed_vram_words':148*512*512,
        'native_owned_shadow_copies':120162,'ui_cases':4,'ui_unit_methods':46,'ground_unit_methods':13,
        'allArenaFloorAcceptance':False,'fullFinisherAcceptance':False,'unassistedTowerClearAcceptance':False,
        'fullPortAcceptance':False,'release_promoted':False,
        'failed_v812_preserved':current['failed_v812_preserved'],
        'limits':'Both slots current normal selection/navigation/cursor/number/preview/ladder/first-fight identity/name-shadow; Dead Pool two-human mobility with Kitana control and actual native floor-shadow rows. Not every arena, state, move, finisher or campaign.',
        'remaining':['other arenas/states and broader moves/CPU/interruption/secret-stage regression',
                     'remaining finisher/cinematic/art/audio variants','genuine complete towers through bosses, continues and endings',
                     'final whole-port regression, matching production CMD and release ZIP']}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ('checked_input_count','sampled_ground_frames','native_owned_shadow_copies','ui_cases','fullPortAcceptance')}))
if __name__=='__main__':main()
