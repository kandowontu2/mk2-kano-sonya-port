"""Source-bound native blade scenes and explicit prior/current blood differences.

Diagnostic ownership tag 4 identifies original blood DMA only; it never
changes guest memory, captured pixels, sprite positions or palette values.
"""
import argparse,json,re,struct
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
import verify_ring_native_lookup_v1342 as current
import verify_native_metadata_build_v1254 as prior
import verify_current_ground_shadow_v1269 as ground
import verify_human_special_matrix as human
import inspect_secondary_display_v1231 as raster
from verify_cpu_pair_display_v635_v3 import group
from verify_finish_display_v798 import check_owned_body_palette,check_latch
ROOT=current.ROOT
raster.HEX |= {'palette_source'}
BLOOD_PALETTE=0xffaf2a40

def events(log):
    return [re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_PALETTE_ALLOCATION',r)
            for r in log.splitlines()if r.startswith('MK2_HSPECIAL_')]

def verify_case(side,old,pins):
    model=prior if old else current
    folder=ROOT/f'audit_v{1387 if old else 1383}_blade_native_{"prior_"if old else ""}p{side}'
    baseline=ROOT/f'audit_v{1252 if old else 1365}_human_blade_p{side}'
    build=json.loads((ROOT/model.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    assert (launch['exit_code'],launch['candidate'],launch['move'],launch['side'],launch['victim'])==(0,model.CANDIDATE,'blade',side,'sub_zero')
    assert launch['assistance']=='none'and launch['cheats_enabled']is False
    assert launch['executable_sha256']==build['executable_sha256']and launch['payload_sha256']==build['payload_sha256']
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    assert before==launch['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items())
    for file,wanted in before.items():
        assert current.digest(file)==wanted,'Changed executed input '+file;pins[file]=wanted
        if Path(file).suffix in('.lua','.json','.ps1'):
            frozen=folder/'input_sources'/Path(file).name
            assert current.digest(frozen)==wanted;pins[str(frozen)]=wanted
    for name in('mk2ks_human_special_matrix_v3.lua','mk2ks_human_blade_full_display_v1382.lua'):
        source=(folder/'input_sources'/name).read_text()
        assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',source)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|stack traceback|access violation',log,re.I)
    assert events(log)==events((baseline/'run.log').read_text(encoding='utf-8-sig'))
    state=human.verify_log(log,'blade',side)
    result,=human.rows(log,'RESULT');target=result['recovered']-1
    for name in('special_before.png','special_recovered.png','special_final.png'):
        assert(folder/'snap'/name).read_bytes()==(baseline/'snap'/name).read_bytes(),'Readonly observer changed actual scene'
        pins[str(baseline/'snap'/name)]=current.digest(baseline/'snap'/name)
    pins[str(baseline/'run.log')]=current.digest(baseline/'run.log')
    guest,_,_,payload=model.reconstruct()
    assert(folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest differs from source'
    image=bytearray(ground.graphics(pins))
    for header,source,destination,magic in((0x1c0000,0x1c4000,0x1e04000,b'KFX1'),(0x1c1000,0x1e6000,0x1e50000,b'KPI1'),(0x1c2000,0x1f4000,0x1e60000,b'KPJ1')):
        assert payload[header:header+4]==magic
        start,count,dest=struct.unpack_from('<III',payload,header+4)
        assert(start,dest)==(source,destination)
        image[destination:destination+count]=payload[source:source+count]
    groups,_,_,_,_=raster.data(folder)
    assert not groups['FLOOR_CHILD_ALLOC']and not groups['FLOOR_CHILD_SPAWN'],'Blade has no projectile child'
    for r in groups['FLOOR_GFX']:
        assert bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'Actual source graphics including all native blood'
    inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
    palette_inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_PALETTE']}
    assert len(inventory)==len(groups['FLOOR_ALL_QUEUE'])and inventory.keys()==palette_inventory.keys()
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    blood={};by_cursor=defaultdict(list)
    for key,q in inventory.items():
        by_cursor[q['cursor']].append(q)
        p=palette_inventory[key]
        assert(p['actor'],p['bank'],p['pc'])==(q['actor'],q['bank']&0x7f00,0xff804420)
        if p['palette_source']!=BLOOD_PALETTE:continue
        assert q['id']==0 and q['body']&2==0 and p['refs']>0
        at=(q['cache']-0xff800000)//8
        assert 0<=at<=len(original)-14 and guest[at:at+14]==original[at:at+14]
        desc=struct.unpack_from('<4hIH',original,at)
        assert desc[4]==q['source']and 0<desc[0]<=128 and 0<desc[1]<=128
        blood[key]=dict(queue=q,palette=p,descriptor=desc)
    assert len(blood)>100,'Real native blood publications required'
    regs={r['event']:r for r in groups['FLOOR_DMA_REGS']};blood_events={};physical={}
    tracked={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    parts=defaultdict(list)
    for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
    for d in groups['FLOOR_DMA']:
        candidates=[q for q in by_cursor[regs[d['event']]['b14']+192]if q['frame']<=d['frame']]
        if not candidates or d['command']&15!=2:continue
        q=max(candidates,key=lambda q:q['frame']);key=(q['frame'],q['cursor'])
        if q['source']!=d['source']:continue
        if key in blood:
            b=blood[key]
            assert d['slot']==0 and d['palette']==b['palette']['bank']
            assert(d['width'],d['height'])==b['descriptor'][:2]
            blood_events[d['event']]=b
        if key in tracked:
            q=tracked[key];assert q['slot']in(1,2)and d['slot']==q['slot']
            expected=group(q,payload,guest);actual=parts[key]
            assert len(actual)==len(expected)and all(all(a[k]==v for k,v in e.items())for a,e in zip(actual,expected))
            assert q['source']==d['source']and q['bank']&0x7f00==d['palette']
            physical[d['event']]=q
    assert len(blood_events)>100
    # Preserve every original pixel operation, adding a diagnostic-only
    # ownership label to the blood operations resolved from actual FIFO.
    Replay=raster.Replay;mask=[None]
    class BloodReplay(Replay):
        def dma(self,d):
            super().dma({**d,'slot':4}if d['event']in blood_events else d)
        def apply(self,kind,d):
            super().apply(kind,d)
            if d['frame']==target-1:mask[0]=(self.body==4).copy()
    raster.Replay=BloodReplay
    try:drawn=raster.inspect(folder)
    finally:raster.Replay=Replay
    assert drawn['frames']>100 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records'])
    count=struct.unpack_from('<H',original,(BLOOD_PALETTE-0xff800000)//8)[0];assert count==15
    off=(BLOOD_PALETTE-0xff800000)//8
    assert guest[off:off+2+count*2]==original[off:off+2+count*2]
    colors=struct.unpack_from('<15H',original,off+2)
    expected_palette=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest for s,dest in((10,16),(5,8),(0,0)))for c in colors],dtype=np.uint32)
    palette_checks=0;own_checks=0
    by_frame=defaultdict(list)
    for d in groups['FLOOR_DMA']:by_frame[d['frame']].append(d)
    ids=(17,9)if side==1 else(9,17)
    for display in groups['FLOOR_DISPLAY']:
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
        for d in by_frame[display['frame']-1]:
            if d['event']in blood_events:
                bank=blood_events[d['event']]['palette']['bank']
                assert np.array_equal(actual[bank:bank+15],expected_palette);palette_checks+=1
            if d['event']in physical and physical[d['event']]['slot']==side:
                check_owned_body_palette(physical[d['event']],actual,guest,ids,side);own_checks+=1
    assert palette_checks>100 and own_checks>100 and mask[0]is not None
    snap=next(r for r in groups['FLOOR_SNAP']if r['frame']==target)
    latch=next(r for r in groups['FLOOR_LATCH']if r['snapshot']==target and r['flip_frame']==target)
    flip=next(r for r in groups['FLOOR_FLIP']if r['event']==latch['event'])
    display=next(r for r in groups['FLOOR_DISPLAY']if r['frame']==target)
    picture=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))
    assert np.array_equal(picture,np.asarray(Image.open(folder/'snap/special_recovered.png').convert('RGB'))),'Exact callback recovery belongs to prior native completed field'
    bound=check_latch(picture,(folder/latch['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),flip['value'],flip['control'],flip['tap'])
    row,col=bound['row'],bound['column'];gore=mask[0][row:row+254,col:col+400]
    assert int(gore.sum())==next(r for r in drawn['records']if r['frame']==target)['body'][4]['pixels']
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=current.digest(path)
    report=dict(passed=True,candidate=model.CANDIDATE,side=side,state=state,recoveryNativeFrame=target,
                replayed=drawn,nativeBloodPublications=len(blood),nativeBloodDraws=len(blood_events),
                originalBloodPaletteSource=f'{BLOOD_PALETTE:08X}',fullBloodPaletteSamples=palette_checks,
                fullOwnPaletteSamples=own_checks,recoveryBloodPixels=int(gore.sum()),
                diagnosticOwnershipLabel4Only=True,fullPortAccepted=False)
    return report,picture,gore

def verify(side):
    pins={};new,picture,mask=verify_case(side,False,pins);old,old_picture,old_mask=verify_case(side,True,pins)
    changed=np.any(picture!=old_picture,axis=2)
    assert changed.any()and not np.any(changed&~(mask|old_mask)),'Every differing pixel must belong to independently reconstructed original native blood'
    for name in('verify_blade_native_gore_v1384.py','inspect_secondary_display_v1231.py','verify_current_ground_shadow_v1269.py','verify_ring_native_lookup_v1342.py','verify_native_metadata_build_v1254.py','verify_human_special_matrix.py','verify_finish_display_v798.py','verify_cpu_pair_display_v635_v3.py'):
        path=ROOT/'tools'/name;pins[str(path)]=current.digest(path)
    return dict(passed=True,candidate=current.CANDIDATE,side=side,current=new,prior=old,
                changedPixels=int(changed.sum()),allDifferencesAreOriginalNativeBlood=True,
                inputHashes=pins,allMoveArtAccepted=False,audioAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('side',type=int,choices=(1,2));args=parser.parse_args()
    out=ROOT/f'audit_v1384_blade_native_gore_p{args.side}_checked';assert not out.exists()
    try:report=verify(args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Blade native gore p'+str(args.side)+' passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)
