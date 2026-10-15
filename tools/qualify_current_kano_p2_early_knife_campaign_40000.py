"""Native campaign gate with exact progressing prior32k record prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_ball_knife_40000.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_ball_knife_40000','audit_current_kano_p2_early_knife_campaign_40000')
source=source.replace('audit_current_kano_p2_scorpion_ball_knife_runtime','audit_current_kano_p2_scorpion_early_knife_runtime')
exec(compile(source,__file__+'::same_native_campaign_gate','exec'))
