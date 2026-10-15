"""Original selector/counter/probability gates; no assumed match reset cadence."""
import json,struct,subprocess
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;stock=root/'mk2/mk2-maincpu.bin';exe=root/'mame-mkp/unidasm.exe'
out=root/'audit_original_shao_taunt_limits_checked';assert not out.exists()
assert sync.sha(stock)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
def dis(at,bits):return subprocess.check_output([str(exe),str(stock),'-arch','tms34010','-skip',str((at-0xff800000)//8),'-count',str(bits),'-basepc',hex(at),'-norawbytes'],text=True)
path=dis(0xff9d0cf0,576);selector=dis(0xff9b1820,112);probability=dis(0xff9b1420,208)
needles=['ff9d0d60: MOVI   FF9D13C0h,A0','ff9d0d90: CALLA  FF9B1820h',
 'ff9d0dc0: MOVE   @1061F30h,A1,0','ff9d0df0: CMP    A0,A1',
 'ff9d0e00: JRHI   FF9CBC30h','ff9d0e50: CALLA  FF9B1420h',
 'ff9d0e80: JRNC   FF9CBC30h','ff9d0ed0: INC    A1','ff9d0ee0: MOVE   A1,@1061F30h,0']
def gate(text):assert all(n in text for n in needles)
gate(path)
for n in needles:
    try:gate(path.replace(n,'',1))
    except AssertionError:pass
    else:raise AssertionError('Removed stock gate accepted')
assert 'ff9b1820: MOVE   @1061AD0h,A14,0' in selector
assert 'ff9b1870: MOVE   *A14,A0,0' in selector
assert 'ff9b1420: MOVE   @1061AD0h,A1,0' in probability
assert 'ff9b14c0: JA     FF80EC20h' in probability
thresholds=list(struct.unpack_from('<10H',stock.read_bytes(),(0xff9d13c0-0xff800000)//8))
assert thresholds==[10,10,10,6,5,4,4,3,3,2]
report=dict(originalTableThresholds=thresholds,selectorAddress='01061AD0',counterAddress='01061F30',
    counterRejectsGreaterThanSelectedThreshold=True,additionalProbabilityGate=True,
    missingGateFaultsRejected=len(needles),counterResetCadenceProved=False,
    runtimeSelectorValueObserved=False,tauntOnlyWinningStrategyProved=False,fullPortAccepted=False,
    stockSHA256=sync.sha(stock),caveat='Do not turn these thresholds into a per-round taunt count without observing counter reset timing.')
out.mkdir();(out/'original-gates.txt').write_text(path+selector+probability)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
