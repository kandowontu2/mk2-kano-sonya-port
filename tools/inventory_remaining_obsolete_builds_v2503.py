"""Read-only exact remaining build inventory against current complete dependency frontiers."""
import argparse,ctypes,json,ntpath
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
FRONTIERS=('audit_v2460_current_native_crouch_jump_checkpoint/checkpoint.json',
 'audit_v2472_current_shao_crouch_exit_progress/report.json',
 'audit_v2481_current_sonya_crouch_exit_extended_boundary/report.json',
 'audit_v2490_next_old_build_solid_recovery_checked/report.json',
 'audit_v2493_current_shao_crouch_exit_exposure/report.json')
def need(ok,label):
 if not ok:raise ValueError(label)
def inventory():
 normalized=ntpath.normcase(ntpath.normpath(str(ROOT)))+'\\';protected=set();pins={};key_count=0
 for name in FRONTIERS:
  path=ROOT/name;report=json.loads(path.read_text());need(report.get('passed',report.get('goalStatus')=='active'),'Actual accepted/current frontier')
  pins[str(path)]=launch.sha(path)
  for file in report['inputHashes']:
   key_count+=1;key=ntpath.normcase(ntpath.normpath(file))
   if key.startswith(normalized):protected.add(key[len(normalized):].split('\\')[0])
 for name in('audit_v2497_current_kano_p1_shao_duck_wait_campaign','audit_v2497_current_sonya_p1_shao_duck_wait_campaign'):
  path=ROOT/name/'input_hashes_before.json';record=json.loads(path.read_text(encoding='utf-8-sig'));pins[str(path)]=launch.sha(path)
  for file in record:
   key_count+=1;key=ntpath.normcase(ntpath.normpath(file))
   if key.startswith(normalized):protected.add(key[len(normalized):].split('\\')[0])
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);size=kernel.GetCompressedFileSizeW
 size.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));size.restype=ctypes.c_uint32
 def allocated(path):
  high=ctypes.c_uint32();ctypes.set_last_error(0);low=size(str(path),ctypes.byref(high));need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual allocation available');return(high.value<<32)|low
 candidates=[];kept=[]
 for folder in sorted(ROOT.iterdir()):
  if not folder.is_dir()or not folder.name.startswith('diagnostic_v')or not(folder/'mkport_candidate.exe').is_file():continue
  if folder.name.casefold()in protected or folder.name=='diagnostic_v1836_ball_register_boundary':kept.append(folder.name);continue
  need(folder.resolve().parent==ROOT.resolve()and not folder.stat().st_file_attributes&0x400,'Exact non-reparse old build inside workspace')
  files=0;directories=1;logical=allocation=0
  for path in folder.rglob('*'):
   meta=path.stat();need(not meta.st_file_attributes&0x400,'No reparse point anywhere in old build inventory')
   if path.is_dir():directories+=1
   elif path.is_file():files+=1;logical+=meta.st_size;allocation+=allocated(path)
   else:raise ValueError('Nonregular old build entry')
  candidates.append(dict(name=folder.name,files=files,directories=directories,logicalBytes=logical,allocatedBytes=allocation,
   executableSHA256=launch.sha(folder/'mkport_candidate.exe'),buildInfoSHA256=launch.sha(folder/'build-info.json')if(folder/'build-info.json').is_file()else None))
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,readOnly=True,filesDeleted=False,dependencyReferencesExamined=key_count,
  dependencyFrontiers=[str(ROOT/n)for n in FRONTIERS],protectedBuildFolders=kept,
  remainingUnreferencedBuildFolders=candidates,remainingUnreferencedCount=len(candidates),
  unreferencedLogicalBytes=sum(r['logicalBytes']for r in candidates),unreferencedAllocatedBytes=sum(r['allocatedBytes']for r in candidates),
  allOldBuildFoldersRemoved=False,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable read-only inventory')
 r=inventory();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','remainingUnreferencedBuildFolders')},indent=2),flush=True)
