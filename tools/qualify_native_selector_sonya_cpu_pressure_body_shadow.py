"""Original body/packed-ROM/floor-shadow model through actual CPU interruption.

All27 successive draw passes1917..1943, both actors, source poses and shadows.
Full actual physical interruption gate remains independent of rendering rows.
No claim for whole2150-row round/reset rendering or current scanout pixels.
"""
import inspect
import json
import re
import traceback
from collections import defaultdict
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_interrupt as mechanics
import qualify_native_selector_sonya_shadow_geometry as geometry

ROOT,need,sha=mechanics.ROOT,mechanics.need,mechanics.sha
capture=mechanics.capture
body=geometry.body
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_body_shadow_checked'
FRAMES=set(range(1917,1944))


def bindings(guest):
    def state_gate(b,current,payload):
        need(current==guest,'Same independently derived complete current guest')
        state=mechanics.gate(b['cpuLog'],guest)
        pair=capture.base.choices.native_state.original.pair
        physical={r['frame']:r for r in pair.rows(b['cpuLog'],'FIELD')}
        posts=b['rows']['MK2_HPHASE_POST_FIELD']
        keys={(int(r['frame']),int(r['slot']))for r in posts}
        need(len(posts)==len(keys)==54 and keys=={(f,s)for f in FRAMES for s in (1,2)},
             'Both complete actual draw callbacks on every successive interrupted/recovered field')
        hexes={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail'}
        for r in posts:
            f,s=int(r['frame']),int(r['slot']);p=physical[f+1];prefix='v'if s==1 else ''
            need(r['writes']=='0'and r['assistance']=='none'and
                 all(int(r[k],16 if k in hexes else 10)==p[prefix+k]for k in
                     ('actor','main','owner','pose','id','action','y','floor','vx','vy','gravity','flags','body','trail','hp')) and
                 int(r['roster'])==p[prefix+'roster'] and int(r['state'])==p[prefix+'state'],
                 'Every actual final body/shadow source word equals independent next physical actor/Main field')
        return dict(passed=True,wholeActualPressureMechanics=state,actualDrawFrames=27,
                    physicalDrawCompleteFields=54,fullPortAcceptance=False)
    source=inspect.getsource(body.check)
    first=source.index(' # The older physical/ownership/health checker')
    last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
    source=mechanics.phases.replace(source,source[first:last],
        " state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_HPHASE_CPU_NATIVE_ENTRY']}\n")
    source=mechanics.phases.replace(source,'ids={side:identity,3-side:4}','ids={1:17,2:18}')
    scope=dict(vars(body),state_gate=state_gate)
    exec(compile(source,__file__+'::whole_original_body_stream_shadow_model_actual_pressure_interruption','exec'),scope)
    return scope['check']


def execute(state):
    need(not OUT.exists(),'Fresh immutable actual interruption rendering qualification')
    parent=mechanics.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    need(proof['passed']and meta['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']and all(sha(p)==h for p,h in pins.items()),
         'Same original terminal44780 pressure data and all full source/native pins intact')
    rows=defaultdict(list)
    for line in text.splitlines():
        if not line.startswith('MK2_HPHASE_'):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(pairs)==len(dict(pairs)),'Every actual rendering row unambiguous')
        row=dict(pairs)
        if 'frame'in row and int(row['frame'])in FRAMES:rows[line.split()[0]].append(row)
    # Select original complete source-stream receipts from descriptors actually
    # used in this exact window; unused other-round receipts are not fabricated
    # into an observed projection or accepted as this finite interruption.
    streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text())
    used={f"{body.num(r,'graphic'):08X}_{body.num(r,'width')}_{body.num(r,'height')}_{body.num(r,'command'):04X}"
          for r in rows['MK2_HPHASE_PROJECTION']}
    selected=[r for r in streams if r['stream']in used]
    need(len(selected)==len(used)>0,'Every actual interrupted-window source stream retained exactly once')
    b=dict(move='leg',side=2,folder=folder,report_path=folder/'result.json',report=meta,
           cpuLog=text,rows=rows,streams=selected)
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(state['guest'][a:z]==stock[a:z],'Entire original native body/shadow clipping/projection kernels unchanged')
    check=bindings(state['guest']);positive=check(b,state['guest'],state['payload'],state['gfx32'])
    runner=geometry.template.scope['current'].prior.shadow_faults
    faults=runner(dict(b,report=dict(meta,sourceBoundBodyShadowSemantics=positive)),
                  state['guest'],state['payload'],state['gfx32'],check)
    need(len(faults)==11 and check(b,state['guest'],state['payload'],state['gfx32'])==positive,
         'All eleven original body/packed-ROM/shadow corruption tests and full positive restored')
    for p in (Path(__file__),parent,Path(mechanics.__file__),Path(geometry.__file__),Path(body.__file__),
              ROOT/'tools/verify_move_phase_shadow_v5089.py',folder/'shadow_stream_memory_proofs.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed source/evidence');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every complete original input after rendering faults')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholeActualInterruptedWindowBodyShadow=positive,originalBodyShadowFaultsRejected=faults,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],actualFrames=sorted(FRAMES),
        finiteCPUInterruptionBodyShadowAccepted=True,wholePressureRoundResetRenderingAccepted=False,
        wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,allArenaCPUContextsAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS both full native body/packed-ROM/floor shadows on27 interrupted/recovery passes;11 faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual interrupted-window body/shadow rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
