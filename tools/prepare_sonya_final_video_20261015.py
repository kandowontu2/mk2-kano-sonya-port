"""Prepare recording only from an independently qualified complete campaign."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_final_20261015_preparation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()

def main():
    pa=argparse.ArgumentParser();pa.add_argument('benchmark');a=pa.parse_args()
    assert re.fullmatch('[a-z0-9_]+',a.benchmark) and not OUT.exists()
    case=ROOT/a.benchmark;proof=json.loads((case/'qualification.json').read_text())
    assert proof['passed'] and proof['proof']['fullNativeCampaignAndOwnEnding'] and len(proof['faultsRejected'])==6
    launch=json.loads((case/'launch.json').read_text());controller=Path(launch['command'][-1])
    assert controller.resolve().is_relative_to(ROOT) and sha(controller)==proof['sourceSHA256']==launch['luaSHA256']
    body=controller.read_text()
    assert ':write_' not in body and ':pixels(' not in body and ':snapshot(' not in body and 'io.open' not in body
    old=ROOT/'video_sonya_early_ladder_20261015_preparation'
    capture=(old/'campaign.lua').read_text().split('-- Stream every native video frame.',1)[1]
    assert 'video_frames<=200001' in capture and 'VIDEO_FULL_STOP' in capture
    lua=body+'\n-- Stream every native video frame.'+capture
    assert lua.startswith(body) and lua[len(body):].count('register_frame_done')==1
    OUT.mkdir();(OUT/'campaign.lua').write_text(lua)
    runner=(old/'run.py').read_text()
    runner=runner.replace('video_sonya_early_ladder_20261015','video_sonya_final_20261015')
    assert sha(old/'campaign.lua') in runner
    runner=runner.replace(sha(old/'campaign.lua'),sha(OUT/'campaign.lua'))
    # Fail immediately and release synchronous pipe if native boot fails before
    # Lua opens the stream; do not wait for a600sec encoder timeout.
    marker='  while any(p.poll() is None for _,p,_ in processes):\n'
    assert runner.count(marker)==1
    runner=runner.replace(marker,marker+'''   if game.poll() is not None and stream['bytes']==0:
    limits.append('game_exit_before_video_pipe')
    try:
     with open(pipe_name,'wb'):pass
    except OSError:pass
''',1)
    ast.parse(runner);(OUT/'run.py').write_text(runner)
    (OUT/'preparation.json').write_text(json.dumps(dict(benchmark=a.benchmark,benchmarkProofSHA256=sha(case/'qualification.json'),benchmarkSourceSHA256=sha(controller),luaSHA256=sha(OUT/'campaign.lua'),runnerSHA256=sha(OUT/'run.py'),benchmarkResult=proof['proof'],physicalPolicyByteConserved=True,onlyAddition='Passive native-screen BGRA streaming; unchanged controller and ending observers',expectedPeakMemoryMiB='native~125,encoder~70,host~22;caps320/384/128',temporaryWAVCapMiB=750,videoCapMiB=450,wallCapSeconds=600,recordingNotYetRun=True),indent=2))
    print(OUT)

if __name__=='__main__':main()
