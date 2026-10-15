"""Repair only semantic headed-reaction references; no art/palette/code edits.

Original MKII primary55 loops precisely the first five primary35 body groups.
The old import defaulted to numerically equal MK3 primary55 projectiles. Reuse
each owned block's actual semantic primary35 groups, preserving the native
primary55 script address, loop and every other byte. Include all six normal,
paired-grab/bicycle and effect blocks so native state handoffs stay consistent.
"""
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1217_native_headed_reaction_encoding';assert not OUT.exists()
OLD=ROOT/'diagnostic_v1130_owned_split_invariant_blood/roms/mk2ks/mk2ks.mdata'
ORIGINAL=ROOT/'mk2/mk2-maincpu.bin'
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
assert digest(OLD)=='F95E8D42B982300F7C317CCDA96F0CAD61B50288861A097C618FFD8442F8617C'
assert digest(ORIGINAL)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
old=OLD.read_bytes();original=ORIGINAL.read_bytes();payload=bytearray(old)
u=lambda data,at:struct.unpack_from('<I',data,at)[0]
native_off=lambda address:(address-0xff800000)//8
payload_off=lambda address:(address-0xfe800000)//8
root=native_off(0xff91fc60)
stumble=native_off(u(original,root+35*4));headed=native_off(u(original,root+55*4))
assert original[stumble:stumble+20]==original[headed:headed+20]
assert u(original,stumble+20)==0 and u(original,headed+20)==1 and u(original,headed+24)==u(original,root+55*4)
blocks={'kano':0x100000,'sonya':0x104000,'kano_grab':0x108000,
        'sonya_bicycle':0x10c000,'kano_effect':0x110000,'sonya_effect':0x114000}
changes=[];allowed=set();records={}
for name,base in blocks.items():
 source=payload_off(u(old,base+35*4));target=payload_off(u(old,base+55*4))
 assert base<=source<base+0x4000 and base<=target<base+0x4000
 assert [i for i in range(65) if u(old,base+i*4)==u(old,base+55*4)]==[55]
 assert u(old,source+20)==0 and u(old,target+20)==1 and u(old,target+24)==u(old,base+55*4)
 before=[u(old,target+i*4) for i in range(5)]
 after=[u(old,source+i*4) for i in range(5)]
 assert all(base<=payload_off(ptr)<base+0x4000 for ptr in before+after)
 assert len(set(after))==5 and before!=after
 for index,pointer in enumerate(after):
  at=target+index*4;struct.pack_into('<I',payload,at,pointer);allowed.update(range(at,at+4))
  changes.append(dict(block=name,at=at,old=before[index],new=pointer))
 records[name]=dict(base=base,primary35=source,primary55=target,oldGroups=before,headedBodyGroups=after)
changed=[i for i,(a,b) in enumerate(zip(old,payload)) if a!=b]
assert changed and set(changed)<=allowed and len(payload)==len(old)
assert all(payload[i]==old[i] for i in range(len(old)) if i not in allowed)
folder=OUT/'roms/mk2ks';folder.mkdir(parents=True)
path=folder/'mk2ks.mdata';path.write_bytes(payload)
report=dict(passed=True,inputHashes={str(OLD):digest(OLD),str(ORIGINAL):digest(ORIGINAL),str(Path(__file__).resolve()):digest(__file__)},
 oldPayloadSHA256=digest(OLD),payloadSHA256=digest(path),blocks=records,pointerChanges=changes,
 actualChangedByteOffsets=changed,originalHeadedEqualsStumbleFiveGroups=True,
 allOtherPayloadBytesUnchanged=True,allProjectileDescriptorsAndPathsUnchanged=True,
 allGraphicsAndPalettesUnchanged=True,originalFivePoseAndLoopGrammarUnchanged=True,
 guestCodeChanged=False,fullPortAccepted=False,runtimeVerificationPending=True)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print('Encoded',len(changes),'headed body references in six owned blocks;',len(changed),'bytes changed; runtime verification pending',flush=True)
