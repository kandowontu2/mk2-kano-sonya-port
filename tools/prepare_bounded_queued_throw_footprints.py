"""Retain current-field points; include both native clipped video buffers."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_throw_window_footprint_preparation'
    out=root/'audit_bounded_queued_throw_footprint_preparation';assert not out.exists()
    original=(old/'prepared_observer.lua').read_text()
    out.mkdir()
    for phase,lo,hi in (('opening',114,144),('landing',145,176)):
        lua=original
        needle='frame-ready>=114 and frame-ready<=176';assert lua.count(needle)==2
        lua=lua.replace(needle,f'frame-ready>={lo} and frame-ready<={hi}')
        needle='dx<400 and dy<254 and dx>=actual_dma[16]';assert lua.count(needle)==1
        lua=lua.replace(needle,'dx<400 and dx>=actual_dma[16]')
        needle=' for _,q in ipairs(idle_points)do\n  local xx,yy=q.x-column,q.y-row'
        assert lua.count(needle)==1
        lua=lua.replace(needle,' local future_points={}\n for _,q in ipairs(idle_points)do\n  if q.frame<frame then\n  local xx,yy=q.x-column,q.y-row')
        needle='  end -- full footprint bypasses per-pixel logging\n end'
        assert lua.count(needle)==1
        lua=lua.replace(needle,'  end -- full footprint bypasses per-pixel logging\n  else future_points[#future_points+1]=q end\n end')
        needle=' idle_points={}\n shadow_queries={}';assert lua.count(needle)==1
        lua=lua.replace(needle,r'''
 idle_points=future_points
 shadow_queries={}
 for _,q in ipairs(future_points)do
  if not q.fullbody then
   local key=string.format('%d_%d_%d',q.frame,q.x,q.y)
   shadow_queries[key]=shadow_queries[key]or{}
   shadow_queries[key][#shadow_queries[key]+1]=q
  end
 end''')
        assert ':write_' not in lua
        target=out/f'{phase}_observer.lua';target.write_text(lua)
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}.ps1').read_text()
            runner=runner.replace(old.name+'/prepared_observer.lua',out.name+'/'+target.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace(f'audit_bounded_{fighter}_throw_window_footprint_runtime',
                                  f'audit_bounded_{fighter}_queued_throw_{phase}_runtime')
            (out/f'run_{fighter}_{phase}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
        phases=dict(opening=[114,144],landing=[145,176]),queueFix=True,bothVideoBuffers=True)))

if __name__=='__main__':main()
