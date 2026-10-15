"""Actual ladder DMA sources/palettes near unexplained presented sky pixels."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_ladder_scanout_preparation'
out=sync.ROOT/'audit_bounded_ladder_sky_dma_preparation';assert not out.exists();out.mkdir()
source=(old/'scanout.lua').read_text()
marker='local taps={}\n';assert source.count(marker)==1
source=source.replace(marker,marker+"""taps[#taps+1]=p:install_write_tap(0x01a80010,0x01a8001f,'actual ladder DMA palette census',function(at,data)
 if at~=0x01a80010 or not exit_at then return end
 local age=frame-exit_at
 if not(age==86 or age==87 or age==99 or age==100 or age==199 or age==200)then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local pal=reg(8)&0x7f00
 local ph=2166136261
 for i=0,255 do ph=((ph~p:read_u16(0x01800000+(pal+i)*16))*16777619)&0xffffffff end
 log('SKYDMA',string.format('age=%d pc=%08X command=%04X source=%08X palette=%04X palhash=%08X x=%d y=%d width=%d height=%d',age,cpu.PC.value,data&0xffff,reg(2)|(reg(3)<<16),pal,ph,reg(4)&0x3ff,reg(5)&0x1ff,reg(6)&0x3ff,reg(7)&0x3ff))
end)
""")
lua=out/'sky.lua';lua.write_text(source)
for suffix in ('added','stock'):
 runner=(old/f'run_sonya_p2_{suffix}.ps1').read_text()
 runner=runner.replace(old.name+'/scanout.lua',out.name+'/sky.lua').replace(sync.sha(old/'scanout.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_bounded_ladder_scanout_sonya_p2_{suffix}_runtime',f'audit_bounded_ladder_sky_dma_sonya_p2_{suffix}_runtime')
 (out/f'run_{suffix}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,actualDMAAndPaletteReads=True,noRawMedia=True)))
