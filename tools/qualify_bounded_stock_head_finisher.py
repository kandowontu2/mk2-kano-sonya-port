"""Earned Baraka finisher control/completion; no full art/audio acceptance."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def gate(rows,fighter,ident):
    def tagged(tag):return [r for t,r in rows if t==tag]
    action=tagged('ACTION');wrap=tagged('WRAP');terminal=tagged('BOUNDED_TERMINAL');result=tagged('RESULT')
    assert len(action)==len(wrap)==len(terminal)==len(result)==1
    a,w,t,r=action[0],wrap[0],terminal[0],result[0]
    assert a['variant']=='1' and a['address']=='FF8CB4A0' and a['damage']=='322'
    assert a['actor']!=a['victim_actor'] and a['main']!=a['victim_main']
    assert int(a['frame'])<int(w['frame'])<int(t['frame'])
    assert int(t['frame'])-int(w['frame'])==120
    assert r['damage']=='322' and r['wins']=='2' and r['action']==a['frame'] and r['wrap']==w['frame']
    assert t['reason']=='native_common_completion_followthrough' and t['raw_media']=='none'
    wins=tagged('WIN');assert [x['count'] for x in wins]==['1','2']
    health=tagged('HEALTH')
    damage=[x for x in health if x['pc']=='FF836700' and int(x['after'])<int(x['before'])<=161]
    assert sum(int(x['before'])-int(x['after']) for x in damage)==322
    assert len([x for x in damage if x['after']=='0'])==2
    states=tagged('STATE');assert len(states)>100
    assert all(x['own'].split(':')[-1]=='3' and x['victim'].split(':')[-1]==str(ident) for x in states)
    assert not tagged('CACHE_OVERWRITE') and not tagged('BOUNDED_FAILED')
    return dict(nativeActionAddress=a['address'],actualDamage=322,earnedNativeWins=2,
                nativeActionFrame=int(a['frame']),nativeWrapFrame=int(w['frame']),
                followthroughFields=120,actualTrueIDStateObservations=len(states),cacheOverwrites=0)

def main():
    out=sync.ROOT/'audit_bounded_stock_head_finisher_checked';assert not out.exists()
    results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line and len(line)<65536
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                tag=line.split(' ',1)[0].removeprefix('MK2_STOCK_HEAD_V921_')
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                assert r['victim']==fighter and r['side']=='1' and r['killer']=='baraka'
                assert r['writes']=='0' and r['assistance']=='none';rows.append((tag,r))
        positive=gate(rows,fighter,ident);faults=[]
        for name,key,value in (('wrong_damage','damage','321'),('missing_native_win','wins','1'),
                               ('wrong_wrap','wrap','0')):
            bad=copy.deepcopy(rows);next(r for t,r in bad if t=='RESULT')[key]=value
            try:gate(bad,fighter,ident)
            except AssertionError:faults.append(name)
            else:raise AssertionError('Fault accepted '+name)
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=terminal,
            logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        fullFinisherArtAccepted=False,fullFinisherAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
