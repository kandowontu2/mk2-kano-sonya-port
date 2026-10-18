"""Check actual donor credit strings; no internet or emulator modifications."""
import hashlib
import json
from pathlib import Path
import zipfile
PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]
with zipfile.ZipFile(ROOT/'mk3.zip') as archive:
    program=bytearray(1048576)
    program[::2]=archive.read('mk321u54.bin');program[1::2]=archive.read('mk321u63.bin')
digest=hashlib.sha256(program).hexdigest().upper()
assert digest=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
records=[]
for actor,credit in (('kano',b'RICHARD DIVIZIO\\nAS\\nKANO AND KABAL\0'),
                     ('sonya',b'KERRI HOSKINS\\nAS\\nSONYA\0')):
    assert program.count(credit)==1
    records.append(dict(actor=actor,fileOffset=program.index(credit),donorCredit=credit[:-1].decode('ascii')))
report=dict(donorProgramSHA256=digest,credits=records,ownCastRuntimeVerified=False,releaseReady=False)
(PORT/'DONOR_CAST_CREDIT_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
