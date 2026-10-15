"""Finite Jax-only physical policy, current native identity and paid advancement."""
import ast
import copy
import json
import re
import verify_native_source_sync as sync


def load(path):
    result=[]
    for line in path.read_text().splitlines():
        assert 'LUA ERROR' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            result.append((line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return result


def ownership(entries):
    for r in entries:
        assert r['id']==r['roster']=='18' and r['entry']=='FFFFB400' and r['pc']=='FFFFB420'
        assert r['actor']==r['a8'] and r['main']==r['a13']


def main():
    sync.verify();root=sync.ROOT
    case=root/'audit_current_sonya_p2_jax_ring_spacing_runtime'
    out=root/'audit_current_sonya_p2_jax_ring_spacing_checked';assert not out.exists()
    terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
    assert terminal['limitReason'] in (None,'wall_limit')
    assert terminal['exitCode']==0 if terminal['limitReason'] is None else terminal['exitCode']!=0
    assert terminal['elapsedSeconds']<=181 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(root/'audit_current_sonya_p2_jax_ring_spacing_preparation/campaign.lua')
    assert not (case/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in case.rglob('*'))
    rows=load(case/'run.log');prior=load(root/'audit_current_sonya_p2_kano_short_leg_runtime/run.log')
    last=max(int(r['frame']) for t,r in rows);through=min(last,101525)
    assert [(t,r) for t,r in rows if int(r['frame'])<=through and t!='SONYA_JAX_DAMAGE']==[(t,r) for t,r in prior if int(r['frame'])<=through]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    plans=[r for t,r in rows if t=='SONYA_JAX_RING_PLAN']
    entries=[r for t,r in rows if t=='SPECIAL' and r['move']=='ring' and r['stage']=='8'];ownership(entries)
    jump_plans=[r for t,r in rows if t=='SONYA_JAX_JUMP_PLAN']
    damage=[r for t,r in rows if t=='SONYA_JAX_DAMAGE']
    assert all(r['ids']=='11,18' and 0<=int(r['after'])<int(r['before'])<=161 for r in damage)
    fights=[r for t,r in rows if t=='FIGHT' and r['stage']=='8']
    assert all(r['human']=='18:18' and r['cpu']=='11:11' and r['human_slot']=='2' for r in fights)
    wins=[r for t,r in rows if t=='WIN' and r['stage']=='8']
    advances=[r for t,r in rows if t=='FIGHT' and r['stage']=='9']
    faults=[];proofs=[]
    if entries:
        for key,value in [('id','1'),('a13','00000000'),('entry','FFFFCA00')]:
            bad=copy.deepcopy(entries);bad[0][key]=value
            try:ownership(bad)
            except AssertionError:faults.append(dict(kind='special ownership',key=key))
            else:raise AssertionError('Special fault admitted')
    # Extract only the already-reviewed strict pure gate, not top-level jobs.
    helper=root/'tools/qualify_current_sonya_p2_paid_advances.py'
    code=helper.read_text();node=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef) and n.name=='gate')
    namespace={};exec(compile(ast.get_source_segment(code,node),str(helper)+'::pure_gate','exec'),namespace)
    gate=namespace['gate']
    for advance in advances:
        if advance['cpu']!='4:4':continue
        selection=int(advance['selection']);proof=gate(rows,8,selection,11,4);proofs.append(proof)
        for kind in ('missing_own_round','continued_between_rounds','wrong_next_selection','proxy_next_fight'):
            bad=copy.deepcopy(rows)
            if kind=='missing_own_round':bad.pop(next(i for i,(t,r) in enumerate(bad) if t=='WIN' and r['frame']==proof['ownWins'][0]['frame']))
            elif kind=='continued_between_rounds':
                r=copy.deepcopy(proof['ownWins'][0]);r['frame']=str(int(r['frame'])+1);bad.append(('LOSS',r))
            else:
                r=next(r for t,r in bad if t=='FIGHT' and r['frame']==proof['advance']['frame'])
                r['selection' if kind=='wrong_next_selection' else 'human']='999' if kind=='wrong_next_selection' else '1:1'
            try:gate(bad,8,selection,11,4)
            except AssertionError:faults.append(dict(kind='paid match',fault=kind))
            else:raise AssertionError('Paid match fault admitted')
    report=dict(passed=True,earlierNativePhysicalPrefixVerifiedThrough=through,entireProposed101525PrefixVerified=through==101525,
                ringPlans=len(plans),ownedNativeRingEntries=len(entries),jumpInputPlans=len(jump_plans),
                ownJaxRounds=[r for r in wins if r['slot']=='2'],nextStageActualFights=advances,
                strictSamePaidJaxToKitanaClears=proofs,effectiveFaultsRejected=faults,
                outgoingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
                incomingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
                lastLoggedField=last,terminal=terminal,logSHA256=sync.sha(case/'run.log'),
                paidMatchHelperSHA256=sync.sha(helper),fullCampaignAccepted=False,fullPortAccepted=False,
                scope='One stage8 Jax11 physical ring/backjump successor; plans, actual entries and HP events distinct. Raw totals are not normalized rates or proof every damage event is a ring hit. Wall-censored absence of advancement is not a character defect.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','ringPlans','ownedNativeRingEntries','ownJaxRounds','strictSamePaidJaxToKitanaClears','lastLoggedField','terminal')}))


if __name__=='__main__':main()
