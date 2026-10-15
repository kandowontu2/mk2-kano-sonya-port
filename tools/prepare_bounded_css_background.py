"""Passive fixed marble-edge signatures during physical roster navigation."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_css_cadence_preparation'
out=sync.ROOT/'audit_bounded_css_background_preparation';assert not out.exists();out.mkdir()
source=(old/'css.lua').read_text()
marker="    log('CADENCE',string.format('age=%d roster=%d border=%d posehash=%08X',age,roster,lit,h))"
assert source.count(marker)==1
extra="""    local bh=2166136261
    local bx=side==1 and 0 or 392
    for y=105,240 do for x=bx,bx+7 do bh=((bh~pixel(x,y))*16777619)&0xffffffff end end
    log('BACKGROUND',string.format('age=%d roster=%d hash=%08X',age,roster,bh))
"""
source=source.replace(marker,marker+'\n'+extra)
lua=out/'background.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(old.name+'/css.lua',out.name+'/background.lua').replace(sync.sha(old/'css.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_bounded_css_cadence_{fighter}_p{side}_runtime',f'audit_bounded_css_background_{fighter}_p{side}_runtime')
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,physicalInputsOnly=True,scope='Fixed eight-pixel marble strip beside each native pose; not full occluded background')))
