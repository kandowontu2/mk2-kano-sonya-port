"""Bounded three-cue flame-kiss waveform investigation, with pinned ROMs."""
import csv
import hashlib
import json
from pathlib import Path
import wave
import sys
import zipfile
from current_graphics import verify_archive_sockets
from current_sound import verify_latest_playlist
import numpy as np
from scipy.signal import correlate,resample_poly

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
inputs=json.loads((PORT/'generated_dcs/DCS_KISS_INPUTS.json').read_text())
pop=json.loads((PORT/'generated_dcs/DCS_KANO_POP_INPUTS.json').read_text())
assert pop['previousPlaylistSHA256']==inputs['stagedPlaylistSHA256']
verify_latest_playlist()
names=sys.argv[1:] or ['stock_dcs_kiss144','stock_dcs_kissctrl145']
assert len(names)==2
folders=[BASE/name for name in names]
receipts=[json.loads((folder/'execution.json').read_text()) for folder in folders]
for folder,receipt in zip(folders,receipts):
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer
    assert 'return' not in observer.split('function(address,data,mask)',1)[1].split('end)',1)[0]
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
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
    if 2021<=code<=2029:
        assert high['address']==low['address']=='01680000'
        events.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),code=code))
assert len(events)==3 and events[1]['frame']==events[2]['frame']
references={};codecs={}
for clip in inputs['clips']:
    assert sha(Path(clip['source']).read_bytes())==clip['sourceSHA256']
    raw=(BUILD/f'soundp/SNDS/{clip["region"]}.SND').read_bytes()
    assert sha(raw)==clip['pcmSHA256']
    original=np.frombuffer(raw,dtype='<i2').astype(float)
    decoded=np.frombuffer((BUILD/f'soundp/SNDS/{clip["region"]}.AUD').read_bytes(),dtype='<i2').astype(float)
    assert len(original)==len(decoded)==clip['samples']
    cross=correlate(decoded,original,method='fft')
    codecs[clip['region']]=float(np.max(np.abs(cross))/(np.linalg.norm(original)*np.linalg.norm(decoded)))
    references[clip['region']]=resample_poly(decoded,192,125)
begin=int((events[0]['seconds']-.05)*48000)
with wave.open(str(folders[0]/'native_dcs.wav'),'rb') as native,wave.open(str(folders[1]/'native_dcs.wav'),'rb') as control:
    assert native.getparams()==control.getparams() and native.getframerate()==48000 and native.getnchannels()==1
    captured_frames=native.getnframes()
    native.setpos(begin);control.setpos(begin)
    # One six-second fatality window, not full-match floating point recordings.
    delta=np.frombuffer(native.readframes(288000),dtype='<i2').astype(float)-np.frombuffer(control.readframes(288000),dtype='<i2').astype(float)

def measure(signal,reference,event,offset,length):
    template=reference[offset:offset+length]
    assert len(template)==length
    cross=correlate(signal,template,mode='valid',method='fft')
    low=int(event['seconds']*48000)-begin+offset
    high=min(len(cross),low+4800)
    at=low+int(np.argmax(np.abs(cross[low:high])))
    segment=signal[at:at+length]
    score=float(abs(cross[at])/(np.linalg.norm(template)*np.linalg.norm(segment)))
    gain=float(np.dot(segment,template)/np.dot(template,template))
    return dict(correlation=score,referenceOffset=offset,samples=length,
        start=at-offset,gain=gain,latencySeconds=(begin+at-offset)/48000-event['seconds'])

win_events=[]
for high,low in zip(writes,writes[1:]):
    code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    if high['pc']==writes[0]['pc'] and 2018<=code<=2020 and 0<float(high['seconds'])-events[1]['seconds']<4:
        win_events.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),code=code))
assert len(win_events)==1
win_reference=resample_poly(np.frombuffer((BUILD/'soundp/SNDS/KSSW.AUD').read_bytes(),dtype='<i2').astype(float),192,125)
win=measure(delta,win_reference,win_events[0],57600,12000)
clean=delta.copy()
left=win['start'];right=min(len(clean),left+len(win_reference))
clean[left:right]-=win['gain']*win_reference[:right-left]
kiss=measure(clean,references['KSKI'],events[0],0,24000)
# Independent fire window after the victim clip ends, but before the native
# flawless-victory tone replaces this track. No victim fitting sets fire gain.
fire_offset=len(references['KSBV'])+32
fire=measure(clean,references['KSBF'],events[1],fire_offset,4096)
residual=clean.copy()
for fit,region in ((kiss,'KSKI'),(fire,'KSBF')):
    reference=references[region]
    left=max(0,fit['start']);right=min(len(residual),fit['start']+len(reference))
    residual[left:right]-=fit['gain']*reference[left-fit['start']:right-fit['start']]
