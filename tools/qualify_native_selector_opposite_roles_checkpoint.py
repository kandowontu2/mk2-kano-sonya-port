"""Same terminal38692: opposite-role full ledgers, real choices and six views.

Whole actual PCM/DAC/ROM integrity and corruption checks are separate from
the still-open TWO-winner full waveform and body/shadow geometry models.
"""
import hashlib
import json
import re
import struct
import traceback
from pathlib import Path
import capture_native_selector_sonya_human_kano_cpu as capture
import qualify_native_selector_natural_state_health_checkpoint as rasters
import capture_current_subzero_audio_v6213 as dac_model
import read_live_shang_drain_frames as identity

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_opposite_roles_checkpoint_checked'
VISUAL=ROOT/'audit_native_selector_opposite_roles_actual_views.json'
rows=capture.previous.choices.native_state.rows


def gate(text,guest):
    value=capture.gate(text,guest)
    result=rows(text,'MK2_CPU_CHOICE_RESULT')
    need(len(result)==1 and int(result[0]['choices'])==len(value['actualCPUChoices'])==int(result[0]['serial']),
         'Complete actual native choice/result inventory')
    code=rows(text,'MK2_CPU_CHOICE_CODE')
    need(len(code)==2,'Full actual router/RNG code inventories')
    for r in code:
        lo,hi=(int(r[k],16) for k in ('start','stop'))
        words=[int(w,16) for w in r['words'].split(',')]
        need(struct.pack('<'+'H'*len(words),*words)==guest[(lo-0xff800000)//8:(hi-0xff800000)//8],
             'Every whole actual native router/RNG byte source-bound')
    return value


def execute(state):
    need(not OUT.exists(),'Fresh immutable opposite-role checkpoint')
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    parent=json.loads((capture.OUT/'report.json').read_text());meta=json.loads((folder/'result.json').read_text())
    pins=dict(parent['inputHashes'])
    host=next(r for r in identity.census_hosts() if r['ProcessId']==38752)
    need(parent['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']==parent['actualNativeIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (38692,38752,1791755623.140932) and not meta['nativeTerminal']['hostDecodeErrors'] and
         (host['ParentProcessId'],host['createdUnix'])==(40316,1791734919.6266766) and
         all(sha(p)==h for p,h in pins.items()),'Same exact terminal native/retained host and all immutable inputs')
    positive=gate(text,state['guest'])
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and bad!=line,'Effective actual native counterexample')
        return text.replace(line,bad,1)
    health=rows(text,'MK2_CPU_ROUND_HEALTH')[0];flags=rows(text,'MK2_CPU_PAIR_FLAG')[0]
    live=rows(text,'MK2_CPU_PAIR_FIELD')[0];code=rows(text,'MK2_CPU_CHOICE_CODE')[0]
    trials=[
        ('selected_human_proxy',change('MK2_P2CPU_COLD_LIVE','human_id','17')),
        ('selected_cpu_proxy',change('MK2_P2CPU_COLD_LIVE','cpu_id','18')),
        ('native_ladder_pointer',change('MK2_CPU_PAIR_ROM','list','FFFA0000',order=0)),
        ('missing_all_mode_field',text.replace(next(s+'\n' for s in text.splitlines() if s.startswith('MK2_CPU_ROUND_FIELD ')),'',1)),
        ('unexplained_HP',change('MK2_CPU_ROUND_FIELD','hp','160',frame=1815,slot=1)),
        ('health_store_opcode',change('MK2_CPU_ROUND_HEALTH','op0','FFFF',frame=health['frame'],slot=health['slot'])),
        ('health_store_mask',change('MK2_CPU_ROUND_HEALTH','mask','FFFE',frame=health['frame'],slot=health['slot'])),
        ('state_store_opcode',change('MK2_CPU_PAIR_FLAG','op0','FFFF',frame=flags['frame'],slot=flags['slot'])),
        ('state_store_target',change('MK2_CPU_PAIR_FLAG','at','01000000',frame=flags['frame'],slot=flags['slot'])),
        ('live_CPU_owner',change('MK2_CPU_PAIR_FIELD','owner','01000000',frame=live['frame'])),
        ('live_human_proxy',change('MK2_CPU_PAIR_FIELD','vid','1',frame=live['frame'])),
        ('live_floor',change('MK2_CPU_PAIR_FIELD','floor','80',frame=live['frame'])),
        ('choice_owner',change('MK2_CPU_CHOICE_EVENT','owner','01000000',serial=1,kind='entry')),
        ('choice_threshold',change('MK2_CPU_CHOICE_EVENT','a0','000000FB',serial=1,kind='first_call')),
        ('choice_carry',change('MK2_CPU_CHOICE_EVENT','carry','1',serial=1,kind='second_result')),
        ('false_choice_total',change('MK2_CPU_CHOICE_RESULT','choices','2')),
        ('whole_router_code',change('MK2_CPU_CHOICE_CODE','words','FFFF',start=code['start']))]
    faults=[]
    for label,bad in trials:
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError,KeyError,IndexError) as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native corruption accepted '+label)
    need(gate(text,state['guest'])==positive,'Whole exact state/HP/choice positive restored')
    raster=rasters.rasters(images,meta['actualScenes'])
    visual=json.loads(VISUAL.read_text())
    need(visual['passed'] and visual['actualNativeIdentity']==held['identity'] and visual['actualHostIdentity']==host and
         visual['originalIdentityRevalidatedBeforeAndAfter'] and
         [r['index'] for r in visual['actualViewedCallbacks']]==[0,1,2,3,24,29],
         'All six actual independently reviewed native fields')
    for row in visual['actualViewedCallbacks']:
        actual=raster[row['index']]
        need(row['header']==actual['header'] and row['nativeRGBSHA256']==actual['nativeRGBSHA256'] and
             row['SHA256']==actual['header']['sha256'] and row['actualReconstructedAlpha']==actual['actualReconstructedAlpha'],
             'Every actually viewed complete native pixel digest')
    audio=capture.AUDIO[capture.KEY];model=capture.previous.original.audio_model
    for tag,chunks,headers in [('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),
                               ('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])]:
        records=rows(text,tag)
        need(len(records)==len(chunks)==len(headers)==1645 and
             all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper()) for r,h,raw in zip(records,headers,chunks,strict=True)),
             'Every original whole PCM/DAC block and header/digest')
    dac_gate,dac_faults,dac_hash=dac_model.dac_models(1645)
    dac=dac_gate(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    audio_faults=list(dac_faults(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']))
    rom_gate,rom_faults=model.rom_models(audio['expectedROM'])
    rom=[rom_gate(bytes(audio['rom'][phase]),phase) for phase in ('startup','terminal')]
    for phase in ('startup','terminal'):audio_faults.extend(rom_faults(bytes(audio['rom'][phase]),phase))
    need(len(audio_faults)==12,'Whole original DAC and both12MiB ROM fault suites')
    for path in (Path(__file__),Path(capture.__file__),VISUAL,capture.OUT/'report.json',Path(rasters.__file__),Path(dac_model.__file__),
                 ROOT/'tools/read_native_selector_opposite_roles.py',ROOT/'tools/read_native_selector_opposite_roles_remote.py',
                 ROOT/'tools/read_native_selector_opposite_roles_bound.py',ROOT/'tools/read_native_selector_opposite_roles_remote_bound.py',
                 *(p for p in folder.rglob('*') if p.is_file())):
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'Never silently replace historical input');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Complete current source/evidence inventory unchanged')
    report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],wholeNativeStateHealthChoices=positive,
        actualStateHealthChoiceFaultsRejected=faults,wholeOriginalRasters=raster,actualViewedNativeCallbacks=visual,
        wholeNativeDAC=dac,nativeDACModelSHA256=dac_hash,wholeSoundROM=rom,originalDACROMFaultsRejected=audio_faults,
        completeStereoFrames=1645*960,inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        finiteOppositeRoleLedgersChoicesAndViewsAccepted=True,fullBodyShadowGeometryAccepted=False,
        bothWinnerSourceWaveformAccepted=False,allCPUMovesAccepted=False,wholeCampaignAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    OUT.mkdir();capture.previous.choices.current.prior.save(OUT/'report.json',report)
    print('PASS same38692 opposite-role ledgers/native choice/six views/whole DAC-ROM with29 faults',flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original checkpoint rejection')
        OUT.mkdir();capture.previous.choices.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',newNativeGames=0,fullPortAcceptance=False))
        raise
