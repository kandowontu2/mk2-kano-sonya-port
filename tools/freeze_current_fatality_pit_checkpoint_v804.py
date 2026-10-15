"""Current bounded fatality display and Pit-victim continuation checkpoint."""
import argparse
import hashlib
import json
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def check(value, message):
    if not value:raise ValueError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();root,output=args.root.resolve(),args.output.resolve()
    check(not output.exists(),'Do not overwrite checkpoint')
    tracked={}
    def track(path,wanted=None):
        path=Path(path);actual=sha(path)
        check(wanted is None or actual==wanted,'Checked input changed: '+str(path))
        tracked[str(path.resolve())]=actual
    track(Path(__file__))
    fatal_path=root/'audit_v798_current_fatalities_checked/verification.json';track(fatal_path)
    fatal=json.loads(fatal_path.read_text())
    check(fatal['passed'] and len(fatal['cases'])==4 and fatal['fullPortAcceptance'] is False,'Wrong fatality scope')
    for path,value in fatal['inputHashes'].items():track(path,value)
    pit_path=root/'audit_v801_current_pit_victims_checked/verification.json';track(pit_path)
    pit=json.loads(pit_path.read_text())
    check(pit['boundedCurrentPitVictimStateContinueAcceptance'] and pit['ownStagePerformerAcceptance'] is False
          and pit['cinematicAcceptance'] is False and pit['audioWaveformAcceptance'] is False
          and pit['fullPortAcceptance'] is False,'Wrong Pit proof scope')
    for path,value in pit['checked_inputs'].items():track(path,value)
    for tool,folder,count in (('test_finish_slots_v800.py','audit_v800_current_fatality_units',31),
                              ('test_current_pit_victim_v803.py','audit_v803_current_pit_victim_units',5)):
        track(root/'tools'/tool);log=root/folder/'unit-tests.log';track(log)
        text=log.read_text(encoding='utf-8-sig')
        check(f'Ran {count} tests' in text and text.rstrip().endswith('OK'),'Unit evidence not successful')
    # Keep the rejected mutation-target experiment explicitly as failed evidence.
    track(root/'tools/test_current_pit_victim_v802.py')
    failed=root/'audit_v802_current_pit_victim_units/unit-tests.log';track(failed)
    check('FAILED (failures=4)' in failed.read_text(encoding='utf-8-sig'),'Failed experiment history changed')
    track(root/'PLAY_LATEST_TEST_BUILD.cmd','54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784')
    track(root/'mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    frames=sum(c['replayed']['frames'] for c in fatal['cases'].values())
    output.mkdir(parents=True)
    report={'scope':__doc__,'candidate':pit['candidate'],'checked_inputs':tracked,'checked_input_count':len(tracked),
            'fatality_cases':4,'fatality_replayed_frames':frames,
            'indexed_vram_words':frames*512*512,'display_pixels':frames*400*254,
            'held_transition_samples':sum(len(c['held_transition_scanout'])for c in fatal['cases'].values()),
            'own_normal_alternate_palette_entries':sum(c['palette']['own_fighter_palette_entries']for c in fatal['cases'].values()),
            'own_alternate_palette_samples':sum(c['palette']['own_alternate_samples']for c in fatal['cases'].values()),
            'victim_palette_entries':sum(c['palette']['checked_palette_entries']for c in fatal['cases'].values()),
            'pit_cases':2,'pit_terminal_fields':[c['terminal_frame']for c in pit['cases'].values()],
            'boundedFatalityDisplayRegressionAcceptance':True,'boundedPitVictimContinueAcceptance':True,
            'ownStagePerformerAcceptance':False,'fullCinematicAcceptance':False,'fullFinisherAcceptance':False,
            'unassistedTowerClearAcceptance':False,'fullPortAcceptance':False,
            'failed_v802_preserved':'Mutations selected pre-fall launch-pose observations outside the own falling-cache contract; v803 qualifies the exact own first falling group.',
            'next':['genuine own stage-finisher inputs and remaining finisher/cinematic/audio scope',
                    'broader selection/ladder/name/floor-shadow/move/CPU/interruption/secret-stage regression',
                    'complete unassisted towers through bosses, continues, endings',
                    'final matching production launcher and release ZIP']}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in('checked_input_count','fatality_cases','fatality_replayed_frames',
        'own_alternate_palette_samples','pit_terminal_fields','fullPortAcceptance')},indent=2))

if __name__=='__main__':main()
