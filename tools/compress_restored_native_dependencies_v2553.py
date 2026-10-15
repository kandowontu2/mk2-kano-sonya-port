"""Losslessly compress only the fourteen exact freshly restored verification files."""
import argparse,json,subprocess
from pathlib import Path
import recover_dynamic_native_source_dependencies_v2547 as recovery
ROOT=recovery.ROOT

def verify():
 source=ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json'
 r=json.loads(source.read_text());recovery.need(r['passed']and r['restoredFiles']==14,'Actual accepted exact recovery')
 pins=dict(r['inputHashes']);rows=[]
 for record in r['restoredRequiredFiles']:
  p=Path(record['path']).resolve()
  recovery.need(p.is_relative_to(ROOT.resolve())and p!=ROOT.resolve()and p.is_file()and not p.stat().st_file_attributes&0x400,'Exact regular recovery file inside named workspace')
  recovery.need(recovery.sha(p)==record['sha256']and p.stat().st_nlink==1,'Unchanged newly restored file; no shared hardlinks')
  before=recovery.allocated(p)
  result=subprocess.run(['compact.exe','/C','/I','/Q',str(p)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
  recovery.need(result.returncode==0 and recovery.sha(p)==record['sha256'],'Lossless native compression; every file byte preserved')
  rows.append(dict(path=str(p),sha256=record['sha256'],beforeAllocatedBytes=before,afterAllocatedBytes=recovery.allocated(p)))
 for p,h in pins.items():recovery.need(recovery.sha(p)==h,'All recovery/current-game/source pins unchanged')
 pins[str(source)]=recovery.sha(source);pins[str(Path(__file__).resolve())]=recovery.sha(__file__);recovery.launch.module_pins(pins)
 before=sum(r['beforeAllocatedBytes']for r in rows);after=sum(r['afterAllocatedBytes']for r in rows)
 original=json.loads((ROOT/'audit_v2525_remaining_old_build_cleanup_checked/report.json').read_text())
 return dict(passed=True,files=rows,filesCompressed=len(rows),beforeAllocatedBytes=before,afterAllocatedBytes=after,
  additionalAllocatedSavings=before-after,remaining68BuildCleanupNetSavingsAfterRequiredRecovery=original['netAllocatedSavings']-after,
  originalCleanupUnreferencedClaimSuperseded=True,allOldBuildFoldersRemoved=False,currentGameAndSettingsUnchanged=True,
  inputHashes=pins,gameChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();recovery.need(not a.output.exists(),'Immutable compression report')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','files')},indent=2),flush=True)
