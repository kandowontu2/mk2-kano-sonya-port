"""Same physical catches against native ninja/Raiden/Shang animation families."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_air_throw_victims_preparation'
out=sync.ROOT/'audit_bounded_air_throw_stock_families_preparation'
assert not out.exists()
out.mkdir()
for victim in ('sub_zero','raiden','shang_tsung'):
    for side in (1,2):
        runner=(old/f'run_kitana_p{side}.ps1').read_text()
        assert runner.count("SPECIAL_VICTIM='kitana'")==1
        runner=runner.replace("SPECIAL_VICTIM='kitana'",f"SPECIAL_VICTIM='{victim}'")
        runner=runner.replace(f'audit_bounded_air_throw_victim_kitana_p{side}_runtime',f'audit_bounded_air_throw_stock_family_{victim}_p{side}_runtime')
        (out/f'run_{victim}_p{side}.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_bounded_air_throw_victims.py').read_text()
checker=checker.replace('audit_bounded_air_throw_victims_checked','audit_bounded_air_throw_stock_families_checked')
checker=checker.replace("(('sonya', 18), ('kano', 17), ('kitana', 4))","(('sub_zero', 8), ('raiden', 7), ('shang_tsung', 6))")
checker=checker.replace('audit_bounded_air_throw_victim_{victim}', 'audit_bounded_air_throw_stock_family_{victim}')
checker=checker.replace('Sonya/Kano mirror/Kitana victims','SubZero/Raiden/Shang victims')
(out/'qualify.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))\n"+checker)
print('Prepared6 unchanged-controller family cases; no media')
