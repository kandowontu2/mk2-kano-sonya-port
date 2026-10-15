"""Bind true victim packed selector, stock cue, priority slot and sound bytes."""
import copy,json,re,struct
from pathlib import Path
import qualify_bounded_p2_jax_clap_control as control
import verify_native_source_sync as sync

def read(folder,fighter):
    rows=[];groups={}
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if line.startswith('MK2_STOCK_HEAD_V921_'):
                m=control.original.PREFIX.match(line)
                assert m and (m[3],m[4],m[5],m[6],m[7])==(fighter,'2','jax','0','none')
                rows.append((m[1],r))
            elif line.startswith(('MK2_VOICE_','MK2_FINISHER_AUDIO_')):
                assert r['writes']=='0' and r['assistance']=='none'
                groups.setdefault(line.split(' ',1)[0],[]).append(r)
    return rows,groups

def gate(groups,ident,stock):
    frame='3192';base=0x48 if ident==18 else 0x46
    steps=[r for r in groups['MK2_VOICE_SELECTOR_STEP'] if r['frame']==frame]
    assert [r['entry'] for r in steps]==['FFA12220','FFA123D0','FFA12400','FFA12530']
    assert all(r['age']=='55' and r['role']=='2' and int(r['victim_id'])==ident and r['a8']=='010350A0' and r['a13']=='0106B150' for r in steps)
    assert steps[0]['a0']=='00000001' and steps[0]['a1']=='45464748'
    assert all(int(r['a1'],16)==base for r in steps[1:])
    assert steps[1]['a0']==steps[2]['a0']=='00000001' and int(steps[3]['a0'],16)==base
    cue=[r for r in groups['MK2_VOICE_SELECTOR_CUE'] if r['frame']==frame];assert len(cue)==1
    header,packet=struct.unpack_from('<HH',stock,(0xffa0ef20-0xff800000)//8+base*4)
    assert int(cue[0]['cue'],16)==base and int(cue[0]['header'],16)==header and int(cue[0]['packet'],16)==packet
    queue=[r for r in groups['MK2_VOICE_PRIORITY_QUEUE'] if r['frame']==frame];assert len(queue)==1
    q=queue[0];slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}[q['entry']]
    assert slot==1 and int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==packet
    assert q['a8']=='010350A0' and q['a13']=='0106B150'
    pair=[r for r in groups['MK2_FINISHER_AUDIO_PACKET'] if r['frame']==frame];assert len(pair)==2
    command=packet+slot
    assert [r['pc'] for r in pair]==['FFA13C90','FFA13D60'] and int(pair[0]['a0'],16)==command
    assert [int(r['data'],16) for r in pair]==[0xff00|(command>>8),0xff00|(command&255)]
    assert all(r['mask']=='FFFF' and r['a8']==q['a8'] and r['a13']==q['a13'] for r in pair)
    return dict(selectedCue=f'{base:02X}',stockBasePacket=f'{packet:04X}',nativePrioritySlot=slot,actualPacket=f'{command:04X}')

def main():
    out=sync.ROOT/'audit_bounded_p2_jax_voice_priority_checked';assert not out.exists()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes();results={}
    for fighter,ident in [('sonya',18),('kano',17)]:
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_jax_voice_priority_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
        rows,groups=read(folder,fighter)
        old,_=read(sync.ROOT/f'audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime',fighter)
        assert rows==old;physical=control.gate(rows,[],ident)
        src=groups['MK2_VOICE_SELECTOR_SOURCE'];assert len(src)==1
        assert bytes.fromhex(src[0]['hex'])==stock[(0xffa122d0-0xff800000)//8:(0xffa12430-0xff800000)//8]
        positive=gate(groups,ident,stock);faults=[]
        for group,key,value in [('MK2_VOICE_SELECTOR_STEP','a1','00000000'),('MK2_VOICE_PRIORITY_QUEUE','entry','FFA12A10'),('MK2_VOICE_PRIORITY_QUEUE','a8','00000000'),('MK2_FINISHER_AUDIO_PACKET','data','FF00')]:
            bad=copy.deepcopy(groups);next(r for r in bad[group] if r['frame']=='3192')[key]=value
            try:gate(bad,ident,stock)
            except AssertionError:faults.append(group+'.'+key)
            else:raise AssertionError('Fault accepted')
        results[fighter]=dict(**positive,physical=physical,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
