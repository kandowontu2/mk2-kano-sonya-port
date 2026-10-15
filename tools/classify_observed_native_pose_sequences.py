"""Bounded direct-reference census, not a native animation execution proof."""
import json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
RX=re.compile(r'(\w+)=([^\s]+)')
def classify(program,base,root,poses):
    def offset(address):
        assert base<=address<base+len(program)*8 and (address-base)%8==0
        return (address-base)//8
    table=struct.unpack_from('<65I',program,offset(root))
    starts=sorted({p for p in table if root<=p<root+0x20000 and p%16==0})
    result={p:[] for p in poses}
    for animation,start in enumerate(table):
        if start not in starts:continue
        following=[p for p in starts if p>start]
        end=following[0] if following else root+0x20000
        low,high=offset(start),offset(end-16)+2
        assert high-low<=16384
        words={struct.unpack_from('<I',program,at)[0] for at in range(low,high-3,2)}
        for pose in poses:
            if int(pose,16) in words:result[pose].append(animation)
    return result
def main():
    out=ROOT/'audit_observed_native_pose_sequences';assert not out.exists()
    payload_path=sync.BUILD/'roms/mk2ks/mk2ks.mdata'
    payload=payload_path.read_bytes();assert len(payload)==2097152
    stock_path=ROOT/'mk2/mk2-maincpu.bin';stock=stock_path.read_bytes();assert len(stock)<=2097152
    poses={17:set(),18:set(),3:set()}
    for boot in (608,604):
        with (ROOT/f'audit_bounded_native_owned_opaque_boot{boot}_runtime/run.log').open() as stream:
            for line in stream:
                if line.startswith('MK2_BOUNDED_SOLE_FIFO '):
                    r=dict(RX.findall(line));poses[int(r['id'])].add(r['pose'])
    roots={17:0xff000000,18:0xff020000,3:struct.unpack_from('<I',stock,0x020c2a+3*4)[0]}
    census={str(i):dict(root=f'{roots[i]:08X}',directAnimationReferences=classify(payload if i!=3 else stock,
        0xfe800000 if i!=3 else 0xff800000,roots[i],sorted(poses[i]))) for i in poses}
    report=dict(completed=True,census=census,animation0MeansStance=True,
        nativeAnimationExecutionProven=False,standingSoleParityAccepted=False,fullGoalComplete=False,
        sourceSync=sync.verify(),hashes={str(p):sync.sha(p) for p in (payload_path,stock_path,Path(__file__))})
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(census))
if __name__=='__main__':main()
