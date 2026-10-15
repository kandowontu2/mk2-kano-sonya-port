"""Harden unexecuted v2 gate: continuous fresh match, no intervening loss/reselect."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_ending_sonya_crossjoin_v2.py').read_text()
source=source.replace("out=root/'audit_current_kano_ending_sonya_crossjoin_v2_checked'","out=root/'audit_current_kano_ending_sonya_crossjoin_v3_checked'")
marker=' native_state(lo);native_state(hi)\n'
extra=""" native_state(lo);native_state(hi)
 for tag,r in records:
  if not lo<=int(r['frame'])<=hi:continue
  assert tag not in ('LOSS','SELECT','SELECT_ID','SELECT_EXIT','POST_ENDING_BOUND','HOST_BOUND')
  if tag=='STATE':
   assert r['mode']=='2' and r['states'].split(',')[1]=='1' and r['roster'].split(',')[1]=='18' and r['actors'].split(',')[1]==fight['actor'] and int(r['health'].split(',')[1])>0
 assert abs(int(events['POST_ENDING_WALK']['x'])-int(events['POST_ENDING_WALK']['from']))>=4
"""
assert source.count(marker)==1;source=source.replace(marker,extra,1)
old=" ('dead_at_completion',lambda r:next(s for t,s in r if t=='POST_ENDING_COMPLETE').update(hp='0')),"
new=old+"""
 ('intervening_loss',lambda r:r.append(('LOSS',dict(frame=str(int(next(s for t,s in r if t=='POST_ENDING_PUNCH')['frame'])+1),human_slot='2',fighter='kano',writes='0',assistance='none',stage='0')))),
 ('intervening_KO_state',lambda r:r.append(('STATE',dict(frame=str(int(next(s for t,s in r if t=='POST_ENDING_PUNCH')['frame'])+1),human_slot='2',fighter='kano',writes='0',assistance='none',mode='3',states='0,2',roster='17,18',actors='00000000,00000000',health='161,0',stage='0',winner='1')))),
 ('insufficient_walk_delta',lambda r:next(s for t,s in r if t=='POST_ENDING_WALK').update(x=next(s for t,s in r if t=='POST_ENDING_WALK')['from'])),"""
assert source.count(old)==1;source=source.replace(old,new,1)
source=source.replace('terminal=terminal,logSHA256=sync.sha(case/\'run.log\'),SonyaOwnEndingAccepted=False,fullPortAccepted=False,',"terminal=terminal,logSHA256=sync.sha(case/'run.log'),continuousFreshNativeStateAndNoLossReselectAccepted=True,physicalCoinINPUTRecordsAvailable=any(t=='INPUT' and int(r['frame'])>80232 for t,r in rows),coinTimingEvidence='immutable executed source + native actualattract/paidCSS, per-field INPUT logging intentionally suppressed after1690',stockOpcodeBytesVerifiedAtMovePC=False,SonyaOwnEndingAccepted=False,fullPortAccepted=False,")
exec(compile(source,__file__,'exec'))
