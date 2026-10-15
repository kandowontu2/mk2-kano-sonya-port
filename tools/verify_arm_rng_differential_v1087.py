"""Explain native blood variation; do not exempt arbitrary visual differences.

Paired original/new builds use identical physical inputs/read-only observers.
Every RNG result is reconstructed from the ORIGINAL shift/carry/beam rotation.
Every changed image pixel must lie on an actual decoded opaque native blood
pixel drawn before that snapshot. Historical full-image equality is NOT claimed.
"""
import copy
import json
import re
import struct
from pathlib import Path

import numpy as np
from PIL import Image
import verify_native_arm_palette_v1074 as normal
import verify_projectile_render as raster

ROOT=normal.ROOT
OUT=ROOT/'audit_v1087_arm_rng_differential_checked'
MASK32=(1<<32)-1
OLD='diagnostic_v1061_owned_arm_invariant_blood'
NEW=normal.CANDIDATE
BLOOD_SOURCES={int(value,16) for value in (
    '040DA146','040DA58E','040DB246','040DC9A6','040DEA4A','040E13BA',
    '040E438A','040E710A','040EA44A','040F1B86','040F1DFA','040F20D6',
    '040F23CE','040F272E','040F2AEE','040F2EAE','04107A58','04107D98',
    '04108208','04143947','040AC716')}


def is_blood(row):
    # Bank05 is the original blood-puddle fade, not an arbitrary effect bank.
    return row['bank'] in ('0404','0505') and int(row['source'],16) in BLOOD_SOURCES


def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^ ]+)',line)) for line in text.splitlines()
            if line.startswith('MK2_ARM_RNG_V1085_'+tag+' ')]


def rng(text):
    entry,beam,result=(rows(text,tag) for tag in ('ENTRY','HCOUNT','RESULT'))
    assert len(entry)==len(beam)==len(result)>100
    for index,(a,b,c) in enumerate(zip(entry,beam,result),1):
        assert a['serial']==b['serial']==c['serial']==str(index)
        assert a['frame']==b['frame']==c['frame']
        assert a['writes']==b['writes']==c['writes']=='0'
        assert a['assistance']==b['assistance']==c['assistance']=='none'
        seed=int(a['seed'],16)
        shifted=(seed<<1)&MASK32
        overflow=((seed>>31)^(seed>>30))&1
        if not overflow:shifted|=2
        before=(shifted+(seed>>31))&MASK32
        assert int(b['stored_seed'],16)==int(c['stored_seed'],16)==shifted
        assert int(b['before'],16)==int(c['before'],16)==before
        assert b['pc']=='FF80EA90'
        count=int(b['count'],16)
        assert int(c['count'],16)==int(c['a1'],16)==count
        shift=count&31
        rotated=((before<<shift)|(before>>((-shift)&31)))&MASK32
        assert int(c['result'],16)==rotated
    return entry,beam,result


def nonblood(text):
    output=[]
    for row in rows(text,'FIFO'):
        if is_blood(row):continue
        row=dict(row);row.pop('cursor')
        # Varying native blood lifetimes alter free-list addresses for later
        # font/effect objects. Never remove real fighter/owned-arm identities.
        if row['id']=='0' and not 0x0fa00000<=int(row['source'],16)<0x0fb00000:
            row.pop('actor')
        output.append(row)
    return output


def picture_frame(path,start):
    suffix=int(re.search(r'_(\d+)\.png$',path.name)[1])
    return start+suffix if path.name.startswith('stock_head_') else suffix


def require_blood_only(a,b,allowed):
    changed=np.any(a!=b,axis=2)
    assert not np.any(changed&~allowed),'Pixel changed outside decoded native blood'
    return int(changed.sum())


