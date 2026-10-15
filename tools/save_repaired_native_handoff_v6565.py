"""Disclose the timed native boot's automatic1692-byte snapshot; retain failure.

All current launcher/physical/fault/storage/migration gates remain. No native
replay, removed evidence or silently broadened raw-file exemption is needed.
"""
import inspect,json
from pathlib import Path
import save_repaired_public_handoff_v6563 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6566_repaired_native_handoff'
SNAPSHOT=ROOT/'audit_v6554_repaired_default_launcher_checked/boot/snap/mk2ks/0000.png'
FAILURE=ROOT/'audit_v6564_repaired_public_handoff/failure.json'

def main():
 need(not OUT.exists()and not json.loads(FAILURE.read_text())['passed'],'Exact rejected storage receipt preserved')
 need(SNAPSHOT.stat().st_size==1692 and sha(SNAPSHOT)=='E522C91151C2ABD8E22C8732B2E38A853BD7CB7604AFB13169795CBEAAD4A684',
      'One exact native timed-boot endpoint snapshot, not arbitrary raw-file admission')
 video=ROOT/'mame-mkp/src/emu/video.cpp';text=video.read_text()
 start=text.index('if (m_seconds_to_run != 0 && emutime.seconds() >= m_seconds_to_run)')
 body=text[start:start+1800]
 need('save_snapshot(&screen, file);'in body and 'machine().schedule_exit();'in body,
      'Actual native timed-run termination creates snapshot before schedule_exit')
 source=inspect.getsource(original.main)
 changes={"need(p.suffix.lower()not in('.bin','.png','.wav','.rgb','.pcm','.vram'),'No new promotion raw-media output')":
          "need(p==SNAPSHOT.resolve()or p.suffix.lower()not in('.bin','.png','.wav','.rgb','.pcm','.vram'),'Only exact disclosed automatic timed-exit snapshot persists')",
          '<=6563:files.add(p.resolve())':'<=6565:files.add(p.resolve())',
          'newROMPayloadCopies=0,newRawMedia=0,newZIPs=0':'newROMPayloadCopies=0,newRawMedia=1,newZIPs=0'}
 for a,b in changes.items():need(source.count(a)==1,'Only truthful native snapshot and source provenance correction');source=source.replace(a,b,1)
 before="OUT.mkdir();p=OUT/'report.json'"
 after="report.update(preservedStorageGuardFailure=str(FAILURE),nativeTimedExitSnapshot=dict(path=str(SNAPSHOT),bytes=1692,sha256=sha(SNAPSHOT),originSource=str(video)),rawGuestGFXRGBPCMWAVTransportFiles=0)\n for p in (Path(__file__),Path(original.__file__),FAILURE,video):report['inputHashes'][str(p.resolve())]=sha(p)\n OUT.mkdir();p=OUT/'report.json'"
 need(source.count(before)==1,'Add truthful native snapshot receipt before immutable report')
 scope=dict(original.__dict__,__file__=__file__,OUT=OUT,SNAPSHOT=SNAPSHOT,FAILURE=FAILURE,video=video,original=original)
 exec(compile(source.replace(before,after,1),__file__+'::whole_original_handoff_disclosed_native_timed_snapshot','exec'),scope)
 return scope['main']()

if __name__=='__main__':main()
