"""One hidden, bounded campaign trial; never overwrite a prior runtime."""
import json
import subprocess
import sys
from refresh_special_videos import BASE, PORT, FLAGS


def main():
    assert sys.argv[1:] in ([], ['--short-kick'], ['--retreat-ball'], ['--retreat-ball-finish-knife'], ['--varied'], ['--varied-spacing'], ['--varied-spacing-bounded'], ['--varied-counter'], ['--varied-adaptive'], ['--varied-stomp-refresh'], ['--varied-stomp-momentum'], ['--varied-reactive'], ['--varied-finish'], ['--vertical-kick'], ['--vertical-kick-v2'], ['--vertical-kick-early'], ['--recovery-counter'], ['--recovery-counter-approach'])
    variant = sys.argv[1][2:].replace('-', '_') if len(sys.argv)>1 else 'evade_counter'
    name = 'stock_wolf_2219_kano_kintaro_' + variant
    assert not (BASE / name).exists(), 'Never overwrite evidence'
    idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                           'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                          capture_output=True, creationflags=FLAGS)
    assert idle.returncode == 0, 'Existing emulator'
    prior = json.loads((BASE / 'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    policy = 'varied' if variant.startswith('varied_spacing') or variant in ('varied_counter','varied_adaptive','varied_stomp_refresh','varied_stomp_momentum','varied_reactive','varied_finish') else variant.replace('_', '-')
    if variant.startswith('vertical_kick'):policy='vertical-kick'
    if variant.startswith('recovery_counter'):policy='recovery-counter'
    args = prior['testArguments'] + ['--campaign-kano-kintaro-' + policy]
    if variant=='varied_counter':args.append('--campaign-kano-kintaro-varied-counter')
    if variant=='varied_adaptive':args.append('--campaign-kano-kintaro-varied-adaptive')
    if variant=='varied_finish':args.append('--campaign-kano-kintaro-varied-finish')
    if variant=='varied_reactive':args+=['--campaign-kano-kintaro-varied-reactive','--campaign-kano-kintaro-stomp-refresh','--campaign-kano-kintaro-stomp-momentum']
    if variant=='varied_stomp_refresh':args.append('--campaign-kano-kintaro-stomp-refresh')
    if variant=='varied_stomp_momentum':args+=['--campaign-kano-kintaro-stomp-refresh','--campaign-kano-kintaro-stomp-momentum']
    if variant.startswith('vertical_kick'):args+=['--campaign-kano-kintaro-stomp-refresh','--campaign-kano-kintaro-stomp-momentum']
    if variant=='vertical_kick_early':args.append('--campaign-kano-kintaro-vertical-early')
    if variant.startswith('recovery_counter'):args+=['--campaign-kano-kintaro-stomp-refresh','--campaign-kano-kintaro-stomp-momentum']
    if variant=='recovery_counter_approach':args.append('--campaign-kano-kintaro-recovery-approach')
    if variant == 'retreat_ball_finish_knife':
        args.append('--campaign-kano-kintaro-retreat-ball')
    with (BASE / (name + '.stdout.log')).open('w') as out, (BASE / (name + '.stderr.log')).open('w') as err:
        result = subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name, *args],
                                cwd=BASE, stdout=out, stderr=err, creationflags=FLAGS)
    assert result.returncode == 0, 'Inspect preserved stderr/runtime before retrying'
    subprocess.run([sys.executable, str(PORT / 'audit_campaign_run.py'), name],
                   cwd=PORT, check=True, creationflags=FLAGS)


if __name__ == '__main__':
    main()
