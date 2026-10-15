"""Sparse native source/target link fields at ring birth and damage."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_ring_hit_owner_preparation'
out=sync.ROOT/'audit_current_sonya_ring_native_actor_links_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
birth=" ring_children[main]={frame=frame,actor=actor}\n"
assert source.count(birth)==1
source=source.replace(birth,birth+" log('RING_NATIVE_LINKS',string.format('phase=birth main=%08X object=%08X creator=%08X target_actor=%08X target_main=%08X p1_actor=%08X p2_actor=%08X p1_main=%08X p2_main=%08X',main,actor,p:read_u32(main+0x230),p:read_u32(main+0x140),p:read_u32(main+0x170),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u32(slots[1].main),p:read_u32(slots[2].main)))\n")
hit="     log('HIT_OWNER',string.format("
assert source.count(hit)==1
source=source.replace(hit,"     if child then\n      local m=cpu.A13.value\n      log('RING_NATIVE_LINKS',string.format('phase=damage slot=%d before=%d after=%d main=%08X object=%08X creator=%08X target_actor=%08X target_main=%08X p1_actor=%08X p2_actor=%08X p1_main=%08X p2_main=%08X',n,before,after,m,cpu.A8.value,p:read_u32(m+0x230),p:read_u32(m+0x140),p:read_u32(m+0x170),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u32(slots[1].main),p:read_u32(slots[2].main)))\n     end\n"+hit)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_ring_hit_owner_runtime','audit_current_sonya_ring_native_actor_links_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native creator/target pointers;unchanged18500field inputs,90sec/320MiB,no media')
