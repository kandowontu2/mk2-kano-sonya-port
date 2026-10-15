"""Reproduce actual backward morph shadow scan before the narrow asset fix.

Pass means the defect is proved, not that the game or shadow is accepted.
The corrected payload changes only12descriptor source/format fields.
"""
import hashlib,json,struct
from pathlib import Path
from collections import defaultdict
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_morph_render_v3149 as old_render
import verify_native_cpu_ring_erase_v2985 as erase
import inspect_current_cpu_knife_raster_v1975 as raster
import build_native_shang_morphs as assets
ROOT=assembly.ROOT;need=assembly.need
OUT=ROOT/'audit_v3178_native_morph_shadow_bug_reproduced'
CASE=ROOT/'audit_v3167_current_morph_floor_sonya_p2'

def verify():
    need(not OUT.exists(),'Never overwrite defect evidence')
    guest,old,payload,ends,ranges=assembly.expected()
    need((CASE/'guest_maincpu.bin').read_bytes()==guest,'Whole actual pre-fix initialized guest source-bound')
    old_art=old_render.verify(CASE,'sonya',2)
    need(old_art['passed']and old_art['transition_fields']==24 and old_art['native_component_fields']==80,
      'Existing passing full-body morph art test retained; it never proved floor shadows')
    groups,buffers,_,_,owners=raster.data(CASE)
    dmas={d['event']:d for d in groups['FLOOR_DMA']}
    raw_sources=set()
    for i in range(12):
        raw_sources.add(struct.unpack_from('<I',payload,assets.FRAMES+i*20+8)[0])
    rows=defaultdict(list)
    for row in groups['SHADOW_COMPONENT']:
        if row['slot']==2 and row['first_source']in raw_sources:
            rows[row['frame'],row['row']].append(row)
    need(len(rows)==48,'All24actual forward/reverse holds times two real components captured')
    failures=[];reverse_steps=0
    for (frame,cache),copies in sorted(rows.items()):
        first=copies[0];source=first['first_source'];command=first['command'];w=first['width'];h=first['height']
        need((command>>12)&7==6 and not command&128,'Actual morph components use uncompressed six-bit rows')
        need(first['owner']==first['actor']and first['row']==first['cache']+first['component']*112,
          'Real physical own actor/Main and component cache')
        need(0x07ffffff<source+0x02000000<0x12000000,
          'Actual CPU row scanner address lies in unmapped gap, outside stock/imported graphics maps')
        indices=list(range(0,4*(h//4),4));indices.append(indices[-1])
        expected=[source+y*w*6 for y in indices]
        actual=[dmas[r['event']]['source']for r in copies]
        need(len(actual)==len(expected)and actual!=expected,
          'Original copy count reached but row pointers demonstrably not original full sprite rows')
        backwards=sum(b<a for a,b in zip(actual,actual[1:]));reverse_steps+=backwards
        failures.append(dict(frame=frame,component=first['component'],actor=first['actor'],main=first['main'],
          id=first['id'],source=source,command=command,width=w,height=h,
          expectedUncompressedRowSources=expected,actualNativeRowSources=actual,backwardSteps=backwards))
    need(reverse_steps>0,'Actual native row pointer goes backward, not merely a hypothetical mapping problem')
    record=json.loads((ROOT/'audit_v3169_native_morph_shadow_payload/report.json').read_text())
    corrected=(ROOT/'audit_v3169_native_morph_shadow_payload/roms/mk2ks/mk2ks.mdata').read_bytes()
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    expected=bytearray(payload);fields=[]
    for fi,target in enumerate(('kano','sonya')):
        for gi,group in enumerate(assets.SOURCE_GROUPS[target]):
            for ci,descriptor in enumerate(assets.animation.frame_group(donor,group,0xff800000,0xffffffff)):
                source,command,w,h,xo,yo=assets.decoder.component_spec(donor,descriptor)
                at=assets.FRAMES+(fi*6+gi*2+ci)*20
                need(command&128 and(command>>12)&7==6,'Genuine original six-bit compressed morph art')
                struct.pack_into('<IH',expected,at+8,source+0x10000000,command)
                fields.append(at+8)
    need(corrected==expected and assembly.sha(ROOT/'audit_v3169_native_morph_shadow_payload/roms/mk2ks/mk2ks.mdata')==
      'ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3',
      'Entire corrected payload independently reconstructed; only12original native source/format fields')
    pins=assembly.source_check()
    meta=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'))
    for path,wanted in meta['input_hashes'].items():
        need(assembly.sha(path)==wanted,'Actual pre-fix immutable input');pins[path]=wanted
    for path in CASE.rglob('*'):
        if path.is_file():pins[str(path.resolve())]=assembly.sha(path)
    for path in(ROOT/'audit_v3169_native_morph_shadow_payload').rglob('*'):
        if path.is_file():pins[str(path.resolve())]=assembly.sha(path)
    for module in(assembly,old_render,old_render.human,erase,raster,assets):
        path=Path(module.__file__);pins[str(path.resolve())]=assembly.sha(path)
    pins[str(Path(__file__).resolve())]=assembly.sha(__file__)
    report=dict(passed=True,reproducedFailure=True,beforeFixRuntimeMorphShadowsAccepted=False,
      actualDefectiveTransitionComponents=len(failures),actualBackwardRowSteps=reverse_steps,
      failures=failures,originalBodyArtPositiveControlRetained=True,
      correctedPayloadIndependentlyReconstructed=True,changedDescriptors=12,
      correctedRuntimeAcceptancePending=True,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('failures','inputHashes')},indent=2),flush=True)

if __name__=='__main__':verify()
