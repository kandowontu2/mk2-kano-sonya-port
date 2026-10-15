"""Actual morphed victims, earned KOs, native finish/wrap and owned pose rows."""
import copy,inspect,json,re
import verify_native_source_sync as sync
import qualify_bounded_stock_head_finisher as prior

source=inspect.getsource(prior.gate)
source=source.replace("a['address']=='FF8CB4A0'","a['address']=='FFFAAE00'")
before="x['own'].split(':')[-1]=='3' and x['victim'].split(':')[-1]==str(ident)"
assert source.count(before)==1
source=source.replace(before,"x['own'].split(':')[-1]=='17' and x['victim'].split(':')[-1] in ('6',str(ident))")
namespace={};exec(compile(source,__file__+'::earned_native_finish_gate','exec'),namespace)
base=namespace['gate']

def gate(rows,target,ident,side,groups):
    proof=base(rows,target,ident)
    def tagged(tag):return [r for t,r in rows if t==tag]
    first=tagged('FIRST_LIVE');assert len(first)==1 and first[0]['ids']=='17,6'
    assert {int(r['slot']):int(r['target']) for r in tagged('SELECT')}=={side:6,3-side:17}
    stores=tagged('VICTIM_MORPH_STORE');assert len(stores)==1
    form=stores[0]
    assert (form['old'],form['id'],form['roster'],form['pc'],form['a9'])==('6',str(ident),'6','FF86E670',f'{ident:08X}')
    action,wrap=tagged('ACTION')[0],tagged('WRAP')[0]
    assert (form['actor'],form['main'])==(action['victim_actor'],action['victim_main'])
    assert int(form['frame'])<int(action['frame'])<int(wrap['frame'])
    zeros=[r for r in tagged('HEALTH') if r['pc']=='FF836700' and r['after']=='0']
    assert len(zeros)==2 and int(zeros[0]['frame'])<int(form['frame'])<int(zeros[1]['frame'])<int(action['frame'])
    for r in tagged('STATE'):
        expected=6 if int(r['frame'])<=int(form['frame']) else ident
        assert int(r['victim'].split(':')[-1])==expected
    plan=tagged('VICTIM_MORPH_PLAN');assert len(plan)==1
    due=int(plan[0]['due'])
    actual={(int(r['frame']),r['button']) for r in tagged('INPUT') if int(r['slot'])==side and due<=int(r['frame'])<due+40}
    if target=='kano':
        back='Left' if side==1 else 'Right'
        expected={(due+i,back) for i in(0,1,8,9)}|{(due+i,'Down') for i in(4,5)}|{(due+i,'Low_Kick') for i in(8,9)}
    else:expected={(due+i,key) for i in range(8) for key in('Down','Low_Punch','Block')}
    assert actual==expected
    sampled=[r for r in tagged('STATE') if int(action['frame'])+30<=int(r['frame'])<=int(wrap['frame'])]
    assert len(sampled)>=10
    poses=[int(r['poses'].split(',')[1],16) for r in sampled]
    assert all(p in groups for p in poses) and len(set(poses))>=3 and poses[-1]==groups[-1]
    return dict(**proof,actualVictimShangRoster=6,actualVictimFormID=ident,
        formFrame=int(form['frame']),ownedVictimPoseSamples=len(poses),ownedVictimDistinctPoses=len(set(poses)))

if __name__=='__main__':
    source_sync=sync.verify()
    out=sync.ROOT/'audit_bounded_morphed_victim_finishers_checked';assert not out.exists()
    cpp=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    compiled_source=cpp.read_text()
    lua=sync.ROOT/'audit_bounded_morphed_victim_finishers_preparation/finishers.lua'
    cases={}
    for target,ident,array in(('kano',17,'kano_victim_groups'),('sonya',18,'kano_sonya_victim_groups')):
        match=re.search(r'constexpr uint32_t '+array+r'\[\]=\{([^}]+)\};',compiled_source);assert match
        groups=[int(v,16) for v in re.findall(r'0x[0-9a-f]+',match[1])];assert len(groups)==6
        for side in(1,2):
            folder=sync.ROOT/f'audit_bounded_morphed_victim_finisher_{target}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in('.png','.bin','.wav') for p in folder.rglob('*'))
            rows=[]
            for line in (folder/'run.log').read_text().splitlines():
                assert 'LUA ERROR' not in line
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                assert re.search(r' victim='+target+' side='+str(side)+r' killer=kano writes=0 assistance=none ',line)
                rows.append((line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
            proof=gate(rows,target,ident,side,groups)
            broken=copy.deepcopy(rows)
            action=next(r for t,r in broken if t=='ACTION')
            sample=next(r for t,r in broken if t=='STATE' and int(r['frame'])>int(action['frame'])+30)
            sample['poses']=sample['poses'].split(',')[0]+',FF959DD0'
            try:gate(broken,target,ident,side,groups)
            except AssertionError:pass
            else:raise AssertionError('Shang victim pose substituted for actual form accepted')
            cases[f'{target}{side}']=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),proxyShangPoseRejected=True)
    report=dict(passed=True,cases=cases,sourceSync=source_sync,compiledPoseSourceSHA256=sync.sha(cpp),
        fullPortAcceptance=False,scope='Four actual Shang-to-Kano/Sonya victim contexts under native Kano primary finisher, genuine selection/morph/322 damage/two KOs/native action/wrap/+120 fields, sampled victim pose rows match own compiled family. Not direct lookup invocation, full continuous art/audio/retirement, other victim finishers, CPU/campaign or full release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,fullPortAcceptance=False)))
