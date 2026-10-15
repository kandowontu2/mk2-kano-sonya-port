"""Whole current Sonya choices, bicycle lifecycle, native fall, DAC/ROM/RGB.

All three real traveling branches occur. The attempted shadow collector still
emits zero drawing records: preserve that coverage failure explicitly rather
than laundering the transport pass into shadow/art/audio/full-port acceptance.
"""
import hashlib
import inspect
import json
import re
import struct
from pathlib import Path
import capture_native_selector_sonya_choice_visual_audio as capture
import qualify_native_selector_existing_sonya_travel_phases as phase_source
import qualify_native_selector_existing_sonya_travel_phases_finish_boundary as boundary
import qualify_native_selector_natural_state_health_checkpoint as raster_model
import capture_current_subzero_audio_v6213 as dac_model
import read_live_shang_drain_frames as census

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_choice_av_checkpoint_checked'
VISUAL=ROOT/'audit_native_selector_sonya_choice_av_actual_views.json'


def bicycle_gate(text,guest):
    # Same whole positive bicycle model. This later live action has no startup
    # flags no-op, so retain its exact original three move-lock stores.
    source=inspect.getsource(phase_source.bicycle_gate)
    marker="    source=replace(source,\"pair=state.verify_log(log,'kano',guest)\",\"pair=ledger.gate(log,guest);source_gate(log,guest)\")"
    source=phase_source.replace(source,marker,marker+'''
    source=replace(source,"assert guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged'",
        "assert guest[a:b]==original[a:b] or ((lo,hi)==(0xff876650,0xff876b60) and adjacent_finish_operand(guest,original)), 'Original fall plus full source-derived neighboring finisher operand'")
''')
    source=phase_source.replace(source,'ledger=ledger,source_gate=source_gate)',
        'ledger=ledger,source_gate=source_gate,adjacent_finish_operand=adjacent_finish_operand)')
    scope=dict(vars(phase_source),adjacent_finish_operand=boundary.adjacent_finish_operand,__file__=__file__)
    exec(compile(source,__file__+'::whole_bicycle_actual_later_live_context','exec'),scope)
    return scope['bicycle_gate'](text,guest)


