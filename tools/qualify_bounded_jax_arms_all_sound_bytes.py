"""Every observed native high/low command pair in earned arm-rip bounded logs."""
import copy,json,re
from pathlib import Path
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

def gate(packets,begin,end):
    assert packets and len(packets)%2==0
    commands=[]
    for high,low in zip(packets[::2],packets[1::2]):
        assert high['pc']=='FFA13C90' and low['pc']=='FFA13D60' and high['mask']==low['mask']=='FFFF'
        assert high['frame']==low['frame'] and begin<=int(high['frame'])<=end
        assert high['a8']==low['a8'] and high['a13']==low['a13']
        command=int(high['a0'],16);assert command<=65535
        assert int(high['data'],16)==0xff00|(command>>8) and int(low['data'],16)==0xff00|(command&255)
        assert int(low['a0'],16)==int(low['data'],16)
        commands.append(dict(frame=int(high['frame']),command=f'{command:04X}',actor=high['a8'],main=high['a13']))
    return commands

def main():
    out=sync.ROOT/'audit_bounded_jax_arms_all_sound_bytes_checked';assert not out.exists();results={}
    for side in (1,2):
        name='audit_bounded_jax_arms_voice_priority_p1_checked' if side==1 else 'audit_bounded_p2_jax_arms_voice_observed_checked'
        proof_path=sync.ROOT/name/'report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
        for fighter in ('sonya','kano'):
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_voice_priority_runtime'
            assert sync.sha(folder/'run.log')==proof['results'][fighter]['logSha256']
            rows=states(folder,fighter,side);begin=int(next(r for tag,r in rows if tag=='ACTION')['frame']);end=int(next(r for tag,r in rows if tag=='BOUNDED_TERMINAL')['frame'])
            assert end-begin==267;packets=[]
            with (folder/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_FINISHER_AUDIO_PACKET '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['writes']=='0' and r['assistance']=='none';packets.append(r)
            commands=gate(packets,begin,end);faults=[]
            for label,index,key,value in [('wrong_high_byte',0,'data','FF00'),('foreign_low_owner',1,'a8','00000000'),('wrong_low_writer',1,'pc','00000000')]:
                bad=copy.deepcopy(packets);assert bad[index][key]!=value;bad[index][key]=value
                try:gate(bad,begin,end)
                except AssertionError:faults.append(label)
                else:raise AssertionError('Fault accepted')
            results[f'{fighter}P{side}']=dict(commandPairs=len(commands),soundPortBytes=len(packets),nativeCommands=commands,rejectedFaults=faults,logSha256=sync.sha(folder/'run.log'),voiceProofSha256=sync.sha(proof_path))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),allObservedNativePairsVerified=True,allSelectorCallsSourceBound=False,nativeADSPConsumptionVerified=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={key:dict(commandPairs=r['commandPairs'],soundPortBytes=r['soundPortBytes']) for key,r in results.items()})))

if __name__=='__main__':main()
