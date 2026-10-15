"""Earned Kano ending -> real paid Sonya P2 controls; not Sonya's own ending."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
case=root/'audit_current_kano_ending_sonya_crossjoin_v2_runtime'
out=root/'audit_current_kano_ending_sonya_crossjoin_v2_checked';assert not out.exists()
def load(path):
 lines=path.read_text().splitlines();assert not any('LUA ERROR' in s for s in lines)
 return [(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in lines if s.startswith('MK2_NAT_CAMPAIGN_')]
rows=load(case/'run.log');prior=load(root/'audit_current_kano_postending_two_coin_join_runtime/run.log')
assert [(t,r) for t,r in rows if int(r['frame'])<=75116]==[(t,r) for t,r in prior if int(r['frame'])<=75116]
assert [(t,r) for t,r in rows if int(r['frame'])<=80232]==[(t,r) for t,r in prior if int(r['frame'])<=80232]
def gate(records):
 needed=['POST_ENDING_ATTRACT','POST_ENDING_PAID_START','POST_ENDING_FIGHT','POST_ENDING_WALK','POST_ENDING_JUMP','POST_ENDING_PUNCH','POST_ENDING_RECOVERED','POST_ENDING_COMPLETE']
 events={t:r for t,r in records if t in needed}
 assert all(t in events for t in needed) and not any(t=='POST_ENDING_BOUND' for t,r in records)
 assert [int(events[t]['frame']) for t in needed]==sorted(int(events[t]['frame']) for t in needed)
 assert events['POST_ENDING_ATTRACT']['mode']=='1' and events['POST_ENDING_ATTRACT']['frame']=='80232'
 paid=events['POST_ENDING_PAID_START'];assert paid['target']=='18' and paid['previous']=='17' and paid['coin_ages']=='20,50' and paid['start_age']=='100'
 assert int(paid['frame'])==80252
 fight=events['POST_ENDING_FIGHT'];done=events['POST_ENDING_COMPLETE']
 for r in (fight,done):assert r['human']=='18:18' and r['id']==r['roster']=='18' and r['owner']==r['actor']
 assert fight['stage']=='0' and fight['actor']==done['actor'] and fight['main']==done['main'] and int(done['hp'])>0
 lo,hi=int(fight['frame']),int(done['frame'])
 def native_state(frame):
  state=[r for t,r in records if t=='STATE' and int(r['frame'])<=frame][-1]
  assert state['mode']=='2' and state['states'].split(',')[1]=='1' and state['roster'].split(',')[1]=='18' and state['actors'].split(',')[1]==fight['actor']
  return state
 native_state(lo);native_state(hi)
 selected=[r for t,r in records if t=='SELECT_ID' and int(paid['frame'])<int(r['frame'])<lo]
 assert selected and all(r['roster']=='18' for r in selected)
 stores=[r for t,r in records if t=='POST_ENDING_MOVE_STORE' and lo<=int(r['frame'])<=hi]
 assert stores
 for r in stores:
  assert r['id']==r['roster']=='18' and r['actor']==r['owner']==r['a8']==fight['actor'] and r['main']==r['a13']==fight['main']
  assert int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF' and int(r['hp'])>0 and 0xff800000<=int(r['pc'],16)<=0xffffffff
  native_state(int(r['frame']))
 jump=events['POST_ENDING_JUMP'];punch=events['POST_ENDING_PUNCH'];recovery=events['POST_ENDING_RECOVERED']
 assert jump['action'] in ('776','779') and int(jump['y'])<int(jump['floor'])
 assert punch['action'] in ('257','276')
 jumps=[r for r in stores if r['after'] in ('776','779') and int(events['POST_ENDING_WALK']['frame'])<=int(r['frame'])<=int(jump['frame'])]
 punches=[r for r in stores if r['after'] in ('257','276') and int(jump['frame'])<int(r['frame'])<=int(punch['frame'])]
 recovered=[r for r in stores if r['after'] in ('0','771') and int(punch['frame'])<int(r['frame'])<=int(recovery['frame'])]
 assert jumps and punches and recovered and hi-int(recovery['frame'])>=180
 assert all(r['writes']=='0' and r['assistance']=='none' for t,r in records)
 return dict(events=events,ownedJumpStores=jumps,ownedPunchStores=punches,ownedRecoveryStores=recovered)
accepted=gate(rows);faults=[]
for name,mutate in (
 ('missing_owned_jump',lambda r:r.__setitem__(slice(None),[(t,s) for t,s in r if not(t=='POST_ENDING_MOVE_STORE' and s['after'] in ('776','779'))])),
 ('proxy_fresh_identity',lambda r:next(s for t,s in r if t=='POST_ENDING_FIGHT').update(human='1:1')),
 ('wrong_move_owner',lambda r:next(s for t,s in r if t=='POST_ENDING_MOVE_STORE').update(owner='00000000')),
 ('not_actual_attract',lambda r:next(s for t,s in r if t=='POST_ENDING_ATTRACT').update(mode='11')),
 ('dead_at_completion',lambda r:next(s for t,s in r if t=='POST_ENDING_COMPLETE').update(hp='0')),
):
 bad=copy.deepcopy(rows);mutate(bad)
 try:gate(bad)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Fresh crossjoin fault accepted:'+name)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']=='85C0F69A4E78BF9E2D6F61B7EE40500EE6FEC9453DEECD385E5C3A25A879CEFB'
assert not (case/'stderr.log').read_text().strip()
report=dict(earnedKanoEndingPrefixExactlyPreservedThrough=75116,actualCreditsAttractPrefixExactlyPreservedThrough=80232,
 currentEarnedKanoEndingThenPaidSonyaP2ControlsAccepted=True,accepted=accepted,rejectedFaults=faults,
 terminal=terminal,logSHA256=sync.sha(case/'run.log'),SonyaOwnEndingAccepted=False,fullPortAccepted=False,
 scope='One earned KanoP2 ending -> actual attract -> physical two coins/Start/native Sonya18 select -> owned walk/jump/punch/recovery plus180livefields. Not Sonya own ending, allslots, allpostendingstages, heardaudio or pixelacceptance.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
