"""Correct passive winner observation for original Shang roster dispatch."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_morphed_babalities_preparation'
out=sync.ROOT/'audit_bounded_morphed_babality_win_rows_preparation';assert not out.exists()
source=(old/'babalities.lua').read_text()
before=' if not own or at~=0xfffef800+own.id*32 or own.roster~=6 or p:read_u16(slots[side].hp)==0 or p:read_u16(slots[3-side].hp)~=0 then return end'
assert source.count(before)==1
source=source.replace(before," if not own or cpu.PC.value~=0xff8296b0 or(at~=0xfffef800+own.id*32 and at~=0xfffef800+own.roster*32)or own.roster~=6 or own.owner~=own.actor or p:read_u16(slots[side].hp)==0 or p:read_u16(slots[3-side].hp)~=0 then return end")
before=" wins=wins+1;log('WIN','wins='..wins..' total_damage='..damage..' pc='..string.format('%08X',cpu.PC.value))"
assert source.count(before)==1
source=source.replace(before," wins=wins+1;log('WIN',string.format('wins=%d total_damage=%d pc=%08X entry=%08X actor_id=%d roster=%d actor=%08X main=%08X owner=%08X hp=%d victim_hp=%d',wins,damage,cpu.PC.value,at,own.id,own.roster,own.actor,own.main,own.owner,own.hp,p:read_u16(slots[3-side].hp)))")
out.mkdir();lua=out/'babalities.lua';lua.write_text(source)
for side in(1,2):
    runner=(old/f'run_sonya_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/babalities.lua',out.name+'/babalities.lua').replace(sync.sha(old/'babalities.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_morphed_babality_sonya_p{side}_runtime',f'audit_bounded_morphed_babality_win_rows_sonya_p{side}_runtime')
    (out/f'run_sonya_p{side}.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_bounded_morphed_babalities.py').read_text()
before="            folder=sync.ROOT/f'audit_bounded_morphed_babality_{fighter}_p{side}_runtime'"
assert checker.count(before)==1
checker=checker.replace(before,"            if fighter=='sonya':\n                folder=sync.ROOT/f'audit_bounded_morphed_babality_win_rows_sonya_p{side}_runtime'\n                lua=sync.ROOT/'audit_bounded_morphed_babality_win_rows_preparation/babalities.lua'\n            else:\n                folder=sync.ROOT/f'audit_bounded_morphed_babality_kano_p{side}_runtime'\n                lua=sync.ROOT/'audit_bounded_morphed_babalities_preparation/babalities.lua'")
before="    return dict(outcome='native_low_punch_eligibility_rejection',lowPunchCounter=lp[side-1],result=r)"
assert checker.count(before)==1
checker=checker.replace(before,"    wins=tagged('WIN');assert [x['wins'] for x in wins]==['1','2']\n    for win in wins:\n        assert win['pc']=='FF8296B0' and win['roster']=='6' and win['entry']=='FFFEF8C0'\n        assert win['actor']==win['owner']==form['actor'] and win['main']==form['main']\n        assert int(win['hp'])>0 and win['victim_hp']=='0'\n    assert int(wins[1]['frame'])<int(restore['frame']) and wins[1]['actor_id']=='18'\n"+before)
(out/'qualify.py').write_text(checker)
print('Prepared actual original Shang winner-table row observer; game inputs unchanged')
