"""Actual three victim effect calls: stock table, priority, ordered port bytes."""
import copy,json,re,struct
from pathlib import Path
import verify_native_source_sync as sync

def gate(events,side,actor,main,stock):
    selected=[(i,r) for i,(tag,r) in enumerate(events) if tag=='MK2_VOICE_SELECTOR_CUE' and int(r['cue'],16) in (0xa3,0xa5,0xa4)]
    assert [int(r['cue'],16) for _,r in selected]==[0xa3,0xa5,0xa4]
    result=[]
    for (index,c),age in zip(selected,(211+side,211+side,351+side)):
        cue=int(c['cue'],16)
        header,base=struct.unpack_from('<HH',stock,(0xffa0ef20-0xff800000)//8+cue*4)
        assert int(c['header'],16)==header and int(c['packet'],16)==base
        tail=events[index+1:];assert len(tail)>=3
        (tag,q),(htag,high),(ltag,low)=tail[:3]
        assert (tag,htag,ltag)==('MK2_VOICE_PRIORITY_QUEUE','MK2_FINISHER_AUDIO_PACKET','MK2_FINISHER_AUDIO_PACKET')
        assert q['age']==str(age) and all(r['frame']==c['frame'] for r in (q,high,low))
        assert all(r['a8']==actor and r['a13']==main for r in (q,high,low))
        slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}[q['entry']]
        assert int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==base
        command=base+slot
        assert high['pc']=='FFA13C90' and low['pc']=='FFA13D60' and high['mask']==low['mask']=='FFFF'
        assert int(high['a0'],16)==command
        assert int(high['data'],16)==0xff00|(command>>8) and int(low['data'],16)==0xff00|(command&255)
        assert int(low['a0'],16)==int(low['data'],16)
        result.append(dict(cue=f'{cue:02X}',age=age,stockHeader=f'{header:04X}',stockBase=f'{base:04X}',prioritySlot=slot,command=f'{command:04X}'))
    return result

def main():
    out=sync.ROOT/'audit_bounded_kitana_kiss_effect_dispatch_checked';assert not out.exists()
    voice_path=sync.ROOT/'audit_bounded_kitana_kiss_voice_choice_checked/report.json'
    proof=json.loads(voice_path.read_text());assert proof['passed']
    stock_path=sync.ROOT/'mk2/mk2-maincpu.bin';stock=stock_path.read_bytes();results={}
    for side in (1,2):
        for fighter in ('sonya','kano'):
            key=f'{fighter}P{side}';folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kitana_kiss_voice_priority_runtime'
            assert sync.sha(folder/'run.log')==proof['results'][key]['logSha256']
            events=[];action=None
            with (folder/'run.log').open() as stream:
                for line in stream:
                    if line.startswith('MK2_STOCK_HEAD_V921_ACTION '):action=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if not line.startswith(('MK2_VOICE_SELECTOR_CUE ','MK2_VOICE_PRIORITY_QUEUE ','MK2_FINISHER_AUDIO_PACKET ')):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['writes']=='0' and r['assistance']=='none'
                    events.append((line.split(' ',1)[0],r))
            assert action is not None;actor,main=action['victim_actor'],action['victim_main']
            accepted=gate(events,side,actor,main,stock);faults=[]
            selected=next(i for i,(tag,r) in enumerate(events) if tag=='MK2_VOICE_SELECTOR_CUE' and r['cue']=='A3')
            for label,offset,key2,value in [('wrong_table_packet',0,'packet','0000'),('wrong_priority_base',1,'a3','00000000'),('wrong_low_owner',3,'a8','00000000')]:
                bad=copy.deepcopy(events);assert bad[selected+offset][1][key2]!=value
                bad[selected+offset][1][key2]=value
                try:gate(bad,side,actor,main,stock)
                except AssertionError:faults.append(label)
                else:raise AssertionError('Effect fault accepted')
            results[key]=dict(effects=accepted,rejectedFaults=faults,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        voiceProofSha256=sync.sha(voice_path),stockSHA256=sync.sha(stock_path),
        callerReturnPCVerified=False,allSoundOriginsVerified=False,nativeADSPConsumptionVerified=False,
        heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:r['effects'] for k,r in results.items()})))

if __name__=='__main__':main()
