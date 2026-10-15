"""Current retained square/bicycle misses: full motion and original cleanup.

Reuse native47172, not a replay. Historical miss profiles remain unchanged;
explicitly bind their phase mathematics to the actual startup/ordinary-followup
context. No Sonya RNG/fall-instruction tap was recorded in this older game.
Those omissions remain gaps, not synthetic events or execution acceptance.
"""
import hashlib
import inspect
import json
import struct
from pathlib import Path
import current_sonya_cpu_square_contract_v2045 as square
import current_sonya_cpu_bicycle_contract_v2006 as bicycle
import qualify_native_selector_natural_state_health_bound as ledger
import qualify_native_selector_natural_state_health_checkpoint as pixels
import capture_current_subzero_audio_v6213 as artifact
import verify_native_source_sync as migration

ROOT,need,sha = migration.ROOT,migration.need,migration.sha
OUT=ROOT/'audit_native_selector_existing_sonya_travel_phases_checked'
PARENT=ROOT/'audit_native_selector_sonya_choices_pair_checked/report.json'
GUEST='45DFC25120FD2A56E895B094AF7DC40AD2DC97E452F742F473BFB43216DCCF0A'


def replace(source,before,after):
    need(source.count(before)==1,'One exact declared context boundary: '+before)
    return source.replace(before,after,1)


