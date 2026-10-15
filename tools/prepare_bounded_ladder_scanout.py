"""Transient presented-pixel side-region signatures against physical stock control."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_css_teardown_owner_preparation'
out=sync.ROOT/'audit_bounded_ladder_scanout_preparation';assert not out.exists();out.mkdir()
source=(old/'owner.lua').read_text()
source=source.replace("local identity=fighter=='kano'and 17 or 18", "local stock_control=os.getenv('MK2KS_UI_STOCK_CONTROL')=='1'\nlocal identity=stock_control and (fighter=='kano'and 1 or 9) or (fighter=='kano'and 17 or 18)")
source=source.replace("  pulse('High Punch',age,264,8)","  if stock_control then pulse(stock_direction,age,240,4)end\n  pulse('High Punch',age,264,8)")
marker=' if exit_at then\n';assert source.count(marker)==1
extra="""  if not live_at then
   local w,h=manager.machine.video:snapshot_size()
   local raw=manager.machine.video:snapshot_pixels()
   assert(w==400 and h==254 and #raw==406400)
   local left,right=0xcbf29ce484222325,0xcbf29ce484222325
   for y=24,240 do
    for x=0,79 do left=(left~(string.unpack('<I4',raw,(y*400+x)*4+1)&0xffffff))*0x100000001b3 end
    for x=320,399 do right=(right~(string.unpack('<I4',raw,(y*400+x)*4+1)&0xffffff))*0x100000001b3 end
   end
   log('SCANOUT',string.format('age=%d left=%016X right=%016X stock=%d',frame-exit_at,left,right,stock_control and 1 or 0))
  end
"""
source=source.replace(marker,marker+extra)
lua=out/'scanout.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  for control in (False,True):
   suffix='stock' if control else 'added'
   runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
   runner=runner.replace(old.name+'/owner.lua',out.name+'/scanout.lua').replace(sync.sha(old/'owner.lua'),sync.sha(lua))
   runner=runner.replace(f'audit_bounded_css_teardown_owner_{fighter}_p{side}_runtime',f'audit_bounded_ladder_scanout_{fighter}_p{side}_{suffix}_runtime')
   runner=runner.replace('$taskArgs=',f"$env:MK2KS_UI_STOCK_CONTROL='{1 if control else 0}'\n$taskArgs=")
   (out/f'run_{fighter}_p{side}_{suffix}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,presentedPixels=True,rawMedia=False,regions=[[0,79,24,240],[320,399,24,240]],physicalStockControl=True)))
