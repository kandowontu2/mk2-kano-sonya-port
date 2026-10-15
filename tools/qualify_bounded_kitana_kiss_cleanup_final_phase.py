"""Final burst descriptor occupies actual last three victim FIFO fields."""
import inspect
import qualify_bounded_kitana_kiss_cleanup_census as previous

def main():
    source=inspect.getsource(previous.gate)
    before="    assert {int(r['age']) for r in own}==set(range(1,396))"
    assert source.count(before)==1
    source=source.replace(before,"    absent={last+1,last+2}\n    assert not any(int(r['age']) in absent for r in physical)\n    assert {int(r['age']) for r in own}==set(range(1,396))-absent")
    source=source.replace('winnerDrawFields=395','winnerDrawFields=393,physicalBodyFIFOAbsentAges=sorted(absent)')
    assert source.count('>=last-10')==1
    source=source.replace('>=last-10','>=last-2')
    main_source=inspect.getsource(previous.main).replace('audit_bounded_kitana_kiss_cleanup_census_checked','audit_bounded_kitana_kiss_cleanup_final_phase_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::actual_final_phase','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
