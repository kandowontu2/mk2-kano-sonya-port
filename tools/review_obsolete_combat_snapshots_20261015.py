"""Exact four-folder legacy snapshot manifest, retaining original UI source shots."""
from pathlib import Path
p=Path(__file__).with_name('review_obsolete_capture_targets_20261015.py')
s=p.read_text()
replacements={
 "out=R/'audit_obsolete_capture_target_review_20261015'":"out=R/'audit_obsolete_combat_snapshot_review_20261015'",
 "('obj_dump2','native_kano_knife_clean_fast2','native_kano_knife_clean_fast',\n               'native_kano_knife_scan_late_fast','native_kano_knife_scan')":"('special_join_kano','special2p_kano','special2p_sonya','special_health_kano')",
 "path=R/folder/'snap'":"path=R/'snap'/folder",
 "Unreferenced legacy exploratory emulator snapshots, not native ROM/GFX or accepted proof captures.":"Unreferenced legacy combat screenshots, not native ROM/GFX, original select/HUD UI source or accepted audit proof captures.",
 "only five exact /snap subtrees proposed.":"only four exact snap/special* subtrees proposed. Root snap/mk2ks and snap/mk3 retained because original UI source screenshot identity is unresolved.",
 "these exact legacy folder names found storage inventory/census entries only":"these four exact legacy combat folder names found storage inventory/census entries only"
}
for old,new in replacements.items():
    assert s.count(old)==1,old
    s=s.replace(old,new)
exec(compile(s,str(p),'exec'))
