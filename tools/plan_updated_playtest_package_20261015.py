"""Read-only pinned ZIP inspection plus prepared document update plan; no ZIP write."""
import hashlib
import json
import zipfile
from pathlib import Path

R=Path(__file__).resolve().parent.parent
out=R/'audit_updated_playtest_package_preparation_20261015'
dest=out/'plan.json';assert not dest.exists()
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()
old=R/'release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip'
assert sha(old)=='EDAC17A71DC7353ABC35C32D914E8248DB7804DCA6F9AA3A24B9B25EDF2797B7'
prefix='MK2_Kano_Sonya_Playtest/'
with zipfile.ZipFile(old) as z:
    names=z.namelist();assert len(names)==len(set(names))
    manifest=json.loads(z.read(prefix+'RELEASE.json'))
    assert z.read(prefix+'PLAY.cmd')==(R/'PLAY_CURRENT_NATIVE_CHECKED.cmd').read_bytes()
    assert z.read(prefix+'tools/check_current_native_playtest.ps1')==(R/'tools/check_current_native_playtest.ps1').read_bytes()
    assert len([n for n in names if n.endswith('.wav')])==23
    assert not any(n.endswith('MK2_KANO_SONYA_MOVES.txt') for n in names)
    assert 'README.txt' in manifest['files']
report=dict(preparedNotExecuted=True,newZIPs=0,newBuilds=0,oldZIP=str(old),oldZIPRetained=True,
            oldZIPHash=sha(old),oldMembers=len(names),plannedMembers=len(names)+1,
            smallestMemberChanges=['Replace README.txt with prepared concise current-playtest text.',
                                   'Add MK2_KANO_SONYA_MOVES.txt using portable PLAY.cmd name.',
                                   'Regenerate RELEASE.json hashes for those two docs only; retain unfinished status.'],
            launcher='PLAY.cmd and tools/check_current_native_playtest.ps1 already exactly equal current workspace; preserve unchanged bytes. No aliases needed.',
            preparedDocs={p.name:dict(path=str(p),SHA256=sha(p)) for p in (out/'README.txt',out/'MK2_KANO_SONYA_MOVES.txt')},
            streamingAlgorithm='Verify source sync and pinned old ZIP. Open a fresh uniquely named output with ZIP exclusive-create. For every unaffected member stream z.open -> new.open through 1MiB copy buffer, preserving exact UNCOMPRESSED bytes and member names; substitute README, append move guide, regenerate manifest. No staging/extraction. Stream-read every new member digest against retained manifest, check no duplicates, unchanged EXE/mdata/fullROM/23sounds/15sources/CMD; testzip. Recheck old ZIP hash and original source hashes afterward.',
            runtimeCheck='After packaging only, extract once to an exact fresh bounded temporary subtree, run extracted PLAY.cmd --check, optionally one bounded ordinary boot, then remove that exact extraction after containment/non-reparse checks. No persistent duplicate tree.',
            storage='One new ~57MiB deliverable, no intermediate archive/staging tree. Preserve pinned existing ZIP until root decides retention; do not bypass denied bad39MiBZIP deletion.',
            releaseStatus='UNFINISHED CURRENT PLAYTEST',finalPromotion=False,fullPortAccepted=False)
dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
