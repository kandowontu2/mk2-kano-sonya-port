"""Actual3836 true mirror Tomb: full earned state, DCS delivery and winner PCM.

Normal two-human selection, two full-health earned matches and paid rematch.
No overrides. PCM and initialized guest are RAM-only; text compressed before
write. This is not all-stage raster, stock DCS whole-waveform or port acceptance.
"""
import hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import run_jax_arms_native_audio_routes_v4212 as old
import verify_tomb_mirror_contract_v4344 as state
from verify_native_friendship_audio_v791 import existing_sample
ROOT,need,sha=old.ROOT,old.need,old.sha
OUT=ROOT/'audit_v4352_tomb_mirror_audio_ram_observed'

def collector():
    source=inspect.getsource(old.capture)
    changes={
      "audit_v4213_jax_arms_{fighter}_p{side}_audio_queue_{suffix}":"audit_v4351_tomb_mirror_{fighter}_p{side}_{suffix}",
      "mk2ks_jax_arms_audio_routes_ram_v4210.lua":"mk2ks_tomb_mirror_audio_ram_v4342.lua",
      "mk2ks_stock_extended_earned_ram_v3958.lua":"mk2ks_tomb_mirror_driver_ram_v4340.lua",
      "ROOT/'mk2ks_stock_fatality_v1021.lua',ROOT/'mk2ks_arm_palette_trace_v1073.lua',\n        ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua',ROOT/'mk2ks_jax_clap_audio_routes_ram_v4057.lua',\n        Path(state.old.__file__),Path(state.scene_state.__file__),":
        "ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua',ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',\n        ROOT/'mk2ks_current_stage_provenance_v3595.lua',ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua',\n        Path(old.__file__),Path(state.native.__file__),Path(state.native.legacy.__file__),\n        ROOT/'tools/verify_current_tomb_drop_physics_v3618.py',ROOT/'tools/verify_native_friendship_audio_v791.py',",
      "env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',\n        MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0',\n        MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='bbbb_lp',MK2KS_STOCK_GAP='96',\n        MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_OUT=str(folder))":
        "env.update(MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_ARENA='1',MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder))",
      "'-str','150'":"'-str','900'",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Exact full RAM collector adaptation: '+before)
        source=source.replace(before,after)
    scope=dict(old.__dict__);scope.update(__file__=__file__,old=old,state=state)
    exec(compile(source,'<entire4212_RAM_collector_true_mirror_4343>','exec'),scope)
    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()

def preflight():
    capture,digest=collector()
    for name in ('mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_tomb_mirror_audio_ram_v4342.lua'):
        text=(ROOT/name).read_text()
        need('manager.machine:exit'not in text and 'set_value'not in text,'Wrappers preserve original complete physical controller only')
    # Both compiled contracts retain all native 1731 gates, not a new narrow
    # hand-written acceptance parser. The exact adaptations are hashed.
    original=inspect.getsource(state.native.legacy.check_log)
    need(state.contract_source==state.native.source.replace('victim = 18 if own == 17 else 17','victim = own'),
         'Exactly one mirror identity expectation in complete original contract')
    need(state.drop_source==inspect.getsource(state.native.qualify_drop).replace("victim_id=18 if fighter=='kano'else 17","victim_id=17 if fighter=='kano'else 18"),
         'Entire original unpressed RNG/phase/source contract, only real mirror victim ID')
    for gate in ('Every normal arena earned through rematches','Native two full-health KO damage chains',
      'Missing physical paid challenger','Wrong actual facing-specific button sequence','Physical action ownership',
      'Missing consecutive action/cleanup fields','Native retirement/next screen missing or softlock'):
        need(gate in original and gate in state.contract_source,'Every original health/input/cleanup gate retained: '+gate)
    return capture,dict(collectorSHA256=digest,contractSHA256=state.CONTRACT_SHA256,dropSHA256=state.DROP_SHA256)

def pair(fighter,side,guest,capture):
    folder,headers,a=capture(fighter,side,True,guest)
    baseline,oldheaders,b=capture(fighter,side,False,guest)
    text=(folder/'run.log').read_text();base=(baseline/'run.log').read_text()
    selected=lambda t:[s for s in t.splitlines()if s.startswith('MK2_STAGE_')]
    need(selected(text)==selected(base),'All actual earned mirror inputs/health/branch/cleanup identical samples on/off')
    checked=state.check_log(text,fighter,side,1,guest=guest)
    need(state.check_log(base,fighter,side,1,guest=guest)==checked,'Both complete earned/native mirror contracts independently passed')
    faults=state.actual_faults(text,fighter,side,guest)
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape,'Every actual native sound update/time/stereo sample count identical')
    rows=old.rows;begin=rows(text,'BEGIN');end=rows(text,'RESULT')
    own=17 if fighter=='kano'else 18
    need(len(begin)==len(end)==1 and int(begin[0]['id'])==own,'One genuinely executed owned native Tomb audio origin')
    origin=int(begin[0]['origin'])
    need(int(end[0]['origin'])==origin and int(end[0]['frame'])==origin+1101,
         'Actual deferred machine exit after original1100field driver retirement, no shortened scene')
    need(int(headers[0]['frame'])in(origin,origin+1)and int(headers[-1]['frame'])in(origin+1099,origin+1100),
         'Complete actual audio through the native driver retirement window')
    need(all(int(h['bytes'])==3840 for h in headers)and
         all(abs(float(y['seconds'])-float(x['seconds'])-.02)<1e-8 for x,y in zip(headers,headers[1:])),
         'Actual50Hz stereo sound update clock, independent of video callbacks')
    for tag in ('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):
        need(rows(text,tag)==rows(base,tag),'Every native '+tag+' event identical samples on/off')
    sounds=rows(text,'SOUND');delivery=rows(text,'DELIVERY')
    writes=[r for r in sounds if r['pc']in('FFA13C90','FFA13D60')]
    delivered=[]
    for index,write in enumerate(writes):
        first=float(write['seconds']);last=float(writes[index+1]['seconds'])if index+1<len(writes)else first+.1
        hits=[r for r in delivery if first<=float(r['seconds'])<last and int(r['word'],16)==int(write['word'],16)&255]
        need(hits,'Every real native port byte actually read by DCS before the next write')
        delivered.append(dict(write=write,dspRead=hits[0]))
    need(delivered and np.any(b!=0),'Actual non-silent native audio, not a disabled engine')
    routes=rows(text,'ROUTE');screams=[r for r in routes if r['entry']=='FFA11FD0']
    for scream in screams:
        need(int(scream['id'])==own and scream['owner']==scream['a8'],'Genuine native mirror victim voice ownership')
        branch=[r for r in routes if r['frame']==scream['frame']and r['a8']==scream['a8']]
        need(any(r['entry']==('FFA123B0'if own==18 else'FFA122D0')for r in branch),'Correct original mirror victim gender branch')
        need(any(r['entry']=='FFA12530'and int(r['a0'],16)in((0x38,0x39)if own==18 else(0x34,0x35))for r in branch),'Original mirror scream dispatch range')
    need(len(screams)==len([r for r in state.native.records(text,'BRANCH')if r['entry']=='FF8EB290']),
         'Exactly the actual conditional native late victim scream')
    marker='FFFE'if own==17 else'FFFD';marks=[r for r in sounds if r['word']==marker and r['pc']=='FFFB7140']
    need(len(marks)==1,'Exactly one true-ID native winner announcement')
    donor=existing_sample(ROOT,int(marker,16));delta=a.astype(np.int32)-b.astype(np.int32)
    need(np.array_equal(delta[:,0],delta[:,1]),'Actual original dual-mono imported winner cue')
    signal=delta[:,0];offset=int(np.argmax(fftconvolve(signal,donor[::-1],mode='valid')))
    actual=signal[offset:offset+len(donor)];gain=float(np.dot(actual,donor)/np.dot(donor,donor))
    corr=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)));rms=float(np.sqrt(np.mean((actual-donor)**2)))
    need(.999<gain<1.001 and corr>.9995 and rms<2,'Whole genuine winner clip with original interpolation/.21 gain')
    need(not np.any(signal[:offset])and not np.any(signal[offset+len(donor)+2:]),'No phantom imported native effect/audio after winner cleanup')
    onset=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000+offset/48000
    need(abs(onset-float(marks[0]['seconds']))<.0001,'Actual winner onset at genuine native direct marker')
    for observed,enabled in ((text,True),(base,False)):
        channels=rows(observed,'CHANNEL');by={(int(r['frame']),int(r['channel'])):r for r in channels}
        need(len(channels)==len(by)==14*1100 and {int(r['frame'])for r in channels}==set(range(origin+1,origin+1101)),
             'All fourteen native sample channel states through1100complete scene callbacks')
        need(all(r['loop']==r['paused']=='0'for r in channels),'Finite unpaused native sample playback')
        active=[r for r in channels if int(r['sample'])!=0xffffffff]
        if enabled:
            need(active and all(r['channel']=='0'and int(r['sample'])==(2 if own==17 else 3)and r['length']=='32000'for r in active),
                 'Only exact true-ID winner source, no wrongly imported native effect')
        else:need(not active,'Native DCS-only baseline')
        need(all(int(by[origin+1100,n]['sample'])==0xffffffff for n in range(14)),'Every native sample channel retired')
    return dict(passed=True,fighter=fighter,side=side,victim=own,capture=folder.name,baseline=baseline.name,
      inputContract=checked,actualFaultsRejected=faults,nativeDCSDeliveredBytes=delivered,lateOwnedMirrorVictimScreams=len(screams),
      originalWinnerMix=dict(outputSamples=len(donor),gain=gain,correlation=corr,residualRMS=rms,onsetSeconds=onset),
      everyNativeMixedPCMUpdateComparedInRAM=True,rawAudioRasterVRAMROMCopiesWritten=0,
      fullTombRasterAndFloorShadowAccepted=False,nativeDCSStageVictimFullWaveformAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable mirror observation')
    capture,proof=preflight();guest=old.expected()
    print(json.dumps(dict(preflight=proof,guestSHA256=hashlib.sha256(guest).hexdigest().upper())),flush=True)
    case=pair('kano',1,guest,capture)
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for name in (case['capture'],case['baseline']):
        leaf=ROOT/name;meta=json.loads((leaf/'result.json').read_text())
        for path,h in meta['input_hashes'].items():need(path not in pins or pins[path]==h,'Consistent paired inputs');pins[path]=h
        for path in leaf.rglob('*'):
            if path.is_file():pins[str(path)]=sha(path)
    need(all(sha(path)==h for path,h in pins.items()),'Actual input/evidence bytes unchanged')
    return dict(passed=True,candidate=old.NAME,case=case,sourcePreflight=proof,inputHashes=pins,
      actualTrueMirrorContexts=1,completeStageVictimAudioFidelityAccepted=False,
      allStageMirrorBranchesAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite actual terminal result');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('case','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
