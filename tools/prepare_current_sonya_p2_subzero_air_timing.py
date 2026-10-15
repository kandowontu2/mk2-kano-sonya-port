"""Bounded every-frame first SubZero action pair; unchanged physical controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_air_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_air_timing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source=source.replace('frame>=16000','frame>=9000').replace('maximum_fields=16000','maximum_fields=9000')
source+='''
local timing_start=nil
emu.register_frame_done(function()
 if p:read_u16(0x01061b30)~=1 then return end
 if not timing_start then timing_start=frame end
 if frame-timing_start>=1000 then return end
 for n=1,2 do
  local actor=p:read_u32(slots[n].actor)
  local main=p:read_u32(slots[n].main)
  if actor>=0x01000000 and actor<0x01100000 and main>=0x01000000 and main<0x01100000 then
   log('AIR_TIMING',string.format('age=%d slot=%d actor=%08X main=%08X owner=%08X id=%d action=%d x=%d y=%d floor=%d flags=%04X body=%04X hp=%d mode=%d',
    frame-timing_start,n,actor,main,p:read_u32(main+0xc0),p:read_u16(actor+0x1f0),p:read_u16(main+0x1f0),
    p:read_i16(actor+0x90),p:read_i16(actor+0xb0),p:read_i16(main+0x200),p:read_u16(main+0x210),
    p:read_u16(actor+0x160),p:read_u16(slots[n].hp),p:read_u16(0x010601d0)))
  end
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_subzero_air_runtime','audit_current_sonya_p2_subzero_air_timing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared first1000SubZero fields actual action pairs,9000total fields,no media')
