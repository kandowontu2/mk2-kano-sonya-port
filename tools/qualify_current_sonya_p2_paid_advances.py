"""Verify actual paid match wins/next owned fight, distinct from special faults."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_sonya_p2_paid_advances_checked';assert not out.exists()
def load(path):
    return [(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_')]
def gate(rows,stage,selection,cpu,nextcpu):
    fights=[r for t,r in rows if t=='FIGHT' and r['stage']==str(stage) and r['selection']==str(selection)]
    assert fights and all(r['human']=='18:18' and r['cpu']==f'{cpu}:{cpu}' and r['human_slot']=='2' for r in fights)
    start=min(int(r['frame']) for r in fights)
    advances=[r for t,r in rows if t=='FIGHT' and r['stage']==str(stage+1) and int(r['frame'])>start]
    assert advances
    advance=min(advances,key=lambda r:int(r['frame']));end=int(advance['frame'])
    assert advance['selection']==str(selection) and advance['human']=='18:18' and advance['cpu']==f'{nextcpu}:{nextcpu}'
    window=[(t,r) for t,r in rows if start<=int(r['frame'])<end]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in window)
    assert not any(t in ('LOSS','SELECT') for t,r in window)
    own=[r for t,r in window if t=='WIN' and r['stage']==str(stage) and r['slot']=='2']
    enemy=[r for t,r in window if t=='WIN' and r['stage']==str(stage) and r['slot']=='1']
    assert len(own)==2 and len(enemy)<=1
    assert all(r['id']=='18' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in own)
    return dict(start=start,selection=selection,ownWins=own,cpuRoundWins=enemy,advance=advance)
proofs=[];faults=[];pins={}
for name,stage,selection,cpu,nextcpu in [('baraka',6,21,3,17),('kano',7,22,17,11)]:
    case=sync.ROOT/f'audit_current_sonya_p2_{name}_short_leg_runtime'
    report=sync.ROOT/f'audit_current_sonya_p2_{name}_short_leg_checked/report.json'
    old=json.loads(report.read_text());log=case/'run.log'
    assert old['logSHA256']==sync.sha(log)
    rows=load(log);proof=gate(rows,stage,selection,cpu,nextcpu);proofs.append(dict(case=name,**proof))
    for kind in ('missing_own_round','continued_between_rounds','wrong_next_selection','proxy_next_fight'):
        bad=copy.deepcopy(rows)
        if kind=='missing_own_round':
            i=next(i for i,(t,r) in enumerate(bad) if t=='WIN' and r['frame']==proof['ownWins'][0]['frame']);bad.pop(i)
        elif kind=='continued_between_rounds':
            r=copy.deepcopy(proof['ownWins'][0]);r['frame']=str(int(r['frame'])+1);bad.append(('LOSS',r))
        else:
            r=next(r for t,r in bad if t=='FIGHT' and r['frame']==proof['advance']['frame'])
            r['selection' if kind=='wrong_next_selection' else 'human']='999' if kind=='wrong_next_selection' else '1:1'
        try:gate(bad,stage,selection,cpu,nextcpu)
        except AssertionError:faults.append(dict(case=name,fault=kind))
        else:raise AssertionError('Match fault admitted')
    pins[str(log)]=sync.sha(log);pins[str(report)]=sync.sha(report)
result=dict(currentSonyaP2BarakaAndKanoSamePaidClears=True,proofs=proofs,
    effectiveMatchFaultsRejected=faults,inputHashes=pins,
    earlierThreeFaultsWereSpecialOwnershipNotMatchFaults=True,
    fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(samePaidClears=True,cases=2,effectiveMatchFaults=len(faults))))
