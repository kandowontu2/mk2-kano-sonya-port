"""Whole native Ring rendering for three original, naturally chosen lifetimes.

Original decoder/FIFO/DMA/VRAM/flip/palette equations are unchanged. Actual
Ring phase coverage replaces Knife-specific context and its16-pose count;
all independently recorded native Ring poses must be represented exactly.
No missed/unobserved phase, damage, action, source or ownership is invented.
"""
import copy
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_selector_cpu_rings_snapshot_ram as capture
import qualify_native_selector_walkin_knife_display_ram as original
import qualify_native_selector_walkin_knife_display_face_rows as names
import qualify_native_selector_walkin_knife_vram as ram
import qualify_native_selector_cpu_rings_snapshot_transport as transport

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_rings_snapshot_renderer_checked'


def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith(tag+' ')]


def case_text(text,window):
    lines=[]
    for line in text.splitlines():
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            record=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if record.get('window')==str(window):lines.append(line)
    need(lines,'Original full actual drawing observer window present')
    return '\n'.join(lines)+'\n'


def context(text,window):
    birth=rows(text,'MK2_CPU_OVERLAP_CHILD')[window-1]
    retired=rows(text,'MK2_CPU_OVERLAP_RETIRE')[window-1]
    start=[r for r in rows(text,'MK2_STARTUP_PROJECTILE_EVENT')if r['kind']=='ring'][window-1]
    need((start['frame'],birth['frame'],retired['frame'])==
         [('1817','1832','1869'),('2175','2190','2224'),('3027','3042','3079')][window-1] and
         start['id']==birth['id']==retired['id']=='18' and start['a8']==birth['shot_owner']==retired['shot_owner']=='010350A0',
         'Three actual complete unchanged startup/leg-followup/native Ring lifetimes')
    fields=[r for r in rows(text,'MK2_STARTUP_PROJECTILE_FIELD')if r['birth']==birth['frame']]
    need([int(r['frame'])for r in fields]==list(range(int(birth['frame'])+1,int(retired['frame'])+1)) and
         all(r['id']=='18' and r['type']=='81' and r['original_parent']=='010350A0' and
             r['actor']==birth['a8'] and r['main']==birth['a13'] and r['active']=='1' and r['free']=='0' for r in fields),
         'Every independent native Ring child field and active/free owner complete')
    poses={int(r['pose'],16)for r in fields}|{int(birth['pose'],16)}
    return dict(start=int(start['frame']),birth=int(birth['frame']),retirement=int(retired['frame']),
        child=int(birth['a8'],16),main=int(birth['a13'],16),poses=poses,fields=len(fields))


def ownership(groups,state,expected):
    source=inspect.getsource(original.ownership)
    source=original.once(source,"(born[0]['frame'],dead[0]['frame'])==(2259,2312)",
                         "(born[0]['frame'],dead[0]['frame'])==(expected['birth'],expected['retirement'])")
    source=original.once(source,
        '(0x01031d10,0x0106bf30,0x010350a0,0x0106a370,0x010350a0,0x0106b840)',
        "(expected['child'],expected['main'],0x010350a0,0x0106bf30,0x010350a0,0x0106a370)")
    source=original.once(source,"birth['id']==birth['roster']==17 and birth['entry']==0xfffc6000",
                         "birth['id']==birth['roster']==18 and birth['entry']==0xfffc7000")
    source=original.once(source,"(birth['actor'],birth['main'],birth['actor'],birth['parent'],17,17,1)",
                         "(birth['actor'],birth['main'],birth['actor'],birth['parent'],18,18,1)")
    source=original.once(source,
        '(0x01034e90,0x0106b840,18) if q[\'slot\']==1 else (0x010350a0,0x0106a370,17)',
        '(0x01034e90,0x0106a370,17) if q[\'slot\']==1 else (0x010350a0,0x0106bf30,18)')
    source=original.once(source,"len(child_poses)>=16","child_poses==expected['poses']")
    scope=dict(vars(original),expected=expected)
    exec(compile(source,__file__+'::whole_original_ownership_actual_Ring_context','exec'),scope)
    return scope['ownership'](groups,state['payload'],state['guest'])


