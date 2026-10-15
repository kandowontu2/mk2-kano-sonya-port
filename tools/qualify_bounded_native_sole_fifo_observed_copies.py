"""Bind all captured copies; explicitly preserve two unobserved queue entries."""
import inspect
import qualify_bounded_native_sole_fifo_binding as old
scope=dict(vars(old),__file__=__file__)
source=inspect.getsource(old.gate)
before='assert queues and len(queues)==len(draws)'
assert source.count(before)==1
source=source.replace(before,'assert len(queues)==30 and len(draws)==28',1)
before='assert sorted(qkey(r) for r in queues)==sorted(dkey(r) for r in draws)'
assert source.count(before)==1
source=source.replace(before,"""assert {dkey(r) for r in draws}<={qkey(r) for r in queues}
    unobserved=[r for r in queues if qkey(r) not in {dkey(d) for d in draws}]
    assert [(r['frame'],r['slot'],r['source']) for r in unobserved]==[
        ('1826','2','108E07BC'),('1826','2','108E2696')]
    # No clipping/palette/timing explanation is assumed for these two entries.
""",1)
before='physicalActorAndMainUnchanged=True)'
assert source.count(before)==1
source=source.replace(before,'physicalActorAndMainUnchanged=True,unobservedFIFOEntries=unobserved,allFIFOEntriesBound=False)',1)
exec(compile(source,__file__,'exec'),scope)
source=inspect.getsource(old.main)
assert source.count("'fifo_binding_check.json'")==1
source=source.replace("'fifo_binding_check.json'","'fifo_observed_copies_check.json'",1)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
