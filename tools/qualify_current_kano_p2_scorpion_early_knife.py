"""Same native campaign and actually owned ball/knife activation gates."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_ball_knife.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_ball_knife','audit_current_kano_p2_scorpion_early_knife')
exec(compile(source,__file__+'::same_native_campaign_gate','exec'))
