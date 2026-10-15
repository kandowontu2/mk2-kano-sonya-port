-- Complete qualified physical/art/PCM/packet observers, plus read-only DCS
-- ROM-region transport. Native firmware/data and its mirrored/erased lanes
-- stay unchanged; no controller, guest, sound-port or file writes here.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_baraka_packet_origin_v5576.lua','rb'))
local source=f:read('*a');f:close()
assert(load(source,'@entire5576_native_physical_art_audio_packet_observers','t',_ENV))()
local region=assert(manager.machine.memory.regions[':dcs'])
assert(region.size==0xc00000 and region.bytewidth==2 and region.bitwidth==16 and region.length==0x600000)
local frame,checks=0,0
local function dump(phase)
 for offset=0,region.size-1,65536 do
  local words={}
  for at=offset,offset+65532,4 do words[#words+1]=string.pack('<I4',region:read_u32(at))end
  local raw=table.concat(words)
  local hex=raw:gsub('.',function(c)return string.format('%02X',c:byte())end)
  print(string.format('MK2_NATIVE_DCS_ROM phase=%s frame=%d seconds=%.12f writes=0 assistance=none offset=%d bytes=%d size=%d bytewidth=%d bitwidth=%d hex=%s',
   phase,frame,emu.time(),offset,#raw,region.size,region.bytewidth,region.bitwidth,hex))
 end
 checks=checks+1
end
emu.register_frame(function()frame=frame+1;if frame==1 then dump('startup')end end)
emu.register_stop(function()
 dump('terminal')
 assert(checks==2 and frame==5198,'Both complete original sound ROM checks and genuine native terminal')
 print(string.format('MK2_NATIVE_DCS_ROM_RESULT frame=%d checks=%d writes=0 assistance=none',frame,checks))
end)
