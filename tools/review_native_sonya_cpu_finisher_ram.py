"""Display ten actual native Sonya finisher/transition frames, RAM only."""
import io, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image, ImageDraw

def serve(capture):
    names = [f'postjoin_sonya_cpu_finish_age{n}.png' for n in (1,30,60,90,180,240)]
    names += ['postjoin_sonya_cpu_finish_winner30.png']
    names += [f'postjoin_sonya_cpu_finish_age{n}.png' for n in (330,450,900)]
    scenes = capture['images']
    assert {n for n in scenes if n.startswith('postjoin_sonya_cpu_finish_')} == set(names)
    pages = []
    for group in (names[:6], names[6:]):
        atlas = Image.new('RGB', (800, ((len(group)+1)//2)*278))
        draw = ImageDraw.Draw(atlas)
        for i, name in enumerate(group):
            im = scenes[name]
            assert im.size == (400,254)
            x,y = i%2*400, i//2*278
            atlas.paste(im,(x,y+24))
            draw.text((x+3,y+4),name,fill='white')
        stream=io.BytesIO();atlas.save(stream,format='PNG');pages.append(stream.getvalue())
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ('/0','/1'):
                self.send_error(404);return
            raw=pages[int(self.path[1:])]
            self.send_response(200);self.send_header('Content-Type','image/png')
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,dict(port=server.server_port,names=names,rawMediaFilesWritten=0)
