"""Serve real native image stages directly from the retained capture RAM."""
import io,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from PIL import Image,ImageDraw

def serve(captures):
    images=[];keys=list(captures)
    for key,c in captures.items():
        atlas=Image.new('RGB',(800,556));draw=ImageDraw.Draw(atlas)
        for n,(im,stage) in enumerate(zip(c['images'],c['meta']['actualScenes'])):
            x=n%2*400;y=n//2*278
            atlas.paste(im,(x,y+24));draw.text((x+3,y+4),key+' '+stage['stage'],fill='white')
        stream=io.BytesIO();atlas.save(stream,format='PNG');images.append(stream.getvalue())
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:raw=images[int(self.path.strip('/'))]
            except (ValueError,IndexError):self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type','image/png');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,dict(port=server.server_port,cases=keys,rawMediaFilesWritten=0)
