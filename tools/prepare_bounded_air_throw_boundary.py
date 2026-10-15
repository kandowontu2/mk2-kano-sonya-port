"""Longer physical walks and passive native boundary entry ledger."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_air_throw_edges_preparation'
out=sync.ROOT/'audit_bounded_air_throw_boundary_preparation'
assert not out.exists()
base=old/'air_throw.lua'
source=base.read_text()
assert source.count('frame-edge_at<100')==1 and source.count('fields=100')==1
source=source.replace('frame-edge_at<100','frame-edge_at<240').replace('fields=100','fields=240')
marker='local recovered_actors={}'
assert source.count(marker)==1
source=source.replace(marker,marker+'''
taps[#taps+1]=p:install_read_tap(0xff8054e0,0xff8054ef,'actual native boundary entry',function(at)
 if not ready or at~=0xff8054e0 or regs.PC.value~=0xff8054f0 then return end
 for slot=1,2 do
  local a=sample(slot)
  if a and regs.A2.value==a.actor then
   log('BOUNDARY',string.format('slot=%d actor=%08X owner=%08X id=%d x=%d xraw=%08X lower=%d upper=%d camera=%d action=%d cycle=%d',
    slot,a.actor,a.owner,a.id,a.x,a.xraw,regs.A0.value,regs.A1.value,p:read_i16(0x0105d350),a.action,air_cycle))
  end
 end
end)
''')
out.mkdir()
target=out/'air_throw.lua'
target.write_text(source)
for side in (1,2):
    for direction in ('left','right'):
        runner=(old/f'run_{direction}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/air_throw.lua',out.name+'/air_throw.lua').replace(sync.sha(base),sync.sha(target))
        runner=runner.replace('audit_bounded_air_throw_edge_','audit_bounded_air_throw_boundary_')
        (out/f'run_{direction}_p{side}.ps1').write_text(runner)
print('Prepared240field physical walks; read-only native clamp ledger; no media')
