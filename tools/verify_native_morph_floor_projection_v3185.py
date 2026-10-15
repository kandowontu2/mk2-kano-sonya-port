"""Original native morph art, compressed shadow rows and continuous clear.

Four cold normal-input current corrected cases. Full timer write history from
one initial base,32forward and42reverse/recovery scanouts per fixture.
Not every arena, CPU morph/interrupt/KO/victim, other finishers/audio or release.
"""
import inspect,json,re,struct,traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_human_shang_v3148 as old_human
import verify_morph_render_v3149 as old_render
import verify_human_shang_v3174 as human
import verify_morph_render_v3175 as morph
import inspect_native_shadow_rows_v635 as old_rows
import inspect_native_morph_shadow_rows_v3179 as shadows
import verify_native_cpu_ring_erase_v2985 as erase
import inspect_current_cpu_knife_raster_v1975 as raster
import verify_current_ground_shadow_v1859 as graphics
raster.HEX|={'b1','b2','b4','b7','a5','shadow_camera'}
ROOT=assembly.ROOT;need=assembly.need
OUT=ROOT/'audit_v3186_native_morph_floor_projection_checked'

def source_contract():
    need(inspect.getsource(old_human.verify_log)==inspect.getsource(human.verify_log),
      'Every original whole1001-field human command/ID/timer/floor/projectile/restore/control invariant unchanged')
    need(inspect.getsource(old_render.verify_log)==inspect.getsource(morph.verify_log),
      'Every original native composite/palette/DMA/pivot/exact opaque pixel invariant unchanged')
    expected=inspect.getsource(old_rows.inspect).replace("component['id'] in (17,18)","component['id'] in (6,17,18)").replace(
      "if 0x10000000 <= r['source'] < 0x1a000000 and r['command'] & 15 == 8",
      "if r['pc'] in (0xff8015a0,0xff801610) and r['command'] & 15 == 8")
    need(expected==inspect.getsource(shadows.inspect),
      'Every original full row/header/stride/count/copy/writer invariant unchanged; add real stockShangID6 and include stock native shadows')
    erase.source_contract()

