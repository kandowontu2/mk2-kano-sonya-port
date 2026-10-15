"""New compiled packet guard: earned Tomb native DCS delivery and full winner PCM.

Both true performers, physical P1. Native DCS effect/victim full waveform and
all other context regressions remain open. All audio is streamed solely to RAM.
"""
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import run_current_bicycle_block_audio_v3390 as audio
import run_current_tomb_audio_ram_v3661 as prior
import map_current_native_feature_coverage_v3590 as current
import native_tomb_drop_qualification_v3643 as native
from verify_native_friendship_audio_v791 import existing_sample

ROOT,need,sha=current.ROOT,current.need,current.sha
NAME='diagnostic_v3680_native_sound_packet_guard'
LUA='mk2ks_native_sound_delivery_ram_v3681.lua'
OUT=ROOT/'audit_v3684_native_sound_delivery_ram_checked'

def collector(fighter):
    source=inspect.getsource(audio.capture)
    edits={
      "folder=ROOT/f'audit_v3391_current_bicycle_block_audio_p{side}_{suffix}'":f"folder=ROOT/f'audit_v3683_{fighter}_native_sound_p{{side}}_{{suffix}}'",
      "ROOT/'mk2ks_human_special_negative_v9.lua',ROOT/'mk2ks_human_bicycle_block_trace_v3345.lua',":
        "ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',ROOT/'mk2ks_current_stage_provenance_v3595.lua',",
      "ROOT/'mk2ks_human_bicycle_block_push_v3373.lua',":
        "ROOT/'mk2ks_current_tomb_audio_ram_v3660.lua',ROOT/'mk2ks_current_tomb_audio_ram_v3664.lua',ROOT/'tools/native_tomb_drop_qualification_v3643.py',ROOT/'tools/verify_native_friendship_audio_v791.py',",
      'mk2ks_human_bicycle_block_audio_v3386.lua':LUA,
      "env.update(MK2KS_HUMAN_SPECIAL_MOVE='bicycle',MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_SCENARIO='block',\n               MK2KS_HUMAN_SPECIAL_VICTIM='kano',MK2KS_BBLOCK_OUT=str(folder))":
        f"env.update(MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER='{fighter}',MK2KS_STAGE_ARENA='1',MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder))",
      "'-str','65'":"'-str','900'",
      "move='bicycle',side=side,scenario='block',victim='kano'":f"move='native_tomb',side=side,scenario='earned',winner='{fighter}'",
      'state.prior.current.current.EXE':'NEW_EXE',
      'state.prior.current.current.PAYLOAD':'NEW_PAYLOAD',
    }
    for old,new in edits.items():
        need(source.count(old)==(2 if old=='mk2ks_human_bicycle_block_audio_v3386.lua'else 1),'Exact original RAM collector adaptation '+old)
        source=source.replace(old,new)
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    scope=dict(audio.__dict__);scope.update(__file__=__file__,CANDIDATE=NAME,NEW_EXE=build['executable_sha256'],NEW_PAYLOAD=build['payload_sha256'])
    exec(compile(source,'<entire3390collector_newcompiled_packet_guard>','exec'),scope)
    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()

