"""Bounded Windows raw-frame pipe to one low-priority encoder, no raw video file."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import threading
import time
import uuid
import _winapi

FRAME_BYTES = 400 * 254 * 4


class CapturePipe:
    def __init__(self, output, rate, max_frames, timeout):
        self.output = Path(output).resolve()
        assert self.output.parent.is_dir() and not self.output.exists()
        assert 0 < max_frames <= 300000 and 0 < timeout <= 900
        self.address = r'\\.\pipe\mk2ks-' + uuid.uuid4().hex
        self.deadline = time.monotonic() + timeout
        self.limit = max_frames * FRAME_BYTES
        self.stop = threading.Event(); self.error = None; self.result = None
        self.handle = _winapi.CreateNamedPipe(self.address,
            _winapi.PIPE_ACCESS_INBOUND | _winapi.FILE_FLAG_OVERLAPPED | _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE,
            _winapi.PIPE_WAIT, 1, 65536, 65536, 5000, _winapi.NULL)
        ff = shutil.which('ffmpeg'); assert ff
        self.log = self.output.with_suffix('.stderr.log').open('xb')
        self.process = subprocess.Popen([ff, '-v', 'error', '-nostdin', '-f', 'rawvideo',
            '-pixel_format', 'bgra', '-video_size', '400x254', '-framerate', str(rate), '-i', 'pipe:0',
            '-an', '-vf', 'setsar=127/150:max=1000', '-c:v', 'libx264', '-threads', '1',
            '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            '-n', str(self.output)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=self.log,
            bufsize=0, creationflags=subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS)
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _wait(self, operation):
        try:
            while _winapi.WaitForMultipleObjects([operation.event], False, 100) == _winapi.WAIT_TIMEOUT:
                if self.stop.is_set() or time.monotonic() >= self.deadline:
                    raise TimeoutError('Native frame pipe cancelled or timed out')
        except BaseException:
            operation.cancel()
            operation.GetOverlappedResult(True)
            raise
        return operation.GetOverlappedResult(True)

    def _serve(self):
        count = 0; digest = hashlib.sha256()
        try:
            operation = _winapi.ConnectNamedPipe(self.handle, overlapped=True)
            _, error = self._wait(operation)
            assert error == 0, error
            while True:
                try:
                    operation, error = _winapi.ReadFile(self.handle, 65536, overlapped=True)
                    size, error = self._wait(operation) if error == _winapi.ERROR_IO_PENDING else operation.GetOverlappedResult(True)
                except OSError as exc:
                    if exc.winerror == _winapi.ERROR_BROKEN_PIPE:
                        break
                    raise
                if error == _winapi.ERROR_BROKEN_PIPE:
                    break
                assert error == 0, error
                if not size:
                    break
                data = operation.getbuffer()
                assert len(data) == size and count + size <= self.limit
                digest.update(data); count += size
                remaining = memoryview(data)
                while remaining:
                    written = self.process.stdin.write(remaining)
                    assert written and written > 0
                    remaining = remaining[written:]
            self.process.stdin.close()
            assert self.process.wait(timeout=60) == 0, 'Encoder failed; inspect preserved stderr'
            assert count and count % FRAME_BYTES == 0, 'Incomplete raw frame stream'
            self.result = dict(frames=count // FRAME_BYTES, rawBytes=count,
                rawStreamSHA256=digest.hexdigest().upper(), rawVideoFileCreated=False,
                encoderThreads=1, pipeBufferBytes=65536, pythonReadChunkBytes=65536)
        except BaseException as exc:
            self.error = exc
        finally:
            if self.process.poll() is None:
                self.process.kill(); self.process.wait(timeout=10)
            if self.process.stdin and not self.process.stdin.closed:
                self.process.stdin.close()
            _winapi.CloseHandle(self.handle)
            self.log.close()

    def finish(self, timeout=30):
        self.thread.join(timeout)
        if self.thread.is_alive():
            self.abort()
            raise TimeoutError('Capture writer did not close its pipe')
        if self.error:
            raise self.error
        assert self.result
        return self.result

    def abort(self):
        self.stop.set()
        self.thread.join(3)
        assert not self.thread.is_alive(), 'Capture cancellation did not finish'
