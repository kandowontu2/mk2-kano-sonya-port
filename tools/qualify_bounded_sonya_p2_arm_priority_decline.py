"""Native missing pair explained by stock-table request versus all three priorities."""
import copy,json,re,struct
from pathlib import Path
import verify_native_source_sync as sync

def gate(call,decline,stock):
    cue=int(call['cue'],16);header,packet=struct.unpack_from('<HH',stock,(0xffa0ef20-0xff800000)//8+cue*4)
    assert int(call['header'],16)==header and int(call['packet'],16)==packet
    assert decline['pc']=='FFA129E0' and decline['frame']==call['frame'] and decline['a8']==call['a8'] and decline['a13']==call['a13']
    requested=header>>8;priorities=[int(decline['priority'+str(i)]) for i in range(3)]
    assert requested!=0x71 and all(p>requested for p in priorities)
    assert int(decline['a0'],16)==priorities[-1] and int(decline['a1'],16)==requested
    assert int(decline['a3'],16)==packet and int(decline['a4'],16)==header&255
    return dict(cue=f'{cue:02X}',stockHeader=f'{header:04X}',stockBasePacket=f'{packet:04X}',requestedPriority=requested,existingPriorities=priorities,frame=int(call['frame']))

def main():
    out=sync.ROOT/'audit_bounded_sonya_p2_arm_priority_decline_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_sonya_p2_arm_priority_decline_runtime';old=sync.ROOT/'audit_bounded_sonya_p2_jax_arms_voice_priority_runtime'
    t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
    def read(folder):
        original=[];events=[];packets=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith(('MK2_STOCK_HEAD_V921_','MK2_FINISHER_AUDIO_','MK2_VOICE_')):original.append(line)
                if line.startswith(('MK2_ARM_SOUND_CALL ','MK2_ARM_SOUND_DECLINE ')):
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['writes']=='0' and r['assistance']=='none';events.append((line.split(' ',1)[0],r))
                if line.startswith('MK2_FINISHER_AUDIO_PACKET '):packets.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        return original,events,packets
    original,events,packets=read(folder);baseline,_,old_packets=read(old);assert original==baseline and packets==old_packets
    proof=json.loads((sync.ROOT/'audit_bounded_jax_arms_all_sound_bytes_faultsafe_checked/report.json').read_text());assert proof['passed']
    assert sync.sha(old/'run.log')==proof['results']['sonyaP2']['logSha256'] and len(packets)==86
    declines=[(i,r) for i,(tag,r) in enumerate(events) if tag=='MK2_ARM_SOUND_DECLINE'];assert len(declines)==1
    i,d=declines[0];assert i>0 and events[i-1][0]=='MK2_ARM_SOUND_CALL';call=events[i-1][1]
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes();positive=gate(call,d,stock)
    assert not [p for p in packets if p['frame']==d['frame'] and p['a8']==d['a8'] and p['a13']==d['a13']]
    faults=[]
    for key,value in [('priority0','0'),('a3','00000000'),('a8','00000000')]:
        bad=copy.deepcopy(d);bad[key]=value
        try:gate(call,bad,stock)
        except AssertionError:faults.append(key)
        else:raise AssertionError('Fault accepted')
    report=dict(passed=True,nativePriorityDecline=positive,rejectedFaults=faults,allOriginalScalarEventsUnchanged=True,terminal=t,logSha256=sync.sha(folder/'run.log'),baselineSha256=sync.sha(old/'run.log'),checkerSha256=sync.sha(Path(__file__)),sourceSync=sync.verify(),heardAudioAccepted=False,allSelectorCallsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativePriorityDecline=positive,allOriginalScalarEventsUnchanged=True)))

if __name__=='__main__':main()
