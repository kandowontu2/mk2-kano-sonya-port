"""Opposite-slot earned finisher, true identity and native voice ownership."""
import json,re
from pathlib import Path
import qualify_bounded_stock_head_finisher as original
import verify_native_source_sync as sync

PREFIX=re.compile(r'^MK2_STOCK_HEAD_V921_(\w+) frame=(\d+) victim=(\w+) side=(\d+) killer=(\w+) writes=(\d+) assistance=(\w+)(?: |$)')

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_head_finisher_checked';assert not out.exists();results={}
    for fighter,ident,route,pc,command in (('sonya',18,'female','FFA123C0',0x2dd),('kano',17,'male','FFA122E0',0x279)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=[];audio=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if line.startswith('MK2_STOCK_HEAD_V921_'):
                    m=PREFIX.match(line);assert m
                    tag,frame,name,side,killer,writes,assistance=m.groups()
                    assert (name,side,killer,writes,assistance)==(fighter,'2','baraka','0','none')
                    rows.append((tag,r))
                elif line.startswith('MK2_FINISHER_AUDIO_'):
                    assert r['writes']=='0' and r['assistance']=='none'
                    audio.append((line.split(' ',1)[0].removeprefix('MK2_FINISHER_AUDIO_'),r))
        control=original.gate(rows,fighter,ident)
        action=next(r for t,r in rows if t=='ACTION')
        assert action['actor']=='01034E90' and action['victim_actor']=='010350A0'
        branches=[(i,r) for i,(tag,r) in enumerate(audio) if tag=='BRANCH'];assert len(branches)==1
        i,b=branches[0]
        assert int(b['frame'])==control['nativeActionFrame']+58 and b['age']=='58'
        assert b['route']==route and b['pc']==pc and int(b['a2'],16)==int(b['victim_id'])==ident and b['hp']=='0'
        assert b['a8']==b['victim_actor']==action['victim_actor']
        assert b['a13']==b['victim_main']==action['victim_main']
        assert audio[i+1][0]==audio[i+2][0]=='PACKET'
        assert int(audio[i+1][1]['a0'],16)==command
        packets=[r for tag,r in audio if tag=='PACKET'];assert len(packets)>16 and len(packets)%2==0
        for h,l in zip(packets[::2],packets[1::2]):
            cmd=int(h['a0'],16)
            assert h['pc']=='FFA13C90' and l['pc']=='FFA13D60'
            assert h['mask']==l['mask']=='FFFF' and h['frame']==l['frame'] and h['age']==l['age']
            assert h['a8']==l['a8'] and h['a13']==l['a13']
            assert int(h['data'],16)==0xff00|(cmd>>8) and int(l['data'],16)==0xff00|(cmd&255)
        results[fighter]=dict(**control,physicalVictimSlot=2,victimTrueID=ident,nativeVoiceRoute=route,
            voiceCommand=f'{command:04X}',nativeCommandPairs=len(packets)//2,
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        reusedControlGateSha256=sync.sha(Path(original.__file__)),renderedP2EffectsAccepted=False,
        heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
