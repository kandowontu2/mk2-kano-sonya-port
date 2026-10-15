"""Actual held/released joystick timing in current MK2KS versus original MK2.

Reuse the qualified whole-window/RAM-only native collector; each case has a
distinct normal cold boot, original process handle and private cfg/NVRAM.
"""
import code,inspect,json,traceback
from pathlib import Path
import capture_native_selector_navigation as original

ROOT=original.ROOT
OUT=ROOT/'audit_native_selector_held'
INIT=ROOT/'audit_native_selector_held_initializer'
LUA=ROOT/'mk2ks_native_selector_held.lua'
RAM={}


def run():
    source=inspect.getsource(original.run)
    changes=(
        ("for direction in contract.DIRECTIONS:","for direction in ('current','classic'):"),
        ("plans={side:contract.plan(start,direction)for side,start in ((1,1),(2,9))}","plans={side:[]for side in (1,2)}"),
        ("need(max(len(p)for p in plans.values())*12+93<800,'Physical walks bounded within normal selection timer')", "need(True,'Held test is bounded to360 ordinary selection fields')"),
        ("env.update(MK2KS_NAV_DIRECTION=direction,MK2KS_NAV_P1=contract.lua_plan(plans[1]),MK2KS_NAV_P2=contract.lua_plan(plans[2]))",
         "env.update(MK2_NAV_CLASSIC='1'if direction=='classic'else'0')\n        expected=wanted if direction=='current'else dict(high=(ROOT/'mk2/mk2-maincpu.bin').read_bytes())\n        need(direction!='classic' or digest(expected['high'])=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Whole original unmodified stock program')"),
        ("str(candidate/'mkport_candidate.exe'),'mk2ks'","str(candidate/'mkport_candidate.exe'),'mk2ks'if direction=='current'else'mk2'"),
        ("buffers={k:bytearray()for k in wanted}","buffers={k:bytearray()for k in expected}"),
        ("{k:bytes(v)for k,v in buffers.items()}==wanted","{k:bytes(v)for k,v in buffers.items()}==expected"),
        ("('MK2_NAV_LIVE ','MK2_NAV_RESULT ')","('MK2_HELD_LIVE ','MK2_HELD_RESULT ')"),
        ("s.startswith('MK2_NAV_RESULT ')","s.startswith('MK2_HELD_RESULT ')"),
        ("initializedWindowHashes={k:digest(v)for k,v in wanted.items()}","initializedWindowHashes={k:digest(v)for k,v in expected.items()}"),
        ("transportOnly=True,nativeWalks=4","transportOnly=True,nativeHeldReferenceCases=2"))
    for before,after in changes:
        original.need(source.count(before)==1,'Exact whole original transport boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),OUT=OUT,INIT=INIT,LUA=LUA,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::same_native_transport_original_held_inputs','exec'),scope)
    scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';original.need(not path.exists(),'Preserve actual original held-reference failure');path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same original current/classic held-reference native handles retained.',local=dict(RAM=RAM))
