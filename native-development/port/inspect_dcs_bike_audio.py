"""Bounded A/B audio measurements; a diagnostic, not release acceptance."""
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
from scipy.signal import correlate, resample_poly

PORT = Path(__file__).resolve().parent
BASE = PORT.parent / 'baseline'
BUILD = BASE / 'mk2-rebuild-main'
sha = lambda data: hashlib.sha256(data).hexdigest().upper()
manifest = json.loads((PORT/'generated_dcs/DCS_BIKE_INPUTS.json').read_text())
announcer=json.loads((PORT/'generated_dcs/DCS_ANNOUNCER_INPUTS.json').read_text())
assert announcer['previousPlaylistSHA256']==manifest['stagedPlaylistSHA256']
kiss=json.loads((PORT/'generated_dcs/DCS_KISS_INPUTS.json').read_text())
pop=json.loads((PORT/'generated_dcs/DCS_KANO_POP_INPUTS.json').read_text())
assert kiss['previousPlaylistSHA256']==announcer['stagedPlaylistSHA256']
assert pop['previousPlaylistSHA256']==kiss['stagedPlaylistSHA256']
verify_latest_playlist()
names=sys.argv[1:] or ['stock_dcs_bike_native128','stock_dcs_bike_control129']
assert len(names)==2
folders = [BASE/name for name in names]
receipts = [json.loads((folder/'execution.json').read_text()) for folder in folders]
for receipt in receipts:
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['gameMemoryWrites'] and not receipt['customDriver']
assert receipts[0]['controllerSHA256'] == receipts[1]['controllerSHA256']
assert set(receipts[0]['testArguments'])-{'--sound-candidate'}==set(receipts[1]['testArguments'])
for lane, chip in enumerate(('mk321u54.bin','mk321u63.bin')):
    assert receipts[0]['replacementChips'][chip] == sha(b''.join(
        (BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')))
for folder, receipt in zip(folders,receipts):
    observer = (folder/'autoboot.lua').read_text()
    assert sha((folder/'autoboot.lua').read_bytes()) == receipt['controllerSHA256']
    assert ':write_u' not in observer
    assert 'return' not in observer.split('function(address,data,mask)',1)[1].split('end)',1)[0]
    assert receipt['emulatorSHA256'] == 'AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
for chip, digest in receipts[0]['replacementChips'].items():
    if 'music_spch' not in chip:
        assert receipts[1]['replacementChips'][chip] == digest
for candidate, receipt in zip((True, False), receipts):
    assert ('--sound-candidate' in receipt['testArguments'])==candidate
    folder=folders[0 if candidate else 1]
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        verify_archive_sockets(archive)
        for chip in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(BUILD/f'{"soundp" if candidate else "soundw"}/U{chip}.ROM').read_bytes()
    for chip in range(2,6):
        assert receipt['replacementChips'][f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}'] == sha(
            (BUILD/f'{"soundp" if candidate else "soundw"}/U{chip}.ROM').read_bytes())
writes = list(csv.DictReader((folders[0]/'native_sound_writes.csv').open()))
events = []
for high, low in zip(writes,writes[1:]):
    code = ((int(high['data'],16)&255)<<8) | (int(low['data'],16)&255)
    if 2003 <= code <= 2008:
        assert high['address'] == low['address'] == '01680000'
        assert high['mask'] == low['mask'] == '0000ffff'
        events.append(dict(frame=int(high['frame']), seconds=float(high['seconds']), code=code))
rows = list(csv.DictReader((folders[0]/'bike.csv').open()))
tail='--bike-audio-tail' in receipts[0]['testArguments']
assert tail == ('--bike-audio-tail' in receipts[1]['testArguments'])
assert int(rows[-1]['frame']) == (9180 if tail else 9000) and all(row['missing']=='0' for row in rows)
for action, calls, expected in ((516,range(2003,2006),11),(532,range(2006,2009),8)):
    starts = [int(row['frame']) for index,row in enumerate(rows)
        if row['mode']=='2' and row['p2char']=='18' and row['p2action']==str(action)
        and (index==0 or rows[index-1]['p2action']!=str(action))]
    observed = [event['frame'] for event in events if event['code'] in calls]
    assert len(starts) == len(observed) == expected, (action,starts,observed)
    assert all(abs(a-b)<=2 for a,b in zip(starts,observed)), (starts,observed)
results = []
launch_fits = []
with wave.open(str(folders[0]/'native_dcs.wav'),'rb') as native, wave.open(str(folders[1]/'native_dcs.wav'),'rb') as control:
    assert native.getparams() == control.getparams()
    assert native.getframerate() == 48000 and native.getnchannels() == 1
    for clip in manifest['clips']:
        assert sha(Path(clip['source']).read_bytes()) == clip['sourceSHA256']
        raw = (BUILD/f'soundp/SNDS/{clip["region"]}.SND').read_bytes()
        assert sha(raw) == clip['pcmSHA256']
        original = np.frombuffer(raw,dtype='<i2').astype(float)
        decoded = np.frombuffer((BUILD/f'soundp/SNDS/{clip["region"]}.AUD').read_bytes(),dtype='<i2').astype(float)
        assert len(original) == len(decoded) == clip['samples']
        codec = correlate(decoded,original,method='fft')
        codec_score = float(np.max(np.abs(codec))/(np.linalg.norm(original)*np.linalg.norm(decoded)))
        assert codec_score > .97
        reference = resample_poly(decoded,192,125)
        for event in events:
            if event['code'] not in clip['calls']:
                continue
            begin = max(0,int((event['seconds']-.05)*48000))
            native.setpos(begin); control.setpos(begin)
            # Maximum two seconds per stream, independent of full recording size.
            delta = np.frombuffer(native.readframes(96000),dtype='<i2').astype(float) - np.frombuffer(control.readframes(96000),dtype='<i2').astype(float)
            # Isolate a simultaneous cry without changing either recording:
            # fit launch gain only on its earlier, cry-free 4096-sample prefix.
            # Never fit launch gain against the cry segment being evaluated.
            removed_launch = None
            if clip['region'] == 'KSBC':
                previous = [fit for fit in launch_fits if 0 < event['seconds']-fit['seconds'] < .5]
                assert len(previous) == 1
                fit = previous[0]
                offset = fit['sample']-begin
                left = max(0,offset); right = min(len(delta),offset+len(fit['reference']))
                delta[left:right] -= fit['gain']*fit['reference'][left-offset:right-offset]
                removed_launch = fit['frame']
            measures = []
            windows = [(0,4096),(0,8192),(0,len(reference))]
            if clip['region'] == 'KSBC':
                windows.append((24000,24000))
            for reference_offset,length in windows:
                template = reference[reference_offset:reference_offset+length]
                cross = correlate(delta,template,mode='valid',method='fft')
                lo = max(0,int(event['seconds']*48000)-begin+reference_offset)
                hi = min(len(cross),lo+4800)
                lag = lo + int(np.argmax(np.abs(cross[lo:hi])))
                segment = delta[lag:lag+length]
                assert len(segment)==len(template)
                if tail and clip['region']=='KSBC' and length==len(reference):
                    assert begin+lag+length<=native.getnframes()
                denominator = np.linalg.norm(template)*np.linalg.norm(segment)
                score = float(abs(cross[lag])/denominator) if denominator else 0.0
                if clip['region'] == 'KSBL' and length == 4096:
                    assert score > .98
                    launch_fits.append(dict(frame=event['frame'],seconds=event['seconds'],sample=begin+lag,
                        reference=reference,gain=float(np.dot(segment,template)/np.dot(template,template))))
                measures.append(dict(referenceOffset=reference_offset,samples=length,correlation=score,
                    latencySeconds=(begin+lag-reference_offset)/48000-event['seconds']))
            results.append(dict(**event,clip=clip['region'],codecCorrelation=codec_score,
                independentlyFittedLaunchRemoved=removed_launch,measurements=measures))
report = dict(scope='Bicycle native DCS bounded waveform diagnostic',events=results,
    nativeRun=names[0],controlRun=names[1],
    activationEvents=11,unblockedCatchEvents=8,
    capturedSoundROMs={f'U{i}.ROM':sha((BUILD/f'soundp/U{i}.ROM').read_bytes()) for i in range(2,6)},
    programLaneSHA256={chip:receipts[0]['replacementChips'][chip] for chip in ('mk321u54.bin','mk321u63.bin')},
    finalMixAccepted=False,releaseReady=False,fullPortVerified=False)
launches = [event for event in results if event['clip']=='KSBL']
cries = [event for event in results if event['clip']=='KSBC']
assert len(launches)==11 and all(event['measurements'][0]['correlation']>.98 for event in launches)
assert len(cries)==8 and all(event['measurements'][-1]['correlation']>.99 for event in cries)
assert all(0<=event['measurements'][-1]['latencySeconds']<.1 for event in cries)
report.update(nativeLaunchPrefixesVerified=11,nativeCryHalfSecondSegmentsVerified=8,
    completeCryTailCoverage=False,gameMemoryWrites=False,customDriver=False)
if tail:
    assert all(event['measurements'][2]['correlation']>.98 for event in cries)
    report.update(completeCryTailCoverage=True,nativeFullCryMatches=8)
(PORT/'generated_dcs/DCS_BIKE_AUDIO_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
