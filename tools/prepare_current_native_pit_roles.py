"""Physical reciprocal Pit cases; same current Lua and resource limits."""
import verify_native_source_sync as sync

def main():
    sync.verify()
    base=sync.ROOT/'audit_current_native_pit_longkick_preparation'
    out=sync.ROOT/'audit_current_native_pit_roles_preparation';assert not out.exists()
    out.mkdir()
    for winner,side in [('sonya',1),('kano',2),('sonya',2)]:
        runner=(base/'run.ps1').read_text()
        runner=runner.replace("MK2KS_STAGE_WINNER='kano'",f"MK2KS_STAGE_WINNER='{winner}'")
        runner=runner.replace("MK2KS_STAGE_SIDE='1'",f"MK2KS_STAGE_SIDE='{side}'")
        runner=runner.replace('audit_current_native_pit_longkick_kano_p1_runtime',f'audit_current_native_pit_longkick_{winner}_p{side}_runtime')
        (out/f'run_{winner}_p{side}.ps1').write_text(runner)
    print('Prepared three reciprocal physical Pit roles; shared pinned Lua, no copies of build/ROM/media')

if __name__=='__main__':main()
