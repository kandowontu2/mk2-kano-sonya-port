"""Unchanged HK inputs plus passive Baraka throw start; same 90s wall limit."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_guard_ready_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_hk_throw_onset_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if other.roster==9 and stage==5 then\n')
end=source.index('   if other.roster==8 and stage==1 then\n',start)
block=source[start:end].replace('other.roster==9 and stage==5','other.roster==3 and stage==6').replace('~=5 then return end','~=6 then return end').replace('c.id~=9 or c.roster~=9','c.id~=3 or c.roster~=3').replace('rt_taps','bt_taps').replace('REPTILE_THROW_START','BARAKA_THROW_START').replace('passive Reptile throw initiation','passive Baraka throw initiation')
assert 'BARAKA_THROW_START' in block
source='local bt_taps={}\n'+source[:start]+block+source[start:]
old="if frame>=60000 then log('HOST_BOUND','maximum_fields=60000 full_campaign_acceptance=false')"
assert source.count(old)==1
source=source.replace(old,"if frame>=70000 then log('HOST_BOUND','maximum_fields=70000 full_campaign_acceptance=false')")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_guard_ready_runtime','audit_current_sonya_p2_baraka_hk_throw_onset_runtime').replace("'-str','1250'","'-str','1500'")
(out/'run.ps1').write_text(runner)
print('Unchanged HK inputs/passive Baraka throw starts/70k ceiling;still90sec/320MiB/10MiB/no media')
