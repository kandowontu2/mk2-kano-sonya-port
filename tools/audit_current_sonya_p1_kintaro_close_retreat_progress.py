"""Exact pre-boss prefix and same-paid native progression for physical variant."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_liukang_short_leg_progress.py').read_text()
source=source.replace("old=root/'audit_current_sonya_p1_subzero_short_leg_runtime/run.log'","old=root/'audit_current_sonya_p1_boss_light_runtime/run.log'")
source=source.replace("new=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log'","new=root/'audit_current_sonya_p1_kintaro_close_retreat_runtime/run.log'")
source=source.replace("out=root/'audit_current_sonya_p1_liukang_short_leg_progress_checked'","out=root/'audit_current_sonya_p1_kintaro_close_retreat_progress_checked'")
source=source.replace('93653','107553')
old=" attempt=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])][-1]"
new=""" candidates=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])]
 latest=candidates[-1]
 attempt=next(r for r in candidates if r['selection']==latest['selection'])"""
assert source.count(old)==1
source=source.replace(old,new)
source=source.replace('endingAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,',"ownKintaroRoundWins=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='1'],endingAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,")
exec(compile(source,__file__,'exec'))
