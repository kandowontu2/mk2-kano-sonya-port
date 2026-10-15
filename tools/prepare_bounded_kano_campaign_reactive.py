"""Physical policy experiment only from natural stage3; preserve zoning run."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_bounded_kano_campaign_reactive_preparation'
assert not out.exists()
out.mkdir()
base=old/'campaign.lua'
source=base.read_text()
marker=' local stage=p:read_u16(0x01061b30);local schedule=p:read_u32(0x01061b10)\n'
assert source.count(marker)==1
source=source.replace(marker,marker+''' if stage>=3 and stage<15 and strategy~='reactive' then
  strategy='reactive';log('POLICY','stage='..stage..' physical_policy=reactive_jumpkick')
 elseif stage>=15 and strategy~='zoning' then
  strategy='zoning';log('POLICY','stage='..stage..' physical_policy=original_boss_zoning')
 end
''')
lua=out/'campaign.lua'
lua.write_text(source)
runner=(old/'run_kano_p1.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base),sync.sha(lua))
runner=runner.replace('audit_bounded_compact_kano_campaign_p1_runtime','audit_bounded_kano_campaign_reactive_p1_runtime')
(out/'run_kano_p1.ps1').write_text(runner)
print('Prepared stage3 reactive physical policy; unchanged18000field/90sec safety bounds')
