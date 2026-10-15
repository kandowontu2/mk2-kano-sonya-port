"""Check sparse native floor-shadow ownership without claiming full scanout."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def records(folder):
    return [line for line in (folder/'run.log').read_text().splitlines()
            if line.startswith('MK2_NAT_CAMPAIGN_')]

def check_shadow(r):
    assert r['owner']==r['actor']
    assert r['id']==r['roster']
    assert r['pc'] in ('FF8015A0','FF801610')
    assert int(r['command'],16)&15==8 and int(r['color'],16)==0
    assert int(r['height'])==1 and 0<int(r['width'])<=1023
    offset=int(r['row'],16)-int(r['cache'],16)
    assert 0<=offset<12*112 and offset%112==0
    assert int(r['graphic'],16)!=0
    assert r['writes']=='0' and r['assistance']=='none'

out=sync.ROOT/'audit_bounded_campaign_shadows_checked'
assert not out.exists()
prior=sync.ROOT/'audit_bounded_campaign_progress_checked/report.json'
pins=json.loads(prior.read_text())['results']
results={}
for fighter in ('kano','sonya'):
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_campaign_shadows_{fighter}_p{side}_runtime'
        base=sync.ROOT/f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['rawMedia']=='none' and terminal['peakWorkingSetBytes']<=320*1024**2
        assert not (folder/'stderr.log').read_text().strip()
        assert not any(p.suffix.lower() in ('.bin','.png','.wav') for p in folder.rglob('*') if p.is_file())
        assert sync.sha(base/'run.log')==pins[f'{fighter}P{side}']['logSHA256']
        lines=records(folder)
        assert not any(line.startswith('MK2_NAT_CAMPAIGN_SHADOW_UNOWNED ') for line in lines)
        shadows=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines
                 if line.startswith('MK2_NAT_CAMPAIGN_SHADOW ')]
        assert [line for line in lines if not line.startswith('MK2_NAT_CAMPAIGN_SHADOW ')]==records(base)
        assert shadows
        for row in shadows:check_shadow(row)
        identity='17' if fighter=='kano' else '18'
        own=[r for r in shadows if r['slot']==str(side)]
        assert own and all(r['id']==identity for r in own)
        coverage={}
        for row in own:
            key=f"stage{row['stage']}:action{row['action']}"
            coverage.setdefault(key,{'rows':0,'fields':set(),'groundRows':0,'airRows':0})
            c=coverage[key];c['rows']+=1;c['fields'].add(int(row['frame']))
            c['groundRows' if row['actor_y']==row['floor'] else 'airRows']+=1
        for c in coverage.values():c['fields']=sorted(c['fields'])
        faults=[]
        for field,value in [('owner','00000000'),('color','001F'),('height','2'),('command','0000')]:
            bad=dict(own[0]);bad[field]=value
            try:check_shadow(bad)
            except AssertionError:faults.append(field)
            else:raise AssertionError(f'Fault not rejected: {field}')
        results[f'{fighter}P{side}']=dict(terminal=terminal,ownRows=len(own),allRows=len(shadows),
            coverage=coverage,rejectedFaults=faults,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),
    priorCampaignReportSHA256=sync.sha(prior),checkerSHA256=sync.sha(Path(__file__)),
    scope='Sparse native shadow DMA in four unchanged physical 12000-field campaigns. Correct actor/cache ownership, black pen and native one-row command. Not full opaque shadow geometry, every-field scanout, every arena or full campaign acceptance.',
    fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,ownRows={k:v['ownRows'] for k,v in results.items()})))
