"""Current kiss: native packed pain choice, priority, and all observed bytes."""
import copy,json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_jax_arms_all_sound_bytes import gate as packet_gate

def voice_gate(groups,side,ident,ready,actor,main,stock):
    age=180 if side==1 else 181;frame=str(ready+age)
    steps=[r for r in groups['MK2_VOICE_SELECTOR_STEP'] if r['frame']==frame]
    assert [r['entry'] for r in steps]==['FFA12220','FFA123D0','FFA12400','FFA12530']
    assert all(r['age']==str(age) and r['role']==str(side) and int(r['victim_id'])==ident and r['a8']==actor and r['a13']==main for r in steps)
    assert steps[0]['a0']=='00000002' and steps[0]['a1']=='32343638'
    base=0x38 if ident==18 else (0x32 if side==1 else 0x34)
    assert all(int(r['a1'],16)==base for r in steps[1:])
    assert steps[1]['a0']==steps[2]['a0']=='00000002'
    cue=int(steps[3]['a0'],16);assert cue in (base,base+1)
    branch=groups['MK2_FINISHER_AUDIO_BRANCH'];assert len(branch)==1;b=branch[0]
    assert b['frame']==frame and b['a8']==b['victim_actor']==actor and b['a13']==b['victim_main']==main
    assert int(b['a2'],16)==int(b['victim_id'])==ident and b['hp']=='0'
    assert b['route']==('female' if ident==18 else 'male') and b['pc']==('FFA123C0' if ident==18 else 'FFA122E0')
    entries=[r for r in groups['MK2_VOICE_SELECTOR_CUE'] if r['frame']==frame];assert len(entries)==1
    header,packet=struct.unpack_from('<HH',stock,(0xffa0ef20-0xff800000)//8+cue*4)
    assert int(entries[0]['cue'],16)==cue and int(entries[0]['header'],16)==header and int(entries[0]['packet'],16)==packet
    queue=[r for r in groups['MK2_VOICE_PRIORITY_QUEUE'] if r['frame']==frame];assert len(queue)==1;q=queue[0]
    slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}[q['entry']]
    assert int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==packet and q['a8']==actor and q['a13']==main
    pair=[r for r in groups['MK2_FINISHER_AUDIO_PACKET'] if r['frame']==frame and r['a8']==actor and r['a13']==main]
    commands=packet_gate(pair,int(frame),int(frame));assert len(commands)==1 and int(commands[0]['command'],16)==packet+slot
    return dict(voiceAge=age,selectedCue=f'{cue:02X}',nativeVariantCount=2,stockBasePacket=f'{packet:04X}',actualPrioritySlot=slot)

def main():
    out=sync.ROOT/'audit_bounded_kitana_kiss_voice_packets_checked';assert not out.exists()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes();results={}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kitana_kiss_voice_priority_runtime'
            baseline=sync.ROOT/(f'audit_bounded_{fighter}_kitana_kiss_finisher_runtime' if side==1 else f'audit_bounded_p2_{fighter}_kitana_kiss_finisher_runtime')
            def controls(path):
                with path.open() as stream:return [line.strip() for line in stream if line.startswith('MK2_STOCK_HEAD_V921_')]
            control=controls(folder/'run.log');assert control==controls(baseline/'run.log')
            action=dict(re.findall(r'(\w+)=([^\s]+)',next(line for line in control if line.startswith('MK2_STOCK_HEAD_V921_ACTION '))))
            end=dict(re.findall(r'(\w+)=([^\s]+)',next(line for line in control if line.startswith('MK2_STOCK_HEAD_V921_BOUNDED_TERMINAL '))))
            ready=int(action['frame']);assert int(end['frame'])-ready==396
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip();groups={}
            with (folder/'run.log').open() as stream:
                for line in stream:
                    assert '[LUA ERROR]' not in line
                    if not line.startswith(('MK2_VOICE_','MK2_FINISHER_AUDIO_')):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['writes']=='0' and r['assistance']=='none'
                    groups.setdefault(line.split(' ',1)[0],[]).append(r)
            src=groups['MK2_VOICE_SELECTOR_SOURCE'];assert len(src)==1
            assert bytes.fromhex(src[0]['hex'])==stock[(0xffa122d0-0xff800000)//8:(0xffa12430-0xff800000)//8]
            actor,main=action['victim_actor'],action['victim_main']
            accepted=voice_gate(groups,side,ident,ready,actor,main,stock)
            packets=groups['MK2_FINISHER_AUDIO_PACKET'];commands=packet_gate(packets,ready,int(end['frame']))
            faults=[]
            for group,key,value in [('MK2_FINISHER_AUDIO_BRANCH','a2','00000000'),('MK2_VOICE_SELECTOR_STEP','a1','00000000')]:
                bad=copy.deepcopy(groups);assert bad[group][0][key]!=value;bad[group][0][key]=value
                try:voice_gate(bad,side,ident,ready,actor,main,stock)
                except AssertionError:faults.append(group+'.'+key)
                else:raise AssertionError('Voice fault accepted')
            bad=copy.deepcopy(packets);bad[0]['data']='FFFF'
            try:packet_gate(bad,ready,int(end['frame']))
            except AssertionError:faults.append('wrong_high_byte')
            else:raise AssertionError('Packet fault accepted')
            results[f'{fighter}P{side}']=dict(**accepted,commandPairs=len(commands),soundPortBytes=len(packets),
                nativeCommands=commands,rejectedFaults=faults,originalControlUnchanged=True,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        allObservedNativePairsVerified=True,allSelectorCallsSourceBound=False,nativeADSPConsumptionVerified=False,
        stockTimingParityAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:{a:r[a] for a in ('voiceAge','selectedCue','commandPairs')} for k,r in results.items()})))

if __name__=='__main__':main()
