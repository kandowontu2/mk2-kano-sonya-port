"""Original formed-state physical uppercut; strip guest dump and PNG sinks."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_current_morph_hits_preparation'
assert not out.exists()
original=sync.ROOT/'mk2ks_morph_adversity_v3215.lua'
source=original.read_text()
start=source.index("local output=assert(os.getenv('MK2KS_MORPH_CAPTURE_OUT'))")
end=source.index('local function pulse(',start)
source=source[:start]+source[end:]
lines=source.splitlines()
assert sum(':snapshot(' in line for line in lines)==2
source='\n'.join(line for line in lines if ':snapshot(' not in line)+'\n'
assert all(t not in source for t in ('io.open',':snapshot(',':pixels(','read_range','hex='))
out.mkdir()
target=out/'morph_hits.lua'
target.write_text(source)
old=sync.ROOT/'audit_bounded_current_human_morphs_preparation'
for fighter in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/morph.lua',out.name+'/morph_hits.lua').replace(sync.sha(old/'morph.lua'),sync.sha(target))
        runner=runner.replace('audit_bounded_current_human_morph_','audit_bounded_current_morph_hit_')
        runner=runner.replace("$env:MK2KS_HUMAN_SHANG_PROFILE='native'","$env:MK2KS_MORPH_ADVERSITY_PHASE='formed'\n$env:MK2KS_MORPH_ADVERSITY_FORM='added'")
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared4 actual formed-state physical attacks; no dumps/images')
