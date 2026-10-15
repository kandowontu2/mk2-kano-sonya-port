"""In-memory metadata/code/checksum counterexamples; never alter real EXEs."""
import ctypes,json,struct
import verify_native_metadata_build_v1254 as proof
OUT=proof.ROOT/'audit_v1256_native_metadata_corruption_checks';assert not OUT.exists()
old_path=proof.ROOT/proof.prior.CANDIDATE/'mkport_candidate.exe';new_path=proof.ROOT/proof.CANDIDATE/'mkport_candidate.exe'
old=old_path.read_bytes();new=new_path.read_bytes();payload=proof.reconstruct()[3]
pe,sections=proof.sections(new);old_crc=b'10ab3463';old_sha=b'055fbffc9b7ea6f039a2816549e138ab55179379'
checks={}

def recalculate(raw):
 api=ctypes.WinDLL('imagehlp').CheckSumMappedFile
 api.argtypes=(ctypes.c_void_p,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_uint32));api.restype=ctypes.c_void_p
 memory=ctypes.create_string_buffer(bytes(raw),len(raw));stored=ctypes.c_uint32();computed=ctypes.c_uint32()
 assert api(memory,len(raw),ctypes.byref(stored),ctypes.byref(computed))
 struct.pack_into('<I',raw,pe+24+64,computed.value)
 return bytes(raw)

baseline=proof.verify_executable(old,new,payload,old_crc,old_sha);checks['baseline']=dict(passed=True,proof=baseline)
for label in ('host_instruction_changed','host_initial_state_changed','nonmetadata_readonly_constant_changed',
              'native_unwind_table_changed','ROM_CRC_changed','ROM_SHA1_changed','PE_checksum_corrupted',
              'executable_layout_changed','payload_byte_changed'):
 changed=bytearray(new);trial_payload=payload
 if label=='host_instruction_changed':changed[sections['.text'][0]+64]^=1
 elif label=='host_initial_state_changed':changed[sections['.data'][0]+64]^=1
 elif label=='nonmetadata_readonly_constant_changed':changed[sections['.rdata'][0]+64]^=1
 elif label=='native_unwind_table_changed':changed[sections['.xdata'][0]+64]^=1
 elif label=='ROM_CRC_changed':changed[new.index(b'4a606b51')+2]^=1
 elif label=='ROM_SHA1_changed':changed[new.index(b'36a54a06e295ea08f1ce9bda9bfbce6353731ca9')+2]^=1
 elif label=='PE_checksum_corrupted':changed[pe+24+64]^=1
 elif label=='executable_layout_changed':
  table=pe+24+struct.unpack_from('<H',new,pe+20)[0];changed[table+16]^=1
 else:trial_payload=payload[:-1]+bytes([payload[-1]^1])
 # Except the checksum-specific counterexample, give the altered in-memory
 # image a VALID new PE checksum. The byte-equivalence guard must still
 # reject altered code/constants/layout/ROM declaration, not only bad sums.
 altered=bytes(changed) if label=='PE_checksum_corrupted' else recalculate(changed)
 try:proof.verify_executable(old,altered,trial_payload,old_crc,old_sha)
 except AssertionError as error:checks[label]=dict(rejected=True,error=str(error));print(label+' rejected',flush=True)
 else:raise AssertionError(label+' incorrectly accepted')
assert new_path.read_bytes()==new and old_path.read_bytes()==old
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=checks,inMemoryOnly=True,
 actualRuntimeEvidenceChanged=False,fullPortAccepted=False),indent=2)+'\n')
print('Nine code/metadata/checksum counterexamples rejected; real files unchanged',flush=True)
