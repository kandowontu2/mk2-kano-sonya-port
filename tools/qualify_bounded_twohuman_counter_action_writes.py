"""Bind the observed counter to real native high-punch, not uppercut."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    folder=sync.ROOT/'audit_bounded_twohuman_counter_action_writes_runtime'
    base=sync.ROOT/'audit_bounded_twohuman_counter_ports_runtime'
    out=folder/'action_store_check.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    actions=[];trace=[];old=[]
    for location,target in ((folder,trace),(base,old)):
        with (location/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith(('MK2_HSPECIAL_FIELD ','MK2_HSPECIAL_PHYSICAL_PORT ')):target.append(line.strip())
                if location==folder and line.startswith('MK2_HSPECIAL_ACTION_WRITE '):actions.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    assert trace==old and len(actions)==4
    assert [(r['before'],r['value'],r['pc']) for r in actions]==[
        ('0303','0000','FF830B20'),('0000','0101','FF83C340'),
        ('0101','0000','FF8428A0'),('0000','0215','FFF9AEA0')]
    assert all(r['writes']=='0' and r['assistance']=='none' and r['mask']=='FFFF' and int(r['at'],16)==int(r['main'],16)+0x1f0 for r in actions)
    assert actions[1]['a8']=='010350A0' and actions[1]['a13']==actions[1]['main']
    reference=sync.ROOT/'tools/verify_current_human_uppercut_clean_v2153.py'
    uppercut=sync.ROOT/'tools/verify_current_boss_human_uppercut_campaign_v2148.py'
    assert "['action']==0x101" in reference.read_text() and "r['after']==0x107" in uppercut.read_text()
    report=dict(passed=True,nativeActionStores=actions,unchangedPhysicalPortsAndActorFields=True,
        actualAttackAction='0101 high punch',requestedUppercutAction107Observed=False,
        causeOfCrouchAdmissionUnproven=True,fullGoalComplete=False,terminal=terminal,
        sourceSync=sync.verify(),pins={str(p):sync.sha(p) for p in (folder/'run.log',base/'run.log',reference,uppercut,Path(__file__))})
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,actionStores=4,actualAttack='0101',uppercut107Observed=False)))

if __name__=='__main__':main()
