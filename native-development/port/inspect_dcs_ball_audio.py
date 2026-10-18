"""Actual archived ROMs and bounded Ball waveform comparisons, not mix approval."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import wave
import zipfile
import numpy as np
from scipy.signal import correlate,resample_poly
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
names=sys.argv[1:];assert len(names)==2
folders=[BASE/name for name in names]
receipts=[json.loads((folder/'execution.json').read_text()) for folder in folders]
inputs=json.loads((PORT/'generated_dcs/DCS_KANO_BALL_INPUTS.json').read_text())
assert sha((BUILD/'soundp/MK2.PLS').read_bytes())==inputs['stagedPlaylistSHA256']
for folder,receipt,candidate in zip(folders,receipts,(True,False)):
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert ('--sound-candidate' in receipt['testArguments'])==candidate
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    observer=(folder/'autoboot.lua').read_text()
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    assert ':write_u' not in observer and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    assert 'return' not in observer.split('function(address,data,mask)',1)[1].split('end)',1)[0]
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,name in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(name)==b''.join((BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        verify_archive_sockets(archive)
        for chip in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(BUILD/f'{"soundp" if candidate else "soundw"}/U{chip}.ROM').read_bytes()
assert receipts[0]['controllerSHA256']==receipts[1]['controllerSHA256']
assert set(receipts[0]['testArguments'])-{'--sound-candidate'}==set(receipts[1]['testArguments'])
writes=list(csv.DictReader((folders[0]/'native_sound_writes.csv').open()))
events=[]
for high,low in zip(writes,writes[1:]):
    code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    if code in inputs['calls']:
        assert high['address']==low['address']=='01680000'
        events.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),code=code))
rows=list(csv.DictReader((folders[0]/'special.csv').open()))
mirror='--mirror' in receipts[0]['testArguments']
action_key='p2action' if mirror else 'p1action'
victim_hp='p1hp' if mirror else 'p2hp'
starts=[row for i,row in enumerate(rows) if row['mode']=='2' and row[action_key]=='523'
        and (i==0 or rows[i-1][action_key]!='523')]
assert len(events)==len(starts)==13
assert all(abs(event['frame']-int(row['frame']))<=2 for event,row in zip(events,starts))
pcm=(BUILD/'soundp/SNDS/KSKB.SND').read_bytes();assert sha(pcm)==inputs['pcmSHA256']
decoded_bytes=(BUILD/'soundp/SNDS/KSKB.AUD').read_bytes()
decoded=np.frombuffer(decoded_bytes,dtype='<i2').astype(float)
assert len(decoded)==inputs['samples']
reference=resample_poly(decoded,192,125)
results=[]
with wave.open(str(folders[0]/'native_dcs.wav'),'rb') as native,wave.open(str(folders[1]/'native_dcs.wav'),'rb') as control:
    assert native.getparams()==control.getparams() and native.getframerate()==48000 and native.getnchannels()==1
    for event in events:
        begin=max(0,round((event['seconds']-.05)*48000))
        native.setpos(begin);control.setpos(begin)
        delta=np.frombuffer(native.readframes(96000),dtype='<i2').astype(float)-np.frombuffer(control.readframes(96000),dtype='<i2').astype(float)
        measures=[]
        for length in (4096,len(reference)):
            template=reference[:length]
            cross=correlate(delta,template,mode='valid',method='fft')
            lo=max(0,round(event['seconds']*48000)-begin);hi=min(len(cross),lo+4800)
            at=lo+int(np.argmax(np.abs(cross[lo:hi])))
            segment=delta[at:at+length]
            denominator=np.linalg.norm(template)*np.linalg.norm(segment)
            score=float(abs(cross[at])/denominator) if denominator else 0
            measures.append(dict(samples=length,correlation=score,latencySeconds=(begin+at)/48000-event['seconds']))
        assert measures[0]['correlation']>.98
        assert 0<=measures[0]['latencySeconds']<.1
        full=measures[-1]['correlation']>.98
        interruption=None
        if not full:
            finish_call=0x3ae+event['code']-2033
            matches=[]
            for high,low in zip(writes,writes[1:]):
                code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
                if code==finish_call and event['seconds']<float(high['seconds'])<event['seconds']+.5:
                    matches.append(high)
            assert len(matches)==1
            interruption=matches[0]
            assert any(row[victim_hp]=='0' and event['frame']<=int(row['frame'])<=int(interruption['frame'])+2 for row in rows)
            assert event['seconds']+measures[0]['latencySeconds']+4096/48000<float(interruption['seconds'])
        results.append(dict(**event,measurements=measures,fullReferenceMatched=full,
                            nativeFinishHimPreemption=interruption))
report=dict(scope='Bounded native Ball audio diagnostic',nativeRun=names[0],controlRun=names[1],physicalSide=2 if mirror else 1,
    events=results,completeClipMatches=sum(event['fullReferenceMatched'] for event in results),
    decodedSHA256=sha(decoded_bytes),allLaunchesFullyMatched=all(event['fullReferenceMatched'] for event in results),
    provenNativePreemptions=sum(event['nativeFinishHimPreemption'] is not None for event in results),
    finalMixAccepted=False,releaseReady=False,fullPortVerified=False)
output='DCS_BALL_MIRROR_AUDIO_DIAGNOSTIC.json' if mirror else 'DCS_BALL_AUDIO_DIAGNOSTIC.json'
(PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
