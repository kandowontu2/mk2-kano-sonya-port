"""Finite input-free3field ROM/GFX component probe; never forces an ending."""
import json,re,struct
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_loaded_dispatch_boundaries_preparation'
out=root/'audit_current_loaded_sonya_ending_components_preparation';assert not out.exists()
old=root/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
assert sync.sha(old)=='37E02771B1F20CF17D0D619F83033F5FE37FE5B62DCD9519F60872763BE0E57A'
source=old.read_text();stockpath=root/'mk2/mk2-maincpu.bin';stock=stockpath.read_bytes()
assert sync.sha(stockpath)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
block=source[source.index('char const *const ending_story[2][5]'):source.index('\n\t};',source.index('char const *const ending_story[2][5]'))]
strings=[json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"',block)]
assert len(strings)==10;stories=strings[5:]
def pc(byte):return 0xff800000+byte*8
texts=[]
for page in (0,1):
 for segment in range(3 if page==0 else 2):
  slot=pc((0xf4a00 if page==0 else 0xf4b00)+(18*3+segment)*4)
  script=pc(0xf4c00+(5+(3 if page else 0)+segment)*0xc0)
  template_source=(0xff8f5550 if page==0 else 0xff8f59d0)+(8*3+segment)*32
  template=struct.unpack_from('<I',stock,(template_source-0xff800000)//8)[0]
  story=stories[(3 if page else 0)+segment].encode('ascii')+b'\0'
  header=stock[(template-0xff800000)//8:(template-0xff800000)//8+24]
  texts.append(dict(page=page+1,segment=segment,at=slot,pointer=script,headerHex=header.hex().upper(),textHex=story.hex().upper(),textBytes=len(story)))
cursor=0
pictures=[]
for fighter in (0,1):
 for page in (0,1):
  width,height=(124,163) if page==0 else (280,119)
  cursor=(cursor+1)&~1
  if fighter==1:pictures.append(dict(index=52+page,at=pc(0xf4900+(52+page)*4),pointer=0x07100000+cursor*8,width=width,height=height,planes=1,palette=256))
  cursor+=8+256*2+25+(width*height*9+7)//8
continuations={0xff844700:0x270,0xff8448a0:0x270,0xff844720:0x170,0xff844970:0x170,0xff844740:0x190,0xff844ab0:0x190,0xff844760:0x1b0,0xff844b40:0x1b0}
operands={0xff8f51c0:pc(0xf4a00),0xff8f53e0:pc(0xf4b00),0xff8447b0:pc(0xf4900)}
null=pc(0xf4b00+(18*3+2)*4)
expected=dict(texts=texts,pictures=pictures,continuations={f'{k:08X}':v for k,v in continuations.items()},operands={f'{k:08X}':v for k,v in operands.items()},secondPageNull=dict(at=null,value=0),historicalSourceSHA256=sync.sha(old),stockSHA256=sync.sha(stockpath),sourceComponentProofSHA256=sync.sha(root/'audit_current_sonya_ending_component_transfer_checked/report.json'))
lines=['local p=manager.machine.devices[":maincpu"].spaces.program','local frame=0',
 'local function hexbytes(at,count)local s={} for i=0,count-1 do local a=at+i*8;local w=p:read_u16(a&~15);s[#s+1]=string.format("%02X",(w>>(a&8))&255)end return table.concat(s)end',
 'emu.register_frame_done(function()',' frame=frame+1',' if frame~=3 then return end']
for t in texts:
 lines.append(f" local q=p:read_u32(0x{t['at']:08x});print(string.format('MK2_ENDING_TEXT page={t['page']} segment={t['segment']} pointer=%08X header=%s text=%s writes=0 assistance=none',q,hexbytes(q,24),hexbytes(q+192,{t['textBytes']})))")
for p in pictures:
 lines.append(f" local q=p:read_u32(0x{p['at']:08x});print(string.format('MK2_ENDING_PICTURE index={p['index']} pointer=%08X width=%d height=%d planes=%d palette=%d writes=0 assistance=none',q,p:read_u16(q),p:read_u16(q+16),p:read_u16(q+32),p:read_u16(q+48)))")
for at in operands:lines.append(f" print(string.format('MK2_ENDING_OPERAND at={at:08X} value=%08X writes=0 assistance=none',p:read_u32(0x{at:08x})))")
for at in continuations:lines.append(f" print(string.format('MK2_ENDING_CONTINUATION at={at:08X} value=%04X writes=0 assistance=none',p:read_u16(0x{at:08x})))")
lines.append(f" print(string.format('MK2_ENDING_NULL at={null:08X} value=%08X writes=0 assistance=none',p:read_u32(0x{null:08x})))")
lines+=[' print("MK2_ENDING_COMPONENT_DONE fields=3 inputs=0 writes=0 assistance=none")',' manager.machine:exit()','end)']
lua='\n'.join(lines)+'\n'
assert all(x not in lua for x in (':write_',':snapshot(',':set_value('))
out.mkdir();path=out/'components.lua';path.write_text(lua);(out/'expected.json').write_text(json.dumps(expected,indent=2)+'\n')
runner=(base/'run.ps1').read_text().replace(base.name+'/tables.lua',out.name+'/components.lua').replace(sync.sha(base/'tables.lua'),sync.sha(path)).replace('audit_current_loaded_dispatch_boundaries_runtime','audit_current_loaded_sonya_ending_components_runtime').replace('Elapsed.TotalSeconds -gt 90','Elapsed.TotalSeconds -gt 180')
(out/'run.ps1').write_text(runner)
print(json.dumps(dict(preparedOnly=True,textSegments=5,pictureHeaders=pictures,continuationWords=8,operands=3,LuaSHA256=sync.sha(path),expectedSHA256=sync.sha(out/'expected.json'))))
