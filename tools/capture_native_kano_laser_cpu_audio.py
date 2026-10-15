"""Natural campaign/post-ending CPU decisions; physical input/passive whole audio.

Same native handle to terminal. Never restart on an observation timeout.
No new build/ROM/ZIP; native whole media are held only in RAM.
"""
import code
import inspect
import json
import re
from pathlib import Path
import capture_native_kano_laser_audio as original
import run_extended_sonya_p1_campaign_v5207 as campaign

ROOT,need,sha=original.ROOT,original.need,original.sha
LUA=ROOT/'mk2ks_native_kano_laser_cpu_audio.lua'
CONTROLLERS=[LUA,ROOT/'mk2ks_native_kano_laser_cpu_campaign.lua',ROOT/'mk2ks_native_sonya_p1_postending_kano.lua',
             ROOT/'mk2ks_native_kano_p2_postending_sonya.lua',*[ROOT/n for n in campaign.CONTROLLERS],
             ROOT/'mk2ks_native_kano_laser_audio.lua',ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua']


def run():
    guard_path=ROOT/'audit_native_kano_laser_cpu_audio_lua_source/report.json'
    guard=json.loads(guard_path.read_text())
    need(guard['passed'] and guard['actualNativeParserAccepted'] and not guard['gameplayAccepted'],
         'Actual private-candidate Lua parser, not invented gameplay proof')
    pins=dict(guard['inputHashes'])
    for path in [Path(__file__),Path(original.__file__),*CONTROLLERS]:pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All actually parsed/executed sources conserved')
    # The unchanged controller's obsolete file sink is removed by its existing
    # qualified RAM-only wrapper before execution; never allow a gameplay writer.
    for path in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',path.read_text()),'Physical inputs/passive reads only')
    accepted=json.loads((ROOT/'audit_v5214_extended_sonya_p1_whole_campaign_checked/report.json').read_text())
    need(accepted['passed'] and accepted['case']['unassisted_clear_proven'],'Previously actually earned complete Sonya campaign')
    receipt=accepted['case'].get('inputHashes',accepted.get('inputHashes',{}))
    for name in campaign.CONTROLLERS:need(receipt[str(ROOT/name)]==sha(ROOT/name),'Original entire tested campaign unchanged')
    runner=original.functions()
    source=inspect.getsource(runner)
    changes=[("out=ROOT/f'audit_native_kano_laser_audio_p{side}'","out=ROOT/'audit_native_kano_laser_cpu_audio'"),
             ("env['MK2KS_LASER_SIDE']=str(side)","env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1',MK2KS_CAMPAIGN_STRATEGY='guard_punish',MK2KS_BOSS_PHYSICAL_POLICY='shao_ring_retreat',MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900',MK2KS_TEST_BOOT_FRAME='600',MK2KS_CAMPAIGN_OUT=str(out),MK2KS_TWO_PLAYER='0')"),
             ("'-str','180'","'-str','2400'"),
             ("if tag=='MK2_LASER_GUEST':","if tag in ('MK2_LASER_GUEST','MK2_CAMPAIGN_GUEST_RAM'):"),
             ("elif tag=='MK2_LASER_RGB':","elif tag in ('MK2_LASER_RGB','MK2_CAMPAIGN_RAM_FRAME'):"),
             ("'MK2_LASER_RESULT ','MK2_LASER_OVERRUN '","'MK2_LASER_RESULT ','MK2_LASER_OVERRUN ','MK2_LASER_CPU_FIRST_DISPATCH ','MK2_LASER_CPU_SECOND_DISPATCH ','MK2_LASER_CPU_LASER_GUARD ','MK2_LASER_CPU_CONTINUE_LOSS ','MK2_POSTENDING_MATCH ','MK2_NAT_CAMPAIGN_STAGE ','MK2_NAT_CAMPAIGN_ENDING_START ','MK2_NAT_CAMPAIGN_ENDING_COMPLETED '")]
    for old,new in changes:
        need(source.count(old)==1,'Exact source-bound whole transport adaptation: '+old);source=source.replace(old,new)
    scope=dict(runner.__globals__,__file__=__file__,LUA=LUA)
    exec(compile(source,__file__+'::whole_CPU_physical_audio_transport','exec'),scope)
    capture=scope['run'](2);capture['victimID']=17
    need(all(sha(p)==h for p,h in pins.items()),'Same native process terminal with all executed inputs immutable')
    (capture['folder']/'checked_observer_sources.json').write_text(json.dumps(dict(passed=True,sourceOnlyGuard=True,
        nativeAudioAccepted=False,inputHashes=pins,totalSampleChannels=19,victimID=17,goalStatus='active',latestPlayableChanged=False),indent=2)+'\n')
    return capture


if __name__=='__main__':
    capture=run();server=original.transport.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']),pcmCallbacks=len(capture['pcm']))),flush=True)
    code.interact(banner='Same native CPU trial terminal; full native media in RAM.',local=dict(capture=capture,server=server))
