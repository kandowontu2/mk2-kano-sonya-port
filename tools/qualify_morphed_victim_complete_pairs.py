"""Full native pair ledger fills original ownership-gated STATE omissions."""
import copy,inspect,json,re
import verify_native_source_sync as sync
import qualify_bounded_morphed_victim_finishers as old

def complete_pair_gate(rows,ident,side,groups):
    def tagged(tag):return [r for t,r in rows if t==tag]
    action=tagged('ACTION')[0];wrap=tagged('WRAP')[0];result=tagged('RESULT')[0]
    start,end=int(action['frame']),int(result['frame'])
    peers=tagged('PEER');assert not tagged('PEER_MISSING')
    by={(int(r['frame']),int(r['slot'])):r for r in peers}
    assert len(by)==len(peers)==2*(end-start)
    assert set(by)=={(f,s) for f in range(start,end) for s in(1,2)}
    handoff=[]
    for (frame,slot),r in by.items():
        victim=slot==side
        assert (r['actor'],r['main'])==(action['victim_actor'],action['victim_main']) if victim else (r['actor'],r['main'])==(action['actor'],action['main'])
        assert int(r['character_id'])==(ident if victim else 17)
        assert r['roster']==('6' if victim else '17') and int(r['hp'])==(0 if victim else 161)
        if victim:assert r['owner']==r['actor']
        elif r['owner']!=r['actor']:
            assert r['owner']==r['attached'] and 0x01000000<=int(r['owner'],16)<0x01100000
            assert r['owner'] not in(action['actor'],action['victim_actor'])
            assert frame<int(wrap['frame'])
            handoff.append(r)
    assert handoff and len({r['owner'] for r in handoff})==1
    frames=sorted(int(r['frame']) for r in handoff)
    assert frames==list(range(frames[0],frames[-1]+1))
    assert by[end-1,3-side]['owner']==action['actor']
    victim_rows=[by[f,side] for f in range(start,int(wrap['frame'])+1)]
    first=next(i for i,r in enumerate(victim_rows) if int(r['pose'],16)==groups[0])
    poses=[int(r['pose'],16) for r in victim_rows[first:]]
    assert set(poses)==set(groups) and poses[-1]==groups[-1]
    order=list(dict.fromkeys(poses));assert order==groups
    return poses,dict(completePairedFields=end-start,nativeAttachedEffectOwnerFields=len(handoff),
        victimAlwaysOwned=True,attackerOwnerRestored=True,allSixOwnVictimGroupsInOrder=True)

source=inspect.getsource(old.gate)
start=source.index('    sampled=');end=source.index('    return dict(',start)
source=source[:start]+'    poses,pair_summary=complete_pair_gate(rows,ident,side,groups)\n'+source[end:]
namespace=dict(base=old.base,complete_pair_gate=complete_pair_gate)
exec(compile(source,__file__+'::original_morph_health_input_plus_complete_pairs','exec'),namespace)
gate=namespace['gate']

if __name__=='__main__':
    source_sync=sync.verify()
    out=sync.ROOT/'audit_morphed_victim_complete_pairs_checked';assert not out.exists()
    cpp=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    compiled=cpp.read_text()
    lua=sync.ROOT/'audit_morphed_victim_pair_observer_preparation/finishers.lua'
    cases={}
    for target,ident,array in(('kano',17,'kano_victim_groups'),('sonya',18,'kano_sonya_victim_groups')):
        match=re.search(r'constexpr uint32_t '+array+r'\[\]=\{([^}]+)\};',compiled);assert match
        groups=[int(v,16) for v in re.findall(r'0x[0-9a-f]+',match[1])];assert len(groups)==6
        for side in(1,2):
            folder=sync.ROOT/f'audit_morphed_victim_pair_{target}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in('.png','.bin','.wav') for p in folder.rglob('*'))
            text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
            rows=[]
            for line in text.splitlines():
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                assert re.search(r' victim='+target+' side='+str(side)+r' killer=kano writes=0 assistance=none ',line)
                rows.append((line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
            proof=gate(rows,target,ident,side,groups)
            _,pair_proof=complete_pair_gate(rows,ident,side,groups)
            baseline=sync.ROOT/f'audit_bounded_morphed_victim_finisher_{target}_p{side}_runtime/run.log'
            keep=lambda value:[line for line in value.splitlines() if line.startswith('MK2_STOCK_HEAD_V921_') and not line.startswith(('MK2_STOCK_HEAD_V921_PEER ','MK2_STOCK_HEAD_V921_PEER_MISSING '))]
            assert keep(text)==keep(baseline.read_text())
            broken=copy.deepcopy(rows)
            del broken[next(i for i,(t,r) in enumerate(broken) if t=='PEER')]
            try:gate(broken,target,ident,side,groups)
            except AssertionError:pass
            else:raise AssertionError('Missing real pair publication accepted')
            cases[f'{target}{side}']=dict(proof=proof,pairProof=pair_proof,terminal=terminal,
                logSHA256=sync.sha(folder/'run.log'),baselineSHA256=sync.sha(baseline),wholeOriginalTraceUnchanged=True,missingPairRejected=True)
    report=dict(passed=True,cases=cases,sourceSync=source_sync,compiledPoseSourceSHA256=sync.sha(cpp),
        fullPortAcceptance=False,scope='Four genuine Kano primary fatalities against Shang Kano/Sonya forms, all original native morph/selection/damage/command/wrap gates, complete action-through-wrap+120 paired publications, exact owned six-phase victim pose order and native attached attacker effect ownership/restoration. No complete raster/audio, direct table-invocation, full scene retirement, other finishers/CPU/campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,completePairedPublications=True,fullPortAcceptance=False)))
