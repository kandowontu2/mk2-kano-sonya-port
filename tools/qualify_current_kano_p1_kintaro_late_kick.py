"""Direct native P1 chronology, immutable prior runtime evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p1_learned_campaign.py').read_text().replace('audit_current_kano_p1_learned_campaign_runtime','audit_current_kano_p1_kintaro_late_kick_runtime').replace('audit_current_kano_p1_learned_campaign_checked','audit_current_kano_p1_kintaro_late_kick_checked')
exec(compile(source,__file__+'::kintaro_late_kick','exec'))
