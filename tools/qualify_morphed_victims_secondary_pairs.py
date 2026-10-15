"""Earned secondary fatalities with complete actual transformed-victim identity traces."""
import copy, inspect, json, re
import verify_native_source_sync as sync
import qualify_bounded_stock_head_finisher as stock
import qualify_bounded_morphed_victim_finishers as original

def make_gate(killer, killer_id, address):
    code = inspect.getsource(stock.gate)
    code = code.replace("a['variant']=='1'", "a['variant']=='2'")
    code = code.replace("a['address']=='FF8CB4A0'", f"a['address']=='{address}'")
    code = code.replace("x['own'].split(':')[-1]=='3' and x['victim'].split(':')[-1]==str(ident)",
                        f"x['own'].split(':')[-1]=='{killer_id}' and x['victim'].split(':')[-1] in ('6',str(ident))")
    namespace = {}; exec(compile(code, __file__+'::earned', 'exec'), namespace)
    code = inspect.getsource(original.gate)
    code = code.replace("first[0]['ids']=='17,6'", f"first[0]['ids']=='{killer_id},6'")
    code = code.replace('{side:6,3-side:17}', f'{{side:6,3-side:{killer_id}}}')
    start, end = code.index('    sampled='), code.index('    return dict(')
    code = code[:start] + '    poses = paired(rows, ident, side, killer_id)\n' + code[end:]
    namespace = dict(base=namespace['gate'], paired=paired, killer_id=killer_id)
    exec(compile(code, __file__+'::morph', 'exec'), namespace)
    return namespace['gate']

def paired(rows, ident, side, killer_id):
    def tagged(tag): return [r for t,r in rows if t==tag]
    action, result = tagged('ACTION')[0], tagged('RESULT')[0]
    start, end = int(action['frame']), int(result['frame'])
    peers = tagged('PEER'); assert not tagged('PEER_MISSING')
    by = {(int(r['frame']),int(r['slot'])):r for r in peers}
    assert len(by)==len(peers)==2*(end-start)
    assert set(by)=={(f,s) for f in range(start,end) for s in (1,2)}
    for (frame,slot), r in by.items():
        victim = slot==side
        expected = (action['victim_actor'],action['victim_main']) if victim else (action['actor'],action['main'])
        assert (r['actor'],r['main'])==expected and r['owner']==r['actor']
        assert int(r['character_id'])==(ident if victim else killer_id)
        assert int(r['roster'])==(6 if victim else killer_id)
        assert int(r['hp'])==(0 if victim else 161)
    return [int(by[f,side]['pose'],16) for f in range(start,end)]

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_morphed_victims_secondary_pairs_checked'; assert not out.exists()
    lua=sync.ROOT/'audit_morphed_victims_secondary_preparation/finishers.lua'
    cases={}
    for killer,killer_id,address in (('kano',17,'FFD86600'),('sonya',18,'FFD7B000')):
        gate=make_gate(killer,killer_id,address)
        for target,ident in (('kano',17),('sonya',18)):
            for side in (1,2):
                folder=sync.ROOT/f'audit_morphed_victim_secondary_{killer}_{target}_p{side}_runtime'
                terminal=json.loads((folder/'terminal.json').read_text())
                assert terminal['exitCode']==0 and terminal['limitReason'] is None
                assert terminal['observerSha256']==sync.sha(lua)
                assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90
                assert terminal['logBytes']<=10*1024*1024
                assert not (folder/'stderr.log').read_text().strip()
                assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
                rows=[]
                for line in (folder/'run.log').read_text().splitlines():
                    assert 'LUA ERROR' not in line
                    if not line.startswith('MK2_STOCK_HEAD_V921_'): continue
                    assert re.search(r' victim='+target+' side='+str(side)+r' killer='+killer+r' writes=0 assistance=none ',line)
                    rows.append((line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
                proof=gate(rows,target,ident,side,[])
                bad=copy.deepcopy(rows)
                next(r for t,r in bad if t=='PEER' and int(r['slot'])==side)['character_id']='6'
                try: gate(bad,target,ident,side,[])
                except AssertionError: pass
                else: raise AssertionError('Proxy victim identity accepted')
                bad=copy.deepcopy(rows); bad.pop(next(i for i,(t,r) in enumerate(bad) if t=='PEER'))
                try: gate(bad,target,ident,side,[])
                except AssertionError: pass
                else: raise AssertionError('Missing paired field accepted')
                cases[f'{killer}_{target}_p{side}']=dict(proof=proof,terminal=terminal,
                    logSHA256=sync.sha(folder/'run.log'),proxyIdentityRejected=True,missingFieldRejected=True)
    report=dict(passed=True,cases=cases,sourceSync=source_sync,checkerSHA256=sync.sha(__file__),
        fullPortAcceptance=False,fullEffectArtAccepted=False,
        scope='Eight genuine Shang-form victim contexts: native physical morph commands, 322 real damage, two earned KOs, secondary action and common wrap plus 120 fields; complete paired actor/Main/owner/true-ID/roster/health continuity. Not full effect choreography, raster/audio, scene retirement, CPU/campaign or release acceptance.')
    out.mkdir(); (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=8,completePairedIdentity=True,fullPortAcceptance=False)))

if __name__=='__main__': main()
