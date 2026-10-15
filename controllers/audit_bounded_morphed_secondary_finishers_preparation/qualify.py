"""Earned native secondary finishers from genuine Shang added-character forms."""
import copy
import inspect
import json
import re
import verify_native_source_sync as sync
import qualify_bounded_stock_head_finisher as prior

source = inspect.getsource(prior.gate)
source = source.replace("a['variant']=='1'", "a['variant']=='2'")
source = source.replace("a['address']=='FF8CB4A0'", "a['address']=={'kano':'FFD86600','sonya':'FFD7B000'}[fighter]")
before = "x['own'].split(':')[-1]=='3' and x['victim'].split(':')[-1]==str(ident)"
assert source.count(before) == 1
source = source.replace(before, "x['own'].split(':')[-1] in ('6',str(ident)) and x['victim'].split(':')[-1]=='4'")
namespace = {}
exec(compile(source, __file__+'::unchanged_earned_completion_gate', 'exec'), namespace)
base_gate = namespace['gate']

def gate(rows, fighter, identity, side):
    proof = base_gate(rows, fighter, identity)
    def tagged(tag): return [r for t, r in rows if t == tag]
    first = tagged('FIRST_LIVE')
    assert len(first) == 1 and first[0]['ids'] == '6,4'
    selection = tagged('SELECT')
    assert {int(r['slot']): int(r['target']) for r in selection} == {side:6, 3-side:4}
    stores = tagged('MORPH_STORE')
    assert len(stores) == 2
    form, restore = stores
    action, wrap = tagged('ACTION')[0], tagged('WRAP')[0]
    assert (form['old'],form['id'],form['roster'],form['pc'],form['a9']) == ('6',str(identity),'6','FF86E670',f'{identity:08X}')
    assert (restore['old'],restore['id'],restore['roster'],restore['pc'],restore['a0']) == (str(identity),'6','6','FFA16700','00000006')
    assert all((r['actor'],r['main']) == (action['actor'],action['main']) for r in stores)
    assert int(form['frame']) < int(action['frame']) < int(wrap['frame']) < int(restore['frame'])
    zeros = [r for r in tagged('HEALTH') if r['pc']=='FF836700' and r['after']=='0']
    assert len(zeros)==2 and int(zeros[0]['frame']) < int(form['frame']) < int(zeros[1]['frame']) < int(action['frame'])
    states = tagged('STATE')
    for r in states:
        expected = identity if int(form['frame']) < int(r['frame']) <= int(restore['frame']) else 6
        assert int(r['own'].split(':')[-1]) == expected
    intent = tagged('COMBAT_MORPH_BEGIN')
    assert len(intent)==1 and 0<int(intent[0]['victim_hp'])<=41
    due = int(intent[0]['frame'])+80
    presses = {(int(r['frame']),r['button']) for r in tagged('INPUT') if int(r['slot'])==side and due<=int(r['frame'])<due+40}
    if fighter=='kano':
        back = 'Left' if side==1 else 'Right'
        expected = {(due+i,back) for i in (0,1,8,9)} | {(due+i,'Down') for i in (4,5)} | {(due+i,'Low_Kick') for i in (8,9)}
    else:
        expected = {(due+i,key) for i in range(8) for key in ('Down','Low_Punch','Block')}
    assert presses == expected
    return dict(**proof, actualShangRoster=6, actualMorphedIdentity=identity,
        formFrame=int(form['frame']), restoreFrame=int(restore['frame']),
        nativeSecondaryFinisherFromActualForm=True, restoredAfterCommonCompletion=True)

if __name__=='__main__':
    source_sync = sync.verify()
    out = sync.ROOT/'audit_bounded_morphed_secondary_finishers_checked'
    assert not out.exists()
    results = {}
    lua = sync.ROOT/'audit_bounded_morphed_secondary_finishers_preparation/finishers.lua'
    for fighter, identity in (('kano',17),('sonya',18)):
        for side in (1,2):
            folder = sync.ROOT/f'audit_bounded_morphed_secondary_finisher_{fighter}_p{side}_runtime'
            terminal = json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert terminal['observerSha256']==sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
            rows=[]
            for line in (folder/'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and len(line)<65536
                if not line.startswith('MK2_STOCK_HEAD_V921_'): continue
                assert re.search(r' victim=kitana side='+str(3-side)+r' killer='+fighter+r' writes=0 assistance=none ',line)
                rows.append((line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
            proof=gate(rows,fighter,identity,side)
            broken=copy.deepcopy(rows)
            next(r for tag,r in broken if tag=='MORPH_STORE')['pc']='DEADBEEF'
            try: gate(broken,fighter,identity,side)
            except AssertionError: pass
            else: raise AssertionError('Foreign form store accepted')
            results[f'{fighter}{side}']=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),foreignFormWriterRejected=True)
    report=dict(passed=True,results=results,sourceSync=source_sync,
        observerSHA256=sync.sha(lua),fullPortAcceptance=False,
        scope='Four genuine Shang-to-added-form secondary finishers against Kitana, earned two KOs/322 damage, exact physical morph command, real native ID stores and action/wrap/return. Not friendly finishers, morphed victims, complete art/audio, CPU or whole-game acceptance.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,fullPortAcceptance=False)))
