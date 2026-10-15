"""Separate actual camera-cropped pixels from visible RGB mismatches."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_queued_throw_footprint_preparation'
    out=root/'audit_bounded_viewport_throw_footprint_preparation';assert not out.exists()
    out.mkdir()
    for phase in ('opening','landing'):
        lua=(old/f'{phase}_observer.lua').read_text()
        needle='{points=0,source_fail=0,display_fail=0,slots={0,0}}'
        assert lua.count(needle)==2
        lua=lua.replace(needle,'{points=0,source_fail=0,display_fail=0,offscreen=0,slots={0,0}}')
        needle='if actual~=final then footprint_stats.display_fail=footprint_stats.display_fail+1 end'
        assert lua.count(needle)==1
        lua=lua.replace(needle,r'''
   if actual==-1 then footprint_stats.offscreen=footprint_stats.offscreen+1
   elseif actual~=final then
    footprint_stats.display_fail=footprint_stats.display_fail+1
    if footprint_stats.display_fail<=4 then
     log('FOOTPRINT_VISIBLE_GAP',string.format('source_frame=%d slot=%d x=%d y=%d display_x=%d display_y=%d expected=%06X actual=%06X',q.frame,q.slot,q.x,q.y,xx,yy,final,actual))
    end
   end''')
        needle="source_fail=%d display_fail=%d raw_media=none',footprint_stats.source_frame-ready"
        assert lua.count(needle)==1
        lua=lua.replace(needle,"source_fail=%d display_fail=%d offscreen=%d column=%d row=%d raw_media=none',footprint_stats.source_frame-ready")
        needle='footprint_stats.source_fail,footprint_stats.display_fail))'
        assert lua.count(needle)==1
        lua=lua.replace(needle,'footprint_stats.source_fail,footprint_stats.display_fail,footprint_stats.offscreen,column,row))')
        target=out/f'{phase}_observer.lua';target.write_text(lua)
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_{phase}.ps1').read_text()
            runner=runner.replace(old.name+'/'+target.name,out.name+'/'+target.name)
            runner=runner.replace(sync.sha(old/target.name),sync.sha(target))
            runner=runner.replace(f'audit_bounded_{fighter}_queued_throw_{phase}_runtime',
                                  f'audit_bounded_{fighter}_viewport_throw_{phase}_runtime')
            (out/f'run_{fighter}_{phase}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
        actualViewportCroppingExplicit=True,noVisibleMismatchWaiver=True)))

if __name__=='__main__':main()
