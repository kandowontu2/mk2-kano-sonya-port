"""Count actual native CSS-photo/pose FIFO submissions through ladder reveal."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_css_cadence_preparation'
out=sync.ROOT/'audit_bounded_css_teardown_preparation';assert not out.exists();out.mkdir()
source=(old/'css.lua').read_text()
marker='local taps={}\n';assert source.count(marker)==1
source=source.replace(marker,"""local photo_draws,pose_draws=0,0
"""+marker+"""taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'native CSS lifetime FIFO census',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not css_at or live_at then return end
 local src=cpu.A11.value
 if src==0x0f008000 or src==0x0f010000 then photo_draws=photo_draws+1 end
 local actor=cpu.A0.value
 if valid(actor) and (p:read_u16(actor+0x1f0)==17 or p:read_u16(actor+0x1f0)==18) and src>=0x10000000 and src<0x11000000 then pose_draws=pose_draws+1 end
end)
""")
marker='emu.register_frame(function()\n';assert source.count(marker)==1
source=source.replace(marker,marker+""" if css_at and not live_at then
  log('TEARDOWN',string.format('cssphotos=%d addedposes=%d exitframe=%d',photo_draws,pose_draws,exit_at or -1))
 end
 photo_draws,pose_draws=0,0
""")
lua=out/'teardown.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(old.name+'/css.lua',out.name+'/teardown.lua').replace(sync.sha(old/'css.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_bounded_css_cadence_{fighter}_p{side}_runtime',f'audit_bounded_css_teardown_{fighter}_p{side}_runtime')
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,actualNativeFIFO=True,physicalInputsOnly=True,rawMedia=False)))
