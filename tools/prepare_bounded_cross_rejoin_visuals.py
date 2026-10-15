"""Prepare two later-scene PNGs per P1 reciprocal fatality action."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_cross_rejoin_visuals_preparation'
assert not out.exists()
out.mkdir()
base=sync.ROOT/'audit_bounded_secondary_rejoin_roster_ready_preparation/rejoin.lua'
source=base.read_text()
marker=" log('REJOIN_MARKER','sample='..label..' count='..visual_count..' media=none')"
assert source.count(marker)==1
source=source.replace(marker," screen:snapshot('rejoin_'..label..'.png');log('REJOIN_VISUAL_SAVED','sample='..label..' count='..visual_count)")
source=source.replace('assert(visual_count<=3)','assert(visual_count<=2)')
lua=out/'rejoin.lua'
lua.write_text(source)
old=sync.ROOT/'audit_bounded_cross_finisher_rejoin_preparation'
for kind in ('primary','secondary'):
    for fighter in ('kano','sonya'):
        runner=(old/f'run_{kind}_{fighter}_p1.ps1').read_text()
        runner=runner.replace(base.parent.name+'/'+base.name,out.name+'/'+lua.name).replace(sync.sha(base),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_cross_rejoin_{kind}_{fighter}_p1_runtime',f'audit_bounded_cross_rejoin_visual_{kind}_{fighter}_p1_runtime')
        runner=runner.replace("rawMedia='none'","rawMedia='bounded_two_png'")
        (out/f'run_{kind}_{fighter}.ps1').write_text(runner)
print('Prepared eight-image-capped P1 clearing review; no runs started')
