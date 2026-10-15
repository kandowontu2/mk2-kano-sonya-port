"""Actual Jax clap activation/earned rounds/true victims/native completion."""
import copy,json,re
from pathlib import Path
from qualify_bounded_stock_head_body_footprints import PREFIX
import verify_native_source_sync as sync

def gate(rows,ident):
    def tagged(tag):return [r for t,r in rows if t==tag]
    assert all(len(tagged(t))==1 for t in ('ACTION','WRAP','BOUNDED_TERMINAL','RESULT'))
    a,w,t,r=[tagged(tag)[0] for tag in ('ACTION','WRAP','BOUNDED_TERMINAL','RESULT')]
    assert a['address']=='FF8C7820' and a['variant']=='1' and a['damage']=='322'
    assert a['actor']=='010350A0' and a['victim_actor']=='01034E90' and a['main']!=a['victim_main']
    assert int(a['frame'])<int(w['frame'])<int(t['frame']) and int(t['frame'])-int(w['frame'])==120
    assert t['reason']=='native_common_completion_followthrough' and t['raw_media']=='none'
    assert r['damage']=='322' and r['wins']=='2' and r['action']==a['frame'] and r['wrap']==w['frame']
    assert [x['count'] for x in tagged('WIN')]==['1','2']
    damage=[x for x in tagged('HEALTH') if x['pc']=='FF836700' and int(x['after'])<int(x['before'])<=161]
    assert sum(int(x['before'])-int(x['after']) for x in damage)==322 and sum(x['after']=='0' for x in damage)==2
    states=tagged('STATE');assert len(states)>100
    assert all(x['own'].split(':')[-1]=='11' and x['victim'].split(':')[-1]==str(ident) for x in states)
    assert not tagged('CACHE_OVERWRITE') and not tagged('BOUNDED_FAILED')
    return dict(nativeActionAddress=a['address'],nativeActionFrame=int(a['frame']),nativeWrapFrame=int(w['frame']),
        earnedNativeWins=2,actualDamage=322,followthroughFields=120,trueIDStateObservations=len(states),cacheOverwrites=0)

def main():
    out=sync.ROOT/'audit_bounded_jax_clap_finisher_checked';assert not out.exists();results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_jax_clap_finisher_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip();rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                m=PREFIX.match(line);assert m
                assert (m[3],m[4],m[5],m[6],m[7])==(fighter,'1','jax','0','none')
                rows.append((m[1],dict(re.findall(r'(\w+)=([^\s]+)',line))))
        positive=gate(rows,ident);faults=[]
        for key,value in (('address','FF8CB4A0'),('damage','321')):
            bad=copy.deepcopy(rows);next(r for tag,r in bad if tag=='ACTION')[key]=value
            try:gate(bad,ident)
            except AssertionError:faults.append(key)
            else:raise AssertionError('Fault accepted '+key)
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        renderedArtAccepted=False,heardAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
