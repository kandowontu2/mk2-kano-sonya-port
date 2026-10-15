"""Read-only exact graphics-source mismatch triage, not acceptance or asset edits."""
import argparse,json,re,struct
from pathlib import Path
import verify_native_arena_geometry_v1583 as arena

def inspect(folder):
    pins={};arena.campaign.matched(folder,pins)
    log=folder/'run.log';before=arena.campaign.digest(log)
    guest,_,payload=arena.native.grab.expected_guest()
    image=bytearray(arena.native.graphics_model.graphics(pins))
    for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        assert payload[header:header+4]==magic
        first,count,destination=struct.unpack_from('<III',payload,header+4)
        assert first==source and destination==dest and count>0
        image[dest:dest+count]=payload[source:source+count]
    checked=0;failures=[]
    with log.open(encoding='utf-8-sig')as stream:
        for line in stream:
            if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_GFX '):continue
            fields=dict(re.findall(r'(\w+)=([^\s]+)',line))
            raw=bytes.fromhex(fields['data']);first=int(fields['first']);count=int(fields['bytes']);checked+=1
            assert len(raw)==count and 0<=first<first+count<=len(image)
            expected=image[first:first+count]
            if raw!=expected:
                differences=[i for i,(a,b)in enumerate(zip(raw,expected))if a!=b]
                failures.append(dict(frame=int(fields['frame']),key=fields['key'],offset=fields['offset'],
                    first=first,bytes=count,mismatchBytes=len(differences),
                    firstDifferences=[dict(address=first+i,actual=raw[i],expected=expected[i])for i in differences[:20]],
                    firstMismatch=first+differences[0],lastMismatch=first+differences[-1]))
    assert arena.campaign.digest(log)==before
    pins[str(log.resolve())]=before;pins[str((folder/'result.json').resolve())]=arena.campaign.digest(folder/'result.json')
    for module in(arena,arena.native.graphics_model):pins[str(Path(module.__file__).resolve())]=arena.campaign.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=arena.campaign.digest(Path(__file__))
    return dict(diagnosticCompleted=True,graphicsStreamsChecked=checked,graphicsSourceFailures=failures,
                capturesAndGameUnchanged=True,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists(),'Never overwrite evidence'
    report=inspect(args.folder);args.output.parent.mkdir(exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
