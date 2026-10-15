"""Original release-to-rise path; candidate controller loop, not runtime proof."""
import json,subprocess
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;out=root/'audit_original_crouch_guard_release_path_checked'
assert not out.exists()
rom=root/'mk2/mk2-maincpu.bin';exe=root/'mame-mkp/unidasm.exe'
def decode(pc,count):
    return subprocess.check_output([str(exe),str(rom),'-arch','tms34010','-skip',str((pc-0xff800000)//8),'-count',str(count),'-basepc',hex(pc),'-norawbytes'],text=True).replace('\r','')
guard=decode(0xff830300,320);rise=decode(0xff82fc30,480);inputs=decode(0xff831fc0,640)
def verify(g,r,i):
    assert g.index('ff830320: BTST   1h,A0')<g.index('ff830330: JREQ   FF82FC30h')
    assert 'ff830380: MOVI   701h,A0' in g
    assert 'ff82fcc0: JA     FF82FD70h' in r
    assert 'ff82fd70: MOVI   301h,A1' in r and 'ff82fd90: MOVE   A1,*A13(1F0h),0' in r
    assert 'ff831ff0: NOT    A0' in i and 'ff832000: ANDI   Fh,A0' in i
verify(guard,rise,inputs)
faults=[]
for label,g,r,i in [('missing_release_branch',guard.replace('FF82FC30h','FF82FA40h'),rise,inputs),('wrong_rising_action',guard,rise.replace('301h','302h'),inputs)]:
    try:verify(g,r,i)
    except (AssertionError,ValueError):faults.append(label)
    else:raise AssertionError('Invalid release path accepted')
controller=(root/'audit_current_sonya_p2_baraka_ready_forwardjump_preparation/campaign.lua').read_text()
start=controller.index("   elseif fighter=='sonya' and side==2 and other.roster==3 then\n")
branch=controller[start:controller.index('   elseif leg_tactic',start)]
assert 'human.action==769' not in branch and "else press('Down');press('Block')end" in branch
report=dict(passedOriginalControlFlowChecks=True,originalROM_SHA256=sync.sha(rom),controllerSHA256=sync.sha(root/'audit_current_sonya_p2_baraka_ready_forwardjump_preparation/campaign.lua'),originalCrouchGuardAction=1793,originalRisingAction=769,risingActionExcludedFromTrialReadiness=True,trialFallbackReassertsDownBlock=True,controllerFeedbackLoopCandidate=True,actualRuntimeCauseProven=False,loadedCurrentCodeDirectlyObserved=False,rejectedFaults=faults,fullPortAccepted=False)
out.mkdir()
for name,body in [('guard-release.txt',guard),('rise.txt',rise),('input-read.txt',inputs)]:
    (out/name).write_text(body)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
