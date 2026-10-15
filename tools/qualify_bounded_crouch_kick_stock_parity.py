"""Finite light-hit audio routing parity, not heard-audio acceptance."""
import json
import re
import verify_native_source_sync as sync

def main():
    out = sync.ROOT/'audit_bounded_crouch_kick_stock_parity_checked'
    assert not out.exists()
    cases = {}
    for fighter, ident in (('sonya',18), ('kano',17), ('baraka',3), ('mileena',5)):
        suffix = 'pain' if ident >=17 else 'control'
        folder = sync.ROOT/f'audit_bounded_{fighter}_crouch_kick_{suffix}_runtime'
        terminal = json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields=[];branches=[];hits=[];ended=False
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line and len(line)<65536
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));tag=line.split(' ',1)[0]
                if tag.endswith('_FIELD'):fields.append(r)
                elif tag.endswith('_PAIN_BRANCH'):branches.append(r)
                elif tag.endswith('_CONTACT_HEALTH'):hits.append(r)
                elif tag.endswith('_IDLE_TERMINAL'):ended=r['fields']=='240'
        assert ended and len(fields)==480
        for r in fields:
            assert int(r['id'])==int(r['roster'])==(ident if r['slot']=='1' else 4)
            assert r['actor']==r['owner'] and r['writes']=='0' and r['assistance']=='none'
        assert len(hits)==1 and hits[0]['slot']=='1'
        assert hits[0]['before']=='161' and hits[0]['after']=='155'
        assert hits[0]['pc']=='FF836700' and hits[0]['mask']=='FFFF'
        assert len(branches)==1
        r=branches[0]
        assert r['route']=='female' and r['a2']=='00000004'
        assert r['a8']==r['actor2'] and r['a13']==r['main2']
        assert r['id1']==str(ident) and r['id2']=='4'
        assert int(hits[0]['frame'])-int(r['frame'])==6
        cases[fighter]=dict(trueID=ident,damage=6,attackerGruntOnly=True,
                            fieldCount=len(fields),logSha256=sync.sha(folder/'run.log'),
                            terminal=terminal)
    report=dict(passed=True,cases=cases,sourceSync=sync.verify(),
                scope='One crouch LowKick contact per fighter against stock Kitana',
                subjectiveAudioAccepted=False,allAudioContextsAccepted=False,fullGoalComplete=False)
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases=list(cases),damagePerCase=6,
                         nativeVictimPainBranchAbsentInAddedAndStockCases=True)))

if __name__=='__main__':main()
