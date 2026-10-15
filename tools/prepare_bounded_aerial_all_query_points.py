"""Include body-foot queries in actual later-layer/VRAM/presentation tracing."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_aerial_motion_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker=' idle_points[#idle_points+1]={frame=frame,slot=own.slot,id=own.id,x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|pixel}'
    assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
 local q={frame=frame,slot=own.slot,id=own.id,kind='body',x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|pixel}
 idle_points[#idle_points+1]=q
 local query_key=string.format('%d_%d_%d',frame,q.x,q.y)
 shadow_queries[query_key]=shadow_queries[query_key]or{};shadow_queries[query_key][#shadow_queries[query_key]+1]=q
''',1)
    lua=lua.replace("if q.kind=='shadow' then","if q.kind=='shadow' or q.kind=='body' then",1)
    lua=lua.replace("if q.kind=='shadow' and q.frame==frame then","if (q.kind=='shadow' or q.kind=='body') and q.frame==frame then")
    for tag in ('IDLE_VRAM_POINT','IDLE_ALL_DRAW_FINAL','IDLE_SHADOW_COVER'):
        marker="log('"+tag+"',string.format('source_frame=%d"
        assert lua.count(marker)==1
        lua=lua.replace(marker,"log('"+tag+"',string.format('kind=%s source_frame=%d",1)
    lua=lua.replace('    q.frame,q.slot,q.id,q.x,q.y,index,q.source_vram',"    q.kind,q.frame,q.slot,q.id,q.x,q.y,index,q.source_vram",1)
    lua=lua.replace('    q.frame,q.slot,q.id,q.x,q.y,index,q.all_source',"    q.kind,q.frame,q.slot,q.id,q.x,q.y,index,q.all_source",1)
    lua=lua.replace('    q.frame,q.slot,q.id,q.x,q.y,q.cover_index',"    q.kind,q.frame,q.slot,q.id,q.x,q.y,q.cover_index",1)
    out=root/'audit_bounded_aerial_all_query_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_aerial_motion_points_runtime',f'audit_bounded_{fighter}_aerial_all_query_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
