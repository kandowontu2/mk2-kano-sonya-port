"""Stage four existing own announcer clips with original native sound tools."""
import json
import math
import re
import wave
import numpy as np
from scipy.signal import resample_poly
from prepare_dcs_candidate import ROOT,DEST,OUT,sha

def main():
    foundation=json.loads((OUT/'DCS_BIKE_INPUTS.json').read_text())
    audit=json.loads((OUT/'ANNOUNCER_ROUTE_AUDIT.json').read_text())
    assert not (OUT/'DCS_ANNOUNCER_INPUTS.json').exists()
    assert sha((DEST/'MK2.PLS').read_bytes())==foundation['stagedPlaylistSHA256']
    original=(DEST/'MK2.PLS').read_bytes().decode('latin-1').replace('\r\n','\n')
    clips=[];calls='\n; MK2KS native own announcer calls.\n';playlists='\n'
    specs=(('kano','select','KSKN',2009),('sonya','select','KSSN',2012),
           ('kano','wins','KSKW',2015),('sonya','wins','KSSW',2018))
    for actor,suffix,region,first in specs:
        source=ROOT/f'samples/mk2ks/{actor}_{suffix}.wav'
        pinned=next(c for r in audit['routes'] if r['name']==actor for c in r['availableClips'] if c['file']==str(source))
        assert sha(source.read_bytes())==pinned['sha256']
        with wave.open(str(source),'rb') as wav:
            assert wav.getnchannels()==1 and wav.getsampwidth()==2
            rate=wav.getframerate();frames=wav.getnframes()
            samples=np.frombuffer(wav.readframes(frames),dtype='<i2').astype(float)
        gain=16384/float(np.max(np.abs(samples)))
        divisor=math.gcd(rate,31250)
        pcm=resample_poly(samples*gain,31250//divisor,rate//divisor,window=('kaiser',8.6))
        pcm=np.clip(np.rint(pcm),-32768,32767).astype('<i2')
        output=DEST/f'SNDS/{region}.SND';assert not output.exists()
        output.write_bytes(pcm.tobytes())
        delay=math.ceil(len(pcm)/240)+2
        for track,event in enumerate(range(first,first+3),1):
            assert not re.search(rf'^\s*(?:playlist\s+)?{event}\b',original,re.M|re.I)
            calls+=f'\t{event}\timmed\t\t{event}\n'
            playlists+=f"\tplaylist\t{event}, {track}, '{actor} {suffix}'\n"
            playlists+=f"\t0\tsetvol\t{track}, 100\n\t0\tplay\t{track}, '{region.lower()}', 1\n\t{delay}\tend\n\tend\n"
        clips.append(dict(actor=actor,kind=suffix,region=region,calls=list(range(first,first+3)),
            source=str(source),sourceSHA256=pinned['sha256'],gain=gain,samples=len(pcm),
            duration=math.ceil(len(pcm)/31250*60)+2,pcmSHA256=sha(pcm.tobytes())))
    marker=re.search(r'^END\s*$',original,re.M);assert marker
    changed=original[:marker.start()]+calls+original[marker.start():]
    changed=changed.replace('\x1a','').rstrip()+'\n'+playlists+'\x1a\n'
    (DEST/'MK2.PLS').write_bytes(changed.encode('latin-1'))
    (OUT/'KSANNOUNCE.PLS').write_text(calls+playlists,encoding='ascii')
    report=dict(clips=clips,previousPlaylistSHA256=foundation['stagedPlaylistSHA256'],
        stagedPlaylistSHA256=sha((DEST/'MK2.PLS').read_bytes()),runtimeVerified=False,
        finalMixAccepted=False,sourceVoiceProvenanceFullyReviewed=False,releaseReady=False)
    (OUT/'DCS_ANNOUNCER_INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
