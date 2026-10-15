"""Keep the failed helper-boundary audit and include its whole anchor tail.

The native XY-copy helper continues through the actual composite cache
anchor correction, not just the position/facing prefix. Compare the whole
routine to its real RETS; preserve the original executed audit unchanged.
"""
import inspect
import json
from pathlib import Path
import audit_native_kano_laser_victim_position as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_victim_position_complete'


def main():
    prior.need(not OUT.exists() and not prior.OUT.exists(),'Fresh complete successor and preserved first failure receipt')
    old=ROOT/'mk3/mk3-maincpu.bin';new=ROOT/'mk2/mk2-maincpu.bin'
    try:prior.inspect_mapping(old.read_bytes(),new.read_bytes(),old,new)
    except ValueError as error:
        prior.need(str(error)=='Whole helper terminal boundary','Exact original truncated-boundary failure independently reproduced')
        prior.OUT.mkdir()
        (prior.OUT/'failure.json').write_text(json.dumps(dict(error=str(error),
            sourceSHA256=prior.sha(Path(prior.__file__)),auditOnly=True,gameSourceChanged=False,
            explanation='The full XY-copy routine includes native cache-anchor correction through FF83D2E0 RETS.'),indent=2)+'\n')
    else:raise ValueError('Original failing audit no longer fails')
    code=inspect.getsource(prior.inspect_mapping)
    replacements=[('0xff966080,0xff83ce60,0xff83d140','0xff966230,0xff83ce60,0xff83d2f0'),
        ('copy full fixed-point XY and match facing','copy full fixed-point XY, match facing and correct actual composite cache anchor')]
    for first,last in replacements:
        prior.need(code.count(first)==1,'Exact full helper terminal-boundary repair');code=code.replace(first,last)
    main_code=inspect.getsource(prior.main)
    old_text='paths=[Path(__file__),old,new'
    prior.need(main_code.count(old_text)==1,'Complete failed-audit/source provenance')
    main_code=main_code.replace(old_text,"paths=[Path(__file__),Path(prior.__file__),prior.OUT/'failure.json',old,new")
    scope=dict(vars(prior),OUT=OUT,prior=prior,__file__=__file__)
    exec(compile(code,__file__+'::whole_anchor_mapping','exec'),scope)
    exec(compile(main_code,__file__+'::complete_audit','exec'),scope)
    scope['main']()


if __name__=='__main__':main()
