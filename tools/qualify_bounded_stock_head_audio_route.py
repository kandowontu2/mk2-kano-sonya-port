"""Finisher true-ID voice routing/packet grammar, not mixed-waveform proof."""
import copy,json,re
from pathlib import Path
import qualify_bounded_stock_head_body_footprints as original
import verify_native_source_sync as sync

def gate(rows,fighter):
    ident,route,pc,command={'sonya':(18,'female','FFA123C0',0x2dd),'kano':(17,'male','FFA122E0',0x279)}[fighter]
    branches=[(i,r) for i,(tag,r) in enumerate(rows) if tag=='BRANCH'];assert len(branches)==1
    i,b=branches[0]
    assert b['age']=='58' and b['frame']=='3179' and b['route']==route and b['pc']==pc
    assert int(b['a2'],16)==int(b['victim_id'])==ident and b['hp']=='0'
    assert b['a8']==b['victim_actor'] and b['a13']==b['victim_main']
    high,low=rows[i+1:i+3]
    assert high[0]==low[0]=='PACKET'
    assert int(high[1]['a0'],16)==command
    assert all(r['a8']==b['victim_actor'] and r['a13']==b['victim_main'] for _,r in (high,low))
    packets=[r for tag,r in rows if tag=='PACKET'];assert len(packets)%2==0
    decoded=[]
    for h,l in zip(packets[::2],packets[1::2]):
        cmd=int(h['a0'],16)
        assert h['pc']=='FFA13C90' and l['pc']=='FFA13D60'
        assert h['mask']==l['mask']=='FFFF' and h['frame']==l['frame'] and h['age']==l['age']
        assert h['a8']==l['a8'] and h['a13']==l['a13']
        assert int(h['data'],16)==0xff00|(cmd>>8) and int(l['data'],16)==0xff00|(cmd&255)
        decoded.append(dict(age=int(h['age']),command=f'{cmd:04X}',actor=h['a8'],main=h['a13']))
    assert len(decoded)==(11 if fighter=='sonya' else 12)
    return dict(victimTrueID=ident,nativeVoiceRoute=route,victimVoiceCommand=f'{command:04X}',commands=decoded)

def main():
    out=sync.ROOT/'audit_bounded_stock_head_audio_route_checked';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json').read_text())
    assert proof['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_audio_route_runtime'
        baseline=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        states=original.states(folder,fighter);assert states==original.states(baseline,fighter)
        original.state_gate(states,fighter,ident);rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_FINISHER_AUDIO_'):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                assert r['writes']=='0' and r['assistance']=='none'
                rows.append((line.split(' ',1)[0].removeprefix('MK2_FINISHER_AUDIO_'),r))
        positive=gate(rows,fighter);faults=[]
        for key,value in (('a2','00000000'),('a8','00000000'),('route','wrong')):
            bad=copy.deepcopy(rows);next(r for tag,r in bad if tag=='BRANCH')[key]=value
            try:gate(bad,fighter)
            except AssertionError:faults.append(key)
            else:raise AssertionError('Fault accepted '+key)
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        mixedWaveformAccepted=False,heardAudioAccepted=False,allAudioContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,voiceRoutes={f:r['nativeVoiceRoute'] for f,r in results.items()})))

if __name__=='__main__':main()
