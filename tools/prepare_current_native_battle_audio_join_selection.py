"""Keep physical paid join; observe actual selector window and all sample channels."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_battle_audio_join_preparation'
out=sync.ROOT/'audit_current_native_battle_audio_join_selection_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='if n and tonumber(n,16)>=10 and tonumber(n,16)<=13 then'
assert source.count(old)==1
source=source.replace(old,'if n and tonumber(n,16)>=0 and tonumber(n,16)<=18 then')
old='if age<=300 then';assert source.count(old)==1
source=source.replace(old,'if age<=300 or (join_selection and frame-join_selection<=160) then')
old='for n=10,13 do';assert source.count(old)==1
source=source.replace(old,'for n=0,18 do')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_battle_audio_join_runtime','audit_current_native_battle_audio_join_selection_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared actual selector160fields plus first300cue fields,19scalar channels,no media')
