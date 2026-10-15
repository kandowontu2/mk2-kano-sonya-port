"""Exclude clipping/row-skip explanations only where native registers prove it."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def full_native_bounds(r):
    assert r['lrskip']=='0000'
    assert tuple(int(r[k]) for k in ('top','bottom','left','right'))==(0,253,0,511)
    assert r['config']=='0030'

def main():
    root=sync.ROOT;results={};faults=[]
    for fighter in ('sonya','kano'):
        case=root/f'audit_bounded_{fighter}_idle_dma_clip_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        rows=[];unresolved=0
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_DMA_CLIP ' in line:full_native_bounds(r);rows.append(r)
            if '_IDLE_SHADOW_COVER ' in line and r['match']=='0':unresolved+=1
        assert len(rows)=={'sonya':1998,'kano':2018}[fighter]
        assert unresolved=={'sonya':56,'kano':96}[fighter]
        assert sum(r['kind']=='body' for r in rows)==60
        for k,v in [('lrskip','0001'),('left','140'),('top','200')]:
            mutant=dict(rows[0]);mutant[k]=v
            try:full_native_bounds(mutant)
            except AssertionError:faults.append(fighter+'_'+k)
            else:raise AssertionError('Ineffective clip fault')
        results[fighter]=dict(actualClipSkipCommands=len(rows),unresolvedPoints=unresolved,
            clipOrRowSkipExplanationExcludedForTheseCommands=True,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_idle_dma_clip_checked';out.mkdir(exist_ok=False)
    report=dict(passed=True,results=results,rejectedFaults=faults,wholeShadowAcceptance=False,fullGoalComplete=False,
        nextEvidence='All subsequent draw commands at unresolved points and native display handoff timing',
        sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,commands=sum(r['actualClipSkipCommands'] for r in results.values()),unresolved=152)))

if __name__=='__main__':main()
