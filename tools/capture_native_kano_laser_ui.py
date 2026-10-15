"""Full original four-case UI state/pixel suite on the actual current build.

Original physical controls unchanged; genuine combat startup ownership is
allowed only by the existing source-bound owner gate. All19 channels and the
new private finisher pool are observed throughout. Raw media stay in RAM.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_launch_candidate_ui as ui
import capture_native_kano_laser_audio as audio
import qualify_native_current_ui_audio_owners as owners
import kano_ball_launch_context_v6642 as graphics
import serve_native_current_ui_ram as preview

ROOT,need,sha=audio.ROOT,audio.need,audio.sha
BASE=ROOT/'audit_native_kano_laser_ui_ram'
OUT=ROOT/'audit_native_kano_laser_ui_checked'
INIT=ROOT/'audit_native_kano_laser_ui_initializer_source'
LUA=ROOT/'mk2ks_native_kano_laser_ui.lua'
GUARD=ROOT/'audit_native_kano_laser_ui_lua_globals_source/report.json'


def expectation():
    need(not INIT.exists(),'Fresh immutable current UI initializer proof');INIT.mkdir()
    factory=inspect.getsource(audio.functions)
    need(factory.count("return scope['run']")==1,'Exact full current initializer factory')
    factory=factory.replace("return scope['run']",'return scope')
    scope=dict(vars(audio),__file__=__file__)
    exec(compile(factory,__file__+'::exact_current_source_initializer_factory','exec'),scope)
    guest,build=scope['functions']()['expected'](INIT)
    need(graphics.PAYLOAD_SHA==build['payload_sha256'],'Entire current graphics payload equals original independent decoder input')
    gfx=graphics.expected_gfx()
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(audio.__file__).resolve()):sha(audio.__file__),
          str(Path(graphics.__file__).resolve()):sha(graphics.__file__),str(ROOT/audio.NAME/'build-info.json'):sha(ROOT/audio.NAME/'build-info.json')}
    (INIT/'report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,
        wholeExpectedGuestSHA256=build['expected_guest_sha256'],wholeExpectedGFXSHA256=ui.hashlib.sha256(gfx).hexdigest().upper(),
        wholeExpectedGuestBytes=len(guest),wholeExpectedGFXBytes=len(gfx),inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        latestPlayableChanged=False,goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
    return guest,gfx,build


def owner_gate():
    source=inspect.getsource(owners.gate)
    for old,new in [('terminal*14','terminal*19'),('range(14)','range(19)')]:
        need(source.count(old)==1,'Entire original owner coverage extended, not narrowed');source=source.replace(old,new)
    scope=dict(vars(owners),__file__=__file__)
    exec(compile(source,__file__+'::entire19channel_cold_and_genuine_combat_ownership','exec'),scope)
    return scope['gate']


def run():
    need(not BASE.exists() and not OUT.exists() and not ui.identity.census(),'Fresh four-case native run; no live-job replay')
    guard=json.loads(GUARD.read_text())
    need(guard['passed'] and guard['actualNativeParserAccepted'] and guard['wholePhysicalUIByteIdentical'] and
         guard['totalSampleChannels']==19 and not guard['gameplayAccepted'] and all(sha(p)==h for p,h in guard['inputHashes'].items()),
         'Real native Lua compiler proves entire original physical callback and19-channel observer')
    guest,gfx,build=expectation()
    current=SimpleNamespace(ROOT=ROOT,NAME=audio.NAME,EXE_SHA=build['executable_sha256'],GUEST_SHA=build['expected_guest_sha256'],
                            PAYLOAD_SHA=build['payload_sha256'],__file__=__file__,expected=lambda:guest,expected_gfx=lambda:gfx)
    gate=owner_gate();source=inspect.getsource(ui.capture)
    first=source.index('  need(len(owner_rows)==');last=source.index('  need(all(sha(p)==h for p,h in pins.items())',first)
    replacement='''  ownership=owner_gate(text,state['terminal'])
  pools=pool_rows(text,'MK2_UI_FINISH_POOL')
  need(len(pools)==state['terminal'] and [int(r['frame']) for r in pools]==list(range(1,state['terminal']+1)) and
       all(r['actor']==r['main']=='00000000' and r['slot']=='0' and r['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0' and
           r['writes']=='0' and r['assistance']=='none' for r in pools),'Every actual new finisher owner/priority/timer remains clear through full selection/ladder/first match')
  private_channels=[r for r in pool_rows(text,'MK2_UA_CHANNEL') if 14<=int(r['channel'])<=18]
  need(len(private_channels)==5*state['terminal'] and all(r['sample']=='4294967295' and r['length']=='0' and float(r['pos'])==0 for r in private_channels),
       'All five actual new finish sounds remain unowned/inactive, no selection/ladder alias')
'''
    source=source[:first]+replacement+source[last:]
    old='completeColdBattleOwnerFields=len(owner_rows),'
    need(source.count(old)==1,'Actual complete owner report boundary')
    source=source.replace(old,'actualBattleOwnerFields=len(owner_rows),sourceBoundOwnership=ownership,completeFinisherPoolFields=len(pools),')
    ui.BASE=BASE;ui.OUT=OUT;ui.LUA=LUA;ui.current=current
    scope=dict(vars(ui),__file__=__file__,current=current,BASE=BASE,OUT=OUT,LUA=LUA,owner_gate=gate,pool_rows=owners.rows)
    exec(compile(source,__file__+'::whole_original_UI_capture_plus_complete_source_bound_ownership','exec'),scope)
    ui.capture=scope['capture']
    whole_run=inspect.getsource(ui.run)
    old='for p in(Path(__file__),'
    new='for p in(Path(__file__),GUARD,INIT/"report.json",ROOT/"mk2ks_native_kano_laser_ui_channels.lua",ROOT/"mk2ks_launch_candidate_ui.lua",Path(owners.__file__),Path(audio.__file__),Path(graphics.__file__),'
    need(whole_run.count(old)==1,'All original executed-input pins plus complete new observer/source guards')
    whole_run=whole_run.replace(old,new)
    scope=dict(vars(ui),__file__=__file__,GUARD=GUARD,INIT=INIT,owners=owners,audio=audio,graphics=graphics)
    exec(compile(whole_run,__file__+'::all_four_original_state_pixel_fault_suites','exec'),scope)
    report=scope['run']()
    need(all(sha(p)==h for p,h in guard['inputHashes'].items()),'Same fully parsed observer/candidate preserved through all four native terminals')
    return report


if __name__=='__main__':
    try:accepted=run()
    except Exception as error:
        need(not OUT.exists(),'Never overwrite original accepted/failed UI result');OUT.mkdir()
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            completedCases=ui.COMPLETED,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=preview.serve(ui.RAM_CASES)
    code.interact(banner='Same actual UI jobs terminal; original rasters/PCM remain RAM-only.',local=dict(ui=ui,cases=ui.RAM_CASES,server=server))
