"""Complete Sonya burn and native opposite-actor ownership over real forms."""
import copy,inspect,json,re
import verify_native_source_sync as sync
import qualify_bounded_stock_head_finisher as stock
import qualify_bounded_morphed_victim_finishers as original

base_source=inspect.getsource(stock.gate)
base_source=base_source.replace("a['address']=='FF8CB4A0'","a['address']=='FFFAB200'")
base_source=base_source.replace("x['own'].split(':')[-1]=='3' and x['victim'].split(':')[-1]==str(ident)","x['own'].split(':')[-1]=='18' and x['victim'].split(':')[-1] in ('6',str(ident))")
namespace={};exec(compile(base_source,__file__+'::earned_finish_gate','exec'),namespace)
base=namespace['gate']

def burn_pairs(rows,ident,side,groups,outro,counts):
    def tagged(tag):return [r for t,r in rows if t==tag]
    action,wrap,result=tagged('ACTION')[0],tagged('WRAP')[0],tagged('RESULT')[0]
    start,end=int(action['frame']),int(result['frame'])
    peers=tagged('PEER');assert not tagged('PEER_MISSING')
    by={(int(r['frame']),int(r['slot'])):r for r in peers}
    assert len(by)==len(peers)==2*(end-start) and set(by)=={(f,s) for f in range(start,end) for s in(1,2)}
    switched=[]
    for (frame,slot),r in by.items():
        victim=slot==side
        assert (r['actor'],r['main'])==((action['victim_actor'],action['victim_main']) if victim else (action['actor'],action['main']))
        assert int(r['character_id'])==(ident if victim else 18)
        assert r['roster']==('6' if victim else '18') and int(r['hp'])==(0 if victim else 161)
        if victim:assert r['owner']==r['actor']
        elif r['owner']!=r['actor']:
            assert r['owner']==action['victim_actor'] and frame<int(wrap['frame'])
            switched.append(frame)
    assert len(switched)==4*len(groups) and sorted(switched)==list(range(min(switched),max(switched)+1))
    assert by[max(switched)+1,3-side]['owner']==action['actor']
    assert by[end-1,3-side]['owner']==action['actor']
    poses=[int(by[f,side]['pose'],16) for f in sorted(switched)]
    assert poses==[group for group in groups for _ in range(4)]
    expected_outro=[group for group,count in zip(outro,counts) for _ in range(count*4)]
    actual_outro=[int(by[f,3-side]['pose'],16) for f in sorted(switched)[18*4:]]
    assert actual_outro==expected_outro
    return poses,dict(completePairedFields=end-start,nativeOppositeActorOwnerFields=len(switched),
        all29BurnGroupsExactFourFieldTiming=True,allEightOutroGroupsExactTiming=True,
        victimAlwaysOwned=True,attackerOwnerRestored=True)

gate_source=inspect.getsource(original.gate)
gate_source=gate_source.replace("first[0]['ids']=='17,6'","first[0]['ids']=='18,6'")
gate_source=gate_source.replace('{side:6,3-side:17}','{side:6,3-side:18}')
start=gate_source.index('    sampled=');end=gate_source.index('    return dict(',start)
gate_source=gate_source[:start]+'    poses,pair_summary=burn_pairs(rows,ident,side,groups,OUTRO,COUNTS)\n'+gate_source[end:]

if __name__=='__main__':
    source_sync=sync.verify()
    out=sync.ROOT/'audit_morphed_victims_sonya_primary_checked';assert not out.exists()
    cpp=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp';compiled=cpp.read_text()
    def values(name,type_name='uint32_t'):
        match=re.search(r'constexpr '+type_name+' '+name+r'\[\]=\{([^}]+)\};',compiled);assert match
        return [int(v,0) for v in re.findall(r'0x[0-9a-f]+|\b\d+\b',match[1])]
    groups=values('sonya_burn_groups');outro=values('sonya_outro_groups');counts=values('sonya_outro_burn_counts','unsigned')
    assert len(groups)==29 and len(outro)==len(counts)==8 and sum(counts)==11
    context=dict(base=base,burn_pairs=burn_pairs,OUTRO=outro,COUNTS=counts)
    exec(compile(gate_source,__file__+'::real_victim_morph_command_gate','exec'),context);gate=context['gate']
    lua=sync.ROOT/'audit_morphed_victim_pair_observer_preparation/finishers.lua'
    cases={}
    for target,ident in(('kano',17),('sonya',18)):
        for side in(1,2):
            folder=sync.ROOT/f'audit_morphed_victim_sonya_primary_{target}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in('.png','.bin','.wav') for p in folder.rglob('*'))
            rows=[]
            for line in (folder/'run.log').read_text().splitlines():
                assert 'LUA ERROR' not in line
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                assert re.search(r' victim='+target+' side='+str(side)+r' killer=sonya writes=0 assistance=none ',line)
                rows.append((line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
            proof=gate(rows,target,ident,side,groups)
            _,pairs=burn_pairs(rows,ident,side,groups,outro,counts)
            broken=copy.deepcopy(rows)
            next(r for t,r in broken if t=='PEER' and int(r['slot'])==side and r['pose']==f'{groups[0]:08X}')['pose']='FF959DD0'
            try:gate(broken,target,ident,side,groups)
            except AssertionError:pass
            else:raise AssertionError('Shang body substituted in full burn sequence accepted')
            cases[f'{target}{side}']=dict(proof=proof,pairProof=pairs,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),wrongBurnPoseRejected=True)
    report=dict(passed=True,cases=cases,sourceSync=source_sync,compiledPoseSourceSHA256=sync.sha(cpp),fullPortAcceptance=False,
        scope='Four actual Shang Kano/Sonya form victims under Sonya primary finisher: real selection/morph/322 damage/two KOs/native action/wrap/+120, full paired publication, exact29 four-field burn groups and eight timed salute groups, native opposite-actor owner restoration. Not complete raster/palette/audio, direct helper invocation, full scene retirement, secondary/stock finishers/CPU/campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,completeNativeBurnSequence=True,fullPortAcceptance=False)))