def verify():
    source_contract()
    bug_path=ROOT/'audit_v3178_native_morph_shadow_bug_reproduced/report.json'
    bug=json.loads(bug_path.read_text())
    need(bug['passed']and bug['reproducedFailure']and bug['actualDefectiveTransitionComponents']==48 and
      bug['actualBackwardRowSteps']==720 and bug['correctedPayloadIndependentlyReconstructed'],
      'Actual pre-fix failed native shadow rows and independently reconstructed12-descriptor correction retained')
    pins=dict(bug['inputHashes']);pins[str(bug_path)]=assembly.sha(bug_path)
    guest,old,old_payload,ends,ranges=assembly.expected()
    payload=(ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    need(assembly.sha(ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata')==human.PAYLOAD and
      payload==(ROOT/'audit_v3169_native_morph_shadow_payload/roms/mk2ks/mk2ks.mdata').read_bytes(),
      'Whole corrected payload equals independent narrow original-stream reconstruction')
    info=json.loads((ROOT/human.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    need(info['executable_sha256']==human.EXE and info['payload_sha256']==human.PAYLOAD,
      'Exact matched isolated correction executable/payload')
    image=bytearray(graphics.graphics(pins))
    for header,magic in((0x1c0000,b'KFX1'),(0x1c1000,b'KPI1'),(0x1c2000,b'KPJ1'),(0x1d0000,b'KBL1'),(0x118000,b'KSM1')):
        need(payload[header:header+4]==magic,'Actual native auxiliary graphics header')
        start,count,dest=struct.unpack_from('<III',payload,header+4)
        need(count>0 and start+count<=len(payload)and dest+count<=len(image),'Entire native graphics allocation bounds')
        image[dest:dest+count]=payload[start:start+count]
    raster.source(pins);cases={}
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Immutable actual input '+str(path))
        need(str(path)not in pins or pins[str(path)]==actual,'Consistent native input')
        pins[str(path)]=actual
    for target in('kano','sonya'):
        for side in(1,2):
            key=f'{target}_p{side}';folder=ROOT/f'audit_v3184_native_morph_floor_{key}_projection'
            meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            need((meta['exit_code'],meta['lua_errors'],meta['candidate'],meta['target'],meta['side'],meta['profile'],
              meta['executable_sha256'],meta['payload_sha256'],meta['assistance'],meta['cheats_enabled'])==
              (0,0,human.CANDIDATE,target,side,'native',human.EXE,human.PAYLOAD,'none',False),
              'Actual complete normal-input isolated correction case, no cheats/assistance')
            need(before==meta['input_hashes']and all(before.get(p)==h for p,h in info['input_hashes'].items()),
              'Every compiled dependency pinned before and after actual execution')
            need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest unchanged and independently source assembled')
            for path,wanted in before.items():
                pin(path,wanted)
                source=Path(path)
                if source.suffix in('.lua','.ps1','.json'):
                    pin(folder/'input_sources'/source.relative_to(ROOT),wanted)
                if source.suffix=='.lua':
                    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',source.read_text()),
                      'No observer guest/ID/health/AI/RNG/reset assistance')
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            native=human.verify_log(log,target,side,'native');art=morph.verify(folder,target,side)
            need(native['passed']and art['passed'],'Entire original native grammar and exact original art/palette acceptance '+str(native['errors']+art['errors']))
            groups,buffers,_,_,owners=raster.data(folder)
            for row in groups['FLOOR_GFX']:
                lo,hi=row['first'],row['first']+row['bytes']
                need(0<=lo<hi<=len(image)and bytes.fromhex(row['data'])==image[lo:hi],
                  'Every observed body/scene/projectile/stock/imported shadow pixel stream equals independent original ROM source')
            begin=groups['FLOOR_BEGIN'];recovery=groups['FLOOR_RECOVERY'];terminal=groups['FLOOR_RESULT']
            need(len(begin)==len(recovery)==len(terminal)==1,'One genuine morph capture and native restoration')
            stores=[r for t,r in human.rows(log)if t=='STORE']
            reverse=[r for t,r in human.rows(log)if t=='RESTORE_BEGIN']
            start=begin[0]['origin'];restored=int(stores[1]['frame']);reverse_start=int(reverse[0]['frame'])
            need(recovery[0]['frame']==terminal[0]['recovered']==restored and terminal[0]['origin']==start,
              'Actual native restoration store, not guessed timer or forward readiness')
            expected=list(range(start+1,start+33))+list(range(reverse_start+1,restored+31))
            need(len(expected)==74 and [s['frame']for s in groups['FLOOR_SNAP']]==expected and terminal[0]['snapshots']==74,
              'All32forward and42reverse/recovery completed scanouts, no missing transition sample')
            need([r['frame']for r in groups['FLOOR_STATE']]==list(range(start,restored+31)),
              'Complete native morph timer mode/actor/state/HP capture, not only selected transition scenes')
            need(all(r['mode']==2 and r[f'state{side}']==r[f'state{3-side}']==1 and
              r[f'roster{side}']==6 and r[f'roster{3-side}']==17 for r in groups['FLOOR_STATE']),
              'Two actual human actors throughout full native morph timer; original Shang roster retained')
            rows=shadows.inspect(folder)
            need(rows['rowStreamVerified']and not rows['failures']and not rows['oversized_rows'],
              'Every actual native stock/imported/morph shadow row header/source/stride/count/copy/writer exact')
            dmas={r['event']:r for r in groups['FLOOR_DMA']}
            refs={p['graphic']:p for parts in morph.references().values()for p in parts}
            seen=set();geometry=0;transition_copies=0;own_transition_fields=set()
            first_by=defaultdict(list)
            for row in groups['SHADOW_COMPONENT']:
                first_by[row['frame'],row['row']].append(row)
                if row['slot']==side and row['first_source']in refs:
                    part=refs[row['first_source']];flip=bool(row['command']&16)
                    need(row['owner']==row['actor']and row['row']==row['cache']+row['component']*112,
                      'Every actual own transition shadow has its real physical actor/Main and cache component')
                    need((row['width'],row['height'],row['xoff'],row['yoff'],row['command'])==
                      (part['width'],part['height'],part['width']-part['xo']if flip else part['xo'],part['yo'],part['command']+(16 if flip else 0)),
                      'Actual shadow shape/cache/pivot/facing exactly original compressed morph descriptor')
                    seen.add(row['first_source']);own_transition_fields.add(row['frame']);transition_copies+=1
            wanted={p['graphic']for group,parts in morph.references().items()if(group<0xff0c4120)==(target=='kano')for p in parts}
            need(seen==wanted and len(own_transition_fields)==24 and transition_copies>0,
              'All six real original morph parts project actual shadows through24forward/reverse holds')
            projections={(p['frame'],p['row']):p for p in groups['FLOOR_SHADOW_PROJECTION']}
            need(len(projections)==len(groups['FLOOR_SHADOW_PROJECTION'])and set(projections)==set(first_by),
              'Every actual original direct shadow call has its own pose/cache/world/camera/ground/display register evidence')
            short=lambda v:(v&65535)-65536 if v&32768 else v&65535
            subtract=lambda a,b:(((short(a>>16)-short(b>>16))&65535)<<16)|((short(a)-short(b))&65535)
            original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
            lo,hi=((a-0xff800000)//8 for a in(0xff801070,0xff8017b0))
            need(guest[lo:hi]==original[lo:hi],'Entire original MK2 direct shadow world/cache/quarter-height projection code unchanged')
            for proj_key,rows_at in first_by.items():
                r=rows_at[0];d=dmas[r['event']];p=projections[proj_key]
                need(p['pc']==0xff8012c0 and all(p[k]==r[k]for k in('slot','actor','main','owner','id','cache','row','component','floor','stageY')),
                  'Direct projection snapshot belongs to that exact original owned shadow component')
                expected_parts=__import__('verify_cpu_pair_display_v635_v3').group(p,payload,guest)
                part=expected_parts[p['component']]
                need((r['first_source'],r['width'],r['height'],r['xoff'],r['yoff'],r['command'])==
                  (part['source'],part['width'],part['height'],part['dx'],part['dy'],part['command']),
                  'All direct shadow component words equal actual draw-time ROM pose, never substitute queued body pose')
                need(p['body']&16 and p['b4']==subtract(p['world'],p['shadow_camera']) and
                  p['b2']==((p['stageY']-short(p['shadow_camera']>>16)+p['b7'])&65535)<<16,
                  'Exact original world-camera subtraction and native B7 ground offset, not a guessed sole offset')
                top_y=short(p['b4']>>16)-part['dy']
                gap=(short(p['b2']>>16)-top_y)&65535
                expected_y=(short(p['b2']>>16)-(gap//4)+short(p['a5']>>16))&511
                expected_x=(short(p['b4'])-part['dx']+(part['width']-1 if part['command']&16 else 0)+short(p['a5']))&1023
                need((d['x'],d['y'])==(expected_x,expected_y),
                  'Actual source-derived direct quarter-height world/cache/camera/ground/display projection exact')
                geometry+=1
            print(key+': original morph art and '+str(rows['checked_copies'])+' exact native shadow copies; checking buffers',flush=True)
            video=raster.inspect(folder)
            need(video['frames']==74 and all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records']),
              'All74complete scenes independently match actual DMA/CPU/native buffers/palette/screenshot')
            continuous=erase.inspect(folder,guest,human.CANDIDATE)
            need(continuous['passed']and continuous['oneInitialBaseOnly']and not continuous['laterBuffersUsedAsAnchors']and
              continuous['continuousExactPreBuffers']==continuous['continuousExactFlips']==74,
              'Entire timer write history from one initial base, all targets exact with no later buffer anchors')
            for r in groups['FLOOR_DISPLAY']:
                colors=np.fromfile(folder/r['palette_file'],dtype='<u4')
                need(colors[15]==0,'Every completed scene retains actual black native shadow pen')
            for path in folder.rglob('*'):
                if path.is_file():pin(path)
            cases[key]=dict(passed=True,native=native,art=art,shadowRows=rows,
              exactQuarterHeightProjections=geometry,actualOwnTransitionShadowCopies=transition_copies,
              actualOwnTransitionShadowFields=len(own_transition_fields),sampledFrames=74,
              exactScreenPixels=sum(r['display_pixels']for r in video['records']),
              continuousErase=continuous,allArenasAndCPUMorphsAccepted=False)
            print(key+': all74original scenes and continuous native clears exact',flush=True)
    for module in(assembly,human,morph,old_human,old_render,shadows,old_rows,erase,raster,graphics):
        pin(module.__file__)
    pin(Path(__file__));pin(ROOT/human.CANDIDATE/'build-info.json')
    report=dict(passed=True,candidate=human.CANDIDATE,physicalCases=4,cases=cases,
      correctedNativeMorphShadowStreamsAccepted=True,actualDirectNativeProjectionRegistersAccepted=True,
      supersededAssumedGroundOffsetReport=str(ROOT/'audit_v3181_native_morph_floor_checked/report.json'),allOriginalMorphBodyPixelsPalettesGrammarAndControlsRetained=True,
      exactNativeTransitionAndRecoveryScenes=296,
      exactScreenPixels=sum(c['exactScreenPixels']for c in cases.values()),
      actualNativeShadowCopies=sum(c['shadowRows']['checked_copies']for c in cases.values()),
      actualOwnTransitionShadowCopies=sum(c['actualOwnTransitionShadowCopies']for c in cases.values()),
      fullNativeTimerChronologicalEraseAccepted=True,oneInitialBasePerActualFixture=True,
      laterBuffersUsedAsAnchors=False,gameplayPayloadChanged=True,nativeGuestProgramChanged=False,
      allArenasVictimsCPUMorphsInterruptsKOAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins)
    return report

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite native morph floor evidence')
    try:value=verify()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','cases','traceback')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
