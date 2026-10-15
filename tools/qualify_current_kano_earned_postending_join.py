"""Earned ending prefix and fresh physically selected native P2 controls."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_earned_postending_join_runtime'
out=root/'audit_current_kano_earned_postending_join_checked';assert not out.exists()
def load(path):
    lines=path.read_text().splitlines();assert not any('LUA ERROR' in s for s in lines)
    return [(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in lines if s.startswith('MK2_NAT_CAMPAIGN_')]
rows=load(case/'run.log');prior=load(root/'audit_current_kano_p2_shao_backjump_charge_counter_runtime/run.log')
assert [(t,r) for t,r in rows if int(r['frame'])<=75116]==[(t,r) for t,r in prior if int(r['frame'])<=75116]
def gate(records):
    events={t:r for t,r in records if t.startswith('POST_ENDING_')}
    needed=['POST_ENDING_PAID_START','POST_ENDING_FIGHT','POST_ENDING_WALK','POST_ENDING_JUMP','POST_ENDING_PUNCH','POST_ENDING_RECOVERED','POST_ENDING_COMPLETE']
    assert all(t in events for t in needed) and 'POST_ENDING_BOUND' not in events
    assert [int(events[t]['frame']) for t in needed]==sorted(int(events[t]['frame']) for t in needed)
    assert events['POST_ENDING_FIGHT']['human']=='17:17' and events['POST_ENDING_FIGHT']['stage']=='0'
    assert events['POST_ENDING_JUMP']['action'] in ('776','779') and int(events['POST_ENDING_JUMP']['y'])<int(events['POST_ENDING_JUMP']['floor'])
    assert events['POST_ENDING_PUNCH']['action'] in ('257','276')
    assert events['POST_ENDING_COMPLETE']['human']=='17:17' and int(events['POST_ENDING_COMPLETE']['hp'])>0
    assert int(events['POST_ENDING_COMPLETE']['frame'])-int(events['POST_ENDING_RECOVERED']['frame'])>=180
    assert any(t=='SELECT_ID' and int(r['frame'])>75116 and r['roster']=='17' for t,r in records)
    assert all(r['writes']=='0' and r['assistance']=='none' for _,r in records)
    return events
events=gate(rows);rejected=[]
for name,mutate in [('missing_punch',lambda r:r.__setitem__(slice(None),[(t,s) for t,s in r if t!='POST_ENDING_PUNCH'])),
 ('proxy_identity',lambda r:next(s for t,s in r if t=='POST_ENDING_FIGHT').update(human='1:1')),
 ('dead_at_completion',lambda r:next(s for t,s in r if t=='POST_ENDING_COMPLETE').update(hp='0'))]:
    bad=copy.deepcopy(rows);mutate(bad)
    try:gate(bad)
    except AssertionError:rejected.append(name)
    else:raise AssertionError('Fault accepted:'+name)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(earnedEndingPrefixExactlyPreservedThrough=75116,currentKanoP2FreshPostEndingJoinControlsPassed=True,
    events=events,faultsRejected=rejected,terminal=terminal,logSHA256=sync.sha(case/'run.log'),
    scope='One fresh physical Coin/Start/reselect Kano17 after his natural ending; ordinary walk/jump/punch/recovery in stage0. Not all post-ending stages, palettes, audio, or other fighters/slots.',fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
