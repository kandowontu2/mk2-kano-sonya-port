"""Bounded read-only inventory; not a repeat recursive physical-size census."""
import hashlib
import json
import subprocess
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
out=root/'audit_current_storage_classification_20261015'
assert not out.exists()
def run(args):return subprocess.run(args,cwd=root,capture_output=True,text=True,check=True,timeout=30).stdout
census=json.loads((root/'audit_cleanup_candidate_census_20261015/report.json').read_text())
worktrees=run(['git','-C','mame-mkp','worktree','list','--porcelain'])
objects=run(['git','-C','mame-mkp','count-objects','-v'])
exes=run(['rg','--files','-g','*.exe','-g','*.pdb','-g','*.sym','-g','!mame-mkp/3rdparty/**']).splitlines()
games=[p for p in exes if p.lower().endswith('mkport_candidate.exe')]
assert games==['diagnostic_native_selector_layers_long\\mkport_candidate.exe']
assert worktrees.count('worktree ')==1
processes=run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe' OR Name='python.exe' OR Name='pythonw.exe'\" | Select-Object ProcessId,Name,WorkingSetSize,ExecutablePath) | ConvertTo-Json -Compress"])
# This audit's own short-lived Python process is expected, not a background collector.
process_rows=json.loads(processes) if processes.strip() else []
if isinstance(process_rows,dict):process_rows=[process_rows]
classes=[
 dict(group='mame-mkp',classification='required source and reconstruction toolchain',note='OneGitcheckout/currentdirtysource plus pinned245854350Bpack. No looseobjects/garbage. UtilityEXEs and source thirdparty data not obsolete game builds.'),
 dict(group='diagnostic_native_selector_layers_long',classification='required current playable and compiledsource provenance',note='Only surviving mkport_candidate.exe game build; preserve.'),
 dict(group='roms,mk,mk2,mk3,original zips/generated assets',classification='required original data/current reconstruction',note='Only exact three reviewed duplicate stockROMs deleted; other oldfoldercontents not automatically interchangeable.'),
 dict(group='accepted audit directories and tools',classification='required finite proof/reconstruction unless individually superseded and unpinned',note='Historicalcompressedending pixels/waveforms support currentcomponentclosure; not disposable merely because old. SmallnativeauditprobeEXEs are not oldMAMEbuilds.'),
 dict(group='release_current_native_playtest_20261013_complete_roms and release_v5986_current_playtest',classification='pinned currentcheckpoint and historical reconstruction',note='Keep until finalpackage dependencyreview. Oldincomplete39MiBZIP is knownobsolete/incomplete but prior deletionpolicy blocked; no bypass.'),
 dict(group='snap',classification='unresolved exploratory candidate, not qualified for removal',allocatedBytesAtCensus=252686068,note='Mixed exploratory subfolders (cage_hud,fuzz,hybrid,oldmk2tests). Needs exact reconstruction/proofreference review before deletion. No claim all252MB required or safe.'),
 dict(group='obj_dump2 and native_kano_knife exploratory snapshots',classification='reviewed obsolete files deleted',note='2592allowlistedPNG removed; parentLua/cfg/NVRAM/originalassetinputs retained.'),
 dict(group='remaining release_v1863/oldromdirectories/searchaudits',classification='not automatically qualified',note='Topgroup age/naming alone does not prove redundancy; exactreference/dependency review remains possible, not new duplicatebuild evidence.')]
refs=['audit_cleanup_candidate_census_20261015/report.json','audit_cleanup_rom_duplicate_review_20261015/report.json','audit_cleanup_rom_duplicate_review_20261015/deletion_receipt.txt','audit_obsolete_capture_target_review_20261015/deletion_plan.json','audit_obsolete_capture_target_review_20261015/deletion_receipt.json']
report=dict(readOnly=True,originalCensus=dict(allocatedBytes=census['uniqueAllocatedBytes'],logicalBytes=census['logicalBytes'],files=census['files']),
 executedRemovedAllocatedBytes=191583987,arithmeticBaselineAfterThoseRemovals=5327960810,
 arithmeticIsNotFreshCensus=True,note='Newboundedlogs/scripts/packagebytes and metadata mean arithmeticbaseline is not currentphysicalsize; no re-census here.',
 groups=classes,worktrees=worktrees,gitObjects=objects,gameExecutables=games,otherExecutableInventory=[x for x in exes if x not in games],
 processObservation=process_rows,ownAuditPythonExpected=True,noEmulatorObserved=not any(x['Name']=='mkport_candidate.exe' for x in process_rows),
 proofPins={p:hashlib.sha256((root/p).read_bytes()).hexdigest().upper() for p in refs},
 newDeletions=0,newEmulators=0,wholeWorkspaceCleanClaim=False,
 nextAction='After matchingpackage is finalized, root can perform final allocated-size census. Remaining root snap/exploratory data needs exactdependencyreview if further cleanup sought; do not delete unique originalsource or acceptedproof by age.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(out)
