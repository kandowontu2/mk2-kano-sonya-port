"""Continuous opaque footprint checks, bounded row-offset cache per field."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_complete_throw_footprint_preparation'
    out=root/'audit_bounded_throw_window_footprint_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    changes={
        'coverage_context and frame-ready==128':'coverage_context and frame-ready>=114 and frame-ready<=176',
        'if not ready or (frame-ready)%8~=0 or at~=0xff804410':
            'if not ready or ((frame-ready)%8~=0 and not(frame-ready>=114 and frame-ready<=176)) or at~=0xff804410',
        'footprint_stats.points=footprint_stats.points+1':
            'footprint_stats.source_frame=q.frame;footprint_stats.points=footprint_stats.points+1',
        "'source_age=128 points=%d slot1=%d slot2=%d source_fail=%d display_fail=%d raw_media=none',footprint_stats.points":
            "'source_age=%d points=%d slot1=%d slot2=%d source_fail=%d display_fail=%d raw_media=none',footprint_stats.source_frame-ready,footprint_stats.points",
        ' idle_points={}\n shadow_queries={}':
            ' footprint_stats={points=0,source_fail=0,display_fail=0,slots={0,0}}\n idle_points={}\n shadow_queries={}',
        'local function queried_source_pixel(source,w,h,c,sx,sy)':
            'local source_row_cache={}\nlocal source_row_frame=-1\nlocal function queried_source_pixel(source,w,h,c,sx,sy)'}
    for before,after in changes.items():
        assert lua.count(before)==1,before;lua=lua.replace(before,after)
    before=''' for y=0,sy do
  local header=read(bit,8);bit=bit+8
  local pre=(header&15)<<((c>>8)&3);local post=(header>>4)<<((c>>10)&3)
  if y==sy then
   if sx<pre or sx>=w-post then return nil end
   return read(bit+(sx-pre)*bpp,bpp)
  end
  bit=bit+math.max(0,w-pre-post)*bpp
 end'''
    assert lua.count(before)==1
    lua=lua.replace(before,r'''
 if source_row_frame~=frame then source_row_frame=frame;source_row_cache={}end
 local key=string.format('%08X_%d_%d_%04X',mapped,w,h,c)
 local rows=source_row_cache[key]
 if not rows then
  rows={};source_row_cache[key]=rows
  for y=0,h-1 do
   local header=read(bit,8);bit=bit+8
   local pre=(header&15)<<((c>>8)&3);local post=(header>>4)<<((c>>10)&3)
   rows[y]={bit=bit,pre=pre,post=post}
   bit=bit+math.max(0,w-pre-post)*bpp
  end
 end
 local row=assert(rows[sy])
 if sx<row.pre or sx>=w-row.post then return nil end
 return read(row.bit+(sx-row.pre)*bpp,bpp)''')
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_complete_throw_footprint_runtime',
                              f'audit_bounded_{fighter}_throw_window_footprint_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
        captureAges=[114,176],observerSha=sync.sha(target))))

if __name__=='__main__':main()
