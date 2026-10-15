"""Exact original random Tomb drop branch, wait/slow fall/native flight.
Not complete stage art/audio or full stage matrix acceptance; held predicates unchanged.
"""
import json,re,hashlib
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1726_original_tomb_drop_checked'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def verify():
 pins={};folder=ROOT/'audit_v1724_sonya_tomb_p2_branch_provenance'
 def pin(p,h=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=sha(p)
  assert h is None or pins[key]==h.upper(),'Changed evidence '+key
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/source.NAME/'build-info.json').read_text())
 assert meta['exit_code']==0 and meta['candidate']==source.NAME and meta['winner']=='sonya'and meta['side']==2 and meta['arena']==1
 assert meta['assistance']=='none'and meta['guest_writes']==0 and meta['cheats_enabled']is False
 assert before==meta['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items())
 assert meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256']
 for p,h in before.items():
  pin(p,h)
  if Path(p).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(p).name,h)
 guest,_,payload=source.expected();assert (folder/'guest_maincpu.bin').read_bytes()==guest
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();off=lambda a:(a-0xff800000)//8
 for a,b in ((0xff8eaf00,0xff8eb490),(0xff80e980,0xff80ecf0),(0xff876650,0xff876b40),(0xff804000,0xff804170)):
  assert guest[off(a):off(b)]==original[off(a):off(b)],'Complete original branch/random/flight/integration instruction path unchanged'
 driver=(folder/'input_sources/mk2ks_stage_branch_provenance_v1722.lua').read_text()
 assert driver.count("dofile('mk2ks_native_stage_performer_v806.lua')")==1
 assert not re.search(r'write_u\d+|:write_|\.value\s*=(?!=)|load_?state',driver)
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 original_rows=lambda s:'\n'.join(x for x in s.splitlines()if x.startswith('MK2_STAGE_')and not x.startswith('MK2_STAGE_PROVENANCE_'))
 baseline=ROOT/'audit_v1714_sonya_tomb_p2/run.log'
 assert original_rows(log)==original_rows(baseline.read_text(encoding='utf-8-sig')),'Exact failed case reproduced without changing native input/state chronology'
 rows={}
 for tag in ('BRANCH','FIELD','MOTION'):
  rows[tag]=[dict(re.findall(r'(\w+)=([^\s]+)',x))for x in log.splitlines()if x.startswith('MK2_STAGE_PROVENANCE_'+tag+' ')]
 for r in sum(rows.values(),[]):assert r['writes']=='0'and r['assistance']=='none'and r['side']=='2'and r['winner']=='sonya'
 def branch(entry,frame):
  found=[r for r in rows['BRANCH']if r['entry']==entry and int(r['frame'])==frame]
  assert len(found)==1;return found[0]
 held=branch('FF8EB0D0',7799);actor,main=held['actor'],held['main']
 for entry in ('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0'):
  r=branch(entry,7799);assert r['a8']==actor and r['a13']==main and r['io0']=='FFFFFFFF'
 assert branch('FF80EC20',7799)['a0']=='00000032'and branch('FF8EB1A0',7799)['a0']=='00000019'
 assert not any(r['entry']=='FF8EB400'and int(r['frame'])>=7799 for r in rows['BRANCH'])
 assert int(branch('FF8EB200',7927)['frame'])-7799==128
 assert int(branch('FF8EB290',8039)['frame'])-7927==112
 init=branch('FF876650',8039)
 assert tuple(init[k]for k in('a0','a1','a2','a3','a8','a13'))==('00000000','00020000','00008000','00000FFF',actor,main)
 slow=[r for r in rows['MOTION']if r['frame']=='7927'and r['offset']=='60'and r['pc']=='FF8EB240']
 assert len(slow)==2 and [r['value']for r in slow]==['00002000','00000000']and all(r['mask']=='0000FFFF'and r['actor']==actor and r['main']==main and r['id']=='17'for r in slow)
 fields={int(r['frame']):r for r in rows['FIELD']}
 for f in range(7800,8069):
  r=fields[f];assert r['actor']==actor and r['main']==main and r['id']=='17'and r['action']=='0503'
 for f in range(7800,7928):assert (fields[f]['y'],fields[f]['vy'],fields[f]['gravity'])==('-173','00000000','00000000')
 for f in range(7928,8040):
  r=fields[f];assert r['vy']=='00002000'and r['gravity']=='00000000'and int(r['y'])==-173+(f-7928)//8
 first=fields[8040];assert first['y']=='-159'and first['vy']=='00020000'and first['gravity']=='00008000'
 lo,hi,total=0,65535,0
 for f in range(8041,8068):
  a,b=fields[f-1],fields[f];vy=int(b['vy'],16)
  assert vy==int(a['vy'],16)+0x8000 and b['gravity']=='00008000'
  total+=vy;delta=int(b['y'])+159;lo=max(lo,delta*65536-total);hi=min(hi,(delta+1)*65536-1-total);assert lo<=hi
 assert (fields[8068]['y'],fields[8068]['vy'],fields[8068]['gravity'])==('86','00000000','00000000')
 branch('FF8EB3C0',8067)
 for p in (baseline,folder/'result.json',folder/'inputs_before.json',folder/'run.log',folder/'guest_maincpu.bin',ROOT/'mk2/mk2-maincpu.bin',Path(__file__)):pin(p)
 return dict(passed=True,originalRandomTombDropCauseAccepted=True,unpressedNativeControls=True,originalRandomThreshold=50,actualRandomValue=25,
  nativeBranchFrame=7799,nativeSlowFallStart=7927,nativeFastFallStart=8039,nativeFloorLandingField=8068,
  originalHoldDelay=128,originalSlowFallDuration=112,originalSlowFallSpeed=8192,originalFastFallSpeed=131072,originalGravity=32768,
  exactBaseChronologyReproduced=True,heldPredicateChanged=False,fullStageMatrixAccepted=False,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 assert not OUT.exists();report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
