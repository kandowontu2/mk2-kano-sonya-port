"""Passive own actor poses during genuine earned Kano wins."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_current_kano_native_winner_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text()
assert source.count('frame>=18000')==1
source=source.replace('frame>=18000','frame>=10200').replace('maximum_fields=18000','maximum_fields=10200')
source+='''
emu.register_frame_done(function()
 local a,m=p:read_u32(0x01060220),p:read_u32(0x01060260)
 if a>=0x01000000 and a<0x01100000 and m>=0x01000000 and m<0x01100000 and
 p:read_u16(0x01060280)==17 and p:read_u16(0x010602f0)>0 and p:read_u16(0x01060ec0)==0 then
  log('WINNER_POSE',string.format('actor=%08X main=%08X owner=%08X id=%d roster=17 hp=%d cpu_hp=0 pose=%08X action=%d mode=%d stage=%d attached=%08X',
   a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(0x010602f0),p:read_u32(a+0x1d0),p:read_u16(m+0x1f0),p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(m+0x190)))
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run_kano_p1.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_compact_kano_campaign_p1_runtime','audit_current_kano_native_winner_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared10200fields, unchanged physical controller, passive winner poses, no media')
