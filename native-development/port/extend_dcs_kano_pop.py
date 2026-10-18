"""Bounded native DCS staging for the existing project bubble-pop clip."""
import json
import math
import re
import wave
import numpy as np
from scipy.signal import resample_poly
from prepare_dcs_candidate import ROOT,DEST,OUT,sha

def main():
    receipt=OUT/'DCS_KANO_POP_INPUTS.json'
    assert not receipt.exists(),'Never restage over reviewed sound inputs'
    previous=json.loads((OUT/'DCS_KISS_INPUTS.json').read_text())
    playlist_path=DEST/'MK2.PLS'
    assert sha(playlist_path.read_bytes())==previous['stagedPlaylistSHA256']
    original=playlist_path.read_bytes().decode('latin-1').replace('\r\n','\n')
    source=ROOT/'samples/mk2ks/kano_bubble_pop.wav'
    with wave.open(str(source),'rb') as wav:
        assert wav.getnchannels()==1 and wav.getsampwidth()==2
        rate=wav.getframerate();count=wav.getnframes()
        assert rate in (22050,24000,31250,44100,48000) and 0<count<=rate*2
        values=np.frombuffer(wav.readframes(count),dtype='<i2').astype(np.float64)
    peak=float(np.max(np.abs(values)));assert peak>0
    gain=16384/peak;divisor=math.gcd(rate,31250)
    pcm=resample_poly(values*gain,31250//divisor,rate//divisor,window=('kaiser',8.6))
    pcm=np.clip(np.rint(pcm),-32768,32767).astype('<i2')
    assert len(pcm)<=62500
    duration=math.ceil(len(pcm)/31250*60)+2;assert duration<256
    delay=math.ceil(len(pcm)/240)+2
    calls='\n; MK2KS Kano Friendship bubble pop.\n';playlists='\n'
    for track,event in enumerate(range(2030,2033),1):
        assert not re.search(rf'^\s*(?:playlist\s+)?{event}\b',original,re.M|re.I)
        calls+=f'\t{event}\timmed\t\t{event}\n'
        playlists+=f"\tplaylist\t{event}, {track}, 'Kano bubble pop'\n\t0\tsetvol\t{track}, 100\n\t0\tplay\t{track}, 'kskp', 1\n\t{delay}\tend\n\tend\n"
    marker=re.search(r'^END\s*$',original,re.M);assert marker
    changed=original[:marker.start()]+calls+original[marker.start():]
    changed=changed.replace('\x1a','').rstrip()+'\n'+playlists+'\x1a\n'
    output=DEST/'SNDS/KSKP.SND';assert not output.exists()
    output.write_bytes(pcm.tobytes())
    playlist_path.write_bytes(changed.encode('latin-1'))
    (OUT/'KSKPOP.PLS').write_text(calls+playlists,encoding='ascii')
    report=dict(source=str(source),sourceSHA256=sha(source.read_bytes()),sourceRate=rate,sourceFrames=count,
        peak=peak,gain=gain,region='KSKP',calls=[2030,2031,2032],tableIndex=260,
        priority='sp_effect',duration=duration,playlistDelay=delay,samples=len(pcm),rate=31250,
        pcmSHA256=sha(pcm.tobytes()),previousPlaylistSHA256=previous['stagedPlaylistSHA256'],
        stagedPlaylistSHA256=sha(playlist_path.read_bytes()),maximumInputSeconds=2,
        soundROMsBuilt=False,gameCallerImplemented=False,runtimeVerified=False,
        finalMixAccepted=False,sourceProvenanceFullyReviewed=False,releaseReady=False)
    receipt.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
