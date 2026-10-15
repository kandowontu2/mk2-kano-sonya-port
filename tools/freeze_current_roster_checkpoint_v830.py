"""Pin current selectable-roster human contact outcomes, not whole-port fidelity."""
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
        path=Path(path).resolve();actual=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or actual==wanted,'Accepted input changed: '+str(path))
        need(str(path)not in tracked or tracked[str(path)]==actual,'Inconsistent merged input')
        tracked[str(path)]=actual
    track(__file__);reports={}
    names=('audit_v826_current_human_checkpoint','audit_v828_current_roster_human_checked',
           'audit_v829_current_roster_human_units')
    for name in names:
        path=root/name/'verification.json';track(path);proof=json.loads(path.read_text());reports[name]=proof
        need(proof['fullPortAcceptance']is False,'Whole-port scope must remain open')
        for path,wanted in proof.get('checked_inputs',proof.get('inputHashes',{})).items():track(path,wanted)
    current=reports[names[1]];units=reports[names[2]]
    need(current['passed']and not current['failures']and current['cases_count']==len(current['cases'])==252,
         'Complete actual current selectable-roster outcomes')
    need(current['candidate']=='diagnostic_v786_native_fighter_fade_exclusions','Exact current candidate')
    roster={'kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden',
            'sub_zero','reptile','scorpion','jax','kano','sonya'}
    expected={(move,side,victim,air)for move in('knife','ball','blade','choke','ring','square','bicycle','leg')
              for side in(1,2)for victim in roster for air in((False,True)if move=='square'else(False,))}
    actual={(c['move'],c['side'],c['victim'],c['air'])for c in current['cases']}
    need(actual==expected and all(c['passed']for c in current['cases']),'Every declared move/slot/opponent/air fixture')
    need(units['passed']and units['methods']==15 and units['baseline_cases']==252,'Actual successful checker methods')
    path=root/names[2]/'unit-tests.log';track(path);text=path.read_text()
    need('Ran 15 tests'in text and text.rstrip().endswith('OK'),'Successful actual unit output')
    reused=0;new=0
    for case in current['cases']:
        folder=root/case['capture']
        if folder.name.startswith('audit_v820_'):reused+=1
        else:need(folder.name.startswith('audit_v827_'),'No historical capture replacement');new+=1
        manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        frozen={Path(path).name:sha for path,sha in manifest.items()if Path(path).suffix in('.lua','.ps1','.json')}
        sources=list((folder/'input_sources').iterdir())
        need({p.name for p in sources}==set(frozen),'Complete frozen capture source inventory')
        for source in sources:track(source,frozen[source.name])
    need((new,reused)==(234,18),'Fresh wider roster and unchanged current controls')
    track(root/'PLAY_LATEST_TEST_BUILD.cmd','54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784')
    track(root/'mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    output.mkdir()
    proof={'candidate':current['candidate'],'checked_inputs':tracked,'checked_input_count':len(tracked),
        'allSelectableHumanContactOutcomesAcceptance':True,'human_contact_cases':252,
        'fresh_wider_roster_cases':234,'reused_current_sub_zero_controls':18,
        'pairedFields':current['pairedFields'],'new_checker_unit_methods':15,
        'fullPortAcceptance':False,'fullMoveArtAudioChoreographyAcceptance':False,'fullCpuAcceptance':False,
        'allArenaFloorAcceptance':False,'fullFinisherAcceptance':False,'unassistedTowerClearAcceptance':False,
        'release_promoted':False,
        'limits':current['scope'],
        'remaining':['broader CPU contacts/choreography and human block/miss/interruption/KO states',
                     'remaining move/finisher/cinematic art/audio variants and wider arena/secret-stage/camera grounding',
                     'genuine complete towers through both bosses, continues and endings',
                     'final whole-port regression, matching production CMD and release ZIP']}
    (output/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({k:proof[k]for k in('checked_input_count','human_contact_cases','pairedFields','new_checker_unit_methods','fullPortAcceptance')}))

if __name__=='__main__':main()
