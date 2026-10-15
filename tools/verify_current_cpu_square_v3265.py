"""Fresh corrected3172 CPU Square contact, complete native art/shadow/erase.

Reuse unchanged phase/raster/erase contracts; reconstruct the full guest and
all corrected asset bytes independently. No broad CPU/arena/audio promotion.
"""
import hashlib, json, struct, sys, traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import build_native_shang_morphs as morph
import verify_native_cpu_square_inventory_v2998 as inventory
import native_cpu_square_hit_contract_v3037 as phase
import verify_native_cpu_square_hit_v3040 as model
import verify_native_cpu_square_hit_render_v3044 as render
import verify_native_cpu_ring_erase_v2985 as erase
import verify_human_shang_v3174 as current
ROOT=assembly.ROOT
CASE='audit_v3264_current_native_cpu_square_hit'
STATE_OUT=ROOT/'audit_v3266_current_cpu_square_state_checked'
OUT=ROOT/'audit_v3267_current_cpu_square_render_erase_checked'
need=assembly.need

def expected_current():
    guest,old,payload,ends,ranges=assembly.expected()
    need(hashlib.sha256(guest).hexdigest().upper()=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Full independently assembled native guest, no masked bytes')
    donor=ROOT/'mk3/mk3-maincpu.bin'
    need(assembly.sha(donor)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651','Original donor program')
    program=donor.read_bytes(); output=bytearray(payload); allowed=set(); count=0
    for fi,target in enumerate(('kano','sonya')):
        for gi,group in enumerate(morph.SOURCE_GROUPS[target]):
            descriptors=morph.animation.frame_group(program,group,0xff800000,0xffffffff)
            need(len(descriptors)==2,'Actual original two-component morphology')
            for ci,descriptor in enumerate(descriptors):
                source,command,w,h,xo,yo=morph.decoder.component_spec(program,descriptor)
                at=morph.FRAMES+(fi*6+gi*2+ci)*20
                original=struct.unpack_from('<4hIHI',payload,at)
                need(original[:4]==(w,h,xo,yo) and original[5]==0x6000 and command&0x80 and (command>>12)&7==6,'Only original compressed six-bit descriptor conversion')
                tagged=source+0x10000000
                need((tagged-0x0a000000)//8==0xc00000+source//8,'Identical original graphics data for CPU scanner and blitter')
                struct.pack_into('<IH',output,at+8,tagged,command)
                allowed.update(range(at+8,at+14)); count+=1
    changed={i for i,(a,b) in enumerate(zip(payload,output)) if a!=b}
    need(count==12 and changed and changed<=allowed and len(output)==len(payload),'Every other asset byte, palette, pivot and sequence unchanged')
    need(hashlib.sha256(output).hexdigest().upper()==current.PAYLOAD,'Independent complete corrected payload')
    return guest,old,bytes(output),ends,ranges

def run():
    need(not STATE_OUT.exists() and not OUT.exists(),'Immutable new current CPU proofs')
    expected=expected_current()
    candidate=ROOT/current.CANDIDATE
    need(assembly.sha(candidate/'mkport_candidate.exe')==current.EXE and
        (candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==expected[2],'Actual current matched playable pair')
    # Parameter adaptation only: every reused checker retains its original
    # health/owner/phase/FIFO/projection/palette/shadow/erase assertions.
    assembly.NAME=current.CANDIDATE
    assembly.expected=lambda:expected
    pins={}; folder=ROOT/CASE
    log,guest,value=inventory.capture(folder,'new','kano','guard_until_close','jump_guard',pins)
    typed=phase.verify(log,guest,'kano')
    baseline=ROOT/'audit_v3035_native_cpu_square_hit_new_kano_guard_until_close_jump_guard/run.log'
    prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_')
    actual=[line for line in log.splitlines() if line.startswith(prefixes)]
    prior=[line for line in baseline.read_text(encoding='utf-8-sig').splitlines() if line.startswith(prefixes)]
    need(actual==prior and value['health']['allModePhysicalFields']==3602,'Entire fresh physical/native state/health/CPU/RNG trajectory matches original unaffected gameplay')
    pins[str(baseline)]=assembly.sha(baseline)
    for file,wanted in assembly.source_check().items(): pins[file]=wanted
    for path in (ROOT/'mk3/mk3-maincpu.bin',Path(__file__).resolve(),Path(morph.__file__).resolve()): pins[str(path)]=assembly.sha(path)
    value.update(case=CASE,player='kano',build='new',phase=typed,originalPhysicalAndNativeEventsUnchanged=True,actualOriginalEvents=len(actual))
    state=dict(passed=True,cases={'current_kano':value},actualPhysicalFixtures=1,actualDamage=27,
        actualWholeSourceStateHealthAccepted=True,actualNativeHitAndSeparateRecoveriesAccepted=True,
        independentWholeCorrectedPayloadAccepted=True,fullPortAcceptance=False,inputHashes=pins)
    STATE_OUT.mkdir(); (STATE_OUT/'report.json').write_text(json.dumps(state,indent=2)+'\n')
    model.OUT=STATE_OUT
    render.CASES={'current_kano':(CASE,'new','kano')}
    scene=render.verify('current_kano')
    need(scene['passed'] and scene['candidate']==current.CANDIDATE and scene['allOriginalSquarePosesVisible'],'Current full original poses/palettes/native shadows/projection/scanout')
    erase.source_contract(); erased=erase.inspect(folder,guest,current.CANDIDATE)
    need(erased['passed'] and erased['oneInitialBaseOnly'] and not erased['laterBuffersUsedAsAnchors'] and
        erased['continuousExactFlips']==scene['sampledFrames'],'Every chronological native erase/pre-buffer/flip from one initial base')
    for table in (scene['inputHashes'],erased['inputHashes']):
        for file,wanted in table.items():
            need(file not in pins or pins[file]==wanted,'Consistent fresh source/evidence pin'); pins[file]=wanted
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools') and Path(file).suffix=='.py': pins[str(Path(file).resolve())]=assembly.sha(file)
    for file,wanted in pins.items(): need(assembly.sha(file)==wanted,'Actual executed/captured input unchanged')
    return dict(passed=True,candidate=current.CANDIDATE,case=CASE,physicalFixtures=1,
        actualSquareDamage=27,wholeStateHealthNativeChoiceAccepted=True,
        sampledFrames=scene['sampledFrames'],exactScreenPixels=scene['exactScreenPixels'],
        nativeShadowCopies=scene['nativeShadowCopies'],sourceBoundProjections=scene['sourceBoundProjections'],
        continuousExactFlips=erased['continuousExactFlips'],laterBuffersUsedAsAnchors=False,
        originalCPUHumanInputsAndGameplayTrajectoryUnchanged=True,fullCurrentSquareHitPhaseArtShadowEraseAccepted=True,
        allCPUContextsArenasKOOverlapAudioAccepted=False,gameBytesChanged=False,fullPortAcceptance=False,
        scene=scene,erase=erased,inputHashes=pins)
if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite current CPU evidence')
    try: result=run()
    except Exception as error: result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inputHashes','scene','erase')},indent=2),flush=True)
    raise SystemExit(0 if result['passed'] else 1)
