"""Bounded actual-frame/native-audio clip; never a campaign-completion claim."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from verify_finisher_roms import verify
import zipfile

PORT=Path(__file__).resolve().parent
run=PORT.parent/'baseline'/sys.argv[1]
assert run.parent==PORT.parent/'baseline' and run.is_dir()
receipt=json.loads((run/'execution.json').read_text())
assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
rows=list(csv.DictReader((run/'finisher_capture.csv').open()))
assert 1<len(rows)<=800
assert [int(r['frame']) for r in rows]==list(range(int(rows[0]['frame']),int(rows[0]['frame'])+len(rows)))
assert all((r['width'],r['height'],r['bytes'])==('400','254','406400') for r in rows)
rate=(len(rows)-1)/(float(rows[-1]['seconds'])-float(rows[0]['seconds']))
assert 50<rate<60
raw=run/'finisher_capture.bgra';wav=run/'native_dcs.wav'
assert raw.stat().st_size==len(rows)*406400 and wav.is_file()
output=run/'native_finisher_v2.mp4';assert not output.exists()
hidden=getattr(subprocess,'CREATE_NO_WINDOW',0)|getattr(subprocess,'BELOW_NORMAL_PRIORITY_CLASS',0)
def command(args):
    return subprocess.run(args,capture_output=True,text=True,timeout=45,check=True,creationflags=hidden)
ff=shutil.which('ffmpeg');fp=shutil.which('ffprobe');assert ff and fp
command([ff,'-v','error','-nostdin','-threads','2','-f','rawvideo','-pixel_format','bgra','-video_size','400x254',
         '-framerate',f'{rate:.12f}','-i',str(raw),'-ss',rows[0]['seconds'],'-i',str(wav),
         '-map','0:v:0','-map','1:a:0','-t',f'{len(rows)/rate:.12f}',
         '-vf','setsar=127/150:max=1000','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)])
probe=json.loads(command([fp,'-v','error','-count_frames','-show_streams','-of','json',str(output)]).stdout)
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert int(video['nb_read_frames'])==len(rows) and video['display_aspect_ratio']=='4:3'
assert any(s['codec_type']=='audio' for s in probe['streams'])
command([ff,'-v','error','-xerror','-nostdin','-threads','2','-i',str(output),'-f','null','NUL'])
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()
report=dict(scope='Actual native move/finisher frames, not full movelist or campaign',file=str(output),
    SHA256=sha(output),bytes=output.stat().st_size,frames=len(rows),rate=rate,
    firstGuestFrame=int(rows[0]['frame']),firstGuestSeconds=float(rows[0]['seconds']),
    stockMAME=True,currentFull26ROMBytesVerified=True,nativeAudio=True,exactAudioSyncQualified=False,
    fullVideoAndAudioDecodePassed=True,visualReviewPassed=False,releaseReady=False,
    sourceRawSHA256=sha(raw),sourceWAVSHA256=sha(wav),observerSHA256=receipt['controllerSHA256'])
(run/'FINISHER_VIDEO.json').write_text(json.dumps(report,indent=2)+'\n')
# Only exact verified generated intermediates inside this immutable test run.
assert raw.parent==run and wav.parent==run
raw.unlink();wav.unlink()
print(json.dumps(report,indent=2))
