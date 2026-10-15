"""Current CPU/campaign-scout/playtest checkpoint; no whole-port promotion."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def need(ok,message):
    if not ok:raise ValueError(message)


def main():
    out=ROOT/'audit_v847_current_cpu_campaign_launcher_checkpoint'
    need(not out.exists(),'Refusing to overwrite evidence')
    inputs={};reports={}
    def track(path,wanted=None):
        path=Path(path).resolve();sha=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or wanted==sha,'Pinned input changed: '+str(path))
        need(str(path)not in inputs or inputs[str(path)]==sha,'Inconsistent evidence')
        inputs[str(path)]=sha
    track(__file__)
    names=('audit_v841_current_cpu_display_checkpoint','audit_v843_current_tower_sonya_checked',
           'audit_v844_current_natural_campaign_units','audit_v845_current_playtest_launcher',
           'audit_v846_current_playtest_launcher')
    for name in names:
        path=ROOT/name/'verification.json';track(path);proof=json.loads(path.read_text());reports[name]=proof
        need(proof['fullPortAcceptance']is False,'Full-goal gate remains open')
        for path,wanted in proof.get('checked_inputs',proof.get('inputHashes',{})).items():track(path,wanted)
    prior,campaign,units,failed,launcher=(reports[name]for name in names)
    need(campaign['passed']and not campaign['unassisted_clear_proven']and campaign['stages_reached']==[0]
         and campaign['native_own_round_wins']==0 and campaign['native_owned_projectile_entries']==141,
         'Actual bounded scout, never a fabricated tower clear')
    need(units['passed']and units['methods']==23 and units['baseline_cases']==1,'Actual campaign regression methods')
    path=ROOT/names[2]/'unit-tests.log';track(path)
    text=path.read_text();need('Ran 23 tests'in text and text.rstrip().endswith('OK'),'Actual successful test log')
    need(not failed['passed']and launcher['passed']and launcher['exit_code']==0,'Retain failed quoting test and actual passing CMD boot')
    for name in(names[3],names[4]):track(ROOT/name/'run.log')
    track(ROOT/'STATUS_2026-10-02_CURRENT_CPU_DISPLAY.md')
    proof={**{key:value for key,value in prior.items()if key not in('checked_inputs','checked_input_count')},
           'checked_inputs':inputs,'checked_input_count':len(inputs),
           'newCheckerUnitMethods':104,'currentNamedPlaytestCmdBootAcceptance':True,
           'playtestCmd':'PLAY_CURRENT_V786_TEST_BUILD.cmd',
           'currentSonyaCampaignScoutAcceptance':True,'unassistedTowerClearAcceptance':False,
           'campaignScout':{key:campaign[key]for key in('stages_reached','native_own_round_wins',
                                                      'native_owned_projectile_entries','paid_continue_losses')},
           'release_promoted':False,'fullPortAcceptance':False}
    out.mkdir();(out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({key:proof[key]for key in('checked_input_count','currentCpuDisplayedGrabCases',
                                             'newCheckerUnitMethods','playtestCmd','fullPortAcceptance')},indent=2))


if __name__=='__main__':main()
