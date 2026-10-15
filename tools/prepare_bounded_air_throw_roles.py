"""Reuse physical air controller with scalar ownership/health/events only."""
import verify_native_source_sync as sync

sync.verify()
out = sync.ROOT / 'audit_bounded_air_throw_roles_preparation'
assert not out.exists()
base = (sync.ROOT / 'mk2ks_special_shadow_v5131.lua').read_text()
prefix = base.split('-- BEGIN v1763 read-only consecutive move-phase observer')[0]
assert prefix.count('bank=p:read_u16(a+0x140)}') == 1
prefix = prefix.replace('bank=p:read_u16(a+0x140)}',
    'bank=p:read_u16(a+0x140),xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),callback=p:read_u32(m+0x290)}')
prefix = prefix.replace("'body','trail','bank'})do", "'body','trail','bank','xraw','yraw','callback'})do")
original = (sync.ROOT / 'mk2ks_air_throw_roles_v6039.lua').read_text()
controller = original.split("source=source..'\\n'..[=[", 1)[1].split(']=]', 1)[0]
source = (prefix + controller).replace('MK2_HSPECIAL_', 'MK2_BASIC_')
source += '''
emu.register_frame_done(function()
 if rawget(_G,'MK2_SPECIAL_EXIT_PENDING')then manager.machine:exit()end
end)
'''
assert all(token not in source for token in (':snapshot(', ':pixels(', 'read_range', 'hex=', 'dofile(', 'io.open'))
out.mkdir()
target = out / 'air_throw.lua'
target.write_text(source)
old = sync.ROOT / 'audit_bounded_current_special_cycles_preparation'
runner = (old / 'run_knife_p1.ps1').read_text()
runner = runner.replace(old.name + '/cycles.lua', out.name + '/air_throw.lua')
runner = runner.replace(sync.sha(old / 'cycles.lua'), sync.sha(target))
for fighter, move, victim in (('kano', 'knife', 'jax'), ('sonya', 'ring', 'jax')):
    for side in (1, 2):
        case = runner.replace('audit_bounded_current_special_cycles_knife_p1_runtime',
                              f'audit_bounded_air_throw_roles_{fighter}_p{side}_runtime')
        case = case.replace("SPECIAL_MOVE='knife'", f"SPECIAL_MOVE='{move}'")
        case = case.replace("SPECIAL_SIDE='1'", f"SPECIAL_SIDE='{side}'")
        case = case.replace("SPECIAL_VICTIM='kitana'", f"SPECIAL_VICTIM='{victim}'")
        (out / f'run_{fighter}_p{side}.ps1').write_text(case)
print('Prepared4 physical roles;4500field/90sec/320MiB/10MiB caps;no media')
