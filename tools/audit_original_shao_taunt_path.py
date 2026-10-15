"""Original ROM taunt path, explicitly not runtime timing/strategy proof."""
import json,struct,subprocess
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;stock=root/'mk2/mk2-maincpu.bin';exe=root/'mame-mkp/unidasm.exe'
out=root/'audit_original_shao_taunt_path_checked';assert not out.exists()
assert sync.sha(stock)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
data=stock.read_bytes()
assert struct.unpack_from('<I',data,(0xff9b1db0-0xff800000)//8+13*4)[0]==0xff9d0760
listing=subprocess.check_output([str(exe),str(stock),'-arch','tms34010','-skip',str((0xff9d0cf0-0xff800000)//8),'-count','1536','-basepc','0xff9d0cf0','-norawbytes'],text=True)
needles=['ff9d0f30: MOVK   6h,A0','ff9d0f40: CALLA  FF80EAE0h',
 'ff9d0fd0: CALLA  FFA12430h','ff9d1000: MOVI   18h,A9',
 'ff9d1020: CALLA  FF906090h','ff9d10d0: MOVI   Ah,A0',
 'ff9d10f0: CALLA  FF80DCC0h','ff9d11a0: MOVI   Ah,A0',
 'ff9d11c0: CALLA  FF80DCC0h','ff9d12f0: JR     FF9D3D50h']
def gate(text):assert all(n in text for n in needles)
gate(listing)
for n in needles:
    try:gate(listing.replace(n,'',1))
    except AssertionError:pass
    else:raise AssertionError('Missing original path accepted')
assert list(struct.unpack_from('<6H',data,(0xff9d1460-0xff800000)//8))==list(range(0x43,0x49))
loaded=json.loads((root/'audit_current_loaded_dispatch_boundaries_preparation/expected.json').read_text())
assert loaded['tables']['decision']['values'][13]==0xff9d0760
proof=root/'audit_current_loaded_dispatch_boundaries_checked/report.json'
assert json.loads(proof.read_text())['passed']
out.mkdir();(out/'original-taunt.txt').write_text(listing)
report=dict(originalShaoDecisionEntry='FF9D0760',tauntPath='FF9D0CF0..FF9D12F0',
    originalRngCallRetained='FF80EAE0',announcerTableIDs=list(range(0x43,0x49)),
    animationIndex=24,twoExplicitWaitsOf10Fields=True,missingInstructionFaultsRejected=len(needles),
    stockSHA256=sync.sha(stock),currentLoadedDispatchEvidenceSHA256=sync.sha(proof),
    runtimeTauntObserved=False,completeTauntDurationMeasured=False,winningControllerProved=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
