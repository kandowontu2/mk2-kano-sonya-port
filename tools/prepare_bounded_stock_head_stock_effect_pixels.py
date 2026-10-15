"""Exact observed stock-effect source set, no head/body substitution."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_effect_pixels_preparation'
    out=sync.ROOT/'audit_bounded_stock_head_stock_effect_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_stock_head_remaining_effects_classified/report.json').read_text())
    assert proof['passed']
    sources=proof['results']['sonya']['stockEffectSources']
    assert sources==proof['results']['kano']['stockEffectSources'] and len(sources)==36
    text=(old/'prepared_observer.lua').read_text()
    needle='local idle_owned={}';assert text.count(needle)==1
    table='local stock_effect_sources={'+','.join('[0x'+s+']=true' for s in sources)+'}\n'
    text=text.replace(needle,table+needle)
    needle='p:read_u16(regs.A0.value+0x1f0)==a.id and regs.A11.value>=0x0f600000 and regs.A11.value<0x10000000'
    assert text.count(needle)==1;text=text.replace(needle,'p:read_u16(regs.A0.value+0x1f0)==0 and stock_effect_sources[regs.A11.value]')
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_effect_pixels_runtime',
                              f'audit_bounded_{fighter}_stock_head_stock_effect_pixels_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
