"""Independently bind a real source rebuild to ROM metadata-only changes."""
import ctypes,hashlib,json,re,struct,subprocess,zlib
from pathlib import Path
import verify_native_headed_reaction_v1221 as prior
ROOT=prior.ROOT;CANDIDATE='diagnostic_v1250_native_correct_rom_metadata'
OUT=ROOT/'audit_v1254_native_rom_metadata_checked'

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def reconstruct():
 result=prior.reconstruct()
 assert (ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()==result[3],'Rebuild must retain entire independently reconstructed payload'
 return result

def sections(raw):
 assert raw[:2]==b'MZ'
 pe=struct.unpack_from('<I',raw,60)[0];assert raw[pe:pe+4]==b'PE\0\0'
 count=struct.unpack_from('<H',raw,pe+6)[0];table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
 items={}
 for i in range(count):
  at=table+i*40;name=raw[at:at+8].rstrip(b'\0').decode();size,offset=struct.unpack_from('<II',raw,at+16)
  assert offset+size<=len(raw);items[name]=(offset,size)
 return pe,items

def native_pe_checksum(raw):
 # Windows ImageHlp independently computes the standard PE checksum.
 # https://learn.microsoft.com/windows/win32/api/imagehlp/nf-imagehlp-checksummappedfile
 api=ctypes.WinDLL('imagehlp').CheckSumMappedFile
 api.argtypes=(ctypes.c_void_p,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_uint32))
 api.restype=ctypes.c_void_p
 memory=ctypes.create_string_buffer(raw,len(raw));stored=ctypes.c_uint32();computed=ctypes.c_uint32()
 assert api(memory,len(raw),ctypes.byref(stored),ctypes.byref(computed)),'Native PE checksum calculation failed'
 assert stored.value==computed.value,'Stored PE checksum differs from native independent calculation'
 return computed.value

def verify_executable(old,new,payload,old_crc,old_sha):
 crc=f'{zlib.crc32(payload):08x}'.encode();sha=hashlib.sha1(payload).hexdigest().encode()
 assert len(old)==len(new) and old.count(old_crc)==old.count(old_sha)==1,'One original native ROM hash declaration'
 pe,layout=sections(old);new_pe,new_layout=sections(new)
 assert pe==new_pe and layout==new_layout,'Unchanged executable section layout'
 expected=bytearray(old.replace(old_crc,crc).replace(old_sha,sha))
 # A genuine relink updates the standard PE COFF and export-directory time
 # stamps. These are not machine instructions, game data or runtime state.
 timestamp_ranges=((pe+8,pe+12),(layout['.edata'][0]+4,layout['.edata'][0]+8))
 for lo,hi in timestamp_ranges:expected[lo:hi]=new[lo:hi]
 # IMAGE_OPTIONAL_HEADER.CheckSum is at optional-header byte64. A real
 # relink changes this checksum too; compute it, never waive its bytes.
 checksum=native_pe_checksum(new);struct.pack_into('<I',expected,pe+24+64,checksum)
 assert new==expected,'Rebuilt executable changes bytes outside exact CRC/SHA1, standard link timestamps and independently calculated PE checksum'
 text_at,text_size=layout['.text'];assert old[text_at:text_at+text_size]==new[text_at:text_at+text_size],'Every compiled host instruction must be identical'
 return dict(actualChangedBytes=sum(a!=b for a,b in zip(old,new)),nativeInstructionBytesUnchanged=text_size,
  crc32=crc.decode(),sha1=sha.decode(),PEChecksum=checksum,PEChecksumIndependentlyValidated=True,
  onlyROMHashLinkTimestampAndPEChecksumBytesChanged=True)