def compare_pictures(old,new,texts,start,pins):
    blood=sorted([r for text in texts for r in rows(text,'FIFO') if is_blood(r)],
                 key=lambda r:int(r['frame']))
    assert blood and all(r['id']=='0' and r['writes']=='0' for r in blood)
    before={p.name:p for p in (old/'snap').glob('*.png')}
    after={p.name:p for p in (new/'snap').glob('*.png')}
    assert before.keys()==after.keys()
    accumulated=np.zeros((254,400),dtype=bool)
    masks={};index=0;different=0;changed=0
    for name,path in sorted(after.items(),key=lambda pair:picture_frame(pair[1],start)):
        frame=picture_frame(path,start)
        while index<len(blood) and int(blood[index]['frame'])<frame:
            row=blood[index];index+=1
            size=int(row['size'],16);w,h=size&65535,size>>16
            source=int(row['source'],16);command=int(row['command'],16)>>16
            assert command&15==2 and source<0x06000000
            key=(source,command,w,h)
            if key not in masks:masks[key]=raster.native_pixels(source,command,w,h)!=0
            mask=masks[key];xy=int(row['xy'],16)
            x=(xy&65535)-56;y=(xy>>16)&255
            if command&16:mask=mask[:,::-1];x-=w-1
            if command&32:mask=mask[::-1];y-=h-1
            xa,ya=max(0,x),max(0,y);xb,yb=min(400,x+w),min(254,y+h)
            if xa<xb and ya<yb:
                accumulated[ya:yb,xa:xb]|=mask[ya-y:yb-y,xa-x:xb-x]
        a=np.asarray(Image.open(before[name]).convert('RGB'))
        b=np.asarray(Image.open(path).convert('RGB'))
        assert a.shape==b.shape==(254,400,3)
        count=require_blood_only(a,b,accumulated)
        changed+=count;different+=bool(count)
        for p in (before[name],path):pins[str(p)]=normal.digest(p)
    # An unrelated corner corruption must not be accepted by the scoped mask.
    fake=b.copy();fake[0,0]^=255
    try:require_blood_only(a,fake,accumulated)
    except AssertionError:pass
    else:raise AssertionError('Blood scope accepted unrelated corner corruption')
    return {'actualPNGsCompared':len(after),'differentRGBScenes':different,
            'changedPixelsAllOnDecodedNativeBlood':changed,
            'decodedBloodMasks':len(masks),'persistentBloodCoveragePixels':int(accumulated.sum())}


