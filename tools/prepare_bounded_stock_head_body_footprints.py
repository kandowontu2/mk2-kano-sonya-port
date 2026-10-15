"""Earned finisher driver plus bounded physical-body footprint observer."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_stock_head_finisher_preparation'
    display=root/'audit_bounded_viewport_throw_footprint_preparation/opening_observer.lua'
    out=root/'audit_bounded_stock_head_body_footprint_preparation';assert not out.exists()
    driver=(old/'prepared_observer.lua').read_text()
    needle='action_start=frame';assert driver.count(needle)==1
    driver=driver.replace(needle,'action_start=frame;ready=frame')
    needle='y=p:read_i16(a+0xb0),';assert driver.count(needle)==1
    driver=driver.replace(needle,needle+'floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0),')
    driver='local ready=nil\n'+driver+'\nlocal regs=cpu\n'
    model=display.read_text();marker='local actual_dma={}'
    assert model.count(marker)==1;model=model[model.index(marker):]
    needle='frame-ready>=114 and frame-ready<=144';assert model.count(needle)==2
    model=model.replace(needle,'frame-ready>=0 and frame-ready<=30')
    needle='local a=sample(n);local cache=p:read_u32(a.actor+0x1a0)';assert model.count(needle)==1
    model=model.replace(needle,'local a=sample(n);if not a then return end;local cache=p:read_u32(a.actor+0x1a0)')
    lua=driver+model
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_finisher_runtime',
                              f'audit_bounded_{fighter}_stock_head_body_footprint_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,captureActionAges=[0,30],
        physicalFighterBodiesOnly=True,allGoreEffectActorsAccepted=False,
        driverSha256=sync.sha(old/'prepared_observer.lua'),modelSha256=sync.sha(display),observerSha256=sync.sha(target))))

if __name__=='__main__':main()
