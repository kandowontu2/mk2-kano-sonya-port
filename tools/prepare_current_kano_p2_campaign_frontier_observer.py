"""Retain campaign/owned-state evidence, omit already retained dense hit probes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_sparse_boss_fields_preparation'
out=sync.ROOT/'audit_current_kano_p2_campaign_frontier_observer_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('for n,slot in ipairs(slots)do\n')
end=source.index("taps[#taps+1]=p:install_read_tap(0xfffef800",start)
removed_health=source[start:end]
assert removed_health.count('p:install_write_tap')==1 and "log('HEALTH'" in removed_health
source=source[:start]+source[end:]
start=source.index('    if not boss_action_taps.native_handlers then\n')
end=source.index("    local forward=human.x<other.x and'Right'or'Left'\n",start)
removed_handlers=source[start:end]
assert "log('BOSS_HANDLER'" in removed_handlers and 'for _,address' in removed_handlers
source=source[:start]+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_sparse_boss_fields_runtime','audit_current_kano_p2_campaign_frontier_observer_runtime')
(out/'run.ps1').write_text(runner)
print('Campaign frontier observer: nativewins/IDs/action/special/continues retained;HP/handler dense probes omitted;90sec/320MiB/10MiB/no media')
