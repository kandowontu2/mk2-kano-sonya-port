"""Retirement check with actual two-field whole-FIFO pause, preserved predecessor."""
import inspect
import qualify_bounded_kitana_kiss_cleanup_census as previous

def main():
    source=inspect.getsource(previous.gate)
    before="    assert {int(r['age']) for r in own}==set(range(1,396))"
    assert source.count(before)==1
    source=source.replace(before,"    absent={last+1,last+2}\n    assert {int(r['age']) for r in rows}==set(range(1,396))-absent\n    assert {int(r['age']) for r in own}==set(range(1,396))-absent")
    source=source.replace('winnerDrawFields=395','winnerDrawFields=393,wholeFIFOAbsentAges=sorted(absent)')
    main_source=inspect.getsource(previous.main).replace('audit_bounded_kitana_kiss_cleanup_census_checked','audit_bounded_kitana_kiss_cleanup_observed_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::observed_fifo_pause','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
