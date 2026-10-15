"""Whole same-capture control suite with explicit complete post-field rejection.

The earlier prefix repair's missing-index KeyError is not a semantic fault
proof. Preserve that report; require every actual post-reset field before
calling the unchanged response gate, and rerun every genuine fault without
accepting parser/index exceptions. No gameplay replay.
"""
import inspect
import traceback
import verify_native_kano_laser_post_reset_controls_bound as prior

ROOT,need,once,base=prior.ROOT,prior.need,prior.once,prior.base
OUT=ROOT/'audit_native_kano_laser_post_reset_controls_complete_fields_checked'


def binding():
    source=inspect.getsource(prior.run)
    source=once(source,'    def complete(changed):\n',
        '''    def complete(changed):
        resume=prior.rows(changed,'RESULT')[0]['ready']
        end=prior.ground.prior.rows(changed,'END')[0]['frame']
        observed=[dict(re.findall(r'(\\w+)=([^\\s]+)',s))for s in changed.splitlines()if s.startswith('MK2_HPHASE_POST_FIELD ')]
        selected=[r for r in observed if int(resume)<=int(r['frame'])<int(end)]
        keys={(int(r['frame']),int(r['slot']))for r in selected}
        need(len(keys)==len(selected)and keys=={(f,s)for f in range(int(resume),int(end))for s in (1,2)},
             'Every actual both-slot post-reset draw field, including all real control response fields')
''')
    source=once(source,'except (ValueError,AssertionError,KeyError)as error:',
                'except (ValueError,AssertionError)as error:')
    source=once(source,"            need(not isinstance(error,KeyError)or label=='missing_actual_control_postfield','No parser exception counted as semantic success')\n",'')
    source=once(source,'        originalPrefixFailurePreserved=True,',
                '        originalPrefixFailurePreserved=True,')if '        originalPrefixFailurePreserved=True,'in source else source
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_control_fault_suite_explicit_complete_fields','exec'),scope)
    return scope['run']


def execute(actual):
    try:binding()(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve strict same-capture successor failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(prior.json.dumps(dict(passed=False,error=repr(error))),flush=True)
