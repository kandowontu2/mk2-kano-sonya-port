"""Whole transition trial with original roster guard and retained failed targets.

No passing target changes. Current frame_done VRAM is only a diagnostic, never
selected to rescue a failed latch binding. Preserve every failed field while
continuing actual native RGB/state capture through the real playable rejoin.
"""
import json
import re
from pathlib import Path
import run_native_tomb_transition_rejoin_live as previous

source = previous.once(previous.source,
    "PREFIX = 'audit_native_tomb_transition_rejoin_live'",
    "PREFIX = 'audit_native_tomb_transition_timing'")
source = previous.once(source,
    "records[-1]['frame'] == int(re.search(r'MK2_STAGE_RESULT frame=(\\d+)',text)[1])",
    "records[-1]['frame'] == cf and int(re.search(r'MK2_STAGE_RESULT frame=(\\d+)',text)[1]) == cf+1")
source = previous.once(source,
    "    proof = display.check_latch(rgb, vram, palette, state['start'], state['control'], state['tap'])",
    "    proof = timing_binding(rgb,vram,palette,state)")
source = previous.once(source,"    keep = changed or frame % 120 == 0",
    "    keep = not proof['passed'] or changed or frame % 120 == 0")
source = previous.once(source,'; every native pixel bound", flush=True)',
    '; native binding status recorded", flush=True)')
source = previous.once(source,'        post = verify_rejoin(text,',
    "        RAM['base_report'] = base\n"
    "        (output.parent/(output.name+'_original_scene_report.json')).write_text(json.dumps(base,indent=2)+'\\n')\n"
    '        post = verify_rejoin(text,')
insertion = source.index("if __name__ == '__main__':")
extra = r'''
TIMING_LUA = tuple(ROOT/name for name in ('mk2ks_native_tomb_rejoin_guarded_driver.lua',
    'mk2ks_native_tomb_rejoin_guarded_provenance.lua','mk2ks_native_tomb_rejoin_timing_display.lua'))
_original_source_guard = extension_source_guard
_original_functions = functions
_original_post_line = post_line

def extension_source_guard():
    pins = _original_source_guard()
    frozen = ROOT/'audit_native_tomb_transition_rejoin_live_kano_p1_checked/failed_observer_trial_preservation_and_ram_retirement.json'
    retained = json.loads(frozen.read_text())
    need(retained['passed'] and not retained['fullOriginalTrialAccepted'] and
         all(sha(p)==h for p,h in retained['inputHashes'].items()),'Entire original failed actual transition trial remains frozen')
    for p in TIMING_LUA:
        need(p.is_file(),'All actual passive timing/guard extensions present')
        text=p.read_text()
        need(not re.search(r':write_u\d+|\.value\s*=(?!=)|load_?state',text),'No native game/register writes')
        pins[str(p)]=sha(p)
    pins[str(frozen)]=sha(frozen)
    need('p:read_u16(slots[n].roster)<=18' in TIMING_LUA[0].read_text(),'Original native CSS valid-roster guard restored')
    return pins

def functions(current):
    scope=_original_functions(current)
    # New actual observer and every predecessor are bound in native input pins.
    body=scope['run'].__code__
    scope['LUA']=tuple(scope['LUA'])+TIMING_LUA
    scope['OBSERVER']=TIMING_LUA[-1]
    RAM.update(post_timing={},post_failures=[])
    return scope

def post_line(line):
    _original_post_line(line)
    if line.startswith('MK2_TOMB_POST_TIMING '):
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        decimal={'frame','flip_frame','x1','y1','x2','y2'}
        row={k:int(v,10 if k in decimal else 16)for k,v in row.items()}
        need(row['frame']==RAM['post_states'][-1]['frame'] and row['frame'] not in RAM['post_timing'],
             'One exact actual native timing row per later field')
        RAM['post_timing'][row['frame']]=row

def pixel_matches(rgb,raw,palette,state):
    address=state['start'] if state['control']&0x400 else state['start']^0xfffc
    row=(address>>4)&511
    column=((((address&0x7c)<<4)|(state['tap']&0x3fff))*2)&511
    need(row+254<=512 and column+400<=512,'Original bounded native display crop')
    words=np.frombuffer(raw,dtype='<u2').reshape(512,512)[row:row+254,column:column+400]&0x7fff
    pens=np.frombuffer(palette,dtype='<u4')
    colors=np.stack([(pens>>16)&255,(pens>>8)&255,pens&255],axis=1).astype(np.uint8)
    exact=np.all(rgb==colors[words],axis=2)
    return int(np.count_nonzero(exact)),np.flatnonzero(np.any(~exact,axis=1)).tolist()

def timing_binding(rgb,vram,palette,state):
    frame=state['frame']
    timing=RAM['post_timing'][frame]
    current=RAM['post_raw'].pop(f'display_pre_{frame}.bin')
    digest=previous.previous.model.digest
    try:
        proof=display.check_latch(rgb,vram,palette,state['start'],state['control'],state['tap'])
    except ValueError as error:
        need(str(error)=='Every screenshot pixel matches the actual newly displayed VRAM and palette',
             'Preserve only actual pixel-binding mismatch, not malformed native transport')
        matches,rows=pixel_matches(rgb,vram,palette,state)
        current_matches,current_rows=pixel_matches(rgb,current,palette,state)
        proof=dict(passed=False,pixels=matches,error=repr(error),mismatchedNativeRows=rows,
                   currentVRAMDiagnosticMatches=current_matches,currentVRAMDiagnosticRows=current_rows)
        if len(RAM['post_failures'])<8:
            RAM['post_failures'].append(dict(frame=frame,state=state.copy(),timing=timing.copy(),
                rgb=rgb.copy(),latch=vram,current=current,palette=palette,comparison=proof.copy()))
    proof.update(timing=timing,currentVRAMDiagnosticSHA256=digest(current),
                 currentVRAMNeverSelectedAsPassingTarget=True)
    return proof

'''
source = source[:insertion]+extra+source[insertion:]
scope = dict(__name__=__name__,__file__=__file__)
exec(compile(source,__file__+'::whole_original_no_weakened_display_gates_native_timing_diagnostics','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
