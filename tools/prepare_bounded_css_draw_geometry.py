"""Passive actual native FIFO geometry while selection sprites animate."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_css_background_preparation'
out=sync.ROOT/'audit_bounded_css_draw_geometry_preparation';assert not out.exists();out.mkdir()
source=(old/'background.lua').read_text()
marker='local taps={}\n';assert source.count(marker)==1
source=source.replace(marker,marker+"""taps[#taps+1]=p:install_read_tap(0xff804420,0xff80442f,'CSS native actual FIFO geometry',function(at,data,mask)
 if at~=0xff804420 or cpu.PC.value~=0xff804420 or not css_at or exit_at then return end
 local age=frame-css_at
 if not(age>=54 and age<=70 or age>=78 and age<=94 or age>=224 and age<=260)then return end
 local actor=cpu.A0.value
 if valid(actor)then
  local id=p:read_u16(actor+0x1f0)
  if id==17 or id==18 or id==1 or id==9 then
   log('DRAW',string.format('age=%d actor=%08X id=%d xy=%08X size=%08X source=%08X command=%08X',age,actor,id,cpu.A10.value,cpu.A9.value,cpu.A11.value,cpu.A12.value))
  end
 end
end)
""")
lua=out/'geometry.lua';lua.write_text(source)
for side in (1,2):
 runner=(old/f'run_kano_p{side}.ps1').read_text()
 runner=runner.replace(old.name+'/background.lua',out.name+'/geometry.lua').replace(sync.sha(old/'background.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_bounded_css_background_kano_p{side}_runtime',f'audit_bounded_css_draw_geometry_kano_p{side}_runtime')
 (out/f'run_kano_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,actualNativeFIFO=True,physicalInputsOnly=True)))