def verify():
 pins={}
 def pin(path,wanted=None):
  path=Path(path);actual=digest(path);assert wanted is None or actual==wanted,'Changed evidence '+str(path);pins[str(path)]=actual
 candidate=ROOT/CANDIDATE;build_path=candidate/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
 assert build['metadata_only_source_rebuild'] and build['game_data_changed'] is False
 for file,wanted in build['input_hashes'].items():pin(file,wanted)
 original_path=ROOT/'audit_v1249_rom_metadata_source/midtunit.before.cpp';original=original_path.read_bytes();pin(original_path)
 source_path=candidate/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp';source=source_path.read_bytes();pin(source_path)
 match=re.search(rb'ROM_LOAD\( "mk2ks.mdata", 0x000000, 0x200000, CRC\(([0-9a-f]{8})\) SHA1\(([0-9a-f]{40})\) \)',original)
 assert match,'Exact original ROM declaration'
 guest,_,_,payload=reconstruct();crc=f'{zlib.crc32(payload):08x}'.encode();sha=hashlib.sha1(payload).hexdigest().encode()
 assert source==original.replace(match[1],crc).replace(match[2],sha),'Only source declaration changes; no gameplay edits'
 assert (ROOT/'mame-mkp/src/mame/midway/midtunit.cpp').read_bytes()==original,'Canonical historical source restored exactly; compiled snapshot retained'
 executable_path=candidate/'mkport_candidate.exe';pin(executable_path,build['executable_sha256'])
 payload_path=candidate/'roms/mk2ks/mk2ks.mdata';pin(payload_path,build['payload_sha256'])
 old_path=ROOT/prior.CANDIDATE/'mkport_candidate.exe';old=old_path.read_bytes();pin(old_path)
 binary=verify_executable(old,executable_path.read_bytes(),payload,match[1],match[2])
 assert binary['actualChangedBytes']==52
 for file in ('tools/verify_native_metadata_build_v1254.py','tools/build_metadata_candidate_v1249.ps1',
              'mame-mkp/src/mame/midway/midtunit.cpp','mame-mkp/mkport.exe'):
  pin(ROOT/file)
 assert digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
 return dict(passed=True,candidate=CANDIDATE,executableSHA256=build['executable_sha256'],payloadSHA256=build['payload_sha256'],
  sourceROMMetadataOnlyRebuild=True,wholePayloadIndependentlyReconstructed=True,canonicalHistoricalSourceRestored=True,
  installedExecutableUnchanged=True,executableProof=binary,inputHashes=pins,
  ordinaryInteractiveVideoAudioAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists(),'Preserve evidence';OUT.mkdir()
 report=verify();exe=ROOT/CANDIDATE/'mkport_candidate.exe';rompath=str(ROOT/CANDIDATE/'roms')+';'+str(ROOT/'roms')
 result=subprocess.run([str(exe),'mk2ks','-verifyroms','-rompath',rompath],cwd=ROOT,capture_output=True,text=True)
 (OUT/'verifyroms.log').write_text(result.stdout+result.stderr)
 assert result.returncode==0 and '1 were OK' in result.stdout and not re.search('WRONG CHECKSUMS|might not run correctly|BAD DUMP|NOT FOUND',result.stdout+result.stderr,re.I)
 report['nativeROMAuditAccepted']=True
 boot=subprocess.run([str(exe),'mk2ks','-rompath',rompath,'-samplepath',str(ROOT/'samples'),'-nocheat',
  '-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),
  '-video','none','-sound','none','-str','2','-nothrottle'],cwd=ROOT,capture_output=True,text=True)
 (OUT/'ordinary_boot.log').write_text(boot.stdout+boot.stderr)
 assert boot.returncode==0 and not re.search('WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation',boot.stdout+boot.stderr,re.I)
 report['ordinaryHeadlessBootWithoutSkipGameinfoAccepted']=True
 for path in OUT.rglob('*'):
  if path.is_file():report['inputHashes'][str(path)]=digest(path)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Native ROM audit and ordinary boot clean; whole .text unchanged; only52 ROM-hash/link-timestamp/calculated-PE-checksum bytes differ',flush=True)