def pair(fighter):
    capture,collector_sha=collector(fighter)
    folder,headers,a=capture(1,True);base,oldheaders,b=capture(1,False)
    log=(folder/'run.log').read_text();oldlog=(base/'run.log').read_text()
    rows=prior.rows
    selected=lambda s:[line for line in s.splitlines()if line.startswith('MK2_STAGE_')]
    need(selected(log)==selected(oldlog),'Every native physical control/health/branch/cleanup event remains identical')
    guest=current.current.expected_current()[0]
    need((folder/'guest_maincpu.bin').read_bytes()==(base/'guest_maincpu.bin').read_bytes()==guest,'Every actual guest byte unchanged from reconstructed3172')
    contract=native.check_log(log,fighter,1,1,guest=guest)
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape,'Exact every mixed audio update timeline')
    need(rows(log,'SOUND')==rows(oldlog,'SOUND')and rows(log,'ROUTE')==rows(oldlog,'ROUTE')and
         rows(log,'DELIVERY')==rows(oldlog,'DELIVERY'),'Same native routes and actual DSP delivery with/without imported playback')
    origin=int(rows(log,'BEGIN')[0]['origin'])
    need(origin>1 and int(headers[0]['frame'])in(origin,origin+1)and int(headers[-1]['frame'])==origin+650,'Complete true executed native scene window')
    sounds=rows(log,'SOUND');delivery=rows(log,'DELIVERY')
    native_writes=[r for r in sounds if r['pc']in('FFA13C90','FFA13D60')]
    # The DSP may read the same latch several times, but every sent native byte
    # must be actually read before the next native write, not merely logged.
    deliveries=[]
    for i,write in enumerate(native_writes):
        start=float(write['seconds']);end=float(native_writes[i+1]['seconds'])if i+1<len(native_writes)else start+.1
        matched=[r for r in delivery if start<=float(r['seconds'])<end and int(r['word'],16)==(int(write['word'],16)&255)]
        need(matched,'Actual native DCS byte delivered before the next write: '+str(write))
        deliveries.append(dict(port=write,dspRead=matched[0]))
    victim=18 if fighter=='kano'else 17
    screams=[r for r in rows(log,'ROUTE')if r['entry']=='FFA11FD0']
    for scream in screams:
        need(int(scream['id'])==victim and scream['owner']==scream['a8'],'Owned true victim voice without ID substitution')
        dispatch=[r for r in rows(log,'ROUTE')if r['frame']==scream['frame']and r['a8']==scream['a8']]
        need(any(r['entry']==('FFA123B0'if victim==18 else'FFA122D0')for r in dispatch),'Correct native gender branch')
        need(any(r['entry']=='FFA12530'and int(r['a0'],16)in((0x38,0x39)if victim==18 else(0x34,0x35))for r in dispatch),'Original packed native scream range')
    need(len(screams)==len([r for r in native.records(log,'BRANCH')if r['entry']=='FF8EB290']),'Exactly conditional native late victim scream')
    marker='FFFE'if fighter=='kano'else'FFFD';marks=[r for r in sounds if r['word']==marker and r['pc']=='FFFB7140']
    need(len(marks)==1,'One direct true-ID winner announcement')
    donor=existing_sample(ROOT,int(marker,16))
    delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Original imported dual-mono contribution')
    signal=delta[:,0];offset=int(np.argmax(fftconvolve(signal,donor[::-1],mode='valid')))
    actual=signal[offset:offset+len(donor)];gain=float(np.dot(actual,donor)/np.dot(donor,donor))
    corr=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)));rms=float(np.sqrt(np.mean((actual-donor)**2)))
    need(.999<gain<1.001 and corr>.9995 and rms<2,'Full original16k cue with unchanged native MAME interpolation/.21 gain')
    need(not np.any(signal[:offset])and not np.any(signal[offset+len(donor)+2:]),'No wrongly imported native packets before or after the complete winner clip')
    start=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000;onset=start+offset/48000
    need(abs(onset-float(marks[0]['seconds']))<.0001,'Actual winner onset at native direct marker')
    channels=rows(log,'CHANNEL');by={(int(r['frame']),int(r['channel'])):r for r in channels}
    need(len(by)==len(channels)==14*650,'All actual sample channels throughout650callbacks')
    need(all(r['loop']==r['paused']=='0'for r in channels),'Finite unpaused playback')
    idle=lambda r:int(r['sample'])==0xffffffff
    playing=[r for r in channels if not idle(r)]
    sample=2 if fighter=='kano'else 3
    need(playing and all(r['channel']=='0'and int(r['sample'])==sample and r['length']=='32000'for r in playing),'Only correct full winner source plays; retained idle lengths are not active sounds')
    need(all(idle(by[origin+650,n])for n in range(14))and all(idle(r)for r in rows(oldlog,'CHANNEL')),'Native channel finite cleanup and true DCS-only baseline')
    return dict(passed=True,fighter=fighter,side=1,capture=folder.name,baseline=base.name,inputContract=contract,
      collectorSHA256=collector_sha,nativeDCSActualDeliveries=deliveries,lateOwnedVictimScreams=len(screams),
      originalWinnerMix=dict(outputSamples=len(donor),gain=gain,correlation=corr,residualRMS=rms,onsetSeconds=onset),
      rawAudioFilesWritten=0,nativeDCSStageVictimFullWaveformAccepted=False)

def run():
    need(not OUT.exists(),'Never overwrite runtime evidence')
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    restore=json.loads((ROOT/NAME/'restoration.json').read_text(encoding='utf-8-sig'))
    need(restore['passed']and all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items()),'Exact actual user-file restoration after new compile')
    need(build['payload_sha256']=='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'and
         not build['game_data_changed']and not build['public_build_promoted'],'Narrow host fix, unchanged guest/payload and publicbuild')
    cases=[pair(fighter)for fighter in('kano','sonya')]
    pins={str(Path(__file__).resolve()):sha(__file__),str(ROOT/LUA):sha(ROOT/LUA)}
    for case in cases:
        for name in(case['capture'],case['baseline']):
            leaf=ROOT/name;meta=json.loads((leaf/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent executed source');pins[p]=h
            for file in leaf.rglob('*'):
                if file.is_file():pins[str(file)]=sha(file)
    need(all(sha(p)==h for p,h in pins.items()),'All executed sources/evidence unchanged')
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,
      currentTombBothP1PerformersNativePacketDeliveryAndFullWinnerMixAccepted=True,
      completeStageVictimAudioFidelityAccepted=False,allDirectCueAndSelectionRegressionAccepted=False,
      fullPortAcceptance=False,rawAudioFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
