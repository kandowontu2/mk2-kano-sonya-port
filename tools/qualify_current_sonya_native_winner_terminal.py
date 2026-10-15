"""Successor excludes deadline-dependent terminal controller digest."""
from pathlib import Path
if __name__=='__main__':
    path=Path(__file__).with_name('qualify_current_sonya_native_winner.py')
    code=path.read_text()
    old="if tag in ('WINNER_POSE','WINNER_TABLE','RESULT','HOST_BOUND'):continue"
    assert code.count(old)==1
    code=code.replace(old,"if tag in ('WINNER_POSE','WINNER_TABLE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue")
    exec(compile(code,str(path)+' [terminal digest successor]','exec'),{'__name__':'__main__','__file__':str(path)})
