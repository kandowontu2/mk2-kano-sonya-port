"""Eight actual owned leg cycles in two-human standing/crouched contexts."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;out=root/'audit_current_leg_stance_comparison_checked';assert not out.exists()
def load(path):
    records=[]
    for s in path.read_text().splitlines():
        assert 'LUA ERROR' not in s
        if s.startswith('MK2_HSPECIAL_'):records.append((s.split()[0].removeprefix('MK2_HSPECIAL_'),dict(re.findall(r'(\w+)=([^\s]+)',s))))
    return records
def gate(rows,stance,side):
    results=[r for t,r in rows if t=='RESULT'];assert len(results)==1 and results[0]['completed']=='2'
    entries=[r for t,r in rows if t=='EVENT' and r['entry']=='FFF80800']
    assert len(entries)==2 and {r['attempt'] for r in entries}=={'1','2'}
    assert all(r['actor']==r['a8'] and r['main']==r['a13'] and r['id']=='18' for r in entries)
    damage=[r for t,r in rows if t=='HEALTH' and r['slot']==str(3-side) and int(r['after'])<int(r['before'])]
    assert len(damage)==2 and all(int(r['before'])-int(r['after'])==35 and r['pc']=='FF836700' for r in damage)
    assert len([r for t,r in rows if t=='RECOVERED'])==2
    held=[r for t,r in rows if t=='PREHELD_CROUCH']
    assert len(held)==(2 if stance=='crouched' else 0)
    assert all(r['action']=='770' and r['id']=='18' for r in held)
    fields=[r for t,r in rows if t=='FIELD']
    assert fields and all(r['id']==r['roster']==('18' if r['slot']==str(side) else '3') and r['owner']==r['actor'] for r in fields)
    assert all(r['writes']=='0' and r['assistance']=='none' and r['victim']=='baraka' for _,r in rows)
    return dict(completedCycles=2,damageEach=35,preheldCrouchEvents=len(held),final=results[0])
cases={};rejected=[]
for stance in ('standing','crouched'):
    for side in (1,2):
        folder=root/f'audit_current_leg_stance_{stance}_p{side}_runtime';rows=load(folder/'run.log')
        result=gate(rows,stance,side)
        bad=copy.deepcopy(rows);next(r for t,r in bad if t=='EVENT' and r['entry']=='FFF80800')['id']='1'
        try:gate(bad,stance,side)
        except AssertionError:rejected.append(stance+str(side)+':proxy_entry')
        else:raise AssertionError('Proxy leg accepted')
        terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        result.update(terminal=terminal,logSHA256=sync.sha(folder/'run.log'));cases[stance+str(side)]=result
report=dict(completedPhysicalLegCycles=8,standingCycles=4,preheldCrouchCycles=4,cases=cases,
    wrongIdentityFaultsRejected=rejected,generalCrouchedActivationDefectReproduced=False,
    campaignMissedPlanCauseProved=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='cases'}))
