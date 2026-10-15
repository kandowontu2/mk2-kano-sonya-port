"""Negative checks for the one-anchor native shift-clear verifier.

Mutations are in memory only; original captures and failed evidence unchanged.
"""
import argparse,copy,json
from pathlib import Path
from unittest.mock import patch
import inspect_continuous_move_erase_v1809 as verifier

def main(folder,output):
    verifier.need(not output.exists(),'Never overwrite evidence')
    groups,buffers,_,_,owners=verifier.raster.data(folder)
    reportpath=verifier.current.ROOT/'audit_v1799_human_leg_p1_continuity_checked/report.json'
    accepted=json.loads(reportpath.read_text())
    verifier.need(accepted['passed']and accepted['oneInitialBaseOnly']and not accepted['laterBuffersUsedAsAnchors'],'Accepted original uninterrupted baseline')
    for p,h in accepted['inputHashes'].items():verifier.need(verifier.sha(p)==h,'Baseline pin changed')
    passed=[]
    native=groups['FLOOR_SHIFT_FILL'][0]
    indices=verifier.copies_for_fill(native)
    verifier.need(indices==list(range(0,127*1024,1024)),'Exact original first-page shift callbacks')
    second=groups['FLOOR_SHIFT_FILL'][1]
    verifier.need(verifier.copies_for_fill(second)==list(range(131072,131072+127*1024,1024)),'Exact original second-page shift callbacks')
    scalar=[('opcode','op',0),('caller','pc',0xff817150),('partial_mask','mask',255),
            ('repeated_fill_cycle','status',native['status']|0x02000000),
            ('shift_mode_off','control',native['control']&~0x0800),('window_mode','raster_control',native['raster_control']|0x40),
            ('pixel_size','psize',16),('pixel_shift','pixelshift',0),('conversion','convdp',1024),
            ('width','shape',0x007f0002),('height','shape',0x007e0001),('out_of_vram','native_offset',0xffffffff)]
    for name,key,value in scalar:
        altered=dict(native);altered[key]=value
        try:verifier.copies_for_fill(altered)
        except (ValueError,AssertionError):passed.append(name)
        else:raise ValueError('Accepted corrupt native fill '+name)
    for name,mutate in [
        ('missing_first_clear',lambda g:g['FLOOR_SHIFT_FILL'].pop(0)),
        ('missing_native_source_load',lambda g:g['FLOOR_SHIFT_LOAD'].pop(0)),
        ('wrong_native_source_address',lambda g:g['FLOOR_SHIFT_LOAD'][0].update(address=0x1fc000,index=260096)),
        ('wrong_shift_stream',lambda g:g['FLOOR_SHIFT_FILL'][0].update(ref=999)),
        ('duplicate_transfer_event',lambda g:g['FLOOR_SHIFT_FILL'].append(dict(g['FLOOR_SHIFT_FILL'][0]))),
        ('clear_after_its_pre_target',lambda g:g['FLOOR_SHIFT_FILL'][0].update(event=g['FLOOR_PRE_FRAME'][0]['event']+1)),
    ]:
        altered=copy.deepcopy(groups);mutate(altered)
        with patch.object(verifier.raster,'data',return_value=(altered,buffers,None,None,owners)):
            try:result=verifier.inspect(folder)
            except (ValueError,AssertionError,KeyError):passed.append(name)
            else:
                verifier.need(not result['passed'],'Accepted corrupt observed operations '+name);passed.append(name)
    output.mkdir();report=dict(passed=True,baselineReport=str(reportpath),baselineHash=verifier.sha(reportpath),
      baselinePins=len(accepted['inputHashes']),originalPagesChecked=2,rejectedCorruptions=passed,
      mutationCount=len(passed),mutationsInMemoryOnly=True,guestWrites=False,laterBuffersUsedAsAnchors=False,
      fullPortAcceptance=False,sourceHashes={str(Path(__file__)):verifier.sha(__file__),str(Path(verifier.__file__)):verifier.sha(verifier.__file__)})
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();main(args.folder,args.output)
