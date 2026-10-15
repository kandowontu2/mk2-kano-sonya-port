"""Complete original ADDXY A5 floor projection and effective RAM scanout faults."""
from pathlib import Path
base=Path(__file__).with_name('current_babality_ram_v5452.py')
source=base.read_text()
changes={
 "audit_v5453_current_babality_ram":"audit_v5456_current_babality_ram",
 "audit_v5454_current_babality_progress":"audit_v5457_current_babality_progress",
 "LUA=ROOT/'mk2ks_current_babality_ram_v5452.lua'":"LUA=ROOT/'mk2ks_current_babality_ram_v5455.lua'",
 "Path(display.__file__).resolve(),Path(__file__).resolve(),":"ROOT/'mk2ks_current_babality_ram_v5452.lua',ROOT/'tools/current_babality_ram_v5452.py',Path(display.__file__).resolve(),Path(__file__).resolve(),",
 "   coordinate=world if body&1 else (((world>>16)-(camera>>16))&65535)<<16|((world-camera)&65535)\n   need(int(q['xy'],16)==coordinate and body&2==0,'Original single-frame native world/camera projection, no inferred sprite offset')":
 "   signed=lambda value:(value&65535)-65536 if value&32768 else value&65535\n   x,y=signed(world),signed(world>>16)\n   if not body&1:x-=signed(camera);y-=signed(camera>>16)\n   size=int(q['size'],16);command_word=int(q['command'],16)>>16\n   if command_word&16:x+=(size&65535)-1\n   if command_word&32:y+=(size>>16)-1\n   origin=int(q['display'],16);x+=signed(origin);y+=signed(origin>>16)\n   need((int(q['xy'],16)&1023,int(q['xy'],16)>>16&511)==(x&1023,y&511)and body&2==0,'Complete original single-frame camera/flip/ADDXY A5 projection')",
 "  out.append(bound)":
 "  if age==160:\n   image=images[filename];palette=np.frombuffer(colors,dtype='<u4');vr=np.frombuffer(raw,dtype='<u2').reshape(512,512)\n   pixel_index=int(vr[actual['row'],actual['column']])&0x7fff;pixel_color=int(palette[pixel_index])\n   faults=[]\n   def reject(label,fn):\n    try:fn()\n    except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))\n    else:raise ValueError('Actual scanout counterexample accepted: '+label)\n   altered=image.copy();altered[0,0,0]^=1\n   reject('actual displayed RGB pixel corrupted',lambda:display.check_latch(altered,raw,colors,int(r['start'],16),int(r['control'],16),int(r['tap'],16)))\n   changed=bytearray(colors);struct.pack_into('<I',changed,pixel_index*4,pixel_color^1)\n   reject('actual latched native palette pen corrupted',lambda:display.check_latch(image,raw,changed,int(r['start'],16),int(r['control'],16),int(r['tap'],16)))\n   candidates=np.flatnonzero(palette!=pixel_color);need(len(candidates)>0,'Effective different actual palette color')\n   changed=bytearray(raw);struct.pack_into('<H',changed,(actual['row']*512+actual['column'])*2,int(candidates[0]))\n   reject('actual displayed native VRAM pixel corrupted',lambda:display.check_latch(image,changed,colors,int(r['start'],16),int(r['control'],16),int(r['tap'],16)))\n   bound['effectiveActualScanoutRAMFaults']=faults\n  out.append(bound)",
}
for before,after in changes.items():
 assert source.count(before)==1,before
 source=source.replace(before,after)
exec(compile(source,str(base)+'.complete_native_ADDXY_A5_projection_and_RAM_faults','exec'),globals())
