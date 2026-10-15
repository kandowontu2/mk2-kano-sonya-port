"""Read-only triage of actual campaign costume palette checks, not acceptance."""
import argparse,json,re,struct
from pathlib import Path
from collections import defaultdict
import numpy as np
import verify_native_floor_campaign_v1573 as campaign
import verify_active_launch_cpu_display_v1525 as native

def inspect(folder):
    pins={};campaign.matched(folder,pins)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    assert result['exit_code']==0
    side=result['human_slot'];identity={'kano':17,'sonya':18}[result['player']]
    log=folder/'run.log';before=campaign.digest(log);groups=defaultdict(list)
    selected={'FLOOR_QUEUE','FLOOR_QUEUE_DISPATCH','FLOOR_DMA','FLOOR_SNAP','FLOOR_DISPLAY'}
    hex_fields=native.raster.HEX|{'cursor','row','size','xy','b14','b10','a0','a1','a3','a7'}
    str_fields=native.raster.STR|{'register'}
    with log.open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'^MK2_NAT_CAMPAIGN_(\w+) ',line)
            if not match or match[1]not in selected:continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            campaign.drawing_scope(line,side,result['player'])
            for key,value in row.items():
                if key not in str_fields:row[key]=int(value,16 if key in hex_fields else 10)
            if match[1]=='FLOOR_DMA':row={key:row[key]for key in('frame','event')}
            groups[match[1]].append(row)
    guest,_,_=native.grab.expected_guest()
    queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
    assert len(queues)==len(groups['FLOOR_QUEUE'])
    dmas={r['event']:r for r in groups['FLOOR_DMA']}
    assert len(dmas)==len(groups['FLOOR_DMA'])
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    dispatches=defaultdict(list)
    for r in groups['FLOOR_QUEUE_DISPATCH']:dispatches[dmas[r['event']]['frame']].append(r)
    def palette(off):
        count=struct.unpack_from('<H',guest,off)[0];assert count==(64 if off in(0xf59a0,0xf5a40)else 65)
        raw=struct.unpack_from('<'+str(count)+'H',guest,off+2)
        return np.array([sum(((((c>>shift)&31)<<3)|(((c>>shift)&31)>>2))<<dest
                             for shift,dest in((10,16),(5,8),(0,0)))for c in raw],dtype=np.uint32)
    offsets={'normal':0xfda00 if identity==17 else 0xfdb00,
             'alternate':0xf1500 if identity==17 else 0xf1600,
             'frozen':0xf59a0 if identity==17 else 0xf5a40}
    references={kind:palette(off)for kind,off in offsets.items()}
    failures=[];checked=0
    for snap in groups['FLOOR_SNAP']:
        file=folder/displays[snap['frame']]['palette_file'];actual=np.fromfile(file,dtype='<u4')
        assert len(actual)==32768
        for r in dispatches[snap['frame']-1]:
            if r['slot']!=side:continue
            q=queues[r['queue_frame'],r['cursor']];ids=[None,None];ids[side-1]=identity;checked+=1
            try:native.check_owned_body_palette(q,actual,guest,tuple(ids),side)
            except ValueError as error:
                bank=q['bank']&0x7f00;colors=actual[bank:bank+65]
                failures.append(dict(frame=snap['frame'],arena=snap['arena'],file=snap['file'],error=str(error),
                    actualQueue=q,paletteFile=str(file),
                    exactReferenceMatches={kind:bool(np.array_equal(colors[:len(reference)],reference))for kind,reference in references.items()},
                    referenceMismatchCounts={kind:int((colors[:len(reference)]!=reference).sum())for kind,reference in references.items()},
                    actualColors=colors.tolist(),expectedColors=references['alternate'if q['body']&64 else'normal'].tolist()))
                pins[str(file.resolve())]=campaign.digest(file)
    assert campaign.digest(log)==before
    pins[str(log.resolve())]=before;pins[str((folder/'result.json').resolve())]=campaign.digest(folder/'result.json')
    for module in(campaign,native):pins[str(Path(module.__file__).resolve())]=campaign.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=campaign.digest(Path(__file__))
    return dict(diagnosticCompleted=True,candidate=result['candidate'],fighter=result['player'],humanSlot=side,
                paletteChecks=checked,actualFailures=failures,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists(),'Never overwrite evidence'
    report=inspect(args.folder);args.output.parent.mkdir(exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(diagnosticCompleted=True,paletteChecks=report['paletteChecks'],failures=len(report['actualFailures']),
        firstFailure={k:v for k,v in report['actualFailures'][0].items()if k not in('actualColors','expectedColors','actualQueue')}
        if report['actualFailures']else None),indent=2),flush=True)




