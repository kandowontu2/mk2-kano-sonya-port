"""Current Kitana9 physical spacing: owned move, writer context and paid advancement."""
import ast,copy,json,re
import verify_native_source_sync as sync

def load(path):
    text=path.read_text();assert 'LUA ERROR' not in text
    return [(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in text.splitlines() if s.startswith('MK2_NAT_CAMPAIGN_')]

def owned(entries):
    for r in entries:
        assert r['id']==r['roster']=='18' and r['entry']=='FFFFB400' and r['pc']=='FFFFB420'
        assert r['actor']==r['a8'] and r['main']==r['a13']

def main():
    sync.verify();root=sync.ROOT;case=root/'audit_current_sonya_p2_kitana_ring_spacing_runtime'
    out=root/'audit_current_sonya_p2_kitana_ring_spacing_checked';assert not out.exists()
    terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
    assert terminal['limitReason'] in (None,'wall_limit') and ((terminal['exitCode']==0) if terminal['limitReason'] is None else terminal['exitCode']!=0)
    assert terminal['elapsedSeconds']<=181 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(root/'audit_current_sonya_p2_kitana_ring_spacing_preparation/campaign.lua')
    assert not (case/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.wav','.bin') for p in case.rglob('*'))
    rows=load(case/'run.log');prior=load(root/'audit_current_sonya_p2_jax_standing_guard_runtime/run.log')
    last=max(int(r['frame']) for t,r in rows);through=min(last,104518)
    assert [(t,r) for t,r in rows if int(r['frame'])<=through and t not in ('SONYA_KITANA_CPU_ACTION','SONYA_KITANA_DAMAGE')]==[(t,r) for t,r in prior if int(r['frame'])<=through]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    plans=[r for t,r in rows if t=='SONYA_KITANA_RING_PLAN'];entries=[r for t,r in rows if t=='SPECIAL' and r['move']=='ring' and r['stage']=='9'];owned(entries)
    damage=[r for t,r in rows if t=='SONYA_KITANA_DAMAGE']
    assert all(r['ids']=='4,18' and 0<=int(r['after'])<int(r['before'])<=161 and r['pc']=='FF836700' for r in damage)
    action=[r for t,r in rows if t=='SONYA_KITANA_CPU_ACTION']
    assert all(r['id']==r['roster']=='4' and r['actor']==r['owner'] for r in action)
    fights=[r for t,r in rows if t=='FIGHT' and r['stage']=='9']
    assert all(r['human']=='18:18' and r['cpu']=='4:4' for r in fights)
    helper=root/'tools/qualify_current_sonya_p2_paid_advances.py';code=helper.read_text()
    node=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef) and n.name=='gate');pure=ast.get_source_segment(code,node)
    ko="assert all(r['id']=='18' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in own)"
    positive="""for r in own:
        assert r['id']=='18' and r['pc']=='FF8296B0'
        enemyhp,ownhp=map(int,r['health'].split(','));assert 0<=enemyhp<ownhp<=161
        if enemyhp:
            assert any(t=='STATE' and int(r['frame'])<=int(s['frame'])<=int(r['frame'])+2 and s['mode']=='5' and s['winner']=='2' and s['health']==r['health'] for t,s in window)"""
    assert pure.count(ko)==1;pure=pure.replace(ko,positive);namespace={};exec(compile(pure,str(helper)+'::Kitana_native_positive_HP_or_KO','exec'),namespace);gate=namespace['gate']
    advances=[r for t,r in rows if t=='FIGHT' and r['stage']=='10'];proofs=[];faults=[]
    for advance in advances:
        selection=int(advance['selection'])
        if advance['cpu']!='5:5' or not any(r['selection']==str(selection) for r in fights) or any(p['selection']==selection for p in proofs):continue
        proof=gate(rows,9,selection,4,5);proofs.append(proof)
        for kind in ('missing_own_round','continued_between_rounds','wrong_next_selection','proxy_next_fight'):
            bad=copy.deepcopy(rows)
            if kind=='missing_own_round':bad.pop(next(i for i,(t,r) in enumerate(bad) if t=='WIN' and r['frame']==proof['ownWins'][0]['frame']))
            elif kind=='continued_between_rounds':
                r=copy.deepcopy(proof['ownWins'][0]);r['frame']=str(int(r['frame'])+1);bad.append(('LOSS',r))
            else:
                r=next(r for t,r in bad if t=='FIGHT' and r['frame']==proof['advance']['frame']);r['selection' if kind=='wrong_next_selection' else 'human']='999' if kind=='wrong_next_selection' else '1:1'
            try:gate(bad,9,selection,4,5)
            except AssertionError:faults.append(dict(kind='paid match',fault=kind))
            else:raise AssertionError('Match fault admitted')
    if entries:
        for key,value in [('id','1'),('a13','00000000'),('entry','FFFFCA00')]:
            bad=copy.deepcopy(entries);bad[0][key]=value
            try:owned(bad)
            except AssertionError:faults.append(dict(kind='special ownership',key=key))
            else:raise AssertionError('Special fault admitted')
    wins=[r for t,r in rows if t=='WIN' and r['stage']=='9' and r['slot']=='2']
    report=dict(passed=True,earlierNativePhysicalPrefixVerifiedThrough=through,entire104518PrefixVerified=through==104518,
                ringPlans=len(plans),ownedNativeRingEntries=len(entries),actualCPUActionSetterRecords=action,
                actualHPWriterContext=damage,ownKitanaRounds=wins,strictSamePaidKitanaToMileenaClears=proofs,nextStageActualFights=advances,
                rawWriter230MatchesCPUActor=[r for r in damage if r['writer230']==r['cpu_actor']],
                outgoingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),incomingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
                namedStockMoveAttributionAccepted=False,exactRoundTimerRegisterObserved=False,effectiveFaultsRejected=faults,lastLoggedField=last,
                terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False,
                scope='One Kitana9-only physical policy. Plans, native ring entries and HP events distinct; raw totals not normalized rates or proof every hit is ring. Actual setter and writer context retained without naming fanlift/thrownfan/upper from state numbers alone. Native positive-HP wins require higher ownHP and actual mode5/winner2 round state; no fabricated clock value.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','ringPlans','ownedNativeRingEntries','ownKitanaRounds','strictSamePaidKitanaToMileenaClears','lastLoggedField','terminal')}))

if __name__=='__main__':main()
