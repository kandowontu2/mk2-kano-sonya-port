"""Six actual native finisher/transition snapshots; RAM-only browser review."""
import io,re,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from PIL import Image,ImageDraw
def serve(capture):
    scenes={name:im for name,im in capture['images'].items()if name.startswith('postjoin_finisher_regression_')}
    names=sorted(scenes,key=lambda n:int(re.search(r'age(\d+)',n)[1]))
    if len(names)!=6:raise ValueError('Every six actually captured finisher phases required')
    atlas=Image.new('RGB',(800,834));draw=ImageDraw.Draw(atlas)
    for n,name in enumerate(names):
        x=n%2*400;y=n//2*278
        atlas.paste(scenes[name],(x,y+24));draw.text((x+3,y+4),name,fill='white')
    stream=io.BytesIO();atlas.save(stream,format='PNG');raw=stream.getvalue()
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path!='/0':self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type','image/png')
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,dict(port=server.server_port,names=names,rawMediaFilesWritten=0)
