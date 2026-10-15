"""Review original native RGB arrays in RAM; no screenshots or media copies."""
import io
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image

def serve(cases):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                case, frame = self.path.strip('/').split('/')
                rgb = cases[case][2][f'ui_{int(frame):04d}.png']
                stream = io.BytesIO()
                Image.fromarray(rgb).save(stream, format='PNG')
                data = stream.getvalue()
            except (KeyError, ValueError):
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print('Native RAM review port', server.server_port, flush=True)
    return server
