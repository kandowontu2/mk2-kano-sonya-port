"""One requested current-state portable ZIP from existing tested inputs.

Direct archive streaming, no staging build/source tree. Include actual native
layout, all16voices and required original/donor ROMs, replacing only the base
payload with the qualified current pair. No final-port or portable-boot claim.
"""
import datetime,hashlib,json,zipfile
from pathlib import Path,PurePosixPath
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'release_v5986_current_playtest'
NAME='MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST'
PARENT=ROOT/'audit_v5983_current_launcher_handoff_progress/progress.json'

def digest_stream(stream):
 result=hashlib.sha256()
 while chunk:=stream.read(1048576):result.update(chunk)
 return result.hexdigest().upper()

def run():
 need(not OUT.exists(),'Never overwrite a package or create duplicate staging trees')
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and parent['currentNoWarningOrdinaryStartupAccepted']and
      len(parent['remaining'])==5,'Actual new checked launcher and full objective retained')
 candidate=ROOT/current.NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
 files={'mkport.exe':candidate/'mkport_candidate.exe','roms/mk2.zip':ROOT/'roms/mk2.zip'}
 for p in sorted((ROOT/'roms/mk2ks').iterdir()):
  if p.is_file():files['roms/mk2ks/'+p.name]=p
 files['roms/mk2ks/mk2ks.mdata']=candidate/'roms/mk2ks/mk2ks.mdata'
 for p in sorted((ROOT/'samples/mk2ks').iterdir()):
  if p.is_file():files['samples/mk2ks/'+p.name]=p
 files['artwork/mk2ks/default.lay']=ROOT/'artwork/mk2ks/default.lay'
 for name in('PLAY.cmd','CHECK_FILES.ps1','README.txt'):files[name]=ROOT/'tools/playtest_release_v5984'/name
 files['LICENSE']=ROOT/'mame-mkp/COPYING'
 for name in('midtunit.cpp','midtunit_m.cpp','midtunit_v.cpp','midtunit.h'):
  files['source/mame/midway/'+name]=candidate/'input_sources/mame-mkp/src/mame/midway'/name
 for name,p in files.items():
  rel=PurePosixPath(name)
  need(not rel.is_absolute()and '..'not in rel.parts and ':'not in name and '\\'not in name and p.is_file(),'Safe exact existing package input')
 hashes={name:sha(p)for name,p in files.items()};source_pins={str(p):hashes[name]for name,p in files.items()}
 source_pins[str(PARENT)]=sha(PARENT);source_pins[str(Path(__file__).resolve())]=sha(__file__)
 need(hashes['mkport.exe']==current.EXE_SHA and hashes['roms/mk2ks/mk2ks.mdata']==current.PAYLOAD_SHA,
      'Exact tested current executable/payload, not installed old/default pair')
 voices={name:h for name,h in hashes.items()if name.startswith('samples/mk2ks/')and name.endswith('.wav')}
 declared={Path(p).name:h for p,h in build['input_hashes'].items()if '/samples/mk2ks/'in p.replace('\\','/')and p.endswith('.wav')}
 need(len(voices)==16 and {PurePosixPath(name).name:h for name,h in voices.items()}==declared,'Whole exact compiled sixteen-voice dependency set')
 manifest=dict(candidate=current.NAME,releaseStatus='CURRENT PLAYTEST - unfinished',fullPortAcceptance=False,
               executableSHA256=current.EXE_SHA,payloadSHA256=current.PAYLOAD_SHA,guestSHA256=current.GUEST_SHA,
               documentedScope=str(PARENT.name),files=hashes)
 data=(json.dumps(manifest,indent=2)+'\n').encode('utf-8');manifest_sha=hashlib.sha256(data).hexdigest().upper()
 OUT.mkdir();archive_path=OUT/(NAME+'.zip')
 with zipfile.ZipFile(archive_path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True)as archive:
  for name,p in files.items():archive.write(p,NAME+'/'+name)
  archive.writestr(NAME+'/RELEASE.json',data)
  archive.writestr(NAME+'/play/',b'')
 with zipfile.ZipFile(archive_path)as archive:
  entries=archive.infolist();names=[i.filename for i in entries]
  need(len(names)==len(set(names))==len(files)+2 and archive.testzip()is None,'All archive CRCs, unique exact members and no extra staging/cache/history files')
  for name,wanted in hashes.items():
   with archive.open(NAME+'/'+name)as reader:need(digest_stream(reader)==wanted,'Every full archived file equals actual tested source bytes')
  with archive.open(NAME+'/RELEASE.json')as reader:need(digest_stream(reader)==manifest_sha,'Exact generated manifest bytes embedded')
 need(all(sha(p)==h for p,h in source_pins.items()),'All current/compiled/assets/source/old public inputs unchanged while packaging')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,
             zip=str(archive_path),zipSHA256=sha(archive_path),zipBytes=archive_path.stat().st_size,
             files=len(files),uncompressedSourceBytes=sum(p.stat().st_size for p in files.values()),
             sourceHashes=source_pins,archiveMemberHashes={**hashes,'RELEASE.json':manifest_sha},
             nativeScreenOnlyArtworkIncluded=True,all16CompiledVoiceAssetsIncluded=True,
             correspondingModifiedMidwaySourceModulesIncluded=True,currentStatePlaytest=True,
             portableRuntimeVerificationPending=True,fullPortAcceptance=False,newBuilds=0,
             stagingBuildOrSourceTreesCreated=0,newRawRecordings=0,newZIPs=1)
 (OUT/'package-report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('sourceHashes','archiveMemberHashes')},indent=2),flush=True)

if __name__=='__main__':run()
