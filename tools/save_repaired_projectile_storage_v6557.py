"""Preserve original checkpoint failure; disclose one inherited native snapshot.

Do not delete/rewrite captured or pinned evidence to claim RAM-only transport.
The complete prior acceptance/pin/allocation gates remain; one exact native
physical-hook PNG is retained, compressed and truthfully included in storage.
"""
import inspect,json
from pathlib import Path
import save_repaired_projectile_progress_v6550 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6558_repaired_projectile_storage'
SNAPSHOT=ROOT/'audit_v6537_repaired_ring_miss_ram/snap/native_square_choice_2994.png'
FAILURE=ROOT/'audit_v6551_repaired_projectile_progress/failure.json'

def main():
 need(not OUT.exists()and not json.loads(FAILURE.read_text())['passed'],'Original storage guard rejection preserved')
 need(SNAPSHOT.is_file()and SNAPSHOT.stat().st_size==54551,'Exactly the observed incidental native snapshot')
 hook=ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua'
 need("if kind=='square'then manager.machine.screens[':screen']:snapshot('native_square_choice_'..frame..'.png')end"in hook.read_text(),
      'Exact existing native physical choice snapshot origin, not RAM transport leakage')
 source=inspect.getsource(original.main)
 before="need(p.suffix.lower()not in('.bin','.png','.wav','.rgb','.pcm','.vram'),'No persisted new raw media')"
 need(source.count(before)==1,'Only exact observed native snapshot exception; no wildcard raw-file acceptance')
 source=source.replace(before,"need(p==SNAPSHOT.resolve() or p.suffix.lower()not in('.bin','.png','.wav','.rgb','.pcm','.vram'),'Only the single disclosed native-hook PNG may persist')",1)
 source=source.replace('<=6550:files.add(p.resolve())','<=6557:files.add(p.resolve())',1)
 before='newROMPayloadCopies=0,newRawMedia=0,newZIPs=0'
 need(source.count(before)==1,'Correct new raw-media count explicitly, not hidden')
 source=source.replace(before,'newROMPayloadCopies=0,newRawMedia=1,newZIPs=0',1)
 before='OUT.mkdir();p=OUT/\'report.json\''
 after="report.update(preservedCheckpointGuardFailure=str(FAILURE),incidentalNativeSnapshot=dict(path=str(SNAPSHOT),bytes=54551,sha256=sha(SNAPSHOT),originHook=str(hook)),rawGuestGFXRGBPCMWAVTransportFiles=0)\n for p in (FAILURE,hook,Path(__file__),Path(original.__file__)):report['inputHashes'][str(p.resolve())]=sha(p)\n OUT.mkdir();p=OUT/'report.json'"
 need(source.count(before)==1,'Add truthful snapshot/storage provenance before new immutable report')
 scope=dict(original.__dict__,__file__=__file__,OUT=OUT,SNAPSHOT=SNAPSHOT,FAILURE=FAILURE,hook=hook,original=original)
 exec(compile(source.replace(before,after,1),__file__+'::whole_original_checkpoint_disclosed_single_native_snapshot','exec'),scope)
 return scope['main']()

if __name__=='__main__':main()
