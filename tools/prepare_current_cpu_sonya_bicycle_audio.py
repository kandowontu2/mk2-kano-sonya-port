"""Natural CPU Sonya launch/cry without paid challenger interruption."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_native_start_preparation'
out=sync.ROOT/'audit_current_cpu_sonya_bicycle_audio_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text().replace('frame>=30000','frame>=4000').replace('maximum_fields=30000','maximum_fields=4000')
template=(sync.ROOT/'audit_current_cpu_kano_ball_audio_preparation/campaign.lua').read_text()
observer=template[template.index('local audio_items,audio_channels,audio_launch,audio_signature='):]
observer=observer.replace('tonumber(n,16)>=12 and tonumber(n,16)<=13','tonumber(n,16)>=10 and tonumber(n,16)<=11')
observer=observer.replace('audio_channels[12]','audio_channels[10]').replace('for n=12,13 do','for n=10,11 do')
observer=observer.replace('data~=0x6b03','(data<0x6b01 or data>0x6b02)').replace('sample(2)','sample(1)').replace('actual.id~=17 or actual.roster~=17','actual.id~=18 or actual.roster~=18')
observer=observer.replace(':read(1)',':read(0)').replace('CPU_BALL_','CPU_BICYCLE_')
source+=observer
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_native_start_runtime','audit_current_cpu_sonya_bicycle_audio_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared4000fields; CPU Sonya two-channel voice; unchanged controls; no media')
