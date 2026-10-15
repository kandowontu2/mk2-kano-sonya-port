"""Omit diagnostic-only stage15 action trace; controller readiness taps retained."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p1_extended_default_preparation'
out=sync.ROOT/'audit_current_kano_p1_extended_light_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='      local current_stage=p:read_u16(0x01061b30)\n'
assert source.count(old)==1
source=source.replace(old,old+'      if current_stage==15 then return end -- diagnostic only; no controller variable updated here\n')
assert 'if current_stage==16 and data&0xffff==770' in source
assert 'if entry==0xff9d24c0 then cg_contact=frame;cg_main=c.main end' in source
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p1_extended_default_runtime','audit_current_kano_p1_extended_light_runtime')
(out/'run.ps1').write_text(runner)
print('Samecontrols/noStage15diagnosticActionTrace;140000ceiling/180sec/320MiB/10MiB')