def verify():
    pins={};cases={}
    guest,graphics,_=normal.reconstruct()
    archive=ROOT/'audit_v1070_arm_palette_source_transition/input_sources/midtunit_m.cpp'
    current=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    assert normal.digest(archive)=='29A023356C55A7FA89110FA27FDE2B7A6AB49562967D6BD44C5167B40F7AC2EB'
    assert normal.digest(current)=='1DF1D1217776DBC3830F00ED078589A925A81F7C356F8EADE117907711A68CF6'
    code=current.read_bytes();begin=code.index(b'\t// The native detached-arm constructor')
    end=code.index(b'\t// Every stock head-removal finisher',begin)
    assert code[:begin]+code[end:]==archive.read_bytes(),'Undeclared game-source change'
    for source in (archive,current,Path(__file__),ROOT/'mk2ks_arm_rng_trace_v1085.lua',
                   ROOT/'tools/run_arm_rng_diagnostic_v1086.ps1'):
        pins[str(source)]=normal.digest(source)
    observer=(ROOT/'mk2ks_arm_rng_trace_v1085.lua').read_text()
    assert 'write_u' not in observer and 'install_write_tap' not in observer
    assert ':read_u16(0xc00001c0)' not in observer
    oldguest=(ROOT/'audit_v1062_jax_kano_p1_invariant_blood/guest_maincpu.bin').read_bytes()
    expected=bytearray(oldguest)
    expected[0xfbc00:0xfbc60]=normal.palette_router()
    struct.pack_into('<HI',expected,normal.off(0xff8bed50),0xc080,0xfffde000)
    assert bytes(expected)==guest
    # Both builds execute the exact original RNG, including its HCOUNT operand.
    assert oldguest[normal.off(0xff80e980):normal.off(0xff80eb70)]==guest[normal.off(0xff80e980):normal.off(0xff80eb70)]
    for name in ('kano','sonya'):
        for side in (1,2):
            pair=[ROOT/f'audit_v1086_jax_{name}_p{side}_{v}_rng' for v in ('old','new')]
            texts=[];replay_counts=[]
            for index,folder in enumerate(pair):
                result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
                assert result['exit_code']==0 and result['candidate']==(OLD if index==0 else NEW)
                assert result['player']==name and result['victim_slot']==side
                assert result['killer']=='jax' and result['command']=='bbbb_lp' and result['target_gap']==96
                assert result['assistance']=='none' and not result['cheats_enabled']
                info=json.loads((ROOT/result['candidate']/'build-info.json').read_text(encoding='utf-8-sig'))
                assert result['executable_sha256']==info['executable_sha256']
                assert result['payload_sha256']==info['payload_sha256']
                for filename,wanted in result['input_hashes'].items():
                    assert normal.digest(Path(filename))==wanted,filename
                    pins[filename]=wanted
                text=(folder/'run.log').read_text(encoding='utf-8-sig');texts.append(text)
                assert not re.search(r'\[LUA ERROR\]|fatal error|access violation',text,re.I)
                assert 'MK2_STOCK_HEAD_V921_RESULT frame=5198' in text
                assert ' age=147 ' in next(l for l in text.splitlines() if l.startswith('MK2_STOCK_HEAD_V921_WRAP '))
                assert (folder/'guest_maincpu.bin').read_bytes()==(oldguest if index==0 else guest)
                assert (folder/'native_arm_rip_gfx.bin').read_bytes()==graphics
                prior=ROOT/(f'audit_v1062_jax_{name}_p{side}_invariant_blood' if index==0
                            else f'audit_v1072_jax_{name}_p{side}_native_palette')
                a={p.name:p for p in (folder/'snap').glob('*.png')}
                b={p.name:p for p in (prior/'snap').glob('*.png')}
                assert a.keys()==b.keys() and all(p.read_bytes()==b[k].read_bytes() for k,p in a.items()),'Read-only observer altered replay'
                replay_counts.append(len(a))
                for filename in ('run.log','result.json','guest_maincpu.bin','native_arm_rip_gfx.bin'):
                    pins[str(folder/filename)]=normal.digest(folder/filename)
                for p in b.values():pins[str(p)]=normal.digest(p)
            oldrng,newrng=map(rng,texts)
            first=next(i for i,(a,b) in enumerate(zip(oldrng[1],newrng[1])) if a!=b)
            assert first>50 and oldrng[0][:first+1]==newrng[0][:first+1]
            a,b=oldrng[1][first],newrng[1][first]
            assert a['before']==b['before'] and a['stored_seed']==b['stored_seed']
            assert a['count']!=b['count']
            start=int(re.search(r'MK2_STOCK_HEAD_V921_ACTION frame=(\d+)',texts[0])[1])
            assert int(a['frame'])==start+88
            assert nonblood(texts[0])==nonblood(texts[1]),'Nonblood native drawing changed'
            # Preserve every real fighter/arm actor and DMA geometry; only FIFO
            # slot addresses may differ because the original blood objects vary.
            actual=lambda t:[re.sub(r' cursor=[0-9A-F]{8}','',l) for l in t.splitlines()
                             if l.startswith('MK2_ROLLING_HEAD_V1003_ALL_FIFO ')]
            assert actual(texts[0])==actual(texts[1])
            native=normal.prior.rows(texts[1],'MK2_STOCK_HEAD_V921')
            action=next(r for t,r in native if t=='ACTION')
            assert not normal.check_palette_route(texts[1],action,17 if name=='kano' else 18,False)
            summary=compare_pictures(*pair,texts,start,pins)
            summary.update(readOnlyReplayPNGsExact=replay_counts,
                           originalRNGCalls=[len(oldrng[0]),len(newrng[0])],
                           firstEntropyDifferenceFrame=int(a['frame']),
                           firstEntropyDifferenceSerial=first+1,
                           originalCount=a['count'],newCount=b['count'],
                           samePreRotateValue=a['before'],sameStoredSeed=a['stored_seed'],
                           fighterAndOwnedArmIdentityAndRenderingUnchanged=True,
                           otherNativeRenderingUnchanged=True)
            cases[f'{name}_p{side}']=summary
    return {'passed':True,'errors':[],'cases':cases,'inputHashes':pins,
            'scope':'four unassisted original/new native arm-rip paired replays; actual raster-entropy and blood-only image difference diagnosis',
            'historicalWholeImageEqualityRejected':True,'arbitraryVisualDifferencesExempted':False,
            'naturalAlternateSelectionAccepted':False,'allStockFatalitiesAccepted':False,'fullPortAccepted':False}


if __name__=='__main__':
    if OUT.exists():raise ValueError('Preserve diagnostic evidence')
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2))
