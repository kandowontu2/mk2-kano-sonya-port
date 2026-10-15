"""Original native control-flow proof: post-handoff action0 is not pre-catch idle."""
import json,subprocess
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
out=root/'audit_original_throw_handoff_observation_order_checked'
assert not out.exists()
exe=root/'mame-mkp/unidasm.exe';rom=root/'mk2/mk2-maincpu.bin'
def decode(skip,count,pc):
    return subprocess.check_output([str(exe),str(rom),'-arch','tms34010','-skip',str(skip),'-count',str(count),'-basepc',pc,'-norawbytes'],text=True).replace('\r','')
throw=decode(93616,900,'0xff8b6d80')
handoff=decode(34022,650,'0xff842730')
def verify(a,b):
    assert a.index('ff8b6f30: CALLA  FF842730h')<a.index('ff8b6f80: MOVE   A0,*A13(1F0h),0')<a.index('ff8b6fa0: MOVE   *A13(170h),A1,1')
    assert b.index('ff842850: MOVE   *A13(170h),A13,1')<b.index('ff842870: CLR    A0')<b.index('ff842880: MOVE   A0,*A13(1F0h),0')<b.index('ff8428f0: MOVE   A4,*A13(210h),0')
verify(throw,handoff)
faults=[]
for label,a,b in [('missing_handoff_call',throw.replace('CALLA  FF842730h','CALLA  FF842710h'),handoff),('missing_victim_action_clear',throw,handoff.replace('ff842880: MOVE   A0,*A13(1F0h),0','ff842880: MOVE   A0,*A13(220h),0'))]:
    try:verify(a,b)
    except (AssertionError,ValueError):faults.append(label)
    else:raise AssertionError('Incorrect control flow accepted')
source=(root/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
assert 'constexpr unsigned ground_throw_lookup = 0xfc200;' in source
assert 'emit(rom_offset(0xff8b6e30)' in source
assert '0x09c9,0x002b,0x0d5f,0x2d90,0xff84,0xc080,0x6e80,0xff8b' in source
report=dict(passedOriginalControlFlowChecks=True,originalROM_SHA256=sync.sha(rom),disassemblerSHA256=sync.sha(exe),compiledSourceSHA256=sync.sha(root/'mame-mkp/src/mame/midway/midtunit_m.cpp'),postHandoffCheckpoint='FF8B6FA0',victimActionClearedAt='FF842880',victimHitFlagWrittenAt='FF8428F0',postHandoffHumanZeroIsNotPreCatchIdleProof=True,nextPreHandoffCheckpoint='FF8B6C60',currentGroundLookupPatchPreservesAttackerAndVictimIDs=True,loadedCurrentHandoffBytesDirectlyObserved=False,rejectedControlFlowFaults=faults,fullPortAccepted=False)
out.mkdir();(out/'original-ground-throw.txt').write_text(throw);(out/'original-victim-handoff.txt').write_text(handoff);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
