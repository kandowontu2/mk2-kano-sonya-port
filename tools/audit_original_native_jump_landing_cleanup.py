"""Original normal landing clears velocity; not a blanket victim-phase claim."""
import json,subprocess
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
out=root/'audit_original_native_jump_landing_cleanup_checked'
assert not out.exists()
exe=root/'mame-mkp/unidasm.exe';rom=root/'mk2/mk2-maincpu.bin'
def decode(pc,count):
    return subprocess.check_output([str(exe),str(rom),'-arch','tms34010','-skip',str((pc-0xff800000)//8),'-count',str(count),'-basepc',hex(pc),'-norawbytes'],text=True).replace('\r','')
jump=decode(0xff831320,768)
land=decode(0xff876660,1600)
stop=decode(0xff831a60,160)
zero=decode(0xff80f6b0,160)
def verify(j,l,s,z):
    assert 'ff831320: MOVI   308h,A0' in j and 'ff831340: MOVE   A0,*A13(1F0h),0' in j
    assert 'ff8314e0: JA     FF876660h' in j
    assert l.index('ff876a60: CMP    A0,A1')<l.index('ff876ab0: CALLA  FF831A60h')
    assert 'ff831a60: CALLA  FF80F6B0h' in s
    assert z.index('ff80f6d0: CLR    A1')<z.index('ff80f6e0: MOVE   A1,*A8(40h),1')<z.index('ff80f700: MOVE   A1,*A8(60h),1')
verify(jump,land,stop,zero)
faults=[]
for name,parts in [('missing_landing_stop_call',(jump,land.replace('FF831A60h','FF831A90h'),stop,zero)),('missing_vertical_velocity_clear',(jump,land,stop,zero.replace('*A8(60h)','*A8(80h)'))),('wrong_jump_action',(jump.replace('308h','309h'),land,stop,zero))]:
    try:verify(*parts)
    except (AssertionError,ValueError):faults.append(name)
    else:raise AssertionError('Bad native control-flow accepted')
report=dict(passedOriginalControlFlowChecks=True,originalROM_SHA256=sync.sha(rom),disassemblerSHA256=sync.sha(exe),normalJumpAction=776,normalLandingClearsActorVelocityOffsets=['40','60'],zeroVerticalVelocityGateNotDisprovedByNormalLanding=True,rejectedControlFlowFaults=faults,loadedCurrentRoutineDirectlyObserved=False,victimRecoveryOrGuardHandoffProven=False,fullPortAccepted=False)
out.mkdir()
for name,body in [('jump.txt',jump),('landing.txt',land),('stop.txt',stop),('zero-velocity.txt',zero)]:
    (out/name).write_text(body)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
