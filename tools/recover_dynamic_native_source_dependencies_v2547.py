"""Restore only dynamically required immutable files from exact checked recovery.
Never overwrite existing files; never remove files; never change game/test code.
The old cleanup assertion 'unreferenced' omitted dynamically read dependencies.
"""
import argparse,ctypes,hashlib,json,subprocess,tarfile
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREP=ROOT/'audit_v2518_remaining_old_build_recovery/report.json'
ARCHIVE=ROOT/'audit_v2518_remaining_old_build_recovery/remaining_68_builds_complete_recovery.tar.xz'
EXPECTED_ARCHIVE='862D2C925B09D19A09A8F23E088D6CBA2A34777C8209064F772E8E8C5AF559E7'

def need(ok,label):
 if not ok:raise ValueError(label)

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb')as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest().upper()

def allocated(path):
 fn=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 fn.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));fn.restype=ctypes.c_uint32
 hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=fn(str(path),ctypes.byref(hi))
 need(lo!=0xffffffff or ctypes.get_last_error()==0,'Real restored allocation')
 return(hi.value<<32)|lo

def verify():
 need(sha(ARCHIVE)==EXPECTED_ARCHIVE,'Unchanged exact complete recovery archive')
 prep=json.loads(PREP.read_text());need(prep['passed']and prep['recoveryArchiveSHA256']==EXPECTED_ARCHIVE,'Authoritative original preservation manifest')
 records={r['path']:r for r in prep['inventory']};cache={};seen=set();cache_bytes=0
 with tarfile.open(ARCHIVE,'r|xz')as packed:
  for item in packed:
   if item.isdir():continue
   need(item.isfile()and not item.issym()and not item.islnk()and item.name in records,'Exact original regular member')
   need(item.name not in seen,'Unique recovery member');seen.add(item.name);record=records[item.name]
   keep=item.size<8*1024*1024 or item.name in('diagnostic_v1110_owned_native_split/mkport_candidate.exe','diagnostic_v1130_owned_split_invariant_blood/mkport_candidate.exe')
   digest=hashlib.sha256();parts=[];count=0
   with packed.extractfile(item)as f:
    for block in iter(lambda:f.read(1024*1024),b''):
     digest.update(block);count+=len(block)
     if keep:parts.append(block)
   need(count==item.size==record['bytes']and digest.hexdigest().upper()==record['sha256'],'Original recovery member full-byte hash '+item.name)
   if keep:cache[item.name]=b''.join(parts);cache_bytes+=item.size
 need(seen==set(records),'Every original file independently read; no missing or added members')
 need(cache_bytes<768*1024*1024,'Bounded temporary in-memory recovery cache')
 print('Archive verified; temporary cache='+str(cache_bytes)+' bytes. Restoring only actual missing read dependencies.',flush=True)
 game=ROOT/'diagnostic_v1836_ball_register_boundary';tracked=[game/'mkport_candidate.exe',game/'roms/mk2ks/mk2ks.mdata',game/'build-info.json',ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd']
 tracked+=list((game/'play').glob('cfg/*'))+list((game/'play').glob('nvram/mk2ks/*'))
 before={str(p):sha(p)for p in tracked if p.is_file()};restored=[];reads=set()
 real_open=Path.open
 def recording_open(path,*args,**kwargs):
  mode=args[0]if args else kwargs.get('mode','r')
  if 'r'in mode:reads.add(str(path.resolve()))
  return real_open(path,*args,**kwargs)
 def recover(missing):
  target=Path(missing).resolve();need(target.is_relative_to(ROOT.resolve()),'Missing dependency inside named workspace')
  relative=target.relative_to(ROOT.resolve()).as_posix();need(relative in records,'Only exact original archived dependency may be restored '+relative)
  need(not target.exists(),'Never overwrite a current file')
  for parent in target.parents:
   if parent==ROOT.resolve():break
   if parent.exists():need(parent.is_dir()and not parent.stat().st_file_attributes&0x400,'No reparse ancestor in recovery target')
  data=cache.get(relative)
  if data is None:
   with tarfile.open(ARCHIVE,'r|xz')as packed:
    for item in packed:
     if item.name==relative:
      need(item.isfile()and not item.islnk()and not item.issym(),'Exact regular dependency');data=packed.extractfile(item).read();break
  need(data is not None and len(data)==records[relative]['bytes']and hashlib.sha256(data).hexdigest().upper()==records[relative]['sha256'],'Exact recovered bytes before restore')
  target.parent.mkdir(parents=True,exist_ok=True)
  folder=ROOT/relative.split('/')[0]
  compressed=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
  need(compressed.returncode==0,'Compress only recovered historical dependency leaf')
  with real_open(target,'xb')as f:f.write(data)
  need(sha(target)==records[relative]['sha256'],'Restored dependency full SHA verified')
  restored.append(dict(path=str(target),sha256=sha(target),bytes=target.stat().st_size,allocatedBytes=allocated(target)))
  print('Recovered required dependency '+relative,flush=True)
 Path.open=recording_open
 try:
  for attempt in range(100):
   try:
    guest,old,payload=launch.current.expected()
    break
   except FileNotFoundError as error:
    need(error.filename,'Actual exact missing filename');recover(error.filename)
  else:raise ValueError('Exceeded bounded dependency discovery')
  pins=launch.source_pins()
 finally:Path.open=real_open
 actual=ROOT/'audit_v2515_current_sonya_p1_shao_duck_wait_campaign/guest_maincpu.bin'
 need(guest==actual.read_bytes(),'Whole actual current guest independently reconstructed after exact recovery')
 need(payload==(game/'roms/mk2ks/mk2ks.mdata').read_bytes(),'Whole current payload independently reconstructed')
 need(all(sha(Path(p))==h for p,h in before.items()),'Current game, settings and public launchers unchanged')
 for p in reads:
  path=Path(p)
  if path.is_file()and path.is_relative_to(ROOT.resolve()):pins[p]=sha(path)
 pins.update(before)
 for p in(PREP,ARCHIVE,actual,Path(__file__).resolve(),ROOT/'audit_v2546_guard_walk_source_boundary_failure/failure.json'):pins[str(p)]=sha(p)
 launch.module_pins(pins)
 return dict(passed=True,restoredRequiredFiles=restored,restoredFiles=len(restored),restoredLogicalBytes=sum(r['bytes']for r in restored),restoredAllocatedBytes=sum(r['allocatedBytes']for r in restored),
  dynamicallyReadDependencies=len(reads),originalCleanupUnreferencedClaimSuperseded=True,allOldBuildFoldersRemoved=False,recoveryArchiveUnchanged=True,wholeCurrentGuestAndPayloadReconstructed=True,
  currentGameSettingsAndLaunchersUnchanged=True,inputHashes=pins,gameChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable actual recovery proof')
 a.output.mkdir()
 try:r=verify()
 except Exception as error:
  (a.output/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n');raise
 (a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','restoredRequiredFiles')},indent=2),flush=True)
