"""Natural CPU variety under ordinary midrange human approach and guard inputs."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_native_cpu_move_observer_preparation'
out=sync.ROOT/'audit_current_native_cpu_guard_probe_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
start=source.index("   elseif strategy=='zoning' then")
end=source.index('   else\n    -- Read-only feedback:',start)
source=source[:start]+'''   elseif strategy=='zoning' then
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    if gap>230 then press(forward)
    elseif gap<145 then press(back);press('Block')
    else
     press('Block')
     if frame%360>=180 and frame%360<300 then press('Down')end
    end
'''+source[end:]
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_cpu_move_observer_runtime','audit_current_native_cpu_guard_probe_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared bounded natural CPU guard probe; no guest/CPU choice writes')
