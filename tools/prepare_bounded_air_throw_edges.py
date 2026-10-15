"""Walk both humans toward physical edge before original catch controller."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_air_throw_retirement_preparation'
out=sync.ROOT/'audit_bounded_air_throw_edges_preparation'
assert not out.exists()
base=old/'air_throw.lua'
source=base.read_text()
before="local air_cycle,air_mode,air_at,air_settle=1,'approach',nil,nil"
assert source.count(before)==1
source=source.replace(before,"""local edge_direction=assert(os.getenv('MK2KS_AIR_EDGE_DIRECTION'))
assert(edge_direction=='Left'or edge_direction=='Right')
local edge_at=nil
local air_cycle,air_mode,air_at,air_settle=1,'edge',nil,nil""")
before="   if air_mode=='approach'then"
assert source.count(before)==1
source=source.replace(before,"""   if air_mode=='edge'then
    edge_at=edge_at or frame
    if frame-edge_at<100 then input(1,edge_direction);input(2,edge_direction)
    else
     air_mode='approach';air_settle=nil
     air_log('EDGE_WALK_DONE','direction='..edge_direction..' fields=100 aX='..a.x..' bX='..b.x)
    end
   end
"""+before)
out.mkdir()
target=out/'air_throw.lua'
target.write_text(source)
for side in (1,2):
    for direction in ('Left','Right'):
        runner=(old/f'run_kano_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/air_throw.lua',out.name+'/air_throw.lua').replace(sync.sha(base),sync.sha(target))
        runner=runner.replace("SPECIAL_VICTIM='jax'", "SPECIAL_VICTIM='sonya'")
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_MOVE='knife'",f"$env:MK2KS_AIR_EDGE_DIRECTION='{direction}'\n$env:MK2KS_HUMAN_SPECIAL_MOVE='knife'")
        runner=runner.replace(f'audit_bounded_air_throw_retirement_kano_p{side}_runtime',f'audit_bounded_air_throw_edge_{direction.lower()}_p{side}_runtime')
        (out/f'run_{direction.lower()}_p{side}.ps1').write_text(runner)
print('Prepared4 physical edge walks; no images or forced positions')