def positive(folder,text,display,state,expected,image):
    ram.verify_transport(display);ram.graphics(display,image)
    groups,*_=original.data(text,display)
    semantic=ownership(groups,state,expected)
    value=original.bindings(text,display)(folder)
    need(value['frames']==len(display['rgb']) and all(
        r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in value['records']),
        'Every saved actual Ring whole VRAM/palette/current RGB and shadow pixel exact')
    return value,semantic


def execute(state):
    need(not OUT.exists(),'Fresh immutable three-Ring rendering evidence')
    receipt=json.loads((transport.OUT/'report.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(receipt['passed'] and held['process'].poll()==receipt['nativeExit']==0 and
         held['identity']==receipt['actualNativeIdentity'],'Same original terminal actual three-Ring native game')
    pins=dict(receipt['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All full current source/evidence pins unchanged')
    image=names.runtime_graphics(state,pins);folder,text,_=capture.RAM_CASES[capture.KEY]
    # Byte-complete constructor/child/retirement source, including the actual
    # independent observed opcodes, not merely the declared host constants.
    for r in rows(text,'MK2_STARTUP_PROJECTILE_CODE'):
        import struct
        lo,hi=((int(r[k],16)-0xff800000)//8 for k in ('start','stop'))
        words=[int(w,16)for w in r['words'].split(',')]
        need(struct.pack('<'+'H'*len(words),*words)==state['guest'][lo:hi],'Every original independently captured source program word')
    cases=[];faults=[]
    for window in (1,2,3):
        display=capture.DISPLAY[window];local=case_text(text,window);expected=context(text,window)
        positive_render,owned=positive(folder,local,display,state,expected,image)
        groups,*_=original.data(local,display)
        child_index=next(i for i,r in enumerate(groups['FLOOR_QUEUE'])if r['slot']==3)
        for key in ('actor','main','parent','id','source','xy','bank'):
            changed=copy.deepcopy(groups);changed['FLOOR_QUEUE'][child_index][key]^=1
            try:ownership(changed,state,expected)
            except (ValueError,AssertionError)as error:faults.append(dict(window=window,kind='actual_Ring_owner_'+key,rejectedBy=str(error)))
            else:raise ValueError('Effective actual Ring ownership counterexample admitted '+key)
        file=list(display['rgb'])[25];changed=dict(display,rgb=dict(display['rgb']))
        changed['rgb'][file]=display['rgb'][file].copy();changed['rgb'][file][100,100,0]^=1
        try:original.bindings(local,changed)(folder)
        except (ValueError,AssertionError)as error:faults.append(dict(window=window,kind='actual_current_Ring_RGB_pixel',rejectedBy=str(error)))
        else:raise ValueError('Effective actual Ring rendered pixel counterexample admitted')
        restored,restored_owned=positive(folder,local,display,state,expected,image)
        need(restored==positive_render and restored_owned==owned,'Whole untouched actual Ring positive restored after faults')
        cases.append(dict(window=window,start=expected['start'],birth=expected['birth'],retirement=expected['retirement'],
            independentChildFields=expected['fields'],independentActualPoses=sorted(expected['poses']),
            actualSourceFIFOAndDMA=owned,wholeSavedNativePasses=restored,
            sourceGraphicsStreams=len(display['gfx']),actualRGBFrames=len(display['rgb'])))
    for path in (Path(__file__),Path(capture.__file__),Path(original.__file__),Path(names.__file__),Path(ram.__file__),
                 transport.OUT/'report.json',ROOT/'tools/inspect_secondary_display_v1231.py',ROOT/'tools/inspect_native_scaled_arena_v1716.py'):
        key=str(path.resolve());h=sha(path);need(key not in pins or pins[key]==h,'No executed source/evidence change');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All whole source/native/evidence pins after full restored positives')
    report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,cases=cases,
        actualRGBFrames=receipt['actualRGBFrames'],exactWholeDisplayedPixels=receipt['actualRGBFrames']*400*254,
        exactWholeVRAMWords=receipt['actualRGBFrames']*512*512,
        effectiveOwnershipAndRenderFaultsRejected=faults,inputHashes=pins,
        requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],
        finiteThreeSonyaCPURingSavedPassRenderingAccepted=True,actualVisualReviewAccepted=False,
        fullAudioQualificationAccepted=False,interPassEraseAccepted=False,allArenaCPUContextsAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,
        newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS three actual CPU Ring lifetimes:319 whole current displays and24 faults',flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual three-Ring checker failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
