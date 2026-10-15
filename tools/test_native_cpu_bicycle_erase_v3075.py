"""Actual native one-base Bicycle erase counterexamples, no capture mutation.

Original v1810 FILL/clear/source/ordering tests applied to both fresh
native trajectories. Nonvacuity required; unchanged captures rechecked last.
"""
import copy
import json
import traceback
from pathlib import Path
from unittest.mock import patch
import verify_native_cpu_ring_erase_v2985 as model

ROOT=model.ROOT
OUT=ROOT/'audit_v3076_native_cpu_bicycle_erase_units'

def run():
    path=ROOT/'audit_v3072_native_cpu_bicycle_erase_checked/report.json'
    proof=json.loads(path.read_text());need=model.need
    need(proof['passed'] and proof['originalContinuousReplayContractUnchanged'] and
         proof['oneInitialBaseOnlyPerActualFixture'] and not proof['laterBuffersUsedAsAnchors'], 'Actual unchanged one-base erase replay accepted')
    pins=dict(proof['inputHashes']);pins[str(path)]=model.sha(path)
    render={'cases':proof['cases']}
    guest,control,_,_,_=model.assembly.expected();tests=[]
    for key,case in render['cases'].items():
        folder=ROOT/case['case'];image=guest if key.startswith('new')else control
        groups,buffers,a,b,owners=model.raster.data(folder)
        native=groups['FLOOR_SHIFT_FILL'][0]
        second=groups['FLOOR_SHIFT_FILL'][1]
        pages=[model.copies_for_fill(r)for r in(native,second)]
        need({tuple(p)for p in pages}=={tuple(range(0,127*1024,1024)),tuple(range(131072,131072+127*1024,1024))},
             'Both exact original native framebuffer clear pages reached normally')
        scalar=[('opcode','op',0),('caller','pc',0xff817150),('partial_mask','mask',255),
            ('repeated_fill_cycle','status',native['status']|0x02000000),
            ('shift_mode_off','control',native['control']&~0x0800),
            ('window_mode','raster_control',native['raster_control']|0x40),
            ('pixel_size','psize',16 if native['psize']!=16 else 8),('pixel_shift','pixelshift',0),
            ('conversion','convdp',1024),('width','shape',0x007f0002),
            ('height','shape',0x007e0001),('out_of_vram','native_offset',0xffffffff)]
        for label,column,value in scalar:
            altered=dict(native);altered[column]=value
            need(altered!=native,'Nonvacuous actual FILL mutation '+key+': '+label)
            try:model.copies_for_fill(altered)
            except (ValueError,AssertionError)as error:tests.append(dict(case=key,name=label,rejectedBy=str(error)))
            else:raise ValueError('Accepted corrupt native FILL '+key+': '+label)
        for label,mutate in [
            ('missing_first_clear',lambda g:g['FLOOR_SHIFT_FILL'].pop(0)),
            ('missing_native_source_load',lambda g:g['FLOOR_SHIFT_LOAD'].pop(0)),
            ('wrong_native_source_address',lambda g:g['FLOOR_SHIFT_LOAD'][0].update(address=0x1fc000,index=260096)),
            ('wrong_shift_stream',lambda g:g['FLOOR_SHIFT_FILL'][0].update(ref=999)),
            ('duplicate_transfer_event',lambda g:g['FLOOR_SHIFT_FILL'].append(dict(g['FLOOR_SHIFT_FILL'][0]))),
            ('clear_after_its_pre_target',lambda g:g['FLOOR_SHIFT_FILL'][0].update(event=g['FLOOR_PRE_FRAME'][0]['event']+1)),
        ]:
            altered=copy.deepcopy(groups);mutate(altered)
            need(altered!=groups,'Nonvacuous actual chronological erase mutation '+key+': '+label)
            with patch.object(model.raster,'data',return_value=(altered,buffers,a,b,owners)):
                try:value=model.inspect(folder,image,case['candidate'])
                except (ValueError,AssertionError,KeyError)as error:tests.append(dict(case=key,name=label,rejectedBy=str(error)))
                else:
                    need(not value['passed'],'Accepted corrupt actual continuous erase '+key+': '+label)
                    tests.append(dict(case=key,name=label,rejectedBy=value))
        unchanged=model.inspect(folder,image,case['candidate'])
        need(unchanged['passed'] and all(unchanged[k]==proof['cases'][key][k]for k in
            ('continuousExactPreBuffers','continuousExactFlips','nativeShiftTransfers','shiftLoads','shiftFills','oneInitialBaseOnly')),
            'Final unmodified actual one-base erase replay remains identical')
        print(key+': all18 original actual erase corruptions rejected, original capture unchanged',flush=True)
    need(len(tests)==18,'All18 actual FILL/source/chronological erase counterexamples rejected')
    for file,wanted in pins.items():need(model.sha(file)==wanted,'Actual immutable erase dependencies '+file)
    pins[str(Path(__file__).resolve())]=model.sha(__file__)
    return dict(passed=True,actualPhysicalFixtures=1,actualOriginalEraseCounterexamplesRejected=len(tests),
        counterexamples=tests,actualCapturesUnmodified=True,laterBuffersUsedAsAnchors=False,
        gameChanged=False,allArenaMoveCPUOrMorphsAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    model.need(not OUT.exists(),'Immutable actual native Bicycle erase negative evidence')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('inputHashes','counterexamples','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
