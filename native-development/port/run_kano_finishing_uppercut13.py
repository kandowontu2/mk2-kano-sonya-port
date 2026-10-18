"""One fresh, hidden trial of the explicit13HP takeover threshold."""
import json
import subprocess
import sys
from refresh_special_videos import BASE, PORT, FLAGS, command


def trial_arguments(prior,endurance=False):
    args=list(prior)+['--campaign-kano-kintaro-varied','--campaign-kano-kintaro-varied-finish',
        '--campaign-kano-kintaro-varied-finish-uppercut','--campaign-finish-uppercut-threshold=13']
    if endurance:
        args=[a for a in args if not a.startswith('--campaign-continues=')]
        args+=['--campaign-boss-endurance','--campaign-continues=64']
    return args


def main():
    assert sys.argv[1:] in ([],['--endurance'])
    endurance='--endurance' in sys.argv
    name='stock_wolf_2219_kano_kintaro_varied_finish_uppercut13'
    if endurance:name+='_endurance'
    assert not (BASE/name).exists(),'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    args=trial_arguments(prior['testArguments'],endurance)
    command(BASE/'test_wolf_baseline.py',name,*args)
    command(PORT/'audit_campaign_run.py',name)
    command(PORT/'inspect_kintaro_variety.py',name)
    command(PORT/'inspect_kintaro_ready_counter.py',name)


if __name__=='__main__':main()
