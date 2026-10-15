"""Separate raw opaque artwork from actual native clip-eligible pixels."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_p2_stock_effect_pixels_preparation'
    out=sync.ROOT/'audit_bounded_p2_stock_effect_clip_census_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    replacements=[
        ('local count,low,high=0,nil,nil','local count,low,high,eligible=0,nil,nil,0'),
        ('idle_points[#idle_points+1]={frame=frame,slot=coverage_context.slot','eligible=eligible+1;idle_points[#idle_points+1]={frame=frame,slot=coverage_context.slot'),
        ('return count,low or -999,high or -999,bit-mapped,point_x,point_pixel','return count,low or -999,high or -999,bit-mapped,point_x,point_pixel,eligible'),
        ('local count,top,bottom,bits,px,pixel=opaque_bounds(src,w,h,c)','local count,top,bottom,bits,px,pixel,eligible=opaque_bounds(src,w,h,c)'),
        ('config=%04X skip=%04X\',','config=%04X skip=%04X eligible=%d native_clipped=%d\','),
        ('reg(12),reg(13),reg(15),reg(0)))','reg(12),reg(13),reg(15),reg(0),eligible,count-eligible)))'),
    ]
    for before,after in replacements:
        assert text.count(before)==1,before;text=text.replace(before,after)
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_p2_{fighter}_stock_effect_pixels_runtime',f'audit_bounded_p2_{fighter}_stock_effect_clip_census_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
