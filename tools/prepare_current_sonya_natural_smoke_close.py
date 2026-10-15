"""Closer physical uppercuts; keep original earned Portal prefix intact."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_natural_smoke_preparation'
out=sync.ROOT/'audit_current_sonya_natural_smoke_close_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old="if math.abs(h.x-v.x)>100 then press(side,forward)"
assert source.count(old)==1
source=source.replace(old,"if math.abs(h.x-v.x)>(arena==7 and 62 or 100)then press(side,forward)")
source+='''
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'native Portal uppercut',function(at)
 if at==0xff870dc0 and p:read_u16(0x01061ac0)==7 then
  local h,v=sample(side),sample(3-side)
  if h and v then log('PORTAL_UPPERCUT',string.format('a8=%08X a13=%08X own=%08X main=%08X gap=%d ids=%d,%d',cpu.A8.value,cpu.A13.value,h.actor,h.main,math.abs(h.x-v.x),h.id,v.id))end
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_natural_smoke_runtime','audit_current_sonya_natural_smoke_close_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared only Portal approach62 plus passive native uppercut tap;28000fields/90sec/no media')
