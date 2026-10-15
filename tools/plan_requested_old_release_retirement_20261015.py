"""User-requested obsolete release retirement plan; never removes files."""
import ctypes
import hashlib
import json
from pathlib import Path

R=Path(__file__).resolve().parent.parent
out=R/'audit_requested_old_release_retirement_plan_20261015'
assert not out.exists()
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()
api=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
api.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));api.restype=ctypes.c_uint32
latest=R/'release_mk2_kano_sonya_20261015/MK2_Kano_Sonya_20261015.zip'
latesthash='4B8288D0CC1E94D476D60D87C0EF4DF5B5BB22A0BD123D4943330A2CD223B9B2'
assert sha(latest)==latesthash
files=[
 ('release_current_native_playtest_20261013/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013.zip','9481CF6938EF23CBBA58101C3E0118B137E3005C7A04E9CB0E95B4E3362B8842'),
 ('release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip','EDAC17A71DC7353ABC35C32D914E8248DB7804DCA6F9AA3A24B9B25EDF2797B7'),
 ('release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip','994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'),
 ('release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip','4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C')]
rows=[]
for rel,wanted in files:
    p=R/rel;st=p.lstat();assert not st.st_file_attributes&0x400 and st.st_nlink==1
    assert p.resolve().is_relative_to(R) and p!=latest and sha(p)==wanted
    hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=api(str(p),ctypes.byref(hi))
    if lo==0xffffffff and ctypes.get_last_error():raise ctypes.WinError(ctypes.get_last_error())
    rows.append(dict(path=str(p),bytes=st.st_size,SHA256=wanted,mtimeNS=st.st_mtime_ns,
                     allocatedBytes=(hi.value<<32)|lo,rebuildCurrentDependency=False,
                     priorDeletionPolicyDenialMustNotBeBypassed=rel.startswith('release_current_native_playtest_20261013/')))
build=R/'diagnostic_native_selector_layers_long';info=json.loads((build/'build-info.json').read_text())
preserve={str(latest):latesthash}
for path,wanted in info['canonical_source_hashes_at_compile'].items():
    p=Path(path);assert sha(p)==wanted;preserve[str(p)]=wanted
assert len(info['canonical_source_hashes_at_compile'])==15
for p in [build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json',
          R/'roms/mk2.zip',R/'roms/mk2ks.zip',R/'mk/mk-maincpu.bin',R/'mk2/mk2-maincpu.bin',R/'mk3/mk3-maincpu.bin']:
    if p.exists():preserve[str(p)]=sha(p)
temps=[R/n/'temporary_extracted_package' for n in ('audit_final_native_release_portable_check_20261015',
       'audit_updated_private_playtest_portable_check_20261015','audit_current_native_zip_portable_check_20261013_complete_roms_scoped')]
assert not any(p.exists() for p in temps)
report=dict(readOnlyPlan=True,deletionsPerformed=0,targets=rows,
            allocatedCandidateBytes=sum(x['allocatedBytes'] for x in rows),
            logicalCandidateBytes=sum(x['bytes'] for x in rows),
            latestPreserved=str(latest),latestSHA256=latesthash,preservedHashes=preserve,
            preserveDirectories=['mame-mkp (one Git tree, all current/third-party build sources)','diagnostic_native_selector_layers_long (current binary, compiled snapshots and build manifest)','roms, mk, mk2, mk3, samples, artwork, assets/generators and required original UI/reconstruction inputs'],
            oldArchiveRole='The four exact ZIPs are superseded distributable/recovery artifacts, not inputs to compile current canonical sources or decode current original ROM/GFX. v1836 unique executable recovery will intentionally be discarded under the renewed user request, not described as reconstructable.',
            verifierMigrationRequired=dict(path='tools/verify_native_source_sync.py',
                exactArchivalPin='release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip',
                sites=['FIXED archive entry','original historical REPORTS inputHashes loop (startup ring report pins same archive)'],
                policy='Add an explicit allowlisted retired-archive record referencing exact deletion receipt/path/SHA and missing-state, not a fake relocated byte digest. Retain old report bytes unchanged, flag original unchanged-path gate false for the retired archive. Exempt ONLY this archival artifact; preserve every canonical15 source/current EXE/mdata/compiled snapshot/report hash check and effective mutations. Do not claim the deleted ZIP bytes were freshly revalidated after removal.'),
            finalRemovalSafeguards='Root resolves exact descendant non-reparse file paths, rechecks length/SHA plus latest ZIP/current rebuild preservation, confirms no active build/game uses target, handles any tool denial normally without workaround, records intentional archival-pin retirement. File-only removal; no root/folder recursive deletion.',
            checkedTemporaryExtractionsAlreadyAbsent=[str(p) for p in temps],
            temporaryFilesMatchedByScopedTMP_TEMP_PART_BAKScan=0,
            noNewArchive=True,sourceOrCurrentRebuildInputsSelected=False)
out.mkdir();(out/'deletion_plan.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(files=len(rows),allocatedCandidateBytes=report['allocatedCandidateBytes'],logicalCandidateBytes=report['logicalCandidateBytes'],latestSHA256=latesthash,preservedHashes=len(preserve),temporaryExtractionsAbsent=len(temps))))
