"""Native arm voice packed selector, true victim gender, stock cue and packets."""
import copy,json,re,struct,sys
from pathlib import Path
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

def gate(groups,ident,side,ready,stock):
    frame=str(ready+104);actor='01034E90' if side==1 else '010350A0';main='0106A370' if side==1 else '0106B150'
    steps=[r for r in groups['MK2_VOICE_SELECTOR_STEP'] if r['frame']==frame]
    assert [r['entry'] for r in steps]==['FFA12220','FFA123D0','FFA12400','FFA12530']
    assert all(r['age']=='104' and r['role']==str(side) and int(r['victim_id'])==ident and r['a8']==actor and r['a13']==main for r in steps)
    assert steps[0]['a0']=='00000001' and steps[0]['a1']=='8585B8B7'
    base=0xb7 if ident==18 else 0x85
    assert all(int(r['a1'],16)==base for r in steps[1:]) and steps[1]['a0']==steps[2]['a0']=='00000001' and int(steps[3]['a0'],16)==base
    branches=groups['MK2_FINISHER_AUDIO_BRANCH'];assert len(branches)==1;b=branches[0]
    assert b['frame']==frame and b['a8']==b['victim_actor']==actor and b['a13']==b['victim_main']==main and int(b['a2'],16)==int(b['victim_id'])==ident and b['hp']=='0'
    assert b['route']==('female' if ident==18 else 'male') and b['pc']==('FFA123C0' if ident==18 else 'FFA122E0')
    cue=[r for r in groups['MK2_VOICE_SELECTOR_CUE'] if r['frame']==frame];assert len(cue)==1
    header,packet=struct.unpack_from('<HH',stock,(0xffa0ef20-0xff800000)//8+base*4)
    assert int(cue[0]['cue'],16)==base and int(cue[0]['header'],16)==header and int(cue[0]['packet'],16)==packet
    queue=[r for r in groups['MK2_VOICE_PRIORITY_QUEUE'] if r['frame']==frame];assert len(queue)==1;q=queue[0]
    slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}[q['entry']]
    assert int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==packet and q['a8']==actor and q['a13']==main
    pair=[r for r in groups['MK2_FINISHER_AUDIO_PACKET'] if r['frame']==frame and r['a8']==actor and r['a13']==main];assert len(pair)==2
    command=packet+slot
    assert [r['pc'] for r in pair]==['FFA13C90','FFA13D60'] and int(pair[0]['a0'],16)==command
    assert [int(r['data'],16) for r in pair]==[0xff00|(command>>8),0xff00|(command&255)] and all(r['mask']=='FFFF' for r in pair)
    return dict(voiceAge=104,trueID=ident,physicalVictimSlot=side,selectedCue=f'{base:02X}',stockBasePacket=f'{packet:04X}',actualPrioritySlot=slot,actualPacket=f'{command:04X}')

def main(side):
    assert side in (1,2);out=sync.ROOT/f'audit_bounded_jax_arms_voice_priority_p{side}_checked';assert not out.exists()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes();results={}
    for fighter,ident in [('sonya',18),('kano',17)]:
        folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_voice_priority_runtime'
        baseline=sync.ROOT/(f'audit_bounded_{fighter}_jax_arms_finisher_runtime' if side==1 else f'audit_bounded_p2_{fighter}_jax_arms_finisher_runtime')
        old=states(baseline,fighter,side);assert states(folder,fighter,side)==old
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
        groups={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith(('MK2_VOICE_','MK2_FINISHER_AUDIO_')):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['writes']=='0' and r['assistance']=='none'
                groups.setdefault(line.split(' ',1)[0],[]).append(r)
        src=groups['MK2_VOICE_SELECTOR_SOURCE'];assert len(src)==1 and bytes.fromhex(src[0]['hex'])==stock[(0xffa122d0-0xff800000)//8:(0xffa12430-0xff800000)//8]
        ready=int(next(r for tag,r in old if tag=='ACTION')['frame']);positive=gate(groups,ident,side,ready,stock);faults=[]
        for group,key,value in [('MK2_FINISHER_AUDIO_BRANCH','a2','00000000'),('MK2_VOICE_PRIORITY_QUEUE','a3','00000000'),('MK2_FINISHER_AUDIO_PACKET','data','FF00')]:
            bad=copy.deepcopy(groups);next(r for r in bad[group] if int(r['frame'])==ready+104)[key]=value
            try:gate(bad,ident,side,ready,stock)
            except AssertionError:faults.append(group+'.'+key)
            else:raise AssertionError('Fault accepted')
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),heardAudioAccepted=False,allEffectPacketsVerified=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main(int(sys.argv[1]))
