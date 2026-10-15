"""Actual native P1 stage chronology; no jump-plan success claim."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p1_learned_campaign.py').read_text().replace('audit_current_kano_p1_learned_campaign_runtime','audit_current_kano_p1_kintaro_retreat_jump_runtime').replace('audit_current_kano_p1_learned_campaign_checked','audit_current_kano_p1_kintaro_retreat_jump_checked')
exec(compile(source,__file__+'::kintaro_retreat_jump','exec'))
