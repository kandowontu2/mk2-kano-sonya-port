"""Fresh correction: main40 lookup belongs to finisher window, not later CPU animations."""
from pathlib import Path
prior=Path(__file__).with_name('verify_native_subzero_shatter_matrix_v4955.py')
text=prior.read_text()
before="main=pick('MAIN_LOOKUP')"
after="""main_rows=[r for r in traces if r['tag']==prefix+'MAIN_LOOKUP']
 need(len(main_rows)==1,'Exactly one native finisher main40 lookup in victim lifetime')
 main=main_rows[0]"""
assert text.count(before)==1
text=text.replace(before,after,1).replace('audit_v4956_native_subzero_shatter_matrix_checked','audit_v4958_native_subzero_shatter_matrix_checked',1)
before='for p in(Path(__file__),Path(native.__file__),Path(parser.__file__))'
assert text.count(before)==1
text=text.replace(before,'for p in(prior,Path(__file__),Path(native.__file__),Path(parser.__file__))',1)
exec(compile(text,str(Path(__file__).resolve())+'::finisher_lifetime_lookup','exec'),globals())
