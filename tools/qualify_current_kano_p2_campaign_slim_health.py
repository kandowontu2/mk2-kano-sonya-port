"""Exact retained guest-prefix check against same physical render-skip route."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_campaign_render_skip.py').read_text()
source=source.replace("case=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_runtime'","case=sync.ROOT/'audit_current_kano_p2_campaign_slim_health_runtime'")
source=source.replace("oldcase=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_runtime'","oldcase=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_runtime'")
source=source.replace('audit_current_kano_p2_campaign_render_skip_checked','audit_current_kano_p2_campaign_slim_health_checked')
source=source.replace("lua=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_preparation/campaign.lua'","lua=sync.ROOT/'audit_current_kano_p2_campaign_slim_health_preparation/campaign.lua'")
source=source.replace("priorlua=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_preparation/campaign.lua'","priorlua=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_preparation/campaign.lua'")
source=source.replace("assert source.replace(marker,marker.replace('80000','60000'))==priorlua.read_text()", "assert source.replace(\" if tag=='HEALTH' and frame>=1690 then return end\\n\",'')==priorlua.read_text()")
source=source.replace("if tag not in ('RESULT','HOST_BOUND'):","if tag not in ('HEALTH','RESULT','HOST_BOUND'):")
source=source.replace("assert all(r['human']=='17:17'", "assert [r for r in rows.get('HEALTH',[]) if int(r['frame'])<1690]==[r for r in old.get('HEALTH',[]) if int(r['frame'])<1690]\nassert not any(int(r['frame'])>=1690 for r in rows.get('HEALTH',[]))\nassert all(r['human']=='17:17'")
exec(compile(source,__file__+'::retained_native_prefix_gate','exec'))
