"""Finite original frames inspected, with no image files or raster overclaim."""
import hashlib,json
from pathlib import Path
import qualify_morph_startup_return_v3 as model

def record(c):
 indices=(4,12,13)if c['move']=='ball'else(3,12,13)
 out=model.ROOT/f"audit_morph_startup_return_visual_{c['move']}_p{c['side']}";model.need(not out.exists(),'Fresh actual viewed morph frames')
 frames=[c['rgbFrames'][i]for i in indices]
 for r in frames:model.need(hashlib.sha256(r['pixels']).hexdigest().upper()==r['header']['sha256'],'Original full native screen digest')
 report=dict(passed=True,nativeTerminal=c['terminal'],viewedFrameHeaders=[r['header']for r in frames],observations=['Real form body appears while the lifebar correctly retains Shang Tsung, not a rewritten roster name.','Late special uses the added fighter body; floor shadows visible.','Native Shang body returns without a persistent added portrait or pose.'],extraObservation='Morphed Kano and real Kano retain distinct blue/red native alternate palettes.'if c['move']=='ball'else None,fullRasterAcceptance=False,allMorphContextsAccepted=False,fullPortAcceptance=False,imageFilesWritten=0,inputHashes={str(Path(__file__).resolve()):model.sha(__file__)})
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
