"""Stream native campaign frames without raw video; prove outcomes before labeling."""
import csv
import json
import shutil
import subprocess
import sys
from native_capture_pipe import CapturePipe
from mux_stream_native_audio import timing, mux
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS
from campaign_budget import budget


def main():
    assert sys.argv[1:] in ([], ['--preflight'])
    preflight='--preflight' in sys.argv
    name='stock_wolf_2219_campaign_stream_preflight_v2' if preflight else 'stock_wolf_2219_sonya_campaign_stream'
    out=PORT/('generated_campaign_stream_preflight_v2' if preflight else 'generated_sonya_campaign_2219')
    assert not out.exists() and not (BASE/name).exists(), 'Never overwrite recordings or runtime evidence'
    assert shutil.disk_usage(PORT).free>5*1024**3, 'Reserve for encoded output and temporary native WAV'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_sonya_campaign/execution.json').read_text())
    args=['--game','--campaign','--sonya','--sound-candidate'] if preflight else prior['testArguments']
    assert '--sonya' in args
    maximum=budget(args)['fieldLimit']
    reference=json.loads((BASE/'stock_wolf_2219_video_ball/FINISHER_VIDEO.json').read_text())
    out.mkdir()
    capture=CapturePipe(out/'campaign_video.mp4',reference['rate'],maximum,120 if preflight else 820)
    try:
        with (out/'runner.stdout.log').open('w') as stdout,(out/'runner.stderr.log').open('w') as stderr:
            result=subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args,
                '--audio','--campaign-stream-pipe='+capture.address],cwd=BASE,stdout=stdout,stderr=stderr,creationflags=FLAGS)
        assert result.returncode==0,'Inspect preserved runner logs before retrying'
        execution=json.loads((BASE/name/'execution.json').read_text())
        assert execution['exitCode']==0 and not execution['timedOut'],'Emulator failed; inspect preserved mame.log'
        streamed=capture.finish()
    finally:
        if capture.thread.is_alive():capture.abort()
    run=BASE/name
    def qualify(script):
        subprocess.run([sys.executable,str(PORT/script),name],cwd=PORT,check=True,creationflags=FLAGS)
    qualify('audit_campaign_run.py')
    clear=None
    if not preflight:
        qualify('qualify_campaign_clear.py')
        clear=json.loads((run/'CAMPAIGN_CLEAR_QUALIFICATION.json').read_text())
    with (run/'campaign_capture.csv').open() as source:clock=timing(csv.DictReader(source))
    end=dict(line.split('=',1) for line in (run/'campaign_end.txt').read_text().splitlines())
    assert clock['frames']==streamed['frames']
    assert clock['firstGuestFrame']+clock['frames']-1==int(end['frame']),'Final native field missing from capture'
    if clear:
        assert clock['firstGuestFrame']<clear['firstWinningRoundFrame']<clear['finalBossClearFrame']<=int(end['frame'])
        assert clear['attractReturnFrame']<=int(end['frame'])
    final=out/('NATIVE_CAMPAIGN_PREFLIGHT.mp4' if preflight else 'MKII_SONYA_CAMPAIGN_NATIVE.mp4')
    encoded=mux(run,capture.output,run/'campaign_capture.csv',final,cleanup=True)
    report=dict(scope='Short native campaign recorder preflight' if preflight else 'Earned native Sonya campaign recording',
        file=str(final),SHA256=sha(final),streamed=streamed,encoded=encoded,
        earnedFullCampaignClearVerified=clear is not None,clear=clear,
        subjectiveFullVideoReviewPassed=False,fullPortVerified=False)
    (out/'CAMPAIGN_VIDEO.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Campaign recording ready:',final.name,'frames',clock['frames'],'earned clear',clear is not None,flush=True)


if __name__=='__main__':main()
