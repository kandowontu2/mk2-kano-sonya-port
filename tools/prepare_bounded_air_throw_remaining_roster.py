"""Complete remaining ordinary selectable victim rows, no media."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_air_throw_victims_preparation'
out=sync.ROOT/'audit_bounded_air_throw_remaining_roster_preparation'
assert not out.exists()
out.mkdir()
victims=(('kung_lao',0),('liu_kang',1),('cage',2),('baraka',3),('mileena',5),('reptile',9),('scorpion',10))
for victim,identity in victims:
    for side in (1,2):
        runner=(old/f'run_kitana_p{side}.ps1').read_text()
        runner=runner.replace("SPECIAL_VICTIM='kitana'",f"SPECIAL_VICTIM='{victim}'")
        runner=runner.replace(f'audit_bounded_air_throw_victim_kitana_p{side}_runtime',f'audit_bounded_air_throw_remaining_{victim}_p{side}_runtime')
        (out/f'run_{victim}_p{side}.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_bounded_air_throw_victims.py').read_text()
checker=checker.replace('audit_bounded_air_throw_victims_checked','audit_bounded_air_throw_remaining_roster_checked')
checker=checker.replace("(('sonya', 18), ('kano', 17), ('kitana', 4))",repr(victims))
checker=checker.replace('audit_bounded_air_throw_victim_{victim}','audit_bounded_air_throw_remaining_{victim}')
checker=checker.replace('Twelve current actual Kano catches: Sonya/Kano mirror/Kitana victims','Twenty-eight current actual Kano catches: seven remaining ordinary victims')
checker=checker.replace('contexts=6, catches=12','contexts=14, catches=28')
(out/'qualify.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))\n"+checker)
print('Prepared14 capped physical cases; no images/builds/raw media')