def gate(text,guest):
    ledger=capture.choices.native_state
    whole=ledger.gate(text,guest)
    choices=capture.choices.choices_gate(text,guest,whole['schedule'])
    need(set(choices['observedMoves'])=={'ring','square','bicycle'},'All three naturally executing original RNG branches')
    bike=bicycle_gate(text,guest)
    falls=ledger.rows(text,'MK2_SONYA_NATIVE_FALL')
    need(len(falls)==6,'Whole actual native fall/landing tap inventory')
    for r in falls:
        at=int(r['entry'],16)
        need(r['kind'] in ('fall','landing') and at==({'fall':0xff876660,'landing':0xff876420}[r['kind']]) and
             int(r['pc'],16)==at+16 and int(r['mask'],16)==65535 and
             int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0] and
             r['actor']==r['owner']=='010350A0' and r['main']=='0106BF30' and r['id']=='18' and
             r['writes']=='0' and r['assistance']=='none','Every actual executing fall opcode/PC/mask/real owner')
    own=[r for r in falls if r['kind']=='fall' and int(r['frame'])==bike['fall']]
    need(len(own)==1 and own[0]['action']=='0611' and
         [int(own[0]['a'+str(i)],16) for i in range(4)]==[13,13,0xa000,4] and own[0]['a6']=='FFF9DC00',
         'Bicycle gravity/ceiling switch bound to actually executed original fall and all source parameters')
    rounds=ledger.original.rounds.rows(text,'FIELD')
    by={(r['frame'],r['slot']):r for r in rounds}
    expected=[]
    for frame in range(1818,3618):
        a,b=by[frame,1],by[frame,2]
        if (a['mode']==b['mode']==2 and a['states']==b['states']=='1,0' and a['valid']==b['valid']==1 and
            a['id']==17 and b['id']==18 and a['owner']==a['actor'] and b['owner']==b['actor']):
            expected.append(frame)
    posts=ledger.rows(text,'MK2_HPHASE_POST_FIELD')
    need(expected and not posts and not ledger.rows(text,'MK2_HPHASE_CPU_NATIVE_ENTRY'),
         'Attempted shadow observer truly has zero drawing coverage; do not treat as a shadow pass')
    return dict(wholeNativeHealthState=whole,allThreeActualNativeChoiceBranches=choices,
                completeActualBicycleMiss=bike,actualNativeFallInstructionRows=falls,
                bicycleFallInstructionAccepted=True,expectedShadowDrawingFrames=len(expected),
                observedShadowDrawingRows=len(posts),wholeShadowProvenanceAccepted=False,
                wholeRasterAudioAcceptance=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable mixed native checkpoint')
    host=next(r for r in census.census_hosts() if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766,
         'Original exact currently live retained host')
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    prior=json.loads((capture.OUT/'report.json').read_text());meta=json.loads((folder/'result.json').read_text())
    pins=dict(prior['inputHashes'])
    need(prior['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==prior['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (45784,38752,1791752562.1074715) and all(sha(p)==h for p,h in pins.items()),
         'Same original terminal game and whole current executed inputs, no replay')
    positive=gate(text,state['guest'])
    raster=raster_model.rasters(images,meta['actualScenes'])
    audio=capture.AUDIO[capture.KEY];model=capture.original.audio_model
    for tag,chunks,headers in [('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),
                               ('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])]:
        rows=model.rows(text,tag)
        need(len(rows)==len(chunks)==len(headers)==1646 and
             all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper()) for r,h,raw in zip(rows,headers,chunks,strict=True)),
             'Every entire original RAM sound callback/header/digest, no trimmed samples')
    native_dac,dac_faults,dac_sha=dac_model.dac_models(1646)
    dac=native_dac(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    faults=list(dac_faults(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']))
    rom_gate,rom_faults=model.rom_models(audio['expectedROM'])
    rom=[rom_gate(bytes(audio['rom'][p]),p) for p in ('startup','terminal')]
    for phase in ('startup','terminal'):faults.extend(rom_faults(bytes(audio['rom'][phase]),phase))
    channels=model.rows(text,'MK2_MAUDIO_CHANNEL');precise=model.rows(text,'MK2_TOMB_MIX_CHANNEL')
    need([(int(r['frame']),int(r['channel'])) for r in channels]==[(f,c) for f in range(1818,3619) for c in range(19)] and
         [(r['frame'],r['seconds'],int(r['channel'])) for r in precise]==
         [(h['frame'],h['seconds'],c) for h in audio['pcmHeaders'] for c in range(19)],
         'All nineteen channels on every actual video and precise sound callback')
    for r in channels+precise:
        need(r['loop']==r['paused']==r['writes']=='0' and r['assistance']=='none','Complete passive channel history')
        if int(r['channel'])>=14:
            need(r['sample']=='4294967295' and r['length']=='0' and float(r.get('position',r.get('pos')))==0,
                 'All five private finisher channels actually inactive throughout match')
        if 'bits' in r:need(struct.pack('<d',float(r['position'])).hex().upper()==r['bits'],'Every actual position bit preserved')
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and bad!=line,'Effective real native record counterexample')
        return text.replace(line,bad,1)
    trials=[('choice_proxy',change('MK2_SONYA_CHOICE_EVENT','owner','01000000',serial=7,kind='entry')),
            ('choice_bicycle_threshold',change('MK2_SONYA_CHOICE_EVENT','a0','000000FB',serial=7,kind='first_call')),
            ('choice_false_total',change('MK2_SONYA_CHOICE_RESULT','choices','6')),
            ('fall_mask',change('MK2_SONYA_NATIVE_FALL','mask','FFFE',frame=3210)),
            ('fall_opcode',change('MK2_SONYA_NATIVE_FALL','opcode','FFFF',frame=3210)),
            ('fall_owner',change('MK2_SONYA_NATIVE_FALL','owner','01000000',frame=3210)),
            ('fall_source_parameters',change('MK2_SONYA_NATIVE_FALL','a2','00008000',frame=3210)),
            ('bike_intro_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=3192)),
            ('bike_ceiling_gravity',change('MK2_CPU_PAIR_FIELD','gravity','0000A001',frame=3211))]
    for label,bad in trials:
        try:gate(bad,state['guest'])
        except (AssertionError,ValueError,KeyError,IndexError) as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native corruption accepted: '+label)
    need(gate(text,state['guest'])==positive,'Original complete positive restored after all faults')
    visual=json.loads(VISUAL.read_text())
    need(visual['passed'] and visual['actualNativeIdentity']==held['identity'] and
         [r['index'] for r in visual['actualViewedCallbacks']]==[151,154,156,157], 'Four actual bicycle raster reviews')
    for row in visual['actualViewedCallbacks']:
        actual=raster[row['index']]
        need(row['header']==actual['header'] and row['nativeRGBSHA256']==actual['nativeRGBSHA256'] and
             row['SHA256']==actual['header']['sha256'] and row['actualReconstructedAlpha']==actual['actualReconstructedAlpha'],
             'Every actually viewed native pixel is original callback-digest bound')
    paths=[Path(__file__),VISUAL,capture.OUT/'report.json',Path(phase_source.__file__),Path(boundary.__file__),
           Path(raster_model.__file__),Path(dac_model.__file__),Path(census.__file__),
           ROOT/'tools/read_native_selector_sonya_choice_av_frames.py',ROOT/'tools/read_native_selector_sonya_choice_av_frames_remote.py',
           *(p for p in folder.rglob('*') if p.is_file())]
    for path in paths:
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No historical pin silently replaced')
        pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Fresh final complete current source/behavior/evidence census')
    OUT.mkdir()
    report=dict(passed=True,qualification=positive,actualNativeIdentity=held['identity'],wholeOriginalRasters=raster,
                actuallyViewedBicycleCallbacks=visual,nativeDAC=dac,nativeDACSourceSHA256=dac_sha,
                wholeSoundROM=rom,actualFaultsRejected=faults,videoChannelRows=len(channels),preciseChannelRows=len(precise),
                completeStereoFrames=1646*960,inputHashes=pins,requirements=prior['requirements'],remainingGroups=prior['remainingGroups'],
                goalStatus='active',allThreeActualSonyaChoiceBranchesAccepted=True,finiteBicycleLifecycleAndViewsAccepted=True,
                wholeShadowProvenanceAccepted=False,wholeSourceMixedPCMStillOpen=True,fullPortAcceptance=False,
                publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    capture.choices.current.prior.save(OUT/'report.json',report)
    print('PASS all3 actual Sonya choice branches/full bicycle lifecycle and4views/whole DAC-ROM; zero shadow rows remain explicit gap',flush=True)
    return report
