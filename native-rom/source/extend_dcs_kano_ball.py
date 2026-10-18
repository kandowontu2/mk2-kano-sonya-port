"""Stage a ROM-resident Kano Ball cue; no custom emulator/sample device."""
import json
import math
import re
import wave
import numpy as np
from scipy.signal import resample_poly
from prepare_dcs_candidate import ROOT,DEST,OUT,sha

SOURCE_SHA='3D2FB8BD79C818AA2079B10E869D3F1CF444B914582DB560CA64D4408EE57BD7'

def encode(source):
    assert sha(source.read_bytes())==SOURCE_SHA
    with wave.open(str(source),'rb') as wav:
        assert wav.getnchannels()==1 and wav.getsampwidth()==2
        rate=wav.getframerate();count=wav.getnframes()
        assert 0<count<=rate*2
        data=np.frombuffer(wav.readframes(count),dtype='<i2').astype(np.float64)
    peak=float(np.max(np.abs(data)));assert peak>0
    gain=16384/peak;divisor=math.gcd(rate,31250)
    pcm=resample_poly(data*gain,31250//divisor,rate//divisor,window=('kaiser',8.6))
    pcm=np.clip(np.rint(pcm),-32768,32767).astype('<i2')
    return pcm,dict(source=str(source),sourceSHA256=SOURCE_SHA,sourceRate=rate,
                   sourceFrames=count,peak=peak,gain=gain,samples=len(pcm))

def main():
    receipt=OUT/'DCS_KANO_BALL_INPUTS.json'
    assert not receipt.exists()
    previous=json.loads((OUT/'DCS_KANO_POP_INPUTS.json').read_text())
    path=DEST/'MK2.PLS';assert sha(path.read_bytes())==previous['stagedPlaylistSHA256']
    original=path.read_bytes().decode('latin-1').replace('\r\n','\n')
    source=ROOT/'samples/mk2ks/kano_ball_launch.wav'
    pcm,metadata=encode(source)
    calls='\n; MK2KS native Kano Ball voice.\n';playlists='\n'
    delay=math.ceil(len(pcm)/240)+2
    for track,event in enumerate(range(2033,2036),1):
        assert not re.search(rf'^\s*(?:playlist\s+)?{event}\b',original,re.M|re.I)
        calls+=f'\t{event}\timmed\t\t{event}\n'
        playlists+=f"\tplaylist\t{event}, {track}, 'Kano Ball launch'\n\t0\tsetvol\t{track}, 100\n\t0\tplay\t{track}, 'kskb', 1\n\t{delay}\tend\n\tend\n"
    marker=re.search(r'^END\s*$',original,re.M);assert marker
    changed=original[:marker.start()]+calls+original[marker.start():]
    changed=changed.replace('\x1a','').rstrip()+'\n'+playlists+'\x1a\n'
    output=DEST/'SNDS/KSKB.SND';assert not output.exists()
    output.write_bytes(pcm.tobytes());path.write_bytes(changed.encode('latin-1'))
    (OUT/'KSKBALL.PLS').write_text(calls+playlists,encoding='ascii')
    metadata.update(region='KSKB',calls=[2033,2034,2035],tableIndex=261,
        priority='sp_attkv1',duration=math.ceil(len(pcm)/31250*60)+2,
        rate=31250,pcmSHA256=sha(pcm.tobytes()),playlistDelay=delay,
        previousPlaylistSHA256=previous['stagedPlaylistSHA256'],
        stagedPlaylistSHA256=sha(path.read_bytes()),soundROMsBuilt=False,
        gameCallerImplemented=False,runtimeVerified=False,releaseReady=False)
    receipt.write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metadata,indent=2))

if __name__=='__main__':main()
