"""Successor compares preterminal prefix on both sides of shorter run."""
import verify_native_source_sync as sync
if __name__=='__main__':
    path=sync.ROOT/'audit_current_sonya_winner_visual_screen_preparation/qualify.py'
    code=path.read_text()
    old="assert records==[r for r in old.get(tag,[]) if int(r['frame'])<5400]"
    assert code.count(old)==1
    code=code.replace(old,"assert [r for r in records if int(r['frame'])<5400]==[r for r in old.get(tag,[]) if int(r['frame'])<5400]")
    exec(compile(code,str(path)+' [preterminal prefix successor]','exec'),{'__name__':'__main__','__file__':str(path)})
