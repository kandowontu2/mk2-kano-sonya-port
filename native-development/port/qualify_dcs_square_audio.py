"""Bounded native Square DCS A/B proof; never substitute a sound-port call for audio."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import wave
import zipfile
import numpy as np
from scipy.signal import correlate,resample_poly
from current_graphics import graphics_metadata,verify_archive_sockets
from dcs_source import integrate
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main'
OUT=PORT/'generated_dcs'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
inputs=json.loads((OUT/'DCS_INPUTS.json').read_text())
assert sha(Path(inputs['sourceClip']).read_bytes())==inputs['sourceSHA256']
assert sha((BUILD/'soundp/SNDS/KSSQ.SND').read_bytes())==inputs['stagedPCM_SHA256']
bike_inputs=json.loads((OUT/'DCS_BIKE_INPUTS.json').read_text())
assert bike_inputs['previousPlaylistSHA256']==inputs['stagedPlaylistSHA256']
announcer_inputs=json.loads((OUT/'DCS_ANNOUNCER_INPUTS.json').read_text())
assert announcer_inputs['previousPlaylistSHA256']==bike_inputs['stagedPlaylistSHA256']
kiss_inputs=json.loads((OUT/'DCS_KISS_INPUTS.json').read_text())
pop_inputs=json.loads((OUT/'DCS_KANO_POP_INPUTS.json').read_text())
assert kiss_inputs['previousPlaylistSHA256']==announcer_inputs['stagedPlaylistSHA256']
assert pop_inputs['previousPlaylistSHA256']==kiss_inputs['stagedPlaylistSHA256']
verify_latest_playlist()
assert sha((BUILD/'soundw/MK2.PLS').read_bytes())==inputs['originalPlaylistSHA256']
assert sha((BUILD/'soundp/SNDS/HENRY.EXE').read_bytes())==inputs['HENRYSHA256']
assert sha((BUILD/'soundp/PLBUILD.EXE').read_bytes())==inputs['PLBUILDSHA256']
playlist=(BUILD/'soundp/MK2.PLS').read_text()
for event in (2000,2001,2002):
    assert re.search(rf'^\s*{event}\s+immed\s+{event}\s*$',playlist,re.M)
    assert re.search(rf"playlist\s+{event},\s*{event-1999},\s*'Sonya Square launch'",playlist)
source=(BUILD/'srcp/MKSOUND.ASM').read_text()
marker='\n; MK2KS own native DCS Square launch: playlists2000/2001/2002.\n'
assert source.count(marker)==1
before,extension=source.split(marker)
_,after=extension.split('\ntriple_end\n',1)
assert integrate(before+'\ntriple_end\n'+after)==source
assert (PORT/'asm/SONYAMOV.ASM').read_bytes()==(BUILD/'srcp/SONYAMOV.ASM').read_bytes()
assert re.search(r'calla init_special_act\s+tsound 0feh',(BUILD/'srcp/SONYAMOV.ASM').read_text())
original=np.frombuffer((BUILD/'soundp/SNDS/KSSQ.SND').read_bytes(),dtype='<i2').astype(np.float64)
decoded=np.frombuffer((BUILD/'soundp/SNDS/KSSQ.AUD').read_bytes(),dtype='<i2').astype(np.float64)
assert len(original)==len(decoded)==inputs['samples']
correlation=correlate(decoded,original,method='fft')
at=int(np.argmax(np.abs(correlation)))
codec_score=float(abs(correlation[at])/(np.linalg.norm(original)*np.linalg.norm(decoded)))
assert codec_score>.98 and abs(at-len(original)+1)<100
metadata=graphics_metadata()
cases=[]
names=sys.argv[1:] or ['stock_dcs_square_native130','stock_dcs_square_control131']
assert len(names)==2
for name,candidate in zip(names,(True,False)):
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha((folder/'autoboot.lua').read_bytes())
    assert ('--sound-candidate' in receipt['testArguments'])==candidate
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((BUILD/f'srcp/rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        verify_archive_sockets(archive)
        for chip in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(BUILD/f'{"soundp" if candidate else "soundw"}/U{chip}.ROM').read_bytes()
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        data=b''.join((BUILD/f'srcp/rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        assert receipt['replacementChips'][chip]==sha(data)
    for chip,digest in metadata['sockets'].items(): assert receipt['replacementChips'][chip]==digest
    for chip in range(2,6):
        name=f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}'
        assert receipt['replacementChips'][name]==sha((BUILD/f'{"soundp" if candidate else "soundw"}/U{chip}.ROM').read_bytes())
    rows=list(csv.DictReader((folder/'special.csv').open()))
    assert int(rows[-1]['frame'])==9000 and all(r['missing']=='0' for r in rows)
    starts=[r for i,r in enumerate(rows) if r['mode']=='2' and r['p1char']=='17' and r['p2char']=='18' and r['p2action']=='519'
        and (i==0 or rows[i-1]['p2action']!='519')]
    assert len(starts)==12
    writes=list(csv.DictReader((folder/'native_sound_writes.csv').open()))
    events=[]
    for high,low in zip(writes,writes[1:]):
        code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
        if code in (2000,2001,2002):
            assert high['address']==low['address']=='01680000'
            assert high['mask']==low['mask']=='0000ffff'
            events.append(dict(frame=int(high['frame']),code=code,seconds=float(high['seconds']),writePC=high['pc']))
    assert len(events)==len(starts)
    assert all(abs(event['frame']-int(start['frame']))<=2 for event,start in zip(events,starts))
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    observer=(folder/'autoboot.lua').read_text()
    callback=observer.split('function(address,data,mask)',1)[1].split('end)',1)[0]
    assert 'return' not in callback and ':write_u' not in observer
    cases.append((folder,receipt,events,writes,rows))
assert cases[0][1]['controllerSHA256']==cases[1][1]['controllerSHA256']
assert set(cases[0][1]['testArguments'])-{'--sound-candidate'}==set(cases[1][1]['testArguments'])
assert [(e['frame'],e['code']) for e in cases[0][2]]==[(e['frame'],e['code']) for e in cases[1][2]]
reference=resample_poly(decoded,192,125)
scores=[]
with wave.open(str(cases[0][0]/'native_dcs.wav'),'rb') as native,wave.open(str(cases[1][0]/'native_dcs.wav'),'rb') as control:
    assert native.getparams()==control.getparams()
    assert native.getframerate()==48000 and native.getnchannels()==1 and native.getsampwidth()==2
    for event in cases[0][2]:
        begin=max(0,int((event['seconds']-.05)*48000))
        native.setpos(begin);control.setpos(begin)
        # At most3.4 seconds per stream, regardless of capture length.
        a=np.frombuffer(native.readframes(163200),dtype='<i2').astype(np.float64)
        b=np.frombuffer(control.readframes(163200),dtype='<i2').astype(np.float64)
        delta=a-b
        removed_announcements=[]
        # Own win announcements are absent from the original-bank control.
        # Estimate their gain ONLY after this Square clip must have finished;
        # never fit the nuisance waveform to the launch being verified.
        for high,low in zip(cases[0][3],cases[0][3][1:]):
            if high['pc']!=event['writePC']:
                continue
            code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
            if not (2018<=code<=2020 and .8<float(high['seconds'])-event['seconds']<1.1):
                continue
            clip=next(c for c in announcer_inputs['clips'] if code in c['calls'])
            raw=(BUILD/f'soundp/SNDS/{clip["region"]}.SND').read_bytes()
            assert sha(raw)==clip['pcmSHA256']
            voice=np.frombuffer((BUILD/f'soundp/SNDS/{clip["region"]}.AUD').read_bytes(),dtype='<i2').astype(float)
            voice=resample_poly(voice,192,125)
            offset=24000;template=voice[offset:48000]
            start=int(float(high['seconds'])*48000)-begin
            search_low=start+offset;search_high=search_low+4800
            assert (begin+search_low)/48000>event['seconds']+len(reference)/48000+.1
            cross=correlate(delta,template,mode='valid',method='fft')
            at=search_low+int(np.argmax(np.abs(cross[search_low:search_high])))
            fitted=delta[at:at+len(template)]
            voice_score=float(abs(cross[at])/(np.linalg.norm(template)*np.linalg.norm(fitted)))
            assert voice_score>.95,(event,'Independent win fit failed',voice_score)
            gain=float(np.dot(fitted,template)/np.dot(template,template))
            voice_start=at-offset
            left=max(0,voice_start);right=min(len(delta),voice_start+len(voice))
            delta[left:right]-=gain*voice[left-voice_start:right-voice_start]
            removed_announcements.append(dict(frame=int(high['frame']),code=code,
                independentPostLaunchCorrelation=voice_score,gain=gain))
        c=correlate(delta,reference,mode='valid',method='fft')
        lag=int(np.argmax(np.abs(c)))
        segment=delta[lag:lag+len(reference)]
        score=float(abs(c[lag])/(np.linalg.norm(reference)*np.linalg.norm(segment)))
        preempted=False
        full_score=score
        interruption=None
        active_only=False
        active_score=None
        active_bounds=None
        if score<=.95:
            # A mixed recording need not be silent during the source file's
            # exact digital padding. Verify EVERY nonzero reference sample,
            # retaining the failed whole-file score and a distinct outcome.
            nonzero=np.flatnonzero(reference)
            left,right=int(nonzero[0]),int(nonzero[-1])+1
            template=reference[left:right]
            active_segment=delta[lag+left:lag+right]
            active_score=float(abs(np.dot(active_segment,template))/(
                np.linalg.norm(active_segment)*np.linalg.norm(template)))
            active_bounds=[left,right]
            if active_score>.95:
                active_only=True
                score=active_score
        if score<=.95:
            # Native Finish Him uses base03aeh + effect track index. It may
            # legitimately replace a launch after an actual KO, not play atop it.
            finish_call=0x3ae+(event['code']-2000)
            calls=[]
            for high,low in zip(cases[0][3],cases[0][3][1:]):
                if high['pc']==event['writePC']:
                    code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
                    if code==finish_call and event['seconds']<float(high['seconds'])<event['seconds']+.4:
                        calls.append(high)
            assert len(calls)==1,(event,full_score,'No proven native pre-emption')
            interruption=calls[0]
            assert any(int(r['frame'])>=event['frame'] and int(r['frame'])<=int(interruption['frame'])+2
                and r['p1hp']=='0' for r in cases[0][4])
            prefix=reference[:5120]
            prefix_c=correlate(delta,prefix,mode='valid',method='fft')
            low=max(0,int(event['seconds']*48000)-begin)
            high=min(len(prefix_c),low+4800)
            lag=low+int(np.argmax(np.abs(prefix_c[low:high])))
            segment=delta[lag:lag+len(prefix)]
            score=float(abs(prefix_c[lag])/(np.linalg.norm(prefix)*np.linalg.norm(segment)))
            assert score>.95,(event,full_score,score)
            assert (begin+lag+len(prefix))/48000<float(interruption['seconds'])
            preempted=True
        delay=(begin+lag)/48000-event['seconds']
        assert 0<=delay<.10
        scores.append(dict(**event,decodedClipCorrelation=score,fullClipCorrelation=full_score,
            independentlyRemovedWinAnnouncements=removed_announcements,
            completeNonzeroReferenceMatched=active_only,nonzeroReferenceBounds=active_bounds,
            nonzeroReferenceCorrelation=active_score,
            fullClipMatched=not preempted and not active_only,nativeFinishHimPreemption=preempted,
            interruptionFrame=int(interruption['frame']) if interruption else None,
            outputLatencySeconds=delay))
full_count=sum(s['fullClipMatched'] for s in scores)
active_count=sum(s['completeNonzeroReferenceMatched'] for s in scores)
assert full_count+active_count==11
assert sum(s['nativeFinishHimPreemption'] for s in scores)==1
report=dict(scope='Twelve own Sonya Square launch cues through original DCS ROM tools and stock MAME',
    nativeRun=names[0],controlRun=names[1],
    originalCodecRoundtripCorrelation=codec_score,nativeLaunches=12,controlLaunches=12,
    fullClipMatches=full_count,completeNonzeroReferenceMatches=active_count,provenNativeFinishHimPreemptions=1,
    actualPortEvents=scores,programLaneSHA256={name:cases[0][1]['replacementChips'][name] for name in ('mk321u54.bin','mk321u63.bin')},
    soundROM_SHA256={f'U{i}.ROM':sha((BUILD/f'soundp/U{i}.ROM').read_bytes()) for i in range(2,6)},
    nativeWAV_SHA256=sha((cases[0][0]/'native_dcs.wav').read_bytes()),
    controlWAV_SHA256=sha((cases[1][0]/'native_dcs.wav').read_bytes()),
    hostSampleDevice=False,observerChangesWrites=False,gameMemoryWrites=False,
    nativeSquareAudioVerified=True,finalMixAccepted=False,otherMoveAudioVerified=False,
    sourceVoiceProvenanceFullyReviewed=False,releaseReady=False,fullPortVerified=False)
(OUT/'DCS_SQUARE_AUDIO_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='actualPortEvents'},indent=2))
