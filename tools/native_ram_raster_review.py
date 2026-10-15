"""Local, RAM-only review of original native RGB fields; no image files."""
import hashlib
import io
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from PIL import Image


def start(images, folder):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            query = urlparse(self.path)
            if query.path == '/manifest':
                body = json.dumps(dict(capture=str(folder), frames=[dict(
                    frame=n, rgbSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),
                    width=400, height=254) for n, rgb in sorted(images.items())])).encode()
                kind = 'application/json'
            elif query.path == '/image':
                frame = int(parse_qs(query.query)['frame'][0])
                if frame not in images:
                    self.send_error(404)
                    return
                stream = io.BytesIO()
                Image.fromarray(images[frame]).save(stream, format='PNG')
                body, kind = stream.getvalue(), 'image/png'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(json.dumps(dict(nativeRAMRasterReviewPort=server.server_port, heldNativeFields=len(images))), flush=True)
    return server
