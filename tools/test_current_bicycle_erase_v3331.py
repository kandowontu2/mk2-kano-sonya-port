"""Specific original18 chronological erase corruptions on current Bicycle hit."""
import copy
import json
import traceback
from pathlib import Path
from unittest.mock import patch
import verify_current_bicycle_render_erase_v3322 as current
model=current.erase;need=current.need;ROOT=current.ROOT
OUT=ROOT/'audit_v3332_current_cpu_bicycle_hit_erase_counterexamples'

def run():
    expected=current.current.expected_current()
    current.current.assembly.NAME=current.current.current.CANDIDATE;current.current.assembly.expected=lambda:expected
    path=current.OUT/'report.json';proof=json.loads(path.read_text());need(proof['passed'],'Current actual complete native render/erase proof')
    pins=dict(proof['inputHashes']);pins[str(path)]=model.sha(path)
    folder=ROOT/current.state.CASE;actual=model.raster.data(folder);groups,buffers,a,b,owners=actual
    base=proof['erase'];model.source_contract()
    with patch.object(model.raster,'data',return_value=copy.deepcopy(actual)):
        positive=model.inspect(folder,expected[0],proof['candidate'])
    need(positive['passed'] and positive['continuousExactFlips']==109 and positive['nativeShiftTransfers']==base['nativeShiftTransfers'],'Same mocked-path one-base positive control')
    native,second=groups['FLOOR_SHIFT_FILL'][:2]
    need({tuple(model.copies_for_fill(r))for r in(native,second)}=={tuple(range(0,127*1024,1024)),tuple(range(131072,131072+127*1024,1024))},'Actual two original native clear pages')
    scalars=[
        ('opcode','op',0,'Exact original FILL XY instruction'),
        ('caller','pc',0xff817150,'Exact original FILL XY instruction'),
        ('partial_mask','mask',255,'Exact original FILL XY instruction'),
        ('repeated_fill_cycle','status',native['status']|0x02000000,'First native FILL execution in shift-register mode'),
        ('shift_mode_off','control',native['control']&~0x0800,'First native FILL execution in shift-register mode'),
        ('window_mode','raster_control',native['raster_control']|0x40,'This bounded native clear has no window clipping'),
        ('pixel_size','psize',16 if native['psize']!=16 else 8,'Native pixel size and conversion shift agree'),
        ('pixel_shift','pixelshift',0,'Native pixel size and conversion shift agree'),
        ('conversion','convdp',1024,'Native CONVDP lookup matches original CPU source'),
        ('width','shape',0x007f0002,'Only the original one-column 127-row clear is certified'),
        ('height','shape',0x007e0001,'Only the original one-column 127-row clear is certified'),
        ('out_of_vram','native_offset',0xffffffff,'Native shift callback destination range'),
    ];tests=[]
    for label,column,value,reason in scalars:
        altered=dict(native);altered[column]=value;need(altered!=native,'Nonvacuous actual native fill corruption')
        try:model.copies_for_fill(altered)
        except ValueError as error:
            need(str(error)==reason,'Specific fill rejection, not arbitrary exception');tests.append(dict(name=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted corrupt actual native fill: '+label)
    variants=[
        ('missing_first_clear',lambda g:g['FLOOR_SHIFT_FILL'].pop(0)),
        ('missing_native_source_load',lambda g:g['FLOOR_SHIFT_LOAD'].pop(0)),
        ('wrong_native_source_address',lambda g:g['FLOOR_SHIFT_LOAD'][0].update(address=0x1fc000,index=260096)),
        ('wrong_shift_stream',lambda g:g['FLOOR_SHIFT_FILL'][0].update(ref=999)),
        ('duplicate_transfer_event',lambda g:g['FLOOR_SHIFT_FILL'].append(dict(g['FLOOR_SHIFT_FILL'][0]))),
        ('clear_after_its_pre_target',lambda g:g['FLOOR_SHIFT_FILL'][0].update(event=g['FLOOR_PRE_FRAME'][0]['event']+1)),
    ]
    messages={
        'missing_first_clear':{'Every target and observed original clear accounted'},
        'missing_native_source_load':{'Store uses its actual original preceding source load'},
        'wrong_native_source_address':{'Original source template address'},
        'duplicate_transfer_event':{'Unique original event ordering'},
        'clear_after_its_pre_target':{'Unique original event ordering'},
    }
    for label,change in variants:
        altered=copy.deepcopy(groups);change(altered);need(altered!=groups,'Nonvacuous actual chronological corruption')
        with patch.object(model.raster,'data',return_value=(altered,buffers,a,b,owners)):
            try:result=model.inspect(folder,expected[0],proof['candidate'])
            except KeyError as error:
                need(label=='wrong_shift_stream' and error.args==(999,),'Only explicitly corrupted missing shift reference is a qualified KeyError')
                tests.append(dict(name=label,rejectedBy='Explicitly invented shift reference 999'))
            except ValueError as error:
                need(str(error)in messages.get(label,set()),'Specific chronological rejection, not unrelated failure: '+label+' '+str(error))
                tests.append(dict(name=label,rejectedBy=str(error)))
            else:
                need(label in {'missing_first_clear','clear_after_its_pre_target'} and not result['passed'] and
                     result['failureKind']in {'FLOOR_PRE_FRAME','FLOOR_FLIP'} and result['mismatchCount']>0,'Actual corrupted clear causes a real continuous framebuffer mismatch')
                tests.append(dict(name=label,rejectedBy=result))
    unchanged=model.inspect(folder,expected[0],proof['candidate'])
    need(unchanged['passed'] and all(unchanged[k]==base[k]for k in ('continuousExactPreBuffers','continuousExactFlips','nativeShiftTransfers','shiftLoads','shiftFills','oneInitialBaseOnly')),'Untouched original capture remains identical')
    need(len(tests)==18,'All original18 actual clear/transfer corruptions rejected')
    for file,digest in pins.items():need(model.sha(file)==digest,'Actual capture/source bytes unchanged')
    pins[str(Path(__file__).resolve())]=model.sha(__file__)
    return dict(passed=True,actualCounterexamplesRejected=18,counterexamples=tests,sameMockedPathPositiveControlsAccepted=True,
                specificRejectionReasonsRequired=True,unrelatedMissingEventExceptionsNeverAccepted=True,
                actualCapturesUnmodified=True,oneInitialBaseOnly=True,gameChanged=False,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite actual erase counterexamples')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('counterexamples','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
