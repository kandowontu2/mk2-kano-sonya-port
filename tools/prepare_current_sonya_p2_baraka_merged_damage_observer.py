"""Merge passive stage HP observers; unchanged best physical controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_guard_ready_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_merged_damage_observer_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do\n')
end=source.index('for n,slot in ipairs(slots)do\n',start)
original=source[start:end]
assert original.count('p:install_write_tap')==5
body=original[original.index('  local before,after='):original.index('\n end)\nend')]
body=body.replace('c.id~=8 or c.roster~=8','c.id~=spec[1] or c.roster~=spec[1]').replace("log('SONYA_SUBZERO_DAMAGE',",'log(spec[2],').replace('ids=8,18','ids=%d,18').replace('c.actor,c.main,h.action,c.action','c.actor,c.main,spec[1],h.action,c.action')
merged="""local damage_stages={[1]={8,'SONYA_SUBZERO_DAMAGE'},[2]={2,'SONYA_CAGE_DAMAGE'},[3]={0,'SONYA_KUNGLAO_DAMAGE'},[5]={9,'SONYA_REPTILE_DAMAGE'},[6]={3,'SONYA_BARAKA_DAMAGE'}}
for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(observed_hp,observed_hp+15,'merged passive stage damage',function(at,data,mask)
  if at~=observed_hp or mask~=0xffff then return end
  local spec=damage_stages[p:read_u16(0x01061b30)]
  if not spec then return end
"""+body+"\n end)\nend\n"
source=source[:start]+merged+source[end:]
source=source.replace('frame>=60000','frame>=70000').replace('maximum_fields=60000','maximum_fields=70000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_guard_ready_runtime','audit_current_sonya_p2_baraka_merged_damage_observer_runtime').replace("'-str','1000'","'-str','1500'")
(out/'run.ps1').write_text(runner)
print('Merged passive10stageHPtaps to2, identical best inputs/90sec/320MiB/10MiB/no media')
