"""Finite original creator-field/recovery source with actual owned current effect writer."""
import copy,json,subprocess
import verify_native_source_sync as sync

def gate(rows,code):
    for wanted in ('ff8b28a0: MOVI   FF8B2DF0h,A7','ff8b28d0: CALLR  FF8B5D20h','ff8b29c0: MOVI   604h,A0','ff8b29e0: MOVE   A0,*A13(1F0h),0','ff8b5eb0: MOVE   A8,*A0(230h),1','ff8b5ed0: MOVE   A13,*A0(250h),1'):
        assert wanted in code,wanted
    action=next(r for r in rows['actualCPUActionSetterRecords'] if r['frame']=='104544')
    hit=next(r for r in rows['actualHPWriterContext'] if r['frame']=='104545' and r['victim_slot']=='2')
    assert action['id']=='4' and action['actor']==action['owner'] and action['before']=='8' and action['after']=='1540' and action['pc']=='FF8B2A00'
    assert hit['ids']=='4,18' and hit['cpu_actor']==action['actor'] and hit['writer230']==action['actor']
    assert hit['writer_actor']==hit['writer_owner'] and hit['writer_actor']!=hit['cpu_actor'] and hit['writer_main']!=hit['cpu_main']
    assert int(hit['before'])-int(hit['after'])==32
    return dict(currentCPURecovery=action,currentIndependentCPUCreated32HPWriter=hit)

def main():
    sync.verify();root=sync.ROOT;out=root/'audit_current_kitana_projectile_creator_context_checked';assert not out.exists()
    reportpath=root/'audit_current_sonya_p2_kitana_ring_spacing_checked/report.json';rows=json.loads(reportpath.read_text())
    rom=root/'mk2/mk2-maincpu.bin';binary=root/'mame-mkp/unidasm.exe'
    assert sync.sha(rom)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    assert sync.sha(binary)=='31E81DA741B36E2417C3304ABEFB0D924C9A1C588134573E53AC2FFDD61B8C36'
    code=''
    for pc,bits in ((0xff8b2800,600),(0xff8b5d20,700)):
        code+=subprocess.run([str(binary),str(rom),'-arch','tms34010','-skip',str((pc-0xff800000)//8),'-count',str(bits),'-basepc',hex(pc),'-norawbytes'],check=True,capture_output=True,text=True).stdout
    proof=gate(rows,code);faults=[]
    for label,badcode in [('lost creator230 source',code.replace('A8,*A0(230h)','A8,*A0(240h)',1)),('wrong recovery604',code.replace('604h,A0','608h,A0',1))]:
        try:gate(rows,badcode)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Source fault admitted')
    for label,key,value in [('wrong current creator','writer230','00000000'),('aliased CPU actor rather than effect','writer_actor',proof['currentCPURecovery']['actor'])]:
        bad=copy.deepcopy(rows);next(r for r in bad['actualHPWriterContext'] if r['frame']=='104545' and r['victim_slot']=='2')[key]=value
        try:gate(bad,code)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Creator fault admitted')
    report=dict(passed=True,**proof,originalConstructorAndRecoveryDisassembly=code,effectiveFaultsRejected=faults,
                scope='Original shared projectile constructor stores creating fighter actor atMain230 and creatingMain at250. Current trueKitana4 recovery setterPCFF8B2A00 plus separate32HPwriter230 equals actualKitana actor supports CPU-created projectile-family attribution. Constructor call/current loaded instructions are not independently tapped here; this source/current-context inference does not name every move, prove fan-lift absence, classify uppers, or credit all32HPevents.',
                namedFanThrowFanLiftUpperAccepted=False,inputHashes={str(p):sync.sha(p) for p in (rom,binary,reportpath)},newEmulatorRuns=0,newMedia=0,fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,faults=len(faults))))

if __name__=='__main__':main()
