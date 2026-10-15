"""Lossless stronger Windows compression of exact generated evidence, no deletion."""
import ctypes,json,subprocess
from pathlib import Path
from ctypes import wintypes
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5150_special_shadow_progress/progress.json'
OUT=ROOT/'audit_v5152_shadow_trace_storage_progress'
def main():
 need(not OUT.exists(),'Fresh lossless evidence-storage checkpoint')
 parent=json.loads(PARENT.read_text());need(parent['goalStatus']=='active'and len(parent['remaining'])==5 and parent['everyCurrentEntryBodyPublicationProven'],'Current authoritative full-scope body/shadow proof')
 pinset=dict(parent['newInputHashes']);pinset[str(PARENT.resolve())]=sha(PARENT);pinset[str(Path(__file__).resolve())]=sha(__file__)
 need(all(sha(p)==h for p,h in pinset.items()),'Every authoritative evidence/public/source byte unchanged before compression')
 folders=[]
 for c in parent['verifiedCases']:
  move,side,air=c['move'],c['side'],c['air']
  folders.extend([ROOT/f'audit_v{5144 if air else 5134}_special_repeat_{move}_p{side}_kitana',ROOT/f'audit_v{5145 if air else 5135}_special_repeat_{move}_p{side}_kitana_observed',Path(c['proof']).parent])
 files=sorted({p.resolve()for folder in folders for p in folder.rglob('*')if p.is_file()})
 need(all(ROOT.resolve()in p.parents and any(folder.resolve()in p.parents for folder in folders)for p in files),'Exact validated generated evidence targets within their named workspace folders')
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);allocated=kernel.GetCompressedFileSizeW;allocated.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)];allocated.restype=wintypes.DWORD
 def physical(p):
  high=wintypes.DWORD();ctypes.set_last_error(0);low=allocated(str(p),ctypes.byref(high));need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual Windows physical compressed allocation');return low+(high.value<<32)
 before={str(p):dict(sha256=sha(p),logicalBytes=p.stat().st_size,allocatedBytes=physical(p))for p in files}
 commands=[]
 for folder in sorted(set(folders)):
  targets=[p for p in files if folder.resolve()in p.parents and p.suffix in('.log','.json')]
  if not targets:continue
  result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',*(str(p)for p in targets)],capture_output=True,text=True)
  need(result.returncode==0,'Actual lossless compression terminal success')
  commands.append(dict(folder=str(folder),files=len(targets),exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
 after={str(p):dict(sha256=sha(p),logicalBytes=p.stat().st_size,allocatedBytes=physical(p))for p in files}
 need(all(before[p]['sha256']==after[p]['sha256']and before[p]['logicalBytes']==after[p]['logicalBytes']and after[p]['allocatedBytes']<=before[p]['allocatedBytes']for p in before),'Every selected evidence file byte-exact; physical allocation never increased')
 need(all(sha(p)==h for p,h in pinset.items()),'All native evidence/source/public pins still exact after lossless compression')
 actual_after=sum(v['allocatedBytes']for v in after.values());actual_batch_before=sum(v['allocatedBytes']for v in before.values())
 total_reclaimed=parent['currentTraceAllocatedBytes']-actual_after;need(total_reclaimed>0,'Actual measured trace-space reduction versus prior complete inventory')
 record=dict(schema=1,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],newInputHashes=pinset,
  mergeRule='Lossless storage-only additive checkpoint. All5150body/shadow proofs and all earlier unfinished scope remain authoritative; no content/path deletion or scope contraction.',
  previousGoalTurnClassification='Progress:18 real current native cold boots,20026 owned fields,332 byte-exact prior RGB scenes,1164020 native shadow copies,567206 added-fighter copies and198 genuine semantic faults. Routine-entry body provenance and five visual-review gaps closed for these real Prison/Kitana instances.',
  thisStorageAction='Recompressed only exact current generated immutable JSON/log evidence with supported Windows LZX. All selected file content hashes/sizes and every current source/native/public proof pin remain byte-exact. No files/folders deleted or moved; compression is reversible withWindowsCOMPACT. Parent5150measured79.61MiB before one exactleg-log prototype, whose hash stayed identical and allocation fell4476928to974848bytes. Full inventory now remeasured after bulk compression.',
  currentNativeBodyShadowProof=str(PARENT),currentTraceOriginalAllocatedBytes=parent['currentTraceAllocatedBytes'],currentTraceBeforeBulkAllocatedBytes=actual_batch_before,currentTraceAllocatedBytes=actual_after,currentTraceAllocatedMiB=round(actual_after/(1024**2),2),actualAdditionalTraceBytesReclaimed=total_reclaimed,actualAdditionalTraceMiBReclaimed=round(total_reclaimed/(1024**2),2),actualFilesMeasured=len(files),fileAllocationBefore=before,fileAllocationAfter=after,compressionCommands=commands,
  priorLargeCleanupGiBReclaimed=32.49,filesDeleted=0,foldersDeleted=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,newBuilds=0,newPayloadCopies=0,allNativeSourceEvidenceAndPublicByteHashesUnchanged=True,
  nextAction=parent['nextAction'])
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact storage journal')
 (OUT/'progress.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(goalStatus='active',filesMeasured=len(files),traceAllocatedMiB=record['currentTraceAllocatedMiB'],traceMiBReclaimed=record['actualAdditionalTraceMiBReclaimed'],allHashesUnchanged=True,filesDeleted=0,remaining=record['remaining']),indent=2))
if __name__=='__main__':main()
