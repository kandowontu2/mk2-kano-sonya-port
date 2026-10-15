"""RAM-only native raster contact sheets, with no scaled or synthesized frames."""
import io,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from PIL import Image,ImageDraw

def serve(c):
    scenes=c['rgbFrames'];pages=[]
    for first in range(0,len(scenes),6):
        group=scenes[first:first+6]
        atlas=Image.new('RGB',(800,((len(group)+1)//2)*278));draw=ImageDraw.Draw(atlas)
        for i,scene in enumerate(group):
            h=scene['header'];assert h['width']=='400' and h['height']=='254' and len(scene['pixels'])==406400
            im=Image.frombytes('RGB',(400,254),scene['pixels'],'raw','BGRX')
            x,y=i%2*400,i//2*278
            atlas.paste(im,(x,y+24));draw.text((x+3,y+4),h['stage'],fill='white')
        stream=io.BytesIO();atlas.save(stream,format='PNG');pages.append(stream.getvalue())
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:n=int(self.path[1:]);raw=pages[n];assert n>=0
            except (ValueError,IndexError,AssertionError):self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type','image/png')
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,dict(port=server.server_port,pages=len(pages),actualNativeFrames=len(scenes),rawMediaFilesWritten=0)
