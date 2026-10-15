"""Entire actual guest ROM must differ only at the six-byte call and own stub."""
import argparse
import json
import hashlib
import struct
from pathlib import Path
from verify_pit_initial_cache_v680_v2 import WORDS,BASE
from verify_native_candidate_v680 import ROOT,NAME
from verify_native_pit_scene_v680_v1 import need,digest

def verify(folder):
    folder=Path(folder)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    hashes=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['assistance']=='none' and result['current']==NAME and
         result['old']=='diagnostic_v635_native_shadow_rows' and result['input_hashes']==hashes,'Exact terminal source/binary-controlled pair')
    inputs=dict(hashes)
    for path,sha in hashes.items():need(digest(path)==sha,'Actual capture input changed: '+path)
    old=(folder/result['old']/'guest_maincpu.bin').read_bytes()
    new=(folder/result['current']/'guest_maincpu.bin').read_bytes()
    need(len(old)==len(new)==1048576,'Complete actual guest image')
    at=(0xff85bd30-0xff800000)//8
    need(old[at:at+6]==struct.pack('<HI',0x09e0,0xff180c00),'Exact displaced original coordinate-table MOVI')
    need(new[at:at+6]==struct.pack('<HI',0x0d5f,BASE),'Exact synchronous constructor CALL')
    need(old[0xf9380:0xf9400]==b'\xff'*128,'All original initializer storage truly unused')
    code=struct.pack('<32H',*WORDS)
    need(new[0xf9380:0xf93c0]==code and new[0xf93c0:0xf9400]==b'\xff'*64,'Actual bounded native stub')
    wanted=bytearray(old);wanted[at:at+6]=struct.pack('<HI',0x0d5f,BASE);wanted[0xf9380:0xf93c0]=code
    need(new==wanted,'Every other actual guest ROM byte is unchanged')
    for name in (result['old'],result['current']):
        log=(folder/name/'run.log').read_text(encoding='utf-8-sig')
        need(log.count('MK2_PIT_ROM_CAPTURE bytes=1048576 writes=0 assistance=none')==1 and
             log.count('MK2_PIT_ROM_RESULT')==1 and '[LUA ERROR]'not in log,'Complete read-only native boot capture')
    for path in folder.rglob('*'):
        if path.is_file():inputs[str(path)]=digest(path)
    for file in (__file__,str(ROOT/'tools/verify_pit_initial_cache_v680_v2.py')):inputs[file]=digest(file)
    return dict(passed=True,guest_bytes=1048576,changed_bytes=sum(a!=b for a,b in zip(old,new)),
                allowed_regions=[dict(offset=at,length=6),dict(offset=0xf9380,length=64)],inputHashes=inputs,
                scope='Actual complete guest ROM delta confined to constructor and native preloader; not all gameplay/art/audio acceptance',fullPortAcceptance=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    need(not args.output.exists(),'Never overwrite evidence');proof=verify(args.folder)
    args.output.write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items()if k!='inputHashes'},indent=2))
