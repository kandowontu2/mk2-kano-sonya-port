"""Seal one bounded physical Baraka leg experiment, not full campaign acceptance."""
import copy
import json
import re
import verify_native_source_sync as sync


def load(path):
    rows=[]
    for line in path.read_text().splitlines():
        assert 'LUA ERROR' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            rows.append((line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows


def gate(rows, prior):
    assert [(t,r) for t,r in rows if int(r['frame'])<=50237] == [(t,r) for t,r in prior if int(r['frame'])<=50237]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    plans=[r for t,r in rows if t=='SONYA_BARAKA_SHORT_LEG_PLAN']
    entries=[r for t,r in rows if t=='SPECIAL' and r['move']=='leg' and r['stage']=='6']
    assert plans and entries
    for r in entries:
        assert r['id']==r['roster']=='18' and r['entry']=='FFF80800' and r['pc']=='FFF80830'
        assert r['actor']==r['a8'] and r['main']==r['a13']
        assert any(p['actor']==r['actor'] and p['main']==r['main'] and int(r['frame'])-int(p['frame'])==5 for p in plans)
    fights=[r for t,r in rows if t=='FIGHT']
    assert all(r['human']=='18:18' and r['schedule']=='FFFA3180' for r in fights)
    damage=[r for t,r in rows if t=='SONYA_BARAKA_DAMAGE']
    assert damage and all(r['ids']=='3,18' and int(r['after'])<int(r['before'])<=161 for r in damage)
    rounds=[r for t,r in rows if t=='WIN' and r['stage']=='6' and r['slot']=='2']
    assert all(r['id']=='18' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in rounds)
    attempts={}; selection=None; ended=False; advanced=False
    for tag,r in rows:
        if tag=='FIGHT' and r['stage']=='6':
            selection=r['selection']; attempts.setdefault(selection,dict(firstFight=int(r['frame']),ownWins=[],cpuWins=[],loss=None));ended=False
        elif tag=='WIN' and r['stage']=='6':
            assert selection is not None and not ended
            attempts[selection]['ownWins' if r['slot']=='2' else 'cpuWins'].append(int(r['frame']))
        elif tag=='LOSS' and r['stage']=='6':
            assert selection is not None
            attempts[selection]['loss']=int(r['frame']);ended=True
        elif tag=='STAGE' and r['stage']=='7':
            assert selection is not None and not ended and len(attempts[selection]['ownWins'])==2 and len(attempts[selection]['cpuWins'])<=1
            advanced=True
    return dict(prefixExactlyPreservedThrough=50237,plannedLegChords=len(plans),actualOwnedLegEntries=len(entries),
                ownBarakaRoundWins=rounds,paidBarakaAttempts=attempts,stage7Observed=advanced,
                lastLoggedField=max(int(r['frame']) for t,r in rows),
                outgoingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
                incomingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'))


def main():
    sync.verify()
    case=sync.ROOT/'audit_current_sonya_p2_baraka_short_leg_runtime'
    out=sync.ROOT/'audit_current_sonya_p2_baraka_short_leg_checked';assert not out.exists()
    terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
    assert (terminal['exitCode']==0 and terminal['limitReason'] is None) or terminal['limitReason']=='wall_limit'
    assert terminal['elapsedSeconds']<=181 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_p2_baraka_short_leg_preparation/campaign.lua')
    assert not (case/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in case.rglob('*'))
    rows=load(case/'run.log');prior=load(sync.ROOT/'audit_current_sonya_p2_baraka_ring_finish20_runtime/run.log')
    result=gate(rows,prior);faults=[]
    for label,key,value in [('proxy special identity','id','1'),('wrong native entry','entry','FFFFB400'),('unowned native Main','a13','00000000')]:
        bad=copy.deepcopy(rows);next(r for t,r in bad if t=='SPECIAL' and r['move']=='leg' and r['stage']=='6')[key]=value
        try:gate(bad,prior)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Fault admitted '+label)
    report=dict(passed=True,**result,terminal=terminal,effectiveFaultsRejected=faults,
                logSHA256=sync.sha(case/'run.log'),fullPortAccepted=False,
                caveat='Raw HP totals and isolated wins do not prove a match, normalized strategy improvement, or a game defect. All earlier physical/native chronology retained; game/build untouched.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,plans=result['plannedLegChords'],entries=result['actualOwnedLegEntries'],ownRounds=len(result['ownBarakaRoundWins']),stage7=result['stage7Observed'],terminal=terminal)))


if __name__=='__main__':main()
