"""Observer neutrality and native Kung Lao damage, not campaign acceptance."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_cage_contact_trace.py').read_text()
changes=[('audit_current_sonya_p2_cage_contact_trace','audit_current_sonya_p2_kunglao_contact_trace'),
 ('audit_current_sonya_p2_cage_hk_retreat_runtime','audit_current_sonya_p2_campaign_render_skip_runtime'),
 ('SONYA_CAGE_DAMAGE','SONYA_KUNGLAO_DAMAGE'),("r['ids']=='2,18'","r['ids']=='0,18'"),
 ('cage-contact.json','kunglao-contact.json')]
for before,after in changes:
    assert before in source,before
    source=source.replace(before,after)
exec(compile(source,__file__+'::native_contact_gate','exec'))
