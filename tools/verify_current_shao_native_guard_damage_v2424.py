"""Original Shao descriptor/block route and appended-ID damage callbacks.
Stock blocked damage values are compatible with the observed guard losses;
pose correlations alone do not identify which descriptor executed at each hit.
No original game balance, guest state or captured evidence is changed.
"""
import json,struct,argparse
from pathlib import Path
import verify_current_shao_opening_guard_boss_ledger_v2400 as ledger
ROOT=ledger.ROOT;launch=ledger.launch

def verify():
 pins={};path=ROOT/'audit_v2409_current_shao_opening_damage_states/report.json'
 report=json.loads(path.read_text())
 assert report['passed'] and not report['fullPortAcceptance'] and not report['gameOrCaptureModified']
 for file,wanted in report['inputHashes'].items():
  assert launch.sha(file)==wanted,'Unchanged actual graph '+file
  pins[file]=wanted
 pins[str(path)]=launch.sha(path)
 original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes()
 guest=ledger.native.current_source.expected()[0]
 def data(raw,a,b):return raw[(a-0xff800000)//8:(b-0xff800000)//8]
 def u32(raw,a):return struct.unpack_from('<I',raw,(a-0xff800000)//8)[0]
 ranges=((0xff837900,0xff837d00),(0xff835dc0,0xff836240),(0xff8364c0,0xff836730))
 for a,b in ranges:
  assert data(guest,a,b)==data(original,a,b),'Original guard test/blocked damage/collision store route unchanged'
 assert struct.unpack('<5H',data(original,0xff836040,0xff836090))==(0x4cea,0x270a,0x2d0a,0xa30f,0xb7a8)
 assert struct.unpack('<5H',data(original,0xff837960,0xff8379b0))==(0x0b41,0xf8ff,0xca20,0x0b41,0xf8fe)
 damage_table=u32(guest,0xff836750)
 assert data(guest,damage_table,damage_table+17*32)==data(original,0xff8367b0,0xff8367b0+17*32)
 assert u32(guest,damage_table+17*32)==u32(guest,damage_table+18*32)==0
 outer=u32(guest,0xff8eba30);row=u32(original,0xff8eba90+13*32)
 assert u32(guest,outer+13*32)==row
 assert data(guest,row,row+5*32)==data(original,row,row+5*32)
 descriptors=[]
 for index in range(5):
  address=u32(original,row+index*32)
  assert data(guest,address,address+144)==data(original,address,address+144)
  words=struct.unpack('<9H',data(original,address,address+144))
  descriptors.append(dict(index=index,address=address,words=words,
   originalFullDamage=words[5]>>8,originalBlockedDamage=words[5]&255))
 assert [r['originalBlockedDamage']for r in descriptors]==[16,18,18,18,8]
 cases={}
 for case,(_,_,capture,_)in ledger.CASES.items():
  assert (ROOT/capture/'guest_maincpu.bin').read_bytes()==guest,'Actual initialized guest exactly reconstructed'
  incoming=report['cases'][case]['incoming'];guard=[r for r in incoming if r['actionAtOwnDamage']in(0x700,0x701)]
  assert guard and all(r['physicalBlockHeld']for r in guard)
  cases[case]=dict(actualGuardDamageStores=len(guard),actualGuardDamage=sum(r['damage']for r in guard),
   actualGuard18HPStores=sum(r['damage']==18 for r in guard),
   noAdditionalIncomingDamageScalerForTrueIDs17And18=True,
   scope='Actual native guard action and physical Block; not a per-hit descriptor attribution or complete combat balance acceptance')
 pins[str(original_path)]=launch.sha(original_path);pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 launch.module_pins(pins)
 return dict(passed=True,originalGuardAndBlockedDamageRouteUnchanged=True,
  originalShaoDescriptors=descriptors,trueIDs17And18IncomingDamageCallbackNull=True,
  cases=cases,inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 assert not a.output.exists(),'Immutable native guard damage proof'
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','originalShaoDescriptors')},indent=2),flush=True)
