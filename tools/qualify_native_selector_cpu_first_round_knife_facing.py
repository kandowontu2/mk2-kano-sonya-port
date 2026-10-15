"""Same captured first-round knife: source-derived align/restore redraw rule.

The two preserved rejections were matcher errors (parent type and redraws
incorrectly conditional on Block). No gameplay writes or native replay.
Keep the entire original knife model; source-bound facing replaces only the
incorrect redraw-count predicate, with independent executed register binding.
"""
import inspect,json,struct,traceback
from pathlib import Path
import qualify_native_selector_cpu_first_round_knife_type as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_first_round_knife_facing_checked'


def facing_redraw(log,guest,by,start,hit,actor,redraw):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    def check(at,words):
        need(struct.unpack_from('<'+'H'*len(words),guest,(at-0xff800000)//8)==tuple(words),
             'Whole authored impact routing/align/restore words')
    # Whole router, including both real IDs and the unchanged stock tail call.
    check(0xfffc2800,[0xb500,0x1f0,0x0b40,0xffee,0xca80,0x28f0,0xfffc,
        0x0b40,0xffed,0xca80,0x28f0,0xfffc,0xc080,0x2010,0xff84,
        0x098f,0x0c00,0xb504,0x00f0,0x098f,0x0800,0x0d5f,0x2010,0xff84,
        0x09af,0x0010,0xb505,0x00f0,0x56a4,0x1f64,0xca80,0x2a40,0xfffc,
        0x0d5f,0xb470,0xff83,0x09af,0x0030,0x0960])
    check(0xff8b0090,[0x0d5f,0x2800,0xfffc])
    check(0xff842010,[0x098f,0x8080,0xb7a0,0x0140,0x5608,0x5700,0x5608,
        0x0d3f,0xfadc,0x09af,0x0101,0x0960])
    check(0xff83b470,[0xb504,0x00f0,0x0bc4,0x0010,0x0000,0xb088,0x00f0,
        0xb700,0x01d0,0xc080,0x8790,0xff83])
    # Original align: copy XY; compare F0 bit4; with target body bit1 set,
    # call FF83B470 (flip F0 bit4 and redraw current 1D0 pose). Router then
    # compares saved/current bit4 and calls the same helper to restore facing.
    # The CALLR operand FADC is signed and resolves to FF83CE60.
    need(0xff8420a0+(0xfadc-65536)*16==0xff83ce60,
         'Stock wrapper calls exact original coordinate/facing helper')
    for lo,hi in((0xff842010,0xff8420d0),(0xff83ce60,0xff83d140),(0xff83b470,0xff83b530)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Entire unchanged stock align/flip helper')
    check(0xff83ce60,[0xbb00,0x80,0x80,0xbb00,0xa0,0xa0,0xb501,0xf0,
        0xb402,0xf0,0xb403,0x160,0x1fc3,0xca10])
    model=prior.prior.model
    groups=[r for r in model.knife.overlap.rows(log,'EVENT')
            if r['frame']==hit and r['kind']=='group'and r['a8']==actor]
    independent=[r for r in prior.prior.rows(log,'MK2_STARTUP_PROJECTILE_EVENT')
                 if int(r['frame'])==hit and r['kind']=='group'and int(r['a8'],16)==actor]
    need(len(groups)==len(independent)==4,'Entire original contact travelling/alignment/restore/impact order')
    for old,new in zip(groups,independent):
        need(all(old[k]==int(new[k],16)for k in
             ('a8','a13','pc','a0','a4','a5','xraw','yraw','vx','body','pose','action')),
             'Original and independent executing group registers and complete body words agree')
    incoming=by[start+1,2]['facing']&16
    victim_facing=by[hit,1]['facing']&16
    need(by[hit,2]['facing']&16==incoming and all(r['body']&2 for r in groups),
         'Actual parent-facing inheritance/flight and native redraw-capable child body')
    mismatch=incoming!=victim_facing
    need(len(redraw)==(2 if mismatch else 0),'Source-derived facing count, independent of physical Block')
    if mismatch:
        need(groups[1:3]==redraw and
             (redraw[0]['a4']&16,redraw[1]['a4']&16)==(victim_facing,incoming)and
             redraw[0]['a4']^redraw[1]['a4']==16 and
             redraw[1]['a5']==redraw[0]['a4'] and groups[3]['a4']==redraw[1]['a4'],
             'Actual alignment flip then original-facing restore before impact, not duplicated launch or Block inference')
    return 2 if mismatch else 0


def prepare():
    scope=prior.prepare()
    scope.update(OUT=OUT,__file__=__file__,facing_redraw=facing_redraw)
    source=inspect.getsource(prior.prior.whole_knife)
    marker="    scope=dict(model.knife.knives.__globals__,first_entry=first_entry)"
    replacement='''    before="        assert len(redraw)==(2 if pressed else 0)"
    need(source.count(before)==1,'Only incorrect Block-dependent count predicate replaced')
    source=source.replace(before,"        assert len(redraw)==facing_redraw(log,guest,by,start,hit,a,redraw)",1)
    scope=dict(model.knife.knives.__globals__,first_entry=first_entry,facing_redraw=facing_redraw)'''
    need(source.count(marker)==1,'Preserve whole original first-round knife model')
    exec(compile(source.replace(marker,replacement,1),__file__+'::whole_knife_source_facing','exec'),scope)
    # These functions bind through this successor scope; old frozen functions
    # and their original failure receipts remain untouched.
    exec(compile(inspect.getsource(prior.prior.bindings),__file__+'::whole_bindings','exec'),scope)
    source=inspect.getsource(prior.prior.execute)
    marker="        ('initial_entry_roster',change('MK2_STARTUP_PROJECTILE_EVENT','roster','1,17',kind='knife')),"
    extra="""
        ('initial_parent_is_not_projectile',change('MK2_STARTUP_PROJECTILE_EVENT','type','81',kind='knife')),
        ('initial_parent_is_not_human_slot',change('MK2_STARTUP_PROJECTILE_EVENT','process_slot','1',kind='knife')),
        ('victim_actual_facing',change('MK2_KNIFE_PAIR_FIELD','facing','8012',frame=1838,slot=1)),
        ('alignment_executed_facing',change('MK2_CPU_OVERLAP_EVENT','a4','FFFFE012',frame=1838,kind='group',a4='FFFFE002')),
        ('restored_executed_facing',change('MK2_CPU_OVERLAP_EVENT','a4','FFFFE002',frame=1838,kind='group',a4='FFFFE012')),
        ('independent_alignment_facing',change('MK2_STARTUP_PROJECTILE_EVENT','a4','FFFFE012',sequence=46)),
        ('independent_restore_facing',change('MK2_STARTUP_PROJECTILE_EVENT','a4','FFFFE002',sequence=47)),
        ('independent_redraw_body',change('MK2_STARTUP_PROJECTILE_EVENT','body','0000',sequence=46)),"""
    need(source.count(marker)==1,'Additional effective facing/role fault cases')
    source=source.replace(marker,marker+extra,1)
    marker="    need(gate(text)==positive,'Whole untouched original native positive restored')"
    extra="""
    for label,address in(('align_restore_router',0xfffc29c0),('native_flip_helper',0xff83b4b0),('actual_impact_call_target',0xff8b00a0)):
        altered=bytearray(state['guest']);altered[(address-0xff800000)//8]^=1
        try:bindings(bytes(altered))(text)
        except(AssertionError,ValueError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual source facing fault admitted '+label)
        print('Current first-round source facing fault rejected: '+label,flush=True)
"""
    need(source.count(marker)==1,'Source-program faults evaluated independently in RAM only')
    source=source.replace(marker,extra+'\n'+marker,1).replace('/26 faults','/37 faults')
    exec(compile(source,__file__+'::whole_original_execute_facing_faults','exec'),scope)
    return scope


def safe_execute(state):
    try:
        rejection=json.loads((prior.OUT/'failure.json').read_text())
        need(not rejection['passed']and rejection['error']=='AssertionError()'and rejection['newNativeGames']==0,
             'Exact prior redraw matcher rejection preserved; no game replay')
        return prepare()['execute'](state)
    except Exception as error:
        need(not OUT.exists(),'Preserve successor rejection')
        OUT.mkdir();prior.prior.capture.prior.prior.current.prior.save(OUT/'failure.json',dict(passed=False,
            error=repr(error),traceback=traceback.format_exc(),newNativeGames=0,goalStatus='active',fullPortAcceptance=False))
        raise
