"""Bounded pop-cue/waveform diagnostic; never load a whole match into floats."""
import csv
import json
import math
import re
from pathlib import Path
import sys
import wave
import zipfile
import numpy as np
from scipy.signal import correlate,resample_poly
from build_arm_rip_assets import sha
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
run=BASE/(sys.argv[1] if len(sys.argv)>1 else 'stock_wolf_game363')
receipt=json.loads((run/'execution.json').read_text())
assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['gameMemoryWrites'] and not receipt['customDriver']
assert receipt['nativeDCSAudio']['nonSilent'] and not receipt['nativeDCSAudio']['hostSampleDevice']
inputs=json.loads((PORT/'generated_dcs/DCS_KANO_POP_INPUTS.json').read_text())
verify_latest_playlist()
with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
    for chip in range(2,6):
        name=f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}'
        assert archive.read(name)==(BASE/f'mk2-rebuild-main/soundp/U{chip}.ROM').read_bytes()
writes=list(csv.DictReader((run/'native_sound_writes.csv').open()))
events=[]
for high,low in zip(writes,writes[1:]):
    code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    if code in inputs['calls']:
        assert high['address']==low['address']=='01680000'
        events.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),code=code))
assert len(events)==1
rows=list(csv.DictReader((run/'friend.csv').open()))
active=[r for r in rows if r['death']=='7']
first=int(active[0]['frame']);age=events[0]['frame']-first
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BASE/'mk2-rebuild-main/srcp/MK2P.MAP').read_text())}
pop=[r for r in active if int(r['childshape'],16)==symbols['ks_friend_pose_ff9d2750']]
assert pop and int(pop[0]['frame'])-first==183
# Port taps occur before frame_done updates its counter; compare the actual pose.
assert abs(events[0]['frame']-int(pop[0]['frame']))<=1,age
pcm_path=BASE/'mk2-rebuild-main/soundp/SNDS/KSKP.SND'
pcm=pcm_path.read_bytes();assert sha(pcm)==inputs['pcmSHA256']
reference=np.frombuffer(pcm,dtype='<i2').astype(np.float64)
decoded_path=pcm_path.with_suffix('.AUD')
decoded_bytes=decoded_path.read_bytes()
decoded=np.frombuffer(decoded_bytes,dtype='<i2').astype(np.float64)
assert len(reference)==len(decoded)==inputs['samples']
codec_score=float(abs(np.dot(reference,decoded))/(np.linalg.norm(reference)*np.linalg.norm(decoded)))
reference=decoded
start=max(0,events[0]['seconds']-.1)
with wave.open(str(run/'native_dcs.wav'),'rb') as wav:
    rate=wav.getframerate();channels=wav.getnchannels()
    assert wav.getsampwidth()==2
    wav.setpos(round(start*rate))
    raw=wav.readframes(rate*2)
    observed=np.frombuffer(raw,dtype='<i2').reshape(-1,channels).mean(axis=1)
control_name=sys.argv[2] if len(sys.argv)>2 else None
if control_name:
    control=BASE/control_name
    control_receipt=json.loads((control/'execution.json').read_text())
    assert control_receipt['exitCode']==0 and not control_receipt['timedOut']
    assert receipt['controllerSHA256']==control_receipt['controllerSHA256']
    assert '--sound-candidate' not in control_receipt['testArguments']
    assert set(receipt['testArguments'])-{'--sound-candidate'}==set(control_receipt['testArguments'])
    assert all(control_receipt['replacementChips'][name]==digest for name,digest in receipt['replacementChips'].items() if 'music_spch' not in name)
    with wave.open(str(control/'native_dcs.wav'),'rb') as wav:
        assert wav.getframerate()==rate and wav.getnchannels()==channels
        wav.setpos(round(start*rate));raw=wav.readframes(rate*2)
        baseline=np.frombuffer(raw,dtype='<i2').reshape(-1,channels).mean(axis=1)
    assert len(baseline)==len(observed)
    observed=observed-baseline
divisor=math.gcd(inputs['rate'],rate)
reference=resample_poly(reference,rate//divisor,inputs['rate']//divisor)
scores=correlate(observed,reference,mode='valid',method='fft')
energy=np.r_[0,np.cumsum(observed*observed)]
norm=np.sqrt(np.maximum(energy[len(reference):]-energy[:-len(reference)],1))*np.linalg.norm(reference)
normalized=np.abs(scores)/norm
at=int(np.argmax(normalized));score=float(normalized[at])
report=dict(scope='One native pop call at authored pop pose plus at-most-two-second waveform diagnostic',
    run=run.name,event=events[0],eventAge=age,correlationWithNativeDecodedClip=score,
    nativeCodecVsStagedPCMCorrelation=codec_score,controlRun=control_name,
    completeDecodedClipMatchesIsolatedCapture=bool(control_name and score>.98),
    observedPeak=float(np.max(np.abs(observed))),waveformLatencySeconds=start+at/rate-events[0]['seconds'],
    maximumWaveformSecondsRead=2,wholeMatchFloatArrayAllocated=False,
    controllerSHA256=receipt['controllerSHA256'],pcmSHA256=sha(pcm),decodedSHA256=sha(decoded_bytes),
    finalMixAccepted=False,completePlaybackQualified=False,releaseReady=False)
(run/'kano_pop_audio_diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
