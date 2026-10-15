"""Original ground-pound instructions plus finite current damage correlations."""
import ast
import copy
import json
import re
import struct
import verify_native_source_sync as sync


def main():
    sync.verify();root=sync.ROOT
    out=root/'audit_current_jax_ground_pound_correlation_checked';assert not out.exists()
    old=root/'tools/inspect_jax_137_ground_damage_source_v4805.py'
    tree=ast.parse(old.read_text())
    checks=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHECKS' for t in n.targets)))
    path=root/'mk2/mk2-maincpu.bin';stock=path.read_bytes()
    assert sync.sha(path)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    def source_gate(data):
        for address,words in checks.items():
            start=(address-0xff800000)//8
            assert data[start:start+len(words)*2]==struct.pack('<'+'H'*len(words),*words),hex(address)
    source_gate(stock)
    log=root/'audit_current_sonya_p2_jax_ring_spacing_runtime/run.log'
    report=json.loads((root/'audit_current_sonya_p2_jax_ring_spacing_checked/report.json').read_text())
    assert report['logSHA256']==sync.sha(log)
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.read_text().splitlines() if line.startswith('MK2_NAT_CAMPAIGN_SONYA_JAX_DAMAGE ') and 'cpu_action=311 ' in line and 'victim_slot=2 ' in line]
    def observation_gate(items):
        assert items and all(r['ids']=='11,18' and r['height']=='0' and int(r['before'])-int(r['after'])==21 and r['writes']=='0' and r['assistance']=='none' for r in items)
        block=next(r for r in items if r['frame']=='115768')
        assert block['human_action']=='1792' and block['gap']=='184'
    observation_gate(rows);faults=[]
    for address in (0xff86e070,0xff837c50,0xff837c30,0xff837cb0):
        bad=bytearray(stock);bad[(address-0xff800000)//8]^=1
        try:source_gate(bad)
        except AssertionError:faults.append(dict(kind='stock instruction',address=f'{address:08X}'))
        else:raise AssertionError('Stock instruction mutation admitted')
    for key,value in [('height','1'),('ids','1,18'),('after','0')]:
        bad=copy.deepcopy(rows);bad[0][key]=value
        try:observation_gate(bad)
        except AssertionError:faults.append(dict(kind='current correlation',key=key))
        else:raise AssertionError('Correlation mutation admitted')
    bad=copy.deepcopy(rows);next(r for r in bad if r['frame']=='115768')['human_action']='4'
    try:observation_gate(bad)
    except AssertionError:faults.append(dict(kind='missing actually blocked context'))
    else:raise AssertionError('Blocked-context mutation admitted')
    result=dict(passed=True,nativeActionDecimal=311,nativeActionHex='0137',nativeActionClassification='original ground pound, not a projectile',
                originalInstructionChecks=len(checks),originalDamage=21,
                originalGroundGate='FF837BF0: victim actorVY60 mustzero andYB0 equal victimMainfloor200; caller Carry branchesFF86E020/FF86E060 skipdamage. No Block input test in this gate.',
                currentCorrelatedDamage=rows,effectiveFaultsRejected=faults,
                currentLoadedGroundCodeIndependentlyObserved=False,actualCurrentJumpEvadesDamageProven=False,
                scope='Original stock instruction verification and current passive HP/action/floor correlation only. Runtime caller/Carry capture is still needed for direct causal attribution. Existing block context losing21 is not evidence of a character defect; stock ground gate tests floor/VY, not Block. Next physical controller should prioritize jump edges on actual CPU311 rather than stationary ring startup or floor guard.',
                inputHashes={str(p):sync.sha(p) for p in (old,path,log)},newEmulatorRuns=0,newMedia=0,fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,groundCorrelations=len(rows),faults=len(faults))))


if __name__=='__main__':main()
