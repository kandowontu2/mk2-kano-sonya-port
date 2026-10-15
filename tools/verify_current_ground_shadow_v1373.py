"""Fresh v1340 native mobility shadows and grounding, normal Dead Pool only.

Independently bind captured graphics to original chips/source UI, every native
compressed shadow row, complete sampled drawing passes, palettes and soles.
Do not promote this bounded mobility result to all-arena/all-move acceptance.
"""
import hashlib,json,re,struct,zlib
from collections import defaultdict
from pathlib import Path
import numpy as np
import verify_ring_native_lookup_v1342 as current
import inspect_current_ground_shadow_v811 as raster
from verify_native_idle_feet_v635 import check_presentation
from verify_cpu_pair_display_v635_v3 import group
from verify_finish_display_v798 import check_owned_body_palette
from verify_stock_fire_v1197 import original_graphics,off

ROOT=current.ROOT
OUT=ROOT/'audit_v1373_current_ground_shadow_checked'

def graphics(pins):
    """Source-bound stock/imported ROM pixels and unchanged native HUD masks."""
    image=bytearray(0x2000000);image[:0xc00000]=original_graphics(pins)
    source=ROOT/current.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    pins[str(source)]=current.digest(source)
    declaration=source.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0]
    pattern=r'ROM_LOAD32_BYTE\(\s*"([^"]+)"\s*,\s*(0x[0-9a-f]+)\s*,\s*(0x[0-9a-f]+)\s*,\s*CRC\(([0-9a-f]+)\)\s*SHA1\(([0-9a-f]+)\)'
    count=0
    for filename,at,length,crc,sha in re.findall(pattern,declaration):
        at,length=int(at,16),int(length,16)
        if at<0xc00000:continue
        path=ROOT/'roms/mk2ks'/filename;raw=path.read_bytes();pins[str(path)]=current.digest(path)
        assert len(raw)==length and zlib.crc32(raw)==int(crc,16) and hashlib.sha1(raw).hexdigest()==sha
        image[at:at+length*4:4]=raw;count+=1
    assert count==20,'All declared imported graphics chips'
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pins[str(ROOT/'mk2/mk2-maincpu.bin')]=current.digest(ROOT/'mk2/mk2-maincpu.bin')
    path=ROOT/'roms/mk2ks/mk2ks.ui';ui=path.read_bytes();pins[str(path)]=current.digest(path)
    colors=struct.unpack_from('<H',ui,6)[0];names=8+2*(colors*2+ui[4]*ui[5]);mw,mh=ui[names:names+2]
    ow=struct.unpack_from('<H',original,off(0xffa79400))[0];sourcebits=struct.unpack_from('<I',original,off(0xffa79400)+8)[0]
    ramp=[]
    for y in range(10):
        counts=[0]*16;best=0
        for x in range(ow):
            bit=sourcebits+(y*ow+x)*4;pen=(int.from_bytes(image[bit//8:bit//8+2],'little')>>(bit%8))&15
            if pen==3 or 5<=pen<=11:
                counts[pen]+=1
                if counts[pen]>counts[best]:best=pen
        ramp.append(best)
    for fighter in range(2):
        mask=ui[names+2+fighter*mw*mh:names+2+(fighter+1)*mw*mh]
        xs=[x for y in range(10) for x in range(mw) if mask[y*mw+x]>48];assert xs
        left,right=min(xs),max(xs);fw=right-left+1;w=fw+1
        face=lambda x,y:0<=x<fw and 0<=y<10 and mask[y*mw+left+x]>48
        for y in range(10):
            for x in range(w):
                pen=ramp[y] if face(x,y) else 2 if x and (face(x-1,y) or (y and face(x-1,y-1))) else 0
                pixel=y*w+x;image[0x1e00000+fighter*0x400+pixel//2]|=pen<<((pixel&1)*4)
    return bytes(image)

def check_sources(log,image):
    records=raster.rows(log,'GFX');assert records
    for r in records:
        first,last=r['first'],r['first']+r['bytes']
        assert 0<=first<last<=len(image),'Source-bound graphics bounds'
        assert bytes.fromhex(r['data'])==image[first:last],'Captured graphics differ from independent ROM/UI source'
    return len(records)

def verify_case(fighter,side,image,guest,payload,pins):
    folder=ROOT/f'audit_v1372_ground_shadow_{fighter}_p{side}'
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/current.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    assert (launch['exit_code'],launch['candidate'],launch['fighter'],launch['side'],launch['assistance'])==(0,current.CANDIDATE,fighter,side,'none')
    assert launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
    assert launch['input_hashes']==before
    for file,wanted in before.items():
        assert current.digest(file)==wanted,'Changed executed input '+file;pins[file]=wanted
        if Path(file).suffix in ('.ps1','.lua','.json'):
            assert current.digest(folder/'input_sources'/Path(file).name)==wanted,'Changed frozen capture input'
    assert all(before.get(file)==wanted for file,wanted in build['input_hashes'].items())
    observer=(folder/'input_sources/mk2ks_ground_shadow_v815_probe.lua').read_text()
    assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Read-only physical-input observer'
    assert '-nocheat' in (folder/'input_sources/run_ground_shadow_v815_probe.ps1').read_text()
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation|stack traceback|INVALID',log,re.I)
    final=raster.rows(log,'RESULT');assert len(final)==1 and final[0]['terminalAge']==480
    fields=raster.rows(log,'FIELD');assert len(fields)==962
    assert [(r['age'],r['slot'])for r in fields]==[(age,slot)for age in range(481)for slot in (1,2)]
    ids=(17 if fighter=='kano'else 18,4) if side==1 else (4,17 if fighter=='kano'else 18)
    anchors={17:134,18:135,4:133};parts=defaultdict(list)
    for p in raster.rows(log,'PART'):parts[p['frame'],p['slot']].append(p)
    descriptors=0
    for r in fields:
        assert r['id']==r['roster']==ids[r['slot']-1] and r['owner']==r['actor'] and r['state']==1
        assert r['hp']==161 and r['floor']==r['stageY']-anchors[r['id']],'Original physical floor remains character-owned'
        expected=group(r,payload,guest);observed=parts[r['frame'],r['slot']]
        assert len(expected)==len(observed),'All actual body cache components'
        for e,p in zip(expected,observed):
            assert (p['part'],p['source'],p['width'],p['height'],p['xoff'],p['yoff'])==(e['part'],e['source'],e['width'],e['height'],e['dx'],e['dy']),'Actual body cache differs from source-bound native composite'
            descriptors+=1
    sources=check_sources(log,image)
    value=raster.inspect(folder);check_presentation(value,fighter,side)
    assert value['native_shadow_row_stream_verified'] and value['native_shadow_components']>=900 and value['native_shadow_copies']>20000
    assert all(r['owned_shadow_mismatches']==0 and r['native_shadow_pen_black'] and r['owned_shadow_pixels'][side]>100 for r in value['records'])
    by_field={(r['frame'],r['slot']):r for r in fields};palettes=0
    for snap in raster.rows(log,'SNAP'):
        q=dict(by_field[snap['frame']-1,side]);actual=np.fromfile(folder/snap['palette_file'],dtype='<u4')
        check_owned_body_palette(q,actual,guest,ids,side);palettes+=1
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=current.digest(path)
    return dict(passed=True,fighter=fighter,side=side,nativeCacheComponents=descriptors,sourceBoundGraphics=sources,
                fullOwnedPaletteSamples=palettes,presentation=value,scope=__doc__,allArenaFloorAccepted=False,allMoveFloorAccepted=False,fullPortAccepted=False)

def verify():
    proof=json.loads((current.OUT/'report.json').read_text());assert proof['passed']and proof['candidate']==current.CANDIDATE
    pins=dict(proof['inputHashes'])
    for file,wanted in pins.items():assert current.digest(file)==wanted,'Changed current source proof'
    guest,_,_,payload=current.reconstruct();image=graphics(pins)
    cases={}
    for fighter in ('kano','sonya'):
        for side in (1,2):
            key=f'{fighter}_p{side}';cases[key]=verify_case(fighter,side,image,guest,payload,pins)
            print(key+' current original shadow rows, native soles and complete sampled raster pass',flush=True)
    for file in ('verify_current_ground_shadow_v1373.py','inspect_current_ground_shadow_v811.py','inspect_ground_presentation.py',
                 'inspect_natural_arena_floor_v602.py','verify_native_floor_display_v602.py','verify_native_idle_feet_v635.py',
                 'verify_cpu_pair_display_v635_v3.py','verify_finish_display_v798.py','verify_stock_fire_v1197.py','verify_native_metadata_build_v1254.py'):
        path=ROOT/'tools'/file;pins[str(path)]=current.digest(path)
    return dict(passed=True,candidate=current.CANDIDATE,cases=cases,inputHashes=pins,
                samples=sum(c['presentation']['samples']for c in cases.values()),
                nativeShadowCopies=sum(c['presentation']['native_shadow_copies']for c in cases.values()),
                currentBoundedMobilityGroundShadowAccepted=True,allArenaFloorAccepted=False,allMoveFloorAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve previous evidence'
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Fresh current ground/shadow passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
