"""Observer large-ROM source fix for unchanged native sweep policy."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_sweep_presentation_preparation'
    out=root/'audit_bounded_large_rom_sweep_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    needle='elseif mapped>=0x02000000 then mapped=mapped-0x02000000 end'
    assert lua.count(needle)==1
    lua=lua.replace(needle,'end -- MK2 large-ROM mode keeps native graphics offsets')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_sweep_presentation_runtime',
                              f'audit_bounded_{fighter}_large_rom_sweep_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
