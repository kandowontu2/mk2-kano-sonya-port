"""Reduce only boss diagnostic field formatting; physical controls unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_changed_health_only_preparation'
out=sync.ROOT/'audit_current_kano_p2_sparse_boss_fields_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("    log('BOSS_FIELD',string.format(")
end=source.index('\n',source.index('human.hp,other.hp))',start))
block=source[start:end]
assert block.count("log('BOSS_FIELD'")==1
source=source[:start]+'    if frame%120==0 then\n'+block+'\n    end'+source[end:]
assert source.replace('    if frame%120==0 then\n'+block+'\n    end',block)==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_changed_health_only_runtime','audit_current_kano_p2_sparse_boss_fields_runtime')
(out/'run.ps1').write_text(runner)
print('Sparse passive bossfields120; unchanged controls/nativewins/damage/90sec/320MiB/10MiB/no media')