def source_gate(log,guest):
    need(hashlib.sha256(guest).hexdigest().upper()==GUEST,
         'Entire current source-derived guest, independently compared to actual cold bytes')
    expected={(0xff83ed80,0xff83f060),(0xff837d40,0xff837dc0),
              (0xff861350,0xff861700),(0xfffc3800,0xfffc5800),
              (0xfffc6000,0xfffc8000),(0xfffbc000,0xfffbc150),(0xff80ec20,0xff80ed40)}
    windows=square.original.rows(log,'CODE')+square.rows(log,'MK2_CPU_CHOICE_CODE')
    need(len(windows)==7 and {(r['start'],r['stop']) for r in windows}==expected,
         'Every actual original code window, including preserved Kano-only observer')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for r in windows:
        lo,hi=((r[k]-0xff800000)//8 for k in ('start','stop'))
        words=[int(v,16) for v in r['words'].split(',')]
        need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi], 'All actual observed source words')
        if r['start']<0xfff00000:
            need(guest[lo:hi]==stock[lo:hi], 'Original native cleanup/ready/RNG source unchanged')
    # Keep every original square static instruction assertion; move-specific
    # bytes are part of the actual whole cold guest, not invented CODE rows.
    checks=inspect.getsource(square.source)
    checks=checks[checks.index(' def check(at,words):'):]
    namespace=dict(square.source.__globals__,guest=guest)
    exec(compile('if True:\n'+checks,__file__+'::all_original_square_instruction_signatures','exec'),namespace)
    need(struct.unpack_from('<15H',guest,(0xfff9ab60-0xff800000)//8)==
         (0x09e0,13,0,0x09e1,13,0,0x09e2,0xa000,0,0x09e3,4,0,0x09e6,0xdc00,0xfff9),
         'Actual bicycle ceiling fall parameters in whole cold source')


def square_followup(log,by,ready,actor,main):
    # Square really clears at2020. A NEW ordinary attack starts2026 and clears
    #2063, so requiring no locks/no HP changes during that attack is incorrect.
    flags=square.P.flag_rows(log)
    own=[r for r in flags if r['slot']==2 and ready<r['frame']<=2063]
    for kind,at,mask,setpc,clearpc in (
        ('body',actor+0x160,4,0xff838cf0,0xff83eeb0),
        ('flags',main+0x210,0x10,0xff877d50,0xff83efc0)):
        rows=[r for r in own if r['kind']==kind]
        need(len(rows)==3 and rows[0]['frame']==2026 and rows[0]['pc']==setpc and
             rows[0]['before']&mask==0 and rows[0]['after']==rows[0]['before']|mask and
             all(r['frame']==2063 and r['pc']==clearpc and r['after']==r['before']&(~mask&65535)
                 for r in rows[1:]), 'New ordinary setup and complete later native cleanup, not retained square locks')
        need(all(r['at']==at and (r['actor'],r['main'],r['a8'],r['a13'])==(actor,main,actor,main)
                 for r in rows), 'Original ordinary followup owns same real actor/Main')
    need(set(range(ready+1,2065))<=set(by),'Every callback through new ordinary attack cleanup')
    for frame in range(ready+1,2065):
        r=by[frame];locked=2027<=frame<=2063
        need(r['action']==0x303 and r['y']==r['floor'] and r['trail']==r['vy']==r['gravity']==0 and
             r['flags']&0x1c==(0x10 if locked else 0) and r['body']&0xc==(4 if locked else 0),
             'Every actual follow-up callback tracks separately sourced lock lifetime and grounded control')
    health=[r for r in ledger.rows(log,'MK2_CPU_ROUND_HEALTH') if
            ready<int(r['frame'])<=2063 and r['slot']=='1' and r['before']!=r['after']]
    need([(int(r['frame']),int(r['before'])-int(r['after'])) for r in health]==[(2036,2),(2047,2)],
         'Exact subsequent ordinary damage, separately explained by whole health ledger')
    return dict(ordinarySetup=2026,ordinaryCleanup=2063,postSquareFields=44,ordinaryDamage=4)


def square_gate(log,guest):
    source=inspect.getsource(square.verify)
    first=source.index(" choice=rows(log,'MK2_CPU_CHOICE_EVENT')")
    last=source.index(" fields=P.rows(log,'FIELD')",first)
    source=source[:first]+source[last:]
    source=replace(source,"'stage_floor','hp','vhp'))", "'stage_floor','hp','vhp') if k not in ('hp','vhp') or at<=ready)")
    source=replace(source,"start<=r['frame']<=ready+30", "start<=r['frame']<=ready")
    source=replace(source," fall=one([r for r in rows(log,'MK2_SQUARE_NATIVE_FALL')if r['action']==0x207],'Owned native fall')\n",'')
    source=replace(source,"fling['frame']==fall['frame']==split", "fling['frame']==split")
    source=replace(source," assert(fall['entry'],fall['pc'],fall['actor'],fall['main'],fall['owner'],fall['id'])==(0xff876660,0xff876670,actor,main,actor,18)\n",'')
    source=replace(source,"for r in(fling,fall)","for r in(fling,)")
    first=source.index(' for at in range(ready+1,ready+32):')
    last=source.index(' return dict(',first)
    source=source[:first]+" followup=square_followup(log,by,ready,actor,main)\n"+source[last:]
    source=replace(source,"nativeChoiceSerial=chosen['serial'],firstRandomResult=calls[2]['a0'],secondRandomResult=calls[4]['a0']",
                   'nativeChoiceSerial=None,firstRandomResult=None,secondRandomResult=None')
    source=replace(source,'everyPostRegainCallback=True,lastScene=ready+30',
                   'everyPostRegainCallback=True,lastScene=2064,actualOrdinaryFollowup=followup,nativeRNGObservationAccepted=False,directNativeFallTapAccepted=False')
    scope=dict(square.verify.__globals__,source=source_gate,square_followup=square_followup)
    exec(compile(source,__file__+'::whole_square_motion_actual_followup_context','exec'),scope)
    return scope['verify'](log,guest)


def bicycle_gate(log,guest):
    source=inspect.getsource(bicycle.verify)
    source=replace(source,"pair=state.verify_log(log,'kano',guest)","pair=ledger.gate(log,guest);source_gate(log,guest)")
    source=replace(source,"    assert any(r['start']==0xfff9a400 and r['stop']==0xfff9ad00 for r in codes)\n",'')
    source=replace(source,'set(range(start,end+2))<=set(by)','set(range(start+1,end+2))<=set(by)')
    source=replace(source,'baseline=by[start]','baseline=by[start+1]')
    source=replace(source,'range(start,end+2)','range(start+1,end+2)')
    first=source.index("    falls=[r for r in relevant if r['kind']=='fall']")
    last=source.index('    def advance(a,b,g):',first)
    source=source[:first]+'''    switches=[at for at in range(start+8,end) if by[at]['gravity']==0xffff4000 and by[at+1]['gravity']==0xa000]
    assert len(switches)==1,'One actual ceiling-triggered gravity switch, no synthetic fall event'
    split=switches[0]
'''+source[last:]
    source=replace(source,'subsequentPairContractUnchanged=pair',
                   'wholeNativeStateHealth=pair,nativeRNGObservationAccepted=False,directNativeFallTapAccepted=False')
    scope=dict(bicycle.verify.__globals__,ledger=ledger,source_gate=source_gate)
    exec(compile(source,__file__+'::whole_bicycle_motion_actual_startup_context','exec'),scope)
    return scope['verify'](log,guest)


def gate(log,guest):
    whole=ledger.gate(log,guest)
    return dict(wholeNativeStateHealth=whole,square=square_gate(log,guest),bicycle=bicycle_gate(log,guest),
                nativeRNGObservationAccepted=False,directNativeFallTapAccepted=False,
                allContactsArenasAccepted=False,fullPortAcceptance=False)


def execute(state,capture):
    need(not OUT.exists(),'Fresh immutable existing-evidence phase qualification')
    folder,log,images=capture.RAM_CASES[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed'] and all(sha(p)==h for p,h in pins.items()),'Complete current prior evidence pins')
    need(meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (47172,38752,1791745912.9231853),'Same original terminal47172 handle, no replay')
    need(meta['proofs']['guest']['sha256']==GUEST and meta['proofs']['guest']['everyActualByteComparedInRAM'],
         'Full actual initialized guest proves missing move CODE windows without fabricating observer rows')
    OUT.mkdir()
    try:
        positive=gate(log,state['guest'])
        rasters=pixels.rasters(images,meta['actualScenes'])
        paths=[Path(__file__),PARENT,Path(square.__file__),Path(bicycle.__file__),
               Path(ledger.__file__),Path(pixels.__file__),Path(artifact.__file__),
               *(p for p in folder.rglob('*') if p.is_file())]
        for path in paths:
            key=str(path.resolve());digest=sha(path)
            need(key not in pins or pins[key]==digest,'No historical pin replacement')
            pins[key]=digest
        need(all(sha(p)==h for p,h in pins.items()),'Fresh whole final input census')
        report=dict(passed=True,qualification=positive,actualNativeIdentity=held['identity'],
                    wholeOriginalRasters=rasters,inputHashes=pins,requirements=parent['requirements'],
                    remainingGroups=parent['remainingGroups'],goalStatus='active',fullPortAcceptance=False,
                    faultQualificationPending=True,actualVisualReviewPending=True,
                    newNativeGames=0,newBuilds=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
        artifact.save(OUT/'report.json',report)
        print('PASS current actual square/bicycle motion and complete recovery; faults/visual review pending',flush=True)
        return report
    except Exception as error:
        artifact.save(OUT/'failure.json',dict(passed=False,error=repr(error),inputHashes=pins,
                      originalNativeIdentity=held['identity'],fullPortAcceptance=False,newNativeGames=0))
        raise
