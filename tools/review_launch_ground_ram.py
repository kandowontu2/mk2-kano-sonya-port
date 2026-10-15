"""Serve only already-qualified whole native RGB frames to a RAM-only viewer."""
import hashlib, io, json, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from PIL import Image
import numpy as np
import launch_ground_native_names as model
ROOT,need,sha=model.ROOT,model.need,model.sha

def serve(carriers):
 proof=ROOT/'audit_launch_ground_native_names_checked/report.json';accepted=json.loads(proof.read_text())
 need(accepted['passed']and len(carriers)==4,'Actual current four terminal ground/raster cases')
 images={};receipts=[]
 for c in carriers:
  snaps=model.original.rows(c['text'],'SNAP');key=f"{c['fighter']}_p{c['side']}"
  for age in(16,128,248,368,432,480):
   snap=next(r for r in snaps if r['age']==age);rgb=c['images'][snap['file']]
   buffer=io.BytesIO();Image.fromarray(rgb).save(buffer,format='PNG');raw=buffer.getvalue()
   need(np.array_equal(np.asarray(Image.open(io.BytesIO(raw)).convert('RGB')),rgb),'Whole native RGB PNG RAM encoding exact')
   route=f'/{key}/{age}.png';images[route]=raw
   receipts.append(dict(case=key,age=age,actualNativeFrame=snap['frame'],route=route,nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),wholeNativePixels=101600))
 class ReadOnly(BaseHTTPRequestHandler):
  def do_GET(self):
   if self.path not in images:self.send_error(404);return
   raw=images[self.path];self.send_response(200);self.send_header('Content-Type','image/png');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),ReadOnly);threading.Thread(target=server.serve_forever,daemon=True).start()
 return server,receipts

def receipt(receipts,reviewed):
 out=ROOT/'audit_launch_ground_visual_review';need(not out.exists(),'Fresh finite native review receipt')
 chosen=[r for r in receipts if(r['case'],r['age'])in reviewed];need(len(chosen)==len(reviewed),'Exact actually viewed native frames')
 proof=ROOT/'audit_launch_ground_native_names_checked/report.json'
 report=dict(passed=True,actualNativeFramesReviewed=chosen,inputHashes={str(proof):sha(proof),str(Path(__file__)):sha(__file__)},
             newRasterFiles=0,newRawMedia=0,newBuilds=0,historicalRuntimeAcceptanceTransferred=False,allArenaGroundAcceptance=False,fullPortAcceptance=False)
 out.mkdir();model.previous.save(out/'report.json',report);return report
