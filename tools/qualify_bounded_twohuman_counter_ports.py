"""Actual active-low P2 Down/HP reach native reads, not just input labels."""
import json,re
import verify_native_source_sync as sync

def main():
    folder=sync.ROOT/'audit_bounded_twohuman_counter_ports_runtime'
    baseline=sync.ROOT/'audit_bounded_twohuman_bicycle_uppercut_counter_runtime'
    out=folder/'port_admission_check.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    ports={};reads=[];states=[];oldstates=[]
    for location,target in ((folder,states),(baseline,oldstates)):
        with (location/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if line.startswith('MK2_HSPECIAL_FIELD '):target.append(line.strip())
                if location==folder:
                    if line.startswith('MK2_HSPECIAL_PHYSICAL_PORT '):ports[int(r['age'])]=r
                    elif line.startswith('MK2_HSPECIAL_PORT_READ '):reads.append(r)
    assert states==oldstates and set(ports)==set(range(41))
    for age,r in ports.items():
        word=int(r['in0'],16)
        assert bool(word&0x200)==not (9<=age<=20)
        assert bool(word&0x1000)==not (15<=age<=18)
        assert bool(word&0x400)==not (1<=age<=8)
    punch_reads=[r for r in reads if 15<=int(r['age'])<=18]
    assert punch_reads and all(int(r['value'],16)&0x1200==0 and r['at']=='01600000' for r in punch_reads)
    report=dict(passed=True,unchangedActorStateTrace=True,physicalPortFields=41,
        nativeDownPunchReads=punch_reads,requestedInputLatencyFields=1,
        uppercutDispatchProven=False,incomingInterruptionAccepted=False,fullGoalComplete=False,
        terminal=terminal,sourceSync=sync.verify(),logSHA256=sync.sha(folder/'run.log'))
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,physicalPortFields=41,nativeDownPunchReads=len(punch_reads),uppercutDispatchProven=False)))

if __name__=='__main__':main()
