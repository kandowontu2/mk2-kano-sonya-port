"""Same-paid boss chronology and retained controller/native trace equivalence."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_liukang_short_leg_progress.py').read_text()
source=source.replace("old=root/'audit_current_sonya_p1_subzero_short_leg_runtime/run.log'","old=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log'")
source=source.replace("new=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log'","new=root/'audit_current_sonya_p1_boss_light_runtime/run.log'")
source=source.replace("out=root/'audit_current_sonya_p1_liukang_short_leg_progress_checked'","out=root/'audit_current_sonya_p1_boss_light_progress_checked'")
source=source.replace('93653','107553')
old=" attempt=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])][-1]"
new=""" candidates=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])]
 latest=candidates[-1]
 attempt=next(r for r in candidates if r['selection']==latest['selection'])"""
assert source.count(old)==1
source=source.replace(old,new)
marker="rows=load(new)"
extra="""def retained(path):
 lines=[]
 for s in path.read_text().splitlines():
  if not s.startswith('MK2_NAT_CAMPAIGN_'):continue
  frame=int(re.search(r'\\bframe=(\\d+)',s)[1])
  if frame>111442:continue
  tag=s.split()[0][17:]
  if tag in ('BOSS_ACTION','BOSS_HANDLER'):continue
  if tag=='BOSS_FIELD' and frame%120:continue
  lines.append(s)
 return lines
assert retained(old)==retained(new)
rows=load(new)"""
assert source.count(marker)==1
source=source.replace(marker,extra)
source=source.replace('matchingPrefixRecords=len(prefix(old)),','matchingPrefixRecords=len(prefix(old)),retainedNativeAndPhysicalRecordsEquivalentThrough=111442,retainedEquivalentRecords=len(retained(old)),')
exec(compile(source,__file__,'exec'))
