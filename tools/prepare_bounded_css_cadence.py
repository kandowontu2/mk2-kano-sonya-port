"""Passive frame signatures of native selection border and character pose."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_ui_review_select_preparation'
out=sync.ROOT/'audit_bounded_css_cadence_preparation';assert not out.exists();out.mkdir()
source=(old/'ui.lua').read_text()
source=source.replace('if captured>=8 then return end','if captured>=0 then return end')
marker="  log('SELECT',string.format('age=%d roster=%d css=%d',age,p:read_u16(slots[side].roster),css and 1 or 0))\n"
assert source.count(marker)==1
extra="""  if css then
   local roster=p:read_u16(slots[side].roster)
   local locations={[17]=19,[1]=79,[0]=139,[2]=199,[9]=259,[18]=319}
   local left=locations[roster]
   if left then
    local lit=0
    for y=20,97 do for x=left,left+62 do
     if x<left+4 or x>left+58 or y<24 or y>93 then
      local c=pixel(x,y)
      if (side==1 and c==0x00ff00)or(side==2 and c==0xff0000)then lit=lit+1 end
     end
    end end
    local h=2166136261
    local px=side==1 and 0 or 320
    for y=105,240 do for x=px,px+79 do h=((h~pixel(x,y))*16777619)&0xffffffff end end
    log('CADENCE',string.format('age=%d roster=%d border=%d posehash=%08X',age,roster,lit,h))
   end
  end
"""
source=source.replace(marker,marker+extra)
lua=out/'css.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(old.name+'/ui.lua',out.name+'/css.lua').replace(sync.sha(old/'ui.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_bounded_current_ui_select_{fighter}_p{side}_runtime',f'audit_bounded_css_cadence_{fighter}_p{side}_runtime')
  runner=runner.replace("rawMedia='at most eight bounded PNGs; no video/audio recording'","rawMedia='none'")
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,pixelBuffersDiscarded=True,physicalInputsOnly=True)))
