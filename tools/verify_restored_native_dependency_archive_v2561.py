"""Independently compare only required restored files against original archive bytes."""
import argparse,hashlib,json,tarfile
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT

def need(ok,label):
 if not ok:raise ValueError(label)

def check_manifest(rows,expected):
 need(len(rows)==14 and {r['path']:r['sha256']for r in rows}==expected,'Complete exact required-dependency manifest; no omissions or changed hashes')

def verify():
 recovery_path=ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json'
 compression_path=ROOT/'audit_v2554_restored_native_dependencies_compressed/report.json'
 original_path=ROOT/'audit_v2518_remaining_old_build_recovery/report.json'
 recovered=json.loads(recovery_path.read_text());compressed=json.loads(compression_path.read_text());original=json.loads(original_path.read_text())
 need(recovered['passed']and compressed['passed']and original['passed'],'Actual recovery, original preservation and compression proofs')
 archive=Path(original['recoveryArchive']);need(launch.sha(archive)==original['recoveryArchiveSHA256']=='862D2C925B09D19A09A8F23E088D6CBA2A34777C8209064F772E8E8C5AF559E7','Unchanged complete archive')
 records={r['path']:r for r in original['inventory']};targets={}
 for r in recovered['restoredRequiredFiles']:
  p=Path(r['path']).resolve();need(p.is_relative_to(ROOT.resolve())and not p.stat().st_file_attributes&0x400,'Exact regular restored path inside named root')
  relative=p.relative_to(ROOT).as_posix();need(relative in records and r['sha256']==records[relative]['sha256']and r['bytes']==records[relative]['bytes'],'Every restored file matches original pre-cleanup provenance')
  need(launch.sha(p)==r['sha256'],'Actual restored file unchanged');targets[relative]=r
 expected={r['path']:r['sha256']for r in targets.values()};check_manifest(list(targets.values()),expected)
 mutations=[list(targets.values())[:-1],[dict(r)for r in targets.values()]];mutations[1][0]['sha256']='0'*64
 rejected=[]
 for label,changed in zip(('omitted_required_dependency','changed_required_dependency_hash'),mutations):
  try:check_manifest(changed,expected)
  except ValueError as error:need('Complete exact required-dependency manifest'in str(error),'Specific protection rejection');rejected.append(label)
  else:raise ValueError('Malformed required-dependency protection accepted')
 seen=set();total=0
 with tarfile.open(archive,'r|xz')as packed:
  for member in packed:
   if member.name not in targets:continue
   need(member.isfile()and not member.islnk()and not member.issym()and member.name not in seen,'One exact regular original member')
   record=targets[member.name];digest=hashlib.sha256();count=0
   with packed.extractfile(member)as old,Path(record['path']).open('rb')as restored:
    for chunk in iter(lambda:old.read(1024*1024),b''):
     need(restored.read(len(chunk))==chunk,'Every restored byte equals actual original archived byte');digest.update(chunk);count+=len(chunk)
    need(not restored.read(1),'No extra restored bytes')
   need(count==member.size==record['bytes']and digest.hexdigest().upper()==record['sha256'],'Every original file length/SHA independently verified')
   total+=count;seen.add(member.name)
   if seen==set(targets):break
 need(seen==set(targets),'All fourteen exact dependencies directly compared to archive')
 folders={r.split('/')[0]for r in targets};actual=set()
 for folder in folders:
  for p in(ROOT/folder).rglob('*'):
   need(not p.stat().st_file_attributes&0x400,'No reparse in restored historical leaves')
   if p.is_file():actual.add(p.relative_to(ROOT).as_posix())
 need(len(folders)==8 and actual==set(targets),'Only fourteen required files restored across eight partial leaves; no entire old builds or extras')
 guest,old,payload=launch.current.expected()
 need(guest==(ROOT/'audit_v2515_current_sonya_p1_shao_duck_wait_campaign/guest_maincpu.bin').read_bytes(),'Whole current guest reconstructed with restored historical provenance')
 need(payload==(ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata').read_bytes(),'Whole current payload independently reconstructed')
 pins={}
 for proof_path,proof in((recovery_path,recovered),(compression_path,compressed)):
  for file,wanted in proof['inputHashes'].items():need(launch.sha(file)==wanted,'Current game/settings/required sources/archive unchanged');pins[file]=wanted
  pins[str(proof_path)]=launch.sha(proof_path)
 for p in(original_path,archive,Path(__file__).resolve()):pins[str(p)]=launch.sha(p)
 launch.module_pins(pins)
 return dict(passed=True,independentlyComparedFiles=len(seen),requiredPartialHistoricalFolders=len(folders),exactOriginalBytesCompared=total,
  rejectedSpecificProtectionCounterexamples=rejected,onlyRequiredFilesRestored=True,wholeGuestAndPayloadReconstructed=True,currentGameSettingsAndArchiveUnchanged=True,
  originalCleanupUnreferencedClaimSuperseded=True,allOldBuildFoldersRemoved=False,inputHashes=pins,gameChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable independent restoration proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
