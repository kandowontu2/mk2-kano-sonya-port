"""Serve original captured screen bytes for inspection without image files."""
import hashlib,io,json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from PIL import Image

def serve(c):
 frames=c['rgbFrames']
 class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
   try:
    index=int(self.path.lstrip('/'));record=frames[index];h=record['header'];raw=record['pixels']
    assert hashlib.sha256(raw).hexdigest().upper()==h['sha256']
    im=Image.frombytes('RGB',(int(h['width']),int(h['height'])),raw,'raw','BGRX');out=io.BytesIO();im.save(out,format='PNG');png=out.getvalue()
    self.send_response(200);self.send_header('Content-Type','image/png');self.send_header('Content-Length',str(len(png)));self.end_headers();self.wfile.write(png)
   except Exception:self.send_error(400)
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
 threading.Thread(target=server.serve_forever,daemon=True).start()
 print(json.dumps(dict(port=server.server_port,frames=[dict(index=i,header=r['header'])for i,r in enumerate(frames)])),flush=True)
 return server

def record_review(c):
 from pathlib import Path
 import qualify_launch_challenger_transition as model
 out=model.ROOT/'audit_launch_challenger_transition_visual_square_p1'
 model.need(c['move']=='square'and c['side']==1 and not out.exists(),'Exact previously viewed Sonya P1 frames')
 records=[c['rgbFrames'][i]for i in(3,4,26)]
 for r in records:model.need(hashlib.sha256(r['pixels']).hexdigest().upper()==r['header']['sha256'],'Original actual image digest')
 report=dict(passed=True,nativeTerminal=c['terminal'],viewedFrameHeaders=[r['header']for r in records],observations=['Both top-row portraits and player numbers visible in selection.','New match shows actual Sonya and Kano bodies with matching lifebar names.','Selection portraits and poses absent in viewed match frames.','Floor shadows visible in final viewed match frame.'],fullRasterAcceptance=False,blinkingAnimationAcceptance=False,onePixelBackdropAlignmentAcceptance=False,allSelectionTransitionsAccepted=False,imageFilesWritten=0,inputHashes={str(Path(__file__).resolve()):model.sha(__file__)})
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
