"""Stage four native Friendship variants, with original per-record hold times."""
import json
import math
import re
from prepare_dcs_candidate import ROOT,DEST,OUT,sha
from prepare_chicken_pcm import encode,NAMES

def main():
    receipt=OUT/'DCS_CHICKEN_INPUTS.json';assert not receipt.exists()
    previous=json.loads((OUT/'DCS_KANO_BALL_INPUTS.json').read_text())
    path=DEST/'MK2.PLS';assert sha(path.read_bytes())==previous['stagedPlaylistSHA256']
    original=path.read_bytes().decode('latin-1').replace('\r\n','\n')
    clips=[];calls='\n; MK2KS native Sonya Friendship clucks.\n';playlists='\n'
    outputs=[]
    for index,(name,hold) in enumerate(zip(NAMES,(16,23,20,18))):
        pcm,metadata=encode(ROOT/'samples/mk2ks'/f'{name}.wav')
        region=f'KSC{index}';first=2036+index*3
        output=DEST/f'SNDS/{region}.SND';assert not output.exists()
        outputs.append((output,pcm))
        # Original two-block allowance already contains the one-block guard.
        delay=math.ceil(metadata['unpaddedSamples']/240)+2
        assert len(pcm)//2<=delay*240
        for track,event in enumerate(range(first,first+3),1):
            assert not re.search(rf'^\s*(?:playlist\s+)?{event}\b',original,re.M|re.I)
            calls+=f'\t{event}\timmed\t\t{event}\n'
            playlists+=f"\tplaylist\t{event}, {track}, 'Sonya Friendship {index}'\n\t0\tsetvol\t{track}, 100\n\t0\tplay\t{track}, '{region.lower()}', 1\n\t{delay}\tend\n\tend\n"
        metadata.update(region=region,calls=list(range(first,first+3)),tableIndex=262+index,
                        priority='sp_woosh1',duration=hold)
        clips.append(metadata)
    marker=re.search(r'^END\s*$',original,re.M);assert marker
    changed=original[:marker.start()]+calls+original[marker.start():]
    changed=changed.replace('\x1a','').rstrip()+'\n'+playlists+'\x1a\n'
    for output,pcm in outputs:output.write_bytes(pcm)
    path.write_bytes(changed.encode('latin-1'))
    (OUT/'KSCHICK.PLS').write_text(calls+playlists,encoding='ascii')
    report=dict(clips=clips,previousPlaylistSHA256=previous['stagedPlaylistSHA256'],
                stagedPlaylistSHA256=sha(path.read_bytes()),soundROMsBuilt=False,
                runtimeVerified=False,releaseReady=False)
    receipt.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
