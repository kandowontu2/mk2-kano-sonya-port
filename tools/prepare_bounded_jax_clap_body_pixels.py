"""Current Jax clap body source footprints, complete native action window."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_p2_stock_head_full_vram_preparation'
    out=sync.ROOT/'audit_bounded_jax_clap_body_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_jax_clap_finisher_checked/report.json').read_text())
    assert proof['passed'] and {r['nativeWrapFrame']-r['nativeActionFrame'] for r in proof['results'].values()}=={188}
    text=(old/'prepared_observer.lua').read_text()
    needle='frame-ready>=1 and frame-ready<=174';assert text.count(needle)==2
    text=text.replace(needle,'frame-ready>=1 and frame-ready<=188')
    replacements=[
        ('local count,low,high=0,nil,nil','local count,low,high,eligible=0,nil,nil,0'),
        ('idle_points[#idle_points+1]={frame=frame,slot=coverage_context.slot','eligible=eligible+1;idle_points[#idle_points+1]={frame=frame,slot=coverage_context.slot'),
        ('return count,low or -999,high or -999,bit-mapped,point_x,point_pixel','return count,low or -999,high or -999,bit-mapped,point_x,point_pixel,eligible'),
        ('local count,top,bottom,bits,px,pixel=opaque_bounds(src,w,h,c)','local count,top,bottom,bits,px,pixel,eligible=opaque_bounds(src,w,h,c)'),
        ('config=%04X skip=%04X\',','config=%04X skip=%04X eligible=%d native_clipped=%d\','),
        ('reg(12),reg(13),reg(15),reg(0)))','reg(12),reg(13),reg(15),reg(0),eligible,count-eligible))'),
    ]
    for before,after in replacements:
        assert text.count(before)==1,before;text=text.replace(before,after)
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='2'","$env:MK2KS_CAMPAIGN_SIDE='1'")
        runner=runner.replace("$env:MK2KS_STOCK_KILLER='baraka'","$env:MK2KS_STOCK_KILLER='jax'")
        runner=runner.replace("$env:MK2KS_STOCK_COMMAND='bbbb_hp'","$env:MK2KS_STOCK_COMMAND='fff_lp_release'")
        runner=runner.replace(f'audit_bounded_p2_{fighter}_stock_head_full_vram_runtime',f'audit_bounded_{fighter}_jax_clap_body_pixels_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,sourceColumns=512,actionAges=[1,188],observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
