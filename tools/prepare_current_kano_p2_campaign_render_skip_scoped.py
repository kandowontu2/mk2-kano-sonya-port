"""Scoped host-bound rewrite; never touch hardware addresses containing 60000."""
from pathlib import Path
source=Path(__file__).with_name('prepare_current_kano_p2_campaign_render_skip.py').read_text()
source=source.replace("assert source.count('60000')==2\nsource=source.replace('60000','80000')", "old=\"if frame>=60000 then log('HOST_BOUND','maximum_fields=60000 full_campaign_acceptance=false')\"\nassert source.count(old)==1\nsource=source.replace(old,old.replace('60000','80000'))")
exec(compile(source,__file__+'::scoped_host_bound','exec'))