victim=measure(residual,references['KSBV'],events[2],0,len(references['KSBV']))
def subtract(signal,fit,reference):
    result=signal.copy()
    left=max(0,fit['start']);right=min(len(result),fit['start']+len(reference))
    result[left:right]-=fit['gain']*reference[left-fit['start']:right-fit['start']]
    return result

fire_track=events[1]['code']-2024+1
flaw_call=578+fire_track-1
flaw_events=[]
for high,low in zip(writes,writes[1:]):
    code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    if high['pc']==writes[0]['pc'] and code==flaw_call and 2.75<float(high['seconds'])-events[1]['seconds']<4:
        flaw_events.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),code=code))
nonflawless='--nonflawless' in receipts[0]['testArguments']
assert len(flaw_events)==(0 if nonflawless else 1)
playlist=(BUILD/'soundp/MK2.PLS').read_text()
import re
assert re.search(rf"playlist\s+{flaw_call},\s*{fire_track},\s*'FX: Flawless Victory tone'",playlist)
assert re.search(rf"play\s+{fire_track},\s*'flawtone'",playlist)
# The independent fire fitting interval is after the WHOLE victim reference
# and ends before the observed native replacement command.
assert fire['start']+fire_offset>=victim['start']+len(references['KSBV'])
if flaw_events:
    assert (begin+fire['start']+fire_offset+4096)/48000<flaw_events[0]['seconds']
fire_signal=subtract(subtract(clean,kiss,references['KSKI']),victim,references['KSBV'])
prefix_length=len(references['KSBF']) if nonflawless else int((flaw_events[0]['seconds']-events[1]['seconds']-.05)*48000)
fire_prefix=measure(fire_signal,references['KSBF'],events[1],0,prefix_length)
kiss_signal=subtract(subtract(clean,fire,references['KSBF']),victim,references['KSBV'])
kiss_complete=measure(kiss_signal,references['KSKI'],events[0],0,len(references['KSKI']))
windows={region:[measure(clean,references[region],events[index],offset,12000)
    for offset in range(0,len(references[region])-12000,24000)]
    for region,index in (('KSBF',1),('KSBV',2))}
assert min(codecs.values())>.98
assert win['correlation']>.99 and kiss['correlation']>.99 and fire['correlation']>.99
assert kiss_complete['correlation']>.98 and victim['correlation']>.98 and fire_prefix['correlation']>.98
assert win['start']+57600>=fire['start']+len(references['KSBF'])
if flaw_events:
    assert (begin+fire_prefix['start']+prefix_length)/48000<flaw_events[0]['seconds']
else:
    assert fire_prefix['start']+prefix_length<=len(fire_signal)
    assert begin+fire_prefix['start']+prefix_length<=captured_frames
assert all(0<=fit['latencySeconds']<.1 for fit in (kiss,fire,victim,win,kiss_complete,fire_prefix))
for folder in folders:
    behavior=json.loads((folder/'SPECIAL_ROOT_REGRESSION.json').read_text())
    assert behavior['currentFullROMVerified']
    assert behavior['behavior']['naturalKnockoutsBeforeFatality']==2
    assert behavior['behavior']['nativeCompletionObserved']
    if nonflawless:
        rows=list(csv.DictReader((folder/'kiss.csv').open()))
        finishing=next(row for row in rows if row['winner']=='3')
        assert 0<int(finishing['p1hp'])<161
report=dict(scope='Three native flame-kiss audio cues; bounded mixture investigation',events=events,
    nativeRun=names[0],controlRun=names[1],
    originalCodecCorrelations=codecs,kissPrefix=kiss,independentFireTail=fire,
    independentPostFireWinFit=win,
    nativeSameTrackFlawlessPreemption=flaw_events[0] if flaw_events else None,
    fireUntilBeforePreemption=fire_prefix if flaw_events else None,
    completeUninterruptedFire=fire_prefix if nonflawless else None,
    completeKissAfterIndependentBurnSubtraction=kiss_complete,
    mixedSignalHalfSecondSpacedWindows=windows,
    victimAfterIndependentKissAndFireSubtraction=victim,
    programLaneSHA256={chip:receipts[0]['replacementChips'][chip] for chip in ('mk321u54.bin','mk321u63.bin')},
    soundROM_SHA256={f'U{i}.ROM':sha((BUILD/f'soundp/U{i}.ROM').read_bytes()) for i in range(2,6)},
    boundedCuePlaybackVerified=True,completeKissAndVictimReferencesMatched=True,
    fireWholeReferenceMatched=nonflawless,nativeFlawlessInterruptionVerified=bool(flaw_events),
    audioQualified=False,finalMixAccepted=False,releaseReady=False,fullPortVerified=False)
output='DCS_KISS_NONFLAWLESS_AUDIO_DIAGNOSTIC.json' if nonflawless else 'DCS_KISS_AUDIO_DIAGNOSTIC.json'
(PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
