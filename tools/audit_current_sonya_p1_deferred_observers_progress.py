"""Retained native/control chronology, excluding only intentionally deferred early SPECIAL."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_liukang_short_leg_progress.py').read_text()
source=source.replace("old=root/'audit_current_sonya_p1_subzero_short_leg_runtime/run.log'","old=root/'audit_current_sonya_p1_boss_light_runtime/run.log'")
source=source.replace("new=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log'","new=root/'audit_current_sonya_p1_kintaro_deferred_observers_runtime/run.log'")
source=source.replace("out=root/'audit_current_sonya_p1_liukang_short_leg_progress_checked'","out=root/'audit_current_sonya_p1_deferred_observers_progress_checked'")
source=source.replace('93653','107553')
old=r"return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=107553]"
new=r"return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and not s.startswith('MK2_NAT_CAMPAIGN_SPECIAL ') and int(re.search(r'\bframe=(\d+)',s)[1])<=107553]"
assert source.count(old)==1
source=source.replace(old,new)
old=" attempt=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])][-1]"
new=""" candidates=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])]
 latest=candidates[-1]
 attempt=next(r for r in candidates if r['selection']==latest['selection'])"""
assert source.count(old)==1
source=source.replace(old,new)
source=source.replace("ownedStage12LegEntries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='12' and r['move']=='leg'],","earlySpecialEntryObservationIntentionallyOmitted=True,ownedStage12LegEntries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='12' and r['move']=='leg'],")
source=source.replace('endingAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,',"ownKintaroRoundWins=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='1'],endingAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,")
exec(compile(source,__file__,'exec'))
