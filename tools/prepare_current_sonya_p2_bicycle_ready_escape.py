"""Physical back jump on actual ready recovery, no forced action/position."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_midrange_bicycle_preparation'
out=sync.ROOT/'audit_current_sonya_p2_bicycle_ready_escape_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
changes=[
 ('then kb_start=nil;kb_retry=-1000 end','then kb_start=nil;kb_retry=-1000;ke_start=nil end'),
 ('    if kb_start and frame-kb_start<90 then',"    if ke_start and frame-ke_start<4 then\n     press('Up');press(ke_backward)\n    elseif height>8 then\n     if gap<140 and frame%6<3 then press('High Kick')end\n    elseif kb_start and frame-kb_start<90 then"),
 ("     if age>=20 then press('Down');press('Block')end", "     if age>=24 and ready then\n      kb_start=nil;ke_start=frame;ke_backward=backward;press('Up');press(backward)\n      log('BICYCLE_READY_ESCAPE',string.format('gap=%d action=%d flags=%04X',gap,human.action,human.flags))\n     elseif age>=20 then press('Down');press('Block')end"),
 ('    elseif ready and safe and gap<120 then kb_start=nil;press(backward)',"    elseif ready and gap<120 then kb_start=nil;ke_start=frame;ke_backward=backward;press('Up');press(backward)")]
for before,after in changes:
    assert source.count(before)==1,before
    source=source.replace(before,after)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_midrange_bicycle_runtime','audit_current_sonya_p2_bicycle_ready_escape_runtime')
(out/'run.ps1').write_text(runner)
print('CPU0-only actual-ready backjump/airHK after bicycle;60k/90sec/320MiB/10MiB/no media')
