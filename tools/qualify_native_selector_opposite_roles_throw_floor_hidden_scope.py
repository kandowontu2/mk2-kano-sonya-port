"""Fix only module-scope transport; retain original failed class-scope attempt.

Add effective faults against whole-body eligibility and the real native hide
store. No native game, geometry equation or byte of the build is changed.
"""
from pathlib import Path
import qualify_native_selector_opposite_roles_throw_floor_hidden_body as hidden_parent

ROOT=hidden_parent.ROOT
SCOPE_FAILURE=hidden_parent.OUT/'failure.json'
current=hidden_parent.current
source=hidden_parent.source
source=current.replace(source,
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_body_checked'",
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_scope_checked'")
source=current.replace(source,
    "body_proxy=type('OriginalBodyScope',(),dict(vars(body),check_body=staticmethod(native_check_body)))()",
    "body_proxy=__import__('types').SimpleNamespace(**dict(vars(body),check_body=native_check_body))")
source=current.replace(source,
    'for path in (Path(__file__),Path(parent.__file__),SOURCE,IMPORT_FAILURE,BODY_FAILURE,PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),',
    'for path in (Path(__file__),Path(hidden_parent.__file__),SCOPE_FAILURE,Path(parent.__file__),SOURCE,IMPORT_FAILURE,BODY_FAILURE,PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),')
extra="""    hidden_faults=[]
    frames=set(positive['state']['expectedNativeDrawingFrames'])
    first=rows['MK2_HPHASE_CANDIDATE'][0]
    key=(first['frame'],first['slot'])
    changed=dict(b,rows=copy.copy(rows))
    changed['rows']['MK2_HPHASE_CANDIDATE']=[r for r in rows['MK2_HPHASE_CANDIDATE'] if (r['frame'],r['slot'])!=key]
    try:check(changed,state['guest'],state['payload'],state['gfx32'])
    except (ValueError,AssertionError) as error:hidden_faults.append(dict(fault='missing_entire_eligible_native_body',rejectedBy=str(error)))
    else:raise ValueError('Missing eligible body accepted')
    changed=dict(b,rows=copy.copy(rows))
    changed['rows']['MK2_HPHASE_CANDIDATE']=list(rows['MK2_HPHASE_CANDIDATE'])+[dict(first,frame='3029',slot='1',body='0026')]
    try:hidden_gate(changed,state['guest'],frames)
    except (ValueError,AssertionError) as error:hidden_faults.append(dict(fault='body_drawn_during_native_suppression',rejectedBy=str(error)))
    else:raise ValueError('Body with source skip flag accepted')
    bad_guest=bytearray(state['guest']);bad_guest[(0xff804190-0xff800000)//8]^=1
    try:hidden_gate(b,bytes(bad_guest),frames)
    except (ValueError,AssertionError) as error:hidden_faults.append(dict(fault='original_native_body_skip_opcode',rejectedBy=str(error)))
    else:raise ValueError('Wrong original body skip opcode accepted')
    hide_line=next(s for s in text.splitlines() if s.startswith('MK2_CPU_PAIR_FLAG ') and 'frame=3028 ' in s and 'kind=body ' in s and 'slot=1 ' in s)
    changed_line,count=re.subn(r'\\bafter=\\S+','after=0016',hide_line,count=1)
    need(count==1 and changed_line!=hide_line,'Effective real hide-store corruption')
    try:hidden_gate(dict(b,cpuLog=text.replace(hide_line,changed_line,1)),state['guest'],frames)
    except (ValueError,AssertionError) as error:hidden_faults.append(dict(fault='actual_native_hide_store_value',rejectedBy=str(error)))
    else:raise ValueError('Wrong actual native hide result accepted')
    need(len(hidden_faults)==4,'All four source-bound body-suppression faults reject')
"""
source=current.replace(source,
    '    need(len(faults)==11 and len(extra)==4 and len(floor_faults)==8 and',
    extra+'    need(len(faults)==11 and len(extra)==4 and len(floor_faults)==8 and')
source=current.replace(source,
    'originalThrowFloorFaultsRejected=floor_faults,inputHashes=pins,requirements=parent[\'requirements\'],',
    "originalThrowFloorFaultsRejected=floor_faults,nativeBodySuppressionFaultsRejected=hidden_faults,inputHashes=pins,requirements=parent['requirements'],")
source=current.replace(source,
    "print('PASS whole opposite-role body/ROM/shadow plus original throw-floor source with23 faults',flush=True)",
    "print('PASS whole opposite-role body/ROM/shadow plus original throw-floor/native body-suppression source with27 faults',flush=True)")
scope=dict(hidden_parent.scope,__file__=__file__,SCOPE_FAILURE=SCOPE_FAILURE,hidden_parent=hidden_parent)
exec(compile(source,__file__+'::original_module_scope_and_native_eligibility_faults','exec'),scope)
OUT=scope['OUT']
execute=scope['execute']
safe_execute=scope['safe_execute']
