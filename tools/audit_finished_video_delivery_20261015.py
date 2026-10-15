"""Completion audit for both full campaigns and both complete-movelist videos.

Reads current artifacts and decodes actual AV. Never infers completion from a
status note, plan, old hash or the successful non-recording benchmark alone.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import qualify_sonya_complete_video_bench_20261015 as full

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_finished_video_delivery_20261015'
FF=shutil.which('ffmpeg');FP=shutil.which('ffprobe')

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()

def native_rows(path):
    tags={'RESULT','FIGHT','WIN','PICTURE','TEXT','ENDING_START','ENDING_COMPLETED','HOST_BOUND'}
    rows=[];digest=hashlib.sha256()
    with path.open() as f:
        for line in f:
            if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
            assert ' writes=0 assistance=none ' in line
            digest.update((line.rstrip('\r\n')+'\n').encode())
            tag=line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
            if tag in tags:rows.append((tag,dict(full.RX.findall(line))))
    return rows,digest.hexdigest().upper()

def decode(path):
    p=subprocess.run([FF,'-v','error','-xerror','-nostdin','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','NUL'],capture_output=True,timeout=60,creationflags=0x08000000)
    assert p.returncode==0 and not p.stderr,'Actual complete AV decode: '+str(path)
    p=subprocess.run([FF,'-hide_banner','-loglevel','info','-nostdin','-i',str(path),'-map','0:a:0','-af','volumedetect','-f','null','NUL'],capture_output=True,timeout=45,creationflags=0x08000000)
    assert p.returncode==0
    text=p.stderr.decode(errors='replace');m=re.search(r'max_volume: ([-\d.]+) dB',text)
    assert m and float(m[1])>-85,'Native audio is not silent'
    return dict(entireVideoAndAudioDecodePassed=True,audioPeakDBFS=float(m[1]))

def main():
    assert not OUT.exists()
    sonya=ROOT/'video_sonya_final_20261015';sv=json.loads((sonya/'verification.json').read_text())
    assert sv['passed'] and sv['fullPlaythrough'] and sv['temporaryWAVDeleted']
    sfile=sonya/'Sonya_full_playthrough.mp4'
    sar=json.loads((sonya/'aspect_verification.json').read_text())
    assert sar['passed'] and sar['metadataOnlyStreamCopy'] and sar['audioUnchanged'] and sar['gameplayFramesNotCutOrReencoded']
    assert sha(sfile)==sar['currentSHA256'] and sv['finalSHA256']==sar['previousSHA256']
    srows,sdigest=native_rows(sonya/'run.log');sproof=full.gate(srows)
    bench=ROOT/'video_sonya_shao_counter_bench_20261015';_,bdigest=native_rows(bench/'run.log')
    prep=ROOT/'video_sonya_final_20261015_preparation'
    assert (prep/'campaign.lua').read_bytes().startswith((ROOT/'video_sonya_shao_counter_bench_20261015_preparation/campaign.lua').read_bytes()),'Identical qualified physical-policy bytes'
    kano=ROOT/'video_kano_full_20261015';kv=json.loads((kano/'verification.json').read_text());aspect=json.loads((kano/'aspect_verification.json').read_text())
    assert kv['passed'] and kv['fullPlaythrough'] and aspect['passed'] and aspect['metadataOnlyStreamCopy'] and aspect['audioUnchanged'] and aspect['gameplayFramesNotCutOrReencoded']
    kfile=kano/'Kano_full_playthrough.mp4';assert sha(kfile)==aspect['currentSHA256'] and kv['finalSHA256']==aspect['previousSHA256']
    krows,_=native_rows(kano/'run.log')
    # Same full-campaign gate with only native character identity mapped.
    mapped=[(t,{k:('18:18' if k=='human' and v=='17:17' else '18' if k in ('id','roster') and v=='17' else v) for k,v in r.items()}) for t,r in krows]
    kproof=full.gate(mapped)
    sproof.pop('videoStillRequired',None);kproof.pop('videoStillRequired',None)
    for folder,clip in ((sonya,sfile),(kano,kfile)):
        assert not (folder/'native_audio.wav').exists() and not (folder/'video.mp4').exists()
        p=subprocess.run([FP,'-v','error','-show_streams','-show_format','-of','json',str(clip)],capture_output=True,text=True,check=True,timeout=10,creationflags=0x08000000)
        v=next(x for x in json.loads(p.stdout)['streams'] if x['codec_type']=='video')
        assert v['width']==400 and v['height']==254 and v['sample_aspect_ratio']=='127:150' and v['display_aspect_ratio']=='4:3'
    showcase=ROOT/'videos_showcase_20261015';guide=json.loads((showcase/'DELIVERY_VERIFICATION.json').read_text())
    assert guide['passed'] and sha(ROOT/'MK2_KANO_SONYA_MOVES.txt')==guide['movelistSHA256']
    records=[]
    for actor,clip,proof in [('kano',kfile,kproof),('sonya',sfile,sproof)]:
        records.append(dict(kind='full_playthrough',fighter=actor,file=str(clip),sha256=sha(clip),nativeProof=proof,AV=decode(clip)))
    for item in guide['characters']:
        clip=Path(item['file']);assert sha(clip)==item['sha256'] and len(item['chapters'])==18
        records.append(dict(kind='complete_movelist_showcase',fighter=item['fighter'],file=str(clip),sha256=sha(clip),chapters=item['chapters'],AV=decode(clip)))
    OUT.mkdir()
    report=dict(passed=True,requestedVideos=records,sonyaActualNativeLogMatchesQualifiedBenchmark=sdigest==bdigest,sonyaNativeLogSHA256=sdigest,benchmarkNativeLogSHA256=bdigest,allFourActualAVFilesDecoded=True,fullCampaignsIncludeContinues=True,gameDifficultyHealthAIUnchanged=True,goalCompletionStillRequiresFinalSonyaVisualReview=True,showcaseVisualReviewReceiptSHA256=sha(showcase/'DELIVERY_VERIFICATION.json'))
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(OUT/'report.json')

if __name__=='__main__':main()
