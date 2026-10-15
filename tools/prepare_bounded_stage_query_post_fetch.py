"""Observe VRAM immediately at next native instruction after sprite DMA store."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_stage_query_commands_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    lua=lua.replace('local stage_pending={}','local stage_pending={}\nlocal stage_after_fetch=0',1)
    lua=lua.replace('changed=%d candidate=%d pc=%08X source=','changed=%d candidate=%d after_fetch_pc=%08X pc=%08X source=',1)
    lua=lua.replace('r.candidate and 1 or 0,r.pc,r.source','r.candidate and 1 or 0,stage_after_fetch,r.pc,r.source',1)
    lua+=r'''
local stage_post_fetch=p:install_read_tap(0xff804640,0xff80464f,'next native instruction after draw command',function(at)
 if at~=0xff804640 or regs.PC.value~=0xff804650 then return end
 stage_after_fetch=regs.PC.value;complete_stage_pending();stage_after_fetch=0
end)
emu.register_stop(function()assert(stage_post_fetch)end)
'''
    out=root/'audit_bounded_stage_query_post_fetch_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stage_query_commands_runtime',f'audit_bounded_{fighter}_stage_query_post_fetch_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
