"""Owned native airkick/contact-return windows, not block labels or whole-game proof."""
import collections,json,subprocess
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT
out=root/'audit_current_sonya_p1_kintaro_airkick_windows_checked';assert not out.exists()
stock=root/'mk2/mk2-maincpu.bin';exe=root/'mame-mkp/unidasm.exe'
assert sync.sha(stock)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
text=subprocess.check_output([str(exe),str(stock),'-arch','tms34010','-skip',str((0xff871e40-0xff800000)//8),'-count','1136','-basepc','0xff871e40','-norawbytes'],text=True)
needles=['ff871f30: MOVE   A0,*A13(1F0h),0','ff872020: JA     FF875DF0h','ff872050: JRNC   FF872250h','ff8720b0: MOVE   A0,*A13(1F0h),0','ff872120: JA     FF876590h','ff872270: MOVE   A0,*A13(1F0h),0']
assert all(n in text for n in needles)
path=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log';rows=load(path)
fields={r['frame']:r for r in rows['BOSS_FIELD'] if r['stage']=='15'}
actions=[r for r in rows['BOSS_ACTION'] if r['stage']=='15']
kicks=[r for r in actions if r['after']=='512' and r['pc']=='FF871F50']
cycles=[]
for k in kicks:
 assert k['id']==k['roster']=='18' and k['actor']==k['owner']==k['a8'] and k['main']==k['a13'] and k['mask']=='FFFF'
 f=fields[k['frame']]
 recovery=next((r for r in actions if 0<=int(r['frame'])-int(k['frame'])<=32 and r['main']==k['main'] and r['actor']==k['actor'] and r['before']=='512' and r['after']=='1549'),None)
 if recovery is None:
  cycles.append(dict(entry=k,entryField=f,recovery=None,classification='interrupted or censored; never paired to later round'));continue
 assert recovery['pc'] in ('FF8720D0','FF872290')
 health=[r for r in rows['HEALTH'] if r['slot']=='2' and r['pc']=='FF836700' and int(k['frame'])<=int(r['frame'])<=int(recovery['frame']) and int(r['before'])>int(r['after']) and r['a13']==k['main']]
 cycles.append(dict(entry=k,entryField=f,recovery=recovery,classification='collision-return carry path' if recovery['pc']=='FF8720D0' else 'collision-return no-carry path',cpuHPCallbacks=health,blockClassificationAccepted=False))
captures=[r for r in actions if r['pc']=='FF8428A0' and r['after']=='0']
report=dict(nativeOwnedAirKickEntries=len(kicks),cycles=cycles,
 entryGapRange=[min(int(c['entryField']['gap']) for c in cycles),max(int(c['entryField']['gap']) for c in cycles)],
 entryHeightRange=[min(int(c['entryField']['height']) for c in cycles),max(int(c['entryField']['height']) for c in cycles)],
 classifications=dict(collections.Counter(c['classification'] for c in cycles)),
 actualCapturedAfter1549=sum(c['before']=='1549' for c in captures),
 gapOnlyGate100WouldRejectObservedEntries=any(int(c['entryField']['gap'])>100 for c in cycles),
 proposedUnexecutedChange='Delay HK until actual descending height<=60; current entries all87..94 high. Gap<=100 alone would not alter observed entry snapshots. Lower attack/recovery window hypothesis, not a proven win.',
 sourceDisassembly=text,sourceInstructionsVerified=needles,
 logSHA256=sync.sha(path),completeAttackOwnershipAndBlockingAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('nativeOwnedAirKickEntries','entryGapRange','entryHeightRange','classifications','actualCapturedAfter1549','gapOnlyGate100WouldRejectObservedEntries')}))
