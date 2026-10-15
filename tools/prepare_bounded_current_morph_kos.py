"""Preserve original genuine KO controls; remove only dump/image sinks."""
import verify_native_source_sync as sync

sync.verify()
out = sync.ROOT/'audit_bounded_current_morph_kos_preparation'
assert not out.exists()
source = (sync.ROOT/'mk2ks_morph_adversity_v3226.lua').read_text()
start = source.index("local output=assert(os.getenv('MK2KS_MORPH_CAPTURE_OUT'))")
end = source.index('local function pulse(', start)
source = source[:start]+source[end:]
lines = source.splitlines()
assert sum(':snapshot(' in line for line in lines) == 2
source = '\n'.join(line for line in lines if ':snapshot(' not in line)+'\n'
assert all(t not in source for t in ('io.open', ':snapshot(', ':pixels(', 'read_range', 'hex='))
out.mkdir()
lua = out/'morph_ko.lua'
lua.write_text(source)
old = sync.ROOT/'audit_bounded_current_morph_hits_preparation'
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/morph_hits.lua', out.name+'/morph_ko.lua')
        runner = runner.replace(sync.sha(old/'morph_hits.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_current_morph_hit_', 'audit_bounded_current_morph_ko_')
        runner = runner.replace("MK2KS_MORPH_ADVERSITY_PHASE='formed'", "MK2KS_MORPH_ADVERSITY_PHASE='ko'")
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared four genuine-input KO cases, no raw media; existing resource caps retained')
