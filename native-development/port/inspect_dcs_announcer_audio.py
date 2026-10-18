"""Bounded own announcer waveform proof on stock MAME; not full-port acceptance."""
import csv
import hashlib
import json
import sys
from pathlib import Path
import wave
import zipfile
from current_graphics import verify_archive_sockets
from current_sound import verify_latest_playlist
import numpy as np
from scipy.signal import correlate,resample_poly

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
inputs=json.loads((PORT/'generated_dcs/DCS_ANNOUNCER_INPUTS.json').read_text())
kiss=json.loads((PORT/'generated_dcs/DCS_KISS_INPUTS.json').read_text())
pop=json.loads((PORT/'generated_dcs/DCS_KANO_POP_INPUTS.json').read_text())
assert kiss['previousPlaylistSHA256']==inputs['stagedPlaylistSHA256']
assert pop['previousPlaylistSHA256']==kiss['stagedPlaylistSHA256']
verify_latest_playlist()
names=sys.argv[1:3] or ['stock_dcs_announce134','stock_dcs_anncontrol135']
assert len(names)==2
kano_wins='--kano-wins' in sys.argv
full='--full-announcements' in sys.argv
folders=[BASE/name for name in names]
receipts=[json.loads((folder/'execution.json').read_text()) for folder in folders]
for folder,receipt in zip(folders,receipts):
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer
    callback=observer.split('function(address,data,mask)',1)[1].split('end)',1)[0]
    assert 'return' not in callback
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
assert receipts[0]['controllerSHA256']==receipts[1]['controllerSHA256']
assert set(receipts[0]['testArguments'])-{'--sound-candidate'}==set(receipts[1]['testArguments'])
for chip,digest in receipts[0]['replacementChips'].items():
    if 'music_spch' not in chip:assert receipts[1]['replacementChips'][chip]==digest
for candidate,receipt in zip((True,False),receipts):
    assert ('--sound-candidate' in receipt['testArguments'])==candidate
    with zipfile.ZipFile(folders[0 if candidate else 1]/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        verify_archive_sockets(archive)
        for i in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{i}_music_spch.u{i}')==(BUILD/f'{"soundp" if candidate else "soundw"}/U{i}.ROM').read_bytes()
    for i in range(2,6):
        assert receipt['replacementChips'][f'l1_mortal_kombat_3_u{i}_music_spch.u{i}']==sha(
            (BUILD/f'{"soundp" if candidate else "soundw"}/U{i}.ROM').read_bytes())
for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
    assert receipts[0]['replacementChips'][chip]==sha(b''.join((BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')))
writes=list(csv.DictReader((folders[0]/'native_sound_writes.csv').open()))
events=[]
for high,low in zip(writes,writes[1:]):
    code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    if 2009<=code<=2020:
        assert high['address']==low['address']=='01680000'
        events.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),code=code))
assert len(events)==(4 if kano_wins else 3)
results=[]
with wave.open(str(folders[0]/'native_dcs.wav'),'rb') as native,wave.open(str(folders[1]/'native_dcs.wav'),'rb') as control:
    assert native.getparams()==control.getparams() and native.getframerate()==48000 and native.getnchannels()==1
    for event in events:
        clip=next(clip for clip in inputs['clips'] if event['code'] in clip['calls'])
        assert sha(Path(clip['source']).read_bytes())==clip['sourceSHA256']
        assert sha((BUILD/f'soundp/SNDS/{clip["region"]}.SND').read_bytes())==clip['pcmSHA256']
        decoded=np.frombuffer((BUILD/f'soundp/SNDS/{clip["region"]}.AUD').read_bytes(),dtype='<i2').astype(float)
        reference=resample_poly(decoded,192,125)
        begin=max(0,int((event['seconds']-.05)*48000))
        native.setpos(begin);control.setpos(begin)
        # Less than2.4 seconds per stream; never load a full-match float array.
        delta=np.frombuffer(native.readframes(115000),dtype='<i2').astype(float)-np.frombuffer(control.readframes(115000),dtype='<i2').astype(float)
        template=reference[:8192]
        c=correlate(delta,template,mode='valid',method='fft')
        lo=int(event['seconds']*48000)-begin;hi=lo+4800
        lag=lo+int(np.argmax(np.abs(c[lo:hi])))
        segment=delta[lag:lag+len(template)]
        score=float(abs(c[lag])/(np.linalg.norm(template)*np.linalg.norm(segment)))
        if not full:
            assert score>.95,(event,score)
        latency=(begin+lag)/48000-event['seconds'];assert 0<=latency<.1
        complete_score=None
        if full:
            cross=correlate(delta,reference,mode='valid',method='fft')
            full_lag=lo+int(np.argmax(np.abs(cross[lo:min(len(cross),hi)])))
            segment=delta[full_lag:full_lag+len(reference)]
            assert len(segment)==len(reference) and begin+full_lag+len(reference)<=native.getnframes()
            complete_score=float(abs(cross[full_lag])/(np.linalg.norm(reference)*np.linalg.norm(segment)))
            assert complete_score>.95,(event,complete_score)
        results.append(dict(**event,actor=clip['actor'],kind=clip['kind'],prefixCorrelation=score,
            fullClipCorrelation=complete_score,outputLatencySeconds=latency))
assert {(r['actor'],r['kind']) for r in results}=={('kano','select'),('sonya','select'),('kano' if kano_wins else 'sonya','wins')}
report=dict(events=results,scope='Own native announcer waveforms in a physical stock-MAME match',
    nativeRun=names[0],controlRun=names[1],
    programLaneSHA256={chip:receipts[0]['replacementChips'][chip] for chip in ('mk321u54.bin','mk321u63.bin')},
    kanoWinRuntimeVerified=kano_wins,completeAnnouncementTailsVerified=full,finalMixAccepted=False,releaseReady=False,fullPortVerified=False)
output='DCS_KANO_ANNOUNCER_AUDIO_DIAGNOSTIC.json' if kano_wins else 'DCS_ANNOUNCER_AUDIO_DIAGNOSTIC.json'
(PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
