"""Strict same-attempt Kintaro clear and true native Shao admission."""
import copy,json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_approved_180s_runtime'
out=root/'audit_current_kano_p2_kintaro_advance_checked'
assert not out.exists()
prior=json.loads((root/'audit_current_kano_p2_approved_180s_checked/report.json').read_text())
assert prior['passedFinitePrefixChecks'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=load(case/'run.log')
def gate(records):
    fight=next(r for r in records['FIGHT'] if r['frame']=='63589')
    assert fight['stage']=='15' and fight['human']=='17:17' and fight['cpu']=='12:12'
    nxt=next(r for r in records['FIGHT'] if r['frame']=='69699')
    assert nxt['stage']=='16' and nxt['human']=='17:17' and nxt['cpu']=='13:13' and nxt['schedule']=='FFFA3180'
    wins=[r for r in records['WIN'] if r['stage']=='15' and r['slot']=='2' and 63589<int(r['frame'])<69699]
    assert [r['frame'] for r in wins]==['65340','69176']
    assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
    assert not any(63589<int(r['frame'])<69699 for r in records['LOSS'])
    assert next(r for r in records['WIN'] if r['frame']=='67219')['slot']=='1'
    return dict(kintaroAttempt=fight,ownedRoundWins=wins,nextShaoFight=nxt)
proof=gate(rows);faults=[]
for name in ['wrongwinner','paidloss','proxy_next_actor']:
    bad=copy.deepcopy(rows)
    if name=='wrongwinner':next(r for r in bad['WIN'] if r['frame']=='69176')['slot']='1'
    elif name=='paidloss':bad['LOSS'].append(dict(frame='68000',stage='15'))
    else:next(r for r in bad['FIGHT'] if r['frame']=='69699')['human']='1:1'
    try:gate(bad)
    except (AssertionError,StopIteration):faults.append(name)
    else:raise AssertionError('False native boss clear accepted '+name)
shaowins=[r for r in rows['WIN'] if r['stage']=='16' and r['slot']=='2']
report=dict(passedFiniteChecks=True,currentKintaroMatchCleared=True,trueKanoAdmittedToShao=True,proof=proof,ownedShaoRounds=shaowins,earnedEndingObserved=bool(rows.get('PICTURE') or rows.get('TEXT')),rejectedFaults=faults,logSHA256=sync.sha(case/'run.log'),fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
