"""Pin fresh current human combat evidence alongside the accepted UI/finisher proofs.

This checkpoint is not all-opponent, CPU, tower, ending, art/audio or release acceptance.
"""
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
    need(not output.exists(),'Do not overwrite a checkpoint')
    tracked={}
    def track(path,wanted=None):
        path=Path(path).resolve();actual=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or actual==wanted,'Changed proof input: '+str(path))
        need(str(path)not in tracked or tracked[str(path)]==actual,'Inconsistent merged input')
        tracked[str(path)]=actual
    track(__file__);reports={}
    names=('audit_v819_current_ui_ground_checkpoint','audit_v821_current_full_human_checked',
           'audit_v822_current_full_human_units','audit_v824_current_interrupt_and_ko_checked',
           'audit_v825_current_interrupt_and_ko_units')
    for name in names:
        path=root/name/'verification.json';track(path)
        report=json.loads(path.read_text());reports[name]=report
        need(report['fullPortAcceptance']is False,'Do not broaden accepted scope')
        for path,wanted in report.get('checked_inputs',report.get('inputHashes',{})).items():track(path,wanted)
    matrix=reports[names[1]];lifecycle=reports[names[3]]
    need(matrix['passed']and matrix['boundedMatrixPassed']and len(matrix['cases'])==52 and
         matrix['positiveCases']==18 and matrix['negativeCases']==34 and matrix['pairedFields']==46178,
         'Exact completed current 52-case human matrix')
    need(lifecycle['passed']and len(lifecycle['interruptions'])==10 and len(lifecycle['knockouts'])==4 and
         sum(p['pairedFields']for p in lifecycle['interruptions'])+
         sum(p['actual_fields']for p in lifecycle['knockouts'])==21164,
         'Exact completed current interruption and round-two scope')
    need(matrix['candidate']==lifecycle['candidate']=='diagnostic_v786_native_fighter_fade_exclusions',
         'All new evidence uses the same current candidate')
    for name,count in ((names[2],9),(names[4],30)):
        need(reports[name]['passed']and reports[name]['methods']==count,'Successful actual checker tests')
        path=root/name/'unit-tests.log';track(path);text=path.read_text()
        need(f'Ran {count} tests'in text and text.rstrip().endswith('OK'),'Actual unit output')
    captures=[root/c['capture']for c in matrix['cases']]
    captures += [root/f"audit_v823_interrupt_{c['move']}_p{c['side']}_{c['victim']}"for c in lifecycle['interruptions']]
    captures += [root/f"audit_v823_ko_{c['move']}_p{c['side']}_{c['victim']}"for c in lifecycle['knockouts']]
    need(len(captures)==len(set(captures))==66,'Complete distinct runtime inventory')
    for folder in captures:
        manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        frozen={Path(path).name:wanted for path,wanted in manifest.items()if Path(path).suffix in('.lua','.ps1','.json')}
        for path in (folder/'input_sources').iterdir():
            need(path.name in frozen,'Unexpected frozen source');track(path,frozen[path.name])
        need({p.name for p in (folder/'input_sources').iterdir()}==set(frozen),'Missing frozen source')
    track(root/'PLAY_LATEST_TEST_BUILD.cmd','54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784')
    track(root/'mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    report={'candidate':matrix['candidate'],'checked_inputs':tracked,'checked_input_count':len(tracked),
        'boundedCurrentHumanMatrixAcceptance':True,'boundedCurrentStartupInterruptionAcceptance':True,
        'boundedCurrentRepeatedSpecialKoRoundTwoAcceptance':True,'runtime_cases':66,
        'pairedFields':67342,'human_matrix_cases':52,'startup_interrupt_retry_cases':10,'ko_round_two_cases':4,
        'new_checker_unit_methods':39,'fullPortAcceptance':False,'allOpponentCombatAcceptance':False,
        'allArenaFloorAcceptance':False,'fullFinisherAcceptance':False,'unassistedTowerClearAcceptance':False,
        'release_promoted':False,
        'limits':'Physical two-human eight-special hits/blocks/misses against Sub-Zero in both slots, plus square-wave air contact and leg-grab crouch-block rejection. Three startup interruption families, selected Kano/Sonya/mirror opponents; four full repeated blade/bicycle KO-to-round-two paths. Not every move interruption, opponent, arena, CPU, exact raster/audio or campaign.',
        'remaining':['other opponents/arenas/states and broader CPU/interruption/secret-stage regression',
                     'remaining move/finisher/cinematic/art/audio variants',
                     'genuine complete towers through bosses, continues and endings',
                     'final whole-port regression, matching production CMD and release ZIP']}
    output.mkdir();(output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in('checked_input_count','runtime_cases','pairedFields','new_checker_unit_methods','fullPortAcceptance')}))

if __name__=='__main__':main()
