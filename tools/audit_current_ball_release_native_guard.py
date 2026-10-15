"""Source/ROM guard path and existing observed pre-entry states, not exhaustive runtime proof."""
import json,subprocess
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
out=root/'audit_current_ball_release_native_guard'
assert not out.exists()
source_path=root/'mame-mkp/src/mame/midway/midtunit_m.cpp'
source=source_path.read_text()
start=source.index('\temit(ball_parser,')
end=source.index('\n\t// Same short native body-push',start)
parser=source[start:end]
def source_guard(text):
    assert '0x0b41, 0xffaf, 0xc280, 0x7420, 0xff87' in text
    assert '0xc080, 0x71f0, 0xff87' in text
    assert 'write32(0xff4f0 + 17 * 4, native_address(ball_parser))' in text
source_guard(parser)
rejected=[]
for name,token in [('missing_native_launch_helper','0xc080, 0x71f0, 0xff87'),('wrong_roster_slot','17 * 4'),('missing_charge_reject','0x0b41, 0xffaf, 0xc280, 0x7420, 0xff87')]:
    try:source_guard(parser.replace(token,'REMOVED'))
    except AssertionError:rejected.append(name)
    else:raise AssertionError(name)
rom=root/'mk2/mk2-maincpu.bin'
dis=subprocess.run([str(root/'mame-mkp/unidasm.exe'),str(rom),'-arch','tms34010','-skip','60990','-count','768','-basepc','0xff8771f0'],capture_output=True,text=True,timeout=10)
assert dis.returncode==0 and not dis.stderr
for text in ('ff8771f0:','ff8772c0:','ANDI   1Ch,A4','ff8772f0:','JRNE   FF877420h','ff8773a0:','MOVI   FF861350h,A7'):
    assert text in dis.stdout,text
folder=root/'audit_current_kano_kunglao_ball_recovery_fixed_runtime'
rows=chronology.load(folder/'run.log')
entries=[]
for entry in rows['KANO_KUNGLAO_NATIVE_BALL']:
    prior=[r for r in rows['KUNGLAO_ACTION_CHANGE'] if int(r['frame'])<int(entry['frame']) and r['p1_actor']==entry['actor'] and r['p1_main']==entry['main']]
    assert prior
    last=prior[-1]
    entries.append(dict(entry=entry,lastEarlierActionChange=last,observationAge=int(entry['frame'])-int(last['frame']),earlierHurtBusyBits=int(last['flags'].split(',')[0],16)&0x1c))
out.mkdir();(out/'native_helper_disassembly.txt').write_text(dis.stdout)
report=dict(auditCompleted=True,sourceSHA256=sync.sha(source_path),originalROM_SHA256=sync.sha(rom),actualLogSHA256=sync.sha(folder/'run.log'),nativeLKReleaseSlot=17,chargeThresholdTicks=80,sharedNativeHelper='FF8771F0',sharedHelperRejectsFlagsMask='1C',sourceMutationsRejected=rejected,observedPreEntryStates=entries,exactFlagsAtInstructionAccepted=False,exhaustiveVictimGuardRuntimeAccepted=False,gameDefectEstablished=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(auditCompleted=True,sharedNativeHelper=True,preEntryEarlierBusyMasks=[r['earlierHurtBusyBits'] for r in entries],exhaustiveRuntimeAccepted=False)))
