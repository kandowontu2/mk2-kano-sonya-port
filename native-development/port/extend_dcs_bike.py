"""Append own bicycle launch/cry regions to the verified native sound candidate."""
import json
import math
import re
import wave
import numpy as np
from scipy.signal import resample_poly
from prepare_dcs_candidate import PORT,ROOT,DEST,OUT,sha

def main():
    foundation=json.loads((OUT/'DCS_INPUTS.json').read_text())
    assert not (OUT/'DCS_BIKE_INPUTS.json').exists(), 'Never overwrite a staged extension'
    assert sha((DEST/'MK2.PLS').read_bytes())==foundation['stagedPlaylistSHA256']
    original=(DEST/'MK2.PLS').read_bytes().decode('latin-1').replace('\r\n','\n')
    assert not re.search(r'^\s*(?:playlist\s+)?200[3-8]\b',original,re.M|re.I)
    clips=[];calls='\n; MK2KS Bicycle native launch and paired cry.\n';playlists='\n'
    for label,filename,region,first,index,priority in (
        ('Bicycle launch','sonya_bicycle_launch.wav','KSBL',2003,255,'sp_attkv1'),
        ('Bicycle paired cry','sonya_bicycle_cry.wav','KSBC',2006,256,'sp_bikeyl')):
        source=ROOT/'samples/mk2ks'/filename
        with wave.open(str(source),'rb') as clip:
            assert clip.getnchannels()==1 and clip.getsampwidth()==2
            rate=clip.getframerate();frames=clip.getnframes()
            samples=np.frombuffer(clip.readframes(frames),dtype='<i2').astype(np.float64)
        peak=float(np.max(np.abs(samples)));assert peak>0
        divisor=math.gcd(rate,31250);gain=16384/peak
        pcm=resample_poly(samples*gain,31250//divisor,rate//divisor,window=('kaiser',8.6))
        pcm=np.clip(np.rint(pcm),-32768,32767).astype('<i2')
        assert len(pcm)==math.ceil(frames*31250/rate)
        destination=DEST/'SNDS'/f'{region}.SND';assert not destination.exists()
        destination.write_bytes(pcm.tobytes())
        delay=math.ceil(len(pcm)/240)+2
        duration=math.ceil(len(pcm)/31250*60)+2
        for track,event in enumerate(range(first,first+3),1):
            calls+=f'\t{event}\timmed\t\t{event}\n'
            playlists+=f"\tplaylist\t{event}, {track}, 'Sonya {label}'\n"
            playlists+=f"\t0\tsetvol\t{track}, 100\n\t0\tplay\t{track}, '{region.lower()}', 1\n\t{delay}\tend\n\tend\n"
        clips.append(dict(label=label,source=str(source),sourceSHA256=sha(source.read_bytes()),
            sourceRate=rate,sourceFrames=frames,sourcePeak=peak,gain=gain,region=region,
            pcmSHA256=sha(pcm.tobytes()),samples=len(pcm),rate=31250,
            calls=list(range(first,first+3)),tableIndex=index,priority=priority,duration=duration,playlistDelay=delay))
    marker=re.search(r'^END\s*$',original,re.M);assert marker
    changed=original[:marker.start()]+calls+original[marker.start():]
    changed=changed.replace('\x1a','').rstrip()+'\n'+playlists+'\x1a\n'
    (DEST/'MK2.PLS').write_bytes(changed.encode('latin-1'))
    (OUT/'KSBIKE.PLS').write_text(calls+playlists,encoding='ascii')
    report=dict(clips=clips,previousPlaylistSHA256=foundation['stagedPlaylistSHA256'],
        stagedPlaylistSHA256=sha((DEST/'MK2.PLS').read_bytes()),finalMixAccepted=False,
        sourceVoiceProvenanceFullyReviewed=False,runtimeVerified=False,fullPortVerified=False)
    (OUT/'DCS_BIKE_INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
