"""Full opaque detached-head source footprints, observed native actors only."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_body_completion_preparation'
    out=sync.ROOT/'audit_bounded_stock_head_effect_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_stock_head_effect_census_checked/report.json').read_text())
    assert proof['passed']
    text=(old/'prepared_observer.lua').read_text()
    needle='frame-ready>=61 and frame-ready<=174';assert text.count(needle)==2
    text=text.replace(needle,'frame-ready>=59 and frame-ready<=174')
    needle='if a and a.actor==regs.A0.value then';assert text.count(needle)==1
    text=text.replace(needle,"if slot==1 and a and regs.A0.value>=0x01000000 and regs.A0.value<0x01100000 and regs.A0.value~=a.actor and p:read_u16(regs.A0.value+0x1f0)==a.id and regs.A11.value>=0x0f600000 and regs.A11.value<0x10000000 then")
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_body_completion_runtime',
                              f'audit_bounded_{fighter}_stock_head_effect_pixels_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,actionAges=[59,174],
        observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
