"""Lossless stream-copy display-aspect correction; no gameplay edits or re-encoding."""
import hashlib,json,os,shutil,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent.parent
D=R/'video_kano_full_20261015'
VIDEO=D/'Kano_full_playthrough.mp4'
TEMP=D/'aspect_only.tmp.mp4'
RECEIPT=D/'aspect_verification.json'
HIDDEN=0x08000000
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()
def probe(path):
    p=subprocess.run([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,timeout=10,check=True,creationflags=HIDDEN)
    return json.loads(p.stdout)
def main():
    assert not TEMP.exists() and not RECEIPT.exists()
    old=json.loads((D/'verification.json').read_text())
    assert old['passed'] and old['fullPlaythrough'] and sha(VIDEO)==old['finalSHA256']
    before=probe(VIDEO)
    args=[shutil.which('ffmpeg'),'-hide_banner','-loglevel','error','-nostdin','-i',str(VIDEO),'-map','0','-c','copy','-bsf:v','h264_metadata=sample_aspect_ratio=127/150','-aspect','4:3','-movflags','+faststart',str(TEMP)]
    with (D/'aspect.stderr.log').open('wb') as log:
        p=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=log,creationflags=HIDDEN)
        try:p.wait(timeout=30)
        except subprocess.TimeoutExpired:p.kill();p.wait();raise
    assert p.returncode==0
    after=probe(TEMP)
    ov=next(x for x in before['streams'] if x['codec_type']=='video')
    nv=next(x for x in after['streams'] if x['codec_type']=='video')
    oa=next(x for x in before['streams'] if x['codec_type']=='audio')
    na=next(x for x in after['streams'] if x['codec_type']=='audio')
    assert nv['display_aspect_ratio']=='4:3' and nv['sample_aspect_ratio']=='127:150'
    for key in ('nb_frames','width','height','codec_name','duration'):assert ov[key]==nv[key]
    for key in ('nb_frames','sample_rate','channels','codec_name','duration'):assert oa[key]==na[key]
    assert TEMP.resolve().parent==VIDEO.resolve().parent==D.resolve()
    previous=sha(VIDEO)
    os.replace(TEMP,VIDEO)
    result=dict(passed=True,metadataOnlyStreamCopy=True,video=str(VIDEO),previousSHA256=previous,
        currentSHA256=sha(VIDEO),frames=int(nv['nb_frames']),durationSeconds=nv['duration'],
        sampleAspectRatio=nv['sample_aspect_ratio'],displayAspectRatio=nv['display_aspect_ratio'],
        audioUnchanged=True,gameplayFramesNotCutOrReencoded=True,temporaryFileRemoved=True,args=args)
    RECEIPT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
