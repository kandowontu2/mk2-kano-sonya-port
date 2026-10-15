"""Independent reconstruction of the headed-reaction-only payload change.

Do not import the encoder as expected output. Derive the original MKII
primary35/55 equality and loop grammar from immutable ROM, then substitute
each independently reconstructed owned block's existing primary35 references.
No image, palette, projectile, instruction or other script byte may change.
"""
import hashlib,json,struct
from pathlib import Path
import verify_native_split_blood_v1133 as prior
ROOT=prior.ROOT;CANDIDATE='diagnostic_v1219_owned_native_headed_reaction'
OUT=ROOT/'audit_v1221_native_headed_reaction_encoding_checked'

def reconstruct():
 guest,graphics,assets,old=prior.reconstruct()
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 original_root=(0xff91fc60-0xff800000)//8
 read=lambda data,at:struct.unpack_from('<I',data,at)[0]
 source=(read(original,original_root+140)-0xff800000)//8
 loop=(read(original,original_root+220)-0xff800000)//8
 assert original[source:source+20]==original[loop:loop+20]
 assert read(original,source+20)==0 and read(original,loop+20)==1 and read(original,loop+24)==read(original,original_root+220)
 expected=bytearray(old);changed_fields=[]
 for fighter_index in range(6):
  base=0x100000+fighter_index*0x4000
  stumble=(read(old,base+140)-0xfe800000)//8
  impale=(read(old,base+220)-0xfe800000)//8
  assert base<=stumble<base+0x4000 and base<=impale<base+0x4000
  assert read(old,stumble+20)==0 and read(old,impale+20)==1 and read(old,impale+24)==read(old,base+220)
  assert sum(read(old,base+i*4)==read(old,base+220) for i in range(65))==1
  expected[impale:impale+20]=old[stumble:stumble+20]
  changed_fields.append((impale,stumble))
 actual=(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
 assert actual==expected,'Whole payload differs from independent native semantics reconstruction'
 assert len([i for i,(a,b) in enumerate(zip(old,actual)) if a!=b])==57,'Exact actual bounded reference-only diff'
 # The original projectile/effect references and descriptors are outside
 # the six exclusively primary55 script heads, and remain byte-exact.
 allowed={i for at,_ in changed_fields for i in range(at,at+20)}
 assert all(a==b for i,(a,b) in enumerate(zip(old,actual)) if i not in allowed)
 return guest,graphics,assets,actual

if __name__=='__main__':
 assert not OUT.exists()
 guest,graphics,assets,payload=reconstruct()
 build=json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'));pins={}
 def pin(path,wanted=None):
  path=Path(path);actual=hashlib.sha256(path.read_bytes()).hexdigest().upper();assert wanted is None or wanted==actual;pins[str(path)]=actual
 for file,wanted in build['input_hashes'].items():pin(file,wanted)
 pin(ROOT/CANDIDATE/'mkport_candidate.exe',build['executable_sha256'])
 pin(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
 pin(ROOT/CANDIDATE/'build-info.json');pin(ROOT/'mk2/mk2-maincpu.bin');pin(Path(__file__))
 report=dict(passed=True,candidate=CANDIDATE,payloadSHA256=build['payload_sha256'],
  wholePayloadIndependentlyReconstructed=True,actualChangedBytes=57,
  allOtherPayloadBytesUnchanged=True,allProjectileAssetsAndPathsUnchanged=True,
  originalHeadedReactionGrammarPreserved=True,gameInstructionsChanged=False,
  sourceExecutableReused=True,inputHashes=pins,runtimeAppearanceAccepted=False,fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Whole corrected payload independently reconstructed; exactly 57 reference bytes changed; runtime appearance not asserted',flush=True)
