"""Record only the original native frames actually inspected this turn."""
import hashlib,json
from pathlib import Path
import qualify_launch_challenger_transition as model

def record(c):
 model.need(c['side']==2,'Actual remaining P2 captures')
 out=model.ROOT/f"audit_launch_challenger_transition_visual_{c['move']}_p2"
 model.need(not out.exists(),'Fresh finite visual review')
 indices=(1,3,4)if c['move']=='ball'else(3,4)
 actual=[c['rgbFrames'][i]for i in indices]
 for r in actual:model.need(hashlib.sha256(r['pixels']).hexdigest().upper()==r['header']['sha256'],'Original native full-screen bytes')
 report=dict(passed=True,nativeTerminal=c['terminal'],viewedFrameHeaders=[r['header']for r in actual],observations=['Dedicated portraits, native-style border and centered player numbers visible for both added characters.','Actual Kano/Sonya bodies and matching lifebar names in the joined match.','Selection portraits and poses absent in the viewed match.'],extraObservation='Cold CPU Sonya and human Kano visible with correct names.'if c['move']=='ball'else None,fullRasterAcceptance=False,blinkingAnimationAcceptance=False,onePixelBackdropAlignmentAcceptance=False,allSelectionTransitionsAccepted=False,imageFilesWritten=0,inputHashes={str(Path(__file__).resolve()):model.sha(__file__),str(Path(model.__file__).resolve()):model.sha(model.__file__)})
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
