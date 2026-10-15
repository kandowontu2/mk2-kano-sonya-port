"""Discover current native non-body actors, not effect-art acceptance."""
import json,re
from pathlib import Path
import qualify_bounded_stock_head_body_footprints as original
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_stock_head_effect_census_checked';assert not out.exists()
    prior=json.loads((sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json').read_text())
    assert prior['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_effect_census_runtime'
        baseline=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==prior['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=original.states(folder,fighter);assert rows==original.states(baseline,fighter)
        control=original.state_gate(rows,fighter,ident);actors={};fields=set();total=0
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                assert r['writes']=='0' and r['assistance']=='none'
                age=int(r['age']);assert 1<=age<=174
                fields.add(age);total+=1
                if r['physical']!='0':continue
                source=int(r['source'],16)
                if int(r['id'])!=ident and not 0x0f600000<=source<0x10000000:continue
                a=actors.setdefault(r['actor'],dict(ids=set(),sources=set(),poses=set(),ages=set(),draws=0))
                for key,value in (('ids',r['id']),('sources',r['source']),('poses',r['pose']),('ages',age)):a[key].add(value)
                a['draws']+=1
        assert fields==set(range(1,175)) and actors
        summary={actor:dict(ids=sorted(a['ids']),sources=sorted(a['sources']),poses=sorted(a['poses']),
            firstAge=min(a['ages']),lastAge=max(a['ages']),drawFields=len(a['ages']),draws=a['draws']) for actor,a in actors.items()}
        results[fighter]=dict(**control,nativeDrawFields=len(fields),allFifoDraws=total,
            candidateNonBodyActors=summary,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        effectPixelsAccepted=False,fullFinisherArtAccepted=False,fullFinisherAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results={f:r['candidateNonBodyActors'] for f,r in results.items()})))

if __name__=='__main__':main()
