"""Opposite-slot earned Jax clap and true native victim voice packets."""
import copy,json,re
from pathlib import Path
from qualify_bounded_stock_head_body_footprints import PREFIX
import verify_native_source_sync as sync

def gate(rows,audio,ident):
    def tagged(tag):return [r for t,r in rows if t==tag]
    assert all(len(tagged(t))==1 for t in ('ACTION','WRAP','BOUNDED_TERMINAL','RESULT'))
    a,w,t,r=[tagged(tag)[0] for tag in ('ACTION','WRAP','BOUNDED_TERMINAL','RESULT')]
    assert a['address']=='FF8C7820' and a['variant']=='1' and a['damage']=='322'
    assert a['actor']=='01034E90' and a['victim_actor']=='010350A0' and a['main']!=a['victim_main']
    assert int(w['frame'])-int(a['frame'])==188 and int(t['frame'])-int(w['frame'])==120
    assert t['reason']=='native_common_completion_followthrough' and t['raw_media']=='none'
    assert r['damage']=='322' and r['wins']=='2' and r['action']==a['frame'] and r['wrap']==w['frame']
    assert [x['count'] for x in tagged('WIN')]==['1','2']
    damage=[x for x in tagged('HEALTH') if x['pc']=='FF836700' and int(x['after'])<int(x['before'])<=161]
    assert sum(int(x['before'])-int(x['after']) for x in damage)==322 and sum(x['after']=='0' for x in damage)==2
    states=tagged('STATE');assert len(states)>100
    assert all(x['own'].split(':')[-1]=='11' and x['victim'].split(':')[-1]==str(ident) for x in states)
    assert not tagged('CACHE_OVERWRITE') and not tagged('BOUNDED_FAILED')
    branches=[(i,b) for i,(tag,b) in enumerate(audio) if tag=='BRANCH'];assert len(branches)==1
    i,b=branches[0];female=ident==18
    assert b['age']=='55' and int(b['frame'])==int(a['frame'])+55
    assert b['route']==('female' if female else 'male') and b['pc']==('FFA123C0' if female else 'FFA122E0')
    assert int(b['a2'],16)==int(b['victim_id'])==ident and b['hp']=='0'
    assert b['a8']==b['victim_actor']==a['victim_actor'] and b['a13']==b['victim_main']==a['victim_main']
    assert audio[i+1][0]==audio[i+2][0]=='PACKET'
    command=0x2dd if female else 0x2ab
    assert int(audio[i+1][1]['a0'],16)==command
    assert all(p['a8']==a['victim_actor'] and p['a13']==a['victim_main'] for tag,p in audio[i+1:i+3])
    packets=[p for tag,p in audio if tag=='PACKET'];assert len(packets)>16 and len(packets)%2==0
    for h,l in zip(packets[::2],packets[1::2]):
        cmd=int(h['a0'],16)
        assert h['pc']=='FFA13C90' and l['pc']=='FFA13D60' and h['mask']==l['mask']=='FFFF'
        assert h['frame']==l['frame'] and h['a8']==l['a8'] and h['a13']==l['a13']
        assert int(h['data'],16)==0xff00|(cmd>>8) and int(l['data'],16)==0xff00|(cmd&255)
    return dict(nativeActionFrame=int(a['frame']),nativeWrapFrame=int(w['frame']),earnedNativeWins=2,
        actualDamage=322,trueIDStateObservations=len(states),physicalVictimSlot=2,
        nativeVoiceRoute=b['route'],victimVoiceCommand=f'{command:04X}',nativeCommandPairs=len(packets)//2)

def main():
    out=sync.ROOT/'audit_bounded_p2_jax_clap_audio_route_checked';assert not out.exists();results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip();rows=[];audio=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if line.startswith('MK2_STOCK_HEAD_V921_'):
                    m=PREFIX.match(line);assert m and (m[3],m[4],m[5],m[6],m[7])==(fighter,'2','jax','0','none')
                    rows.append((m[1],r))
                elif line.startswith('MK2_FINISHER_AUDIO_'):
                    assert r['writes']=='0' and r['assistance']=='none'
                    audio.append((line.split(' ',1)[0].removeprefix('MK2_FINISHER_AUDIO_'),r))
        positive=gate(rows,audio,ident);faults=[]
        for key,value in (('a2','00000000'),('a8','00000000'),('route','wrong')):
            bad=copy.deepcopy(audio);next(r for tag,r in bad if tag=='BRANCH')[key]=value
            try:gate(rows,bad,ident)
            except AssertionError:faults.append(key)
            else:raise AssertionError('Fault accepted '+key)
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        renderedP2ArtAccepted=False,heardAudioAccepted=False,allFinisherAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
