"""Correct a checkpoint metadata count without altering executed evidence."""
import json,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5062_normal_subzero_freeze_progress/progress.json'
OUT=ROOT/'audit_v5064_normal_subzero_freeze_progress'

def main():
 need(not OUT.exists(),'Fresh additive counter correction')
 p=json.loads(PARENT.read_text());need(p['goalStatus']=='active'and len(p['remaining'])==5,'Entire original scope retained')
 cases=[ROOT/f'audit_v5046_normal_subzero_{f}_p{s}'for f,s in [('kano',1),('kano',2),('sonya',1),('sonya',2),('kitana',1),('liu_kang',2)]]
 cases.append(ROOT/'audit_v5054_normal_subzero_sonya_p1')
 for folder in cases:
  r=json.loads((folder/'result.json').read_text());proof=json.loads((folder/'guest_memory_proof.json').read_text())
  need(r['nativeExit']==0 and proof['sha256']==native.GUEST_SHA and proof['everyActualByteComparedInRAM'],
       'Actual cold boot guest proof and terminal process evidence')
 need(len(cases)==7,'Six matrix cold boots and one exact SonyaP1 repeated review')
 pins=p['newInputHashes'];pins[str(PARENT)]=sha(PARENT);pins[str(Path(__file__).resolve())]=sha(__file__)
 need(all(sha(path)==digest for path,digest in pins.items()),'Original sources/evidence/public inputs unchanged')
 p.update(parentAdditiveJournals=p['parentAdditiveJournals']+[str(PARENT)],newInputHashes=pins,
  nativeColdBootInstancesThisContinuation=7,successfulNativeColdBootFoldersThisContinuation=[str(f)for f in cases],
  priorFailedCollectorColdBootsRevalidated=4,
  checkpointMetadataCorrection='5062 mistakenly reported8 new boots. Actual process/result/cold guest proofs show six matrix boots5046 plus one repeated SonyaP1 review5054 =7. The older four5040 failure instances and initial5034 transport are existing revalidated evidence, not new successful boots. Corrected additively; source/evidence unchanged and no gameplay/acceptance change.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact checkpoint')
 (OUT/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
 print(json.dumps(dict(passed=True,path=str(OUT/'progress.json'),goalStatus='active',newNativeColdBoots=7,fullPortAcceptance=False),indent=2))

if __name__=='__main__':main()
