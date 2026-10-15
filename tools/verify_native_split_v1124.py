"""Independent own-art and genuine split runtime proof; normal Dead Pool only.

Reconstruct the exact change from the pinned prior native ROM and immutable
source artwork. Do not import the split encoder as its own expected result.
Historical native reconstruction retains its explicit pinned-ROM baseline.
"""
import hashlib
import json
import re
import struct
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects
import verify_native_arm_palette_v1074 as previous
import verify_native_split_grammar_v1100 as grammar

ROOT = previous.ROOT
CANDIDATE = 'diagnostic_v1110_owned_native_split'
OUT = ROOT/'audit_v1124_owned_native_split_checked'
CASES = tuple(f'audit_v1111_kung_lao_{name}_p{side}_owned_split'
              for name in ('kano','sonya') for side in (1,2))
OLD_SOURCE = '1DF1D1217776DBC3830F00ED078589A925A81F7C356F8EADE117907711A68CF6'
NEW_SOURCE = 'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34'
SOURCE_PNGS = {
    'art_native_split_v1106/kano-initial-three.png': '918E8FA9C30B07C503A48BA633225781CC03833F1EBBDDB28D7670A6F19D68D1',
    'art_native_split_v1106/sonya-initial-three.png': 'FFFBC7FB7D751E1ABF20F71AFC2110491AFD30D9D00D0B12350A4110C41033C0',
    'art_native_split_v1104/kano-half-seven.png': 'C621CC82EB73B5978485CBBB1C74D101E99A793A9D131FEDBC5720D56EE186B1',
    'art_native_split_v1104/sonya-half-seven.png': '4DBF329AD8498BFC4F25BD15A3421D9B0B450345CE4740C4BB80863E532BA4CE',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def native(at):
    return 0xff800000+8*at


def connected_sprites(path, count):
    rgba = np.asarray(Image.open(path).convert('RGBA'))
    components, _ = label(rgba[:,:,3] >= 128, np.ones((3,3)))
    sprites = []
    for number, section in enumerate(find_objects(components),1):
        if section is None:
            continue
        selected = components[section] == number
        if np.count_nonzero(selected) < 1000:
            continue
        yy,xx = section
        assert min(xx.start,yy.start) > 0
        assert xx.stop < rgba.shape[1] and yy.stop < rgba.shape[0]
        crop = rgba[section].copy()
        crop[:,:,3][~selected] = 0
        sprites.append((xx.start,Image.fromarray(crop)))
    sprites.sort(key=lambda row:row[0])
    assert len(sprites) == count, 'Required independent alpha components'
    return [image for _,image in sprites]


def body_palette(donor, offset):
    assert struct.unpack_from('<I',donor,offset)[0] == 64
    pens = struct.unpack_from('<64H',donor,offset+4)
    result = [(0,0,0)]
    for pen in pens:
        values = [(pen>>shift)&31 for shift in (10,5,0)]
        result.append(tuple(v*255//31 for v in values))
    return np.asarray(result,dtype=np.uint8)


def packed_six(indices):
    value, count, output = 0,0,bytearray()
    for pen in indices.ravel():
        value |= int(pen)<<count
        count += 6
        while count >= 8:
            output.append(value&255)
            value >>= 8
            count -= 8
    if count:
        output.append(value&255)
    return bytes(output)


def reconstruct():
    source_path = ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    old_path = ROOT/'audit_v1108_split_source_transition/input_sources/midtunit_m.cpp'
    source,old = source_path.read_bytes(),old_path.read_bytes()
    assert digest(source_path) == NEW_SOURCE and digest(old_path) == OLD_SOURCE
    start = source.index(b"\t// Kung Lao's original vertical split table stops")
    end = source.index(b'\t// Dedicated Kano/Sonya headless collapse',start)
    assert source[:start]+source[end:] == old, 'Exact bounded compiled-source transition'
    build = json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    assert (ROOT/CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp').read_bytes() == source
    for file,wanted in build['input_hashes'].items():
        assert digest(Path(file)) == wanted, 'Exact build input '+file
    assert digest(ROOT/CANDIDATE/'mkport_candidate.exe') == build['executable_sha256']
    old_payload = (ROOT/previous.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    assert hashlib.sha256(old_payload).hexdigest().upper() == '5D78E543EA1E387461BD7EFF0958F9829565469CD51D5B2EE0A6CF1D90F0D322'
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    donor = (ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assert hashlib.sha256(stock).hexdigest().upper() == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    assert hashlib.sha256(donor).hexdigest().upper() == '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    for file,wanted in SOURCE_PNGS.items():
        assert digest(ROOT/file) == wanted, 'Immutable source artwork '+file
    wanted = bytearray(old_payload)
    for lo,hi in ((0x1c3800,0x1c4000),(0x172000,0x180000),(0x1bc000,0x1c0000)):
        assert wanted[lo:hi] == b'\xff'*(hi-lo)
    assets = {}
    ranges = ((0x172000,0x180000),(0x1bc000,0x1c0000))
    bank,cursor,gfx,index = 0,0x172000,0x1f60000,0
    used = [0,0]
    extents = ((96,90,82,71,80,90,99),(103,95,81,69,90,99,120))
    for fighter,name in enumerate(('kano','sonya')):
        normal = body_palette(donor,(0x92bbc,0x92cf2)[fighter])
        full = connected_sprites(ROOT/f'art_native_split_v1106/{name}-initial-three.png',3)
        halves = connected_sprites(ROOT/f'art_native_split_v1104/{name}-half-seven.png',7)
        scale = (134+fighter)/full[0].height
        groups = []
        for pose,image in enumerate(full+halves):
            factor = scale if pose<3 else extents[fighter][pose-3]/max(image.size)
            width,height = round(image.width*factor),round(image.height*factor)
            rgba = np.asarray(image.resize((width,height),Image.Resampling.LANCZOS))
            rgb = rgba[:,:,:3].astype(np.int32)
            distance = ((rgb[:,:,None,:]-normal[None,None,1:64,:].astype(np.int32))**2).sum(axis=3)
            indices = (distance.argmin(axis=2)+1).astype(np.uint8)
            indices[rgba[:,:,3]<128] = 0
            packed = packed_six(indices)
            required = (len(packed)+3)&~3
            if cursor+required > ranges[bank][1]:
                used[bank] = cursor-ranges[bank][0]
                bank += 1
                assert bank == 1
                cursor = ranges[bank][0]
            assert cursor+required <= ranges[bank][1]
            left = -width//2 if pose<3 else -width
            top = 139+fighter-height
            descriptor,group,graphic = native(0xfbc80+index*20),native(0xfbe20+index*8),gfx*8
            struct.pack_into('<4hIHIH',wanted,0x1c3900+index*20,width,height,-left,-top,graphic,0x6000,native(0xfda00+fighter*0x100),0)
            struct.pack_into('<2I',wanted,0x1c3b00+index*8,descriptor,0)
            wanted[cursor:cursor+len(packed)] = packed
            assets[graphic] = dict(fighter=name,pose=pose,size=[width,height],indices=indices,
                                  colors=normal,group=group,descriptor=descriptor)
            groups.append(group)
            index += 1
            cursor += required
            gfx += required
        struct.pack_into('<12I',wanted,0x1c3bc0+fighter*48,*(groups[:3]+[0]+groups[3:]+[0]))
    used[bank] = cursor-ranges[bank][0]
    table = list(struct.unpack_from('<17I',stock,previous.off(0xff8cf110)))
    table += [native(0xfbec0),native(0xfbef0)]
    struct.pack_into('<19I',wanted,0x1c3c80,*table)
    header = [0x172000,used[0],0x1bc000,used[1],0x1f60000,0x1c3900,0xfbc80,20,20,
              0x1c3b00,0xfbe20,160,0x1c3bc0,0xfbec0,96,0x1c3c80,0xfbf40,76]
    struct.pack_into('<4s18I',wanted,0x1c3800,b'KSP1',*header)
    payload = (ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    assert bytes(wanted) == payload, 'Whole payload independently reconstructed, not just allowed spans'
    assert hashlib.sha256(payload).hexdigest().upper() == build['payload_sha256']
    prior_guest,_,_ = previous.reconstruct()
    guest = bytearray(prior_guest)
    assert guest[0xfbc80:0xfc000] == b'\xff'*(0xfc000-0xfbc80)
    for src,dst,length in ((0x1c3900,0xfbc80,400),(0x1c3b00,0xfbe20,160),
                           (0x1c3bc0,0xfbec0,96),(0x1c3c80,0xfbf40,76)):
        guest[dst:dst+length] = wanted[src:src+length]
    assert struct.unpack_from('<I',guest,previous.off(0xff8cea70))[0] == 0xff8cf110
    struct.pack_into('<I',guest,previous.off(0xff8cea70),native(0xfbf40))
    # Native scheduler, lookup, actor constructor/mirroring and main0 untouched.
    for lo,hi in ((0xff8ce9f0,0xff8cf110),(0xff842590,0xff842710)):
        baseline = bytearray(stock[previous.off(lo):previous.off(hi)])
        if lo == 0xff8ce9f0:
            struct.pack_into('<I',baseline,previous.off(0xff8cea70)-previous.off(lo),native(0xfbf40))
        assert guest[previous.off(lo):previous.off(hi)] == baseline
    graphics = wanted[0x172000:0x172000+used[0]]+wanted[0x1bc000:0x1bc000+used[1]]
    return bytes(guest),bytes(graphics),assets,payload


def verify(texts=None, check_files=True):
    guest,graphics,assets,payload = reconstruct()
    errors,pins,cases = [],{},{}
    def need(ok, message):
        if not ok:
            errors.append(message)
    info = json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    for file,wanted in info['input_hashes'].items():
        pins[file] = wanted
    for file in SOURCE_PNGS:
        pins[str(ROOT/file)] = digest(ROOT/file)
    for case in CASES:
        directory = ROOT/case
        result = json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
        text = texts[case] if texts is not None else (directory/'run.log').read_text(encoding='utf-8-sig')
        name,side = result['player'],result['victim_slot']
        fighter = 0 if name=='kano' else 1
        identity = 17+fighter
        label = ' '+case
        need(result['exit_code']==0 and result['candidate']==CANDIDATE and result['executable_sha256']==info['executable_sha256'] and result['payload_sha256']==info['payload_sha256'], 'Exact matched terminal build'+label)
        need(result['assistance']=='none' and result['cheats_enabled'] is False and result['killer']=='kung_lao' and result['winner_slot']==3-side and result['command']=='fff_lk' and result['target_gap']==112, 'Physical native fatality'+label)
        for file,wanted in result['input_hashes'].items():
            if check_files:
                need(Path(file).is_file() and digest(Path(file))==wanted,'Unchanged input '+file)
            pins[file] = wanted
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I), 'No runtime error'+label)
        stock = previous.prior.rows(text,'MK2_STOCK_HEAD_V921')
        art = previous.prior.rows(text,'MK2_ROLLING_HEAD_V1003')
        need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+art), 'Read-only observation'+label)
        items = lambda tag:[r for t,r in stock if t==tag]
        actions,wraps,stops = items('ACTION'),items('WRAP'),items('RESULT')
        need(len(actions)==len(wraps)==len(stops)==1,'One activation/completion/terminal'+label)
        if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:
            continue
        action,start = actions[0],int(actions[0]['frame'])
        need(action['damage']=='322' and action['address']=='FF8C6040' and action['variant']=='1' and action['mode']=='2', 'Original activation after actual combat'+label)
        live = items('FIRST_LIVE')
        need(len(live)==1 and live[0]['ids']==f'0,{identity}' and live[0]['victim']==action['victim_actor'] and live[0]['own']==action['actor'], 'True selection and physical owners'+label)
        chain,next_health,killed,damage = True,161,0,0
        for r in items('HEALTH'):
            if r['pc']!='FF836700' or int(r['frame'])>start:
                continue
            before,after = int(r['before']),int(r['after'])
            chain = chain and before==next_health and 0<=after<before<=161
            damage += before-after
            next_health = after
            if after==0:
                killed += 1
                next_health = 161
        need(chain and killed==2 and damage==322 and len(items('WIN'))==2, 'Native collision health and two wins'+label)
        approach = items('APPROACH')
        if len(approach)==1:
            begin = int(approach[0]['frame'])
            pressed = {(int(r['frame']),r['button']) for r in items('INPUT') if r['slot']==str(3-side)}
            forward = 'Left' if side==1 else 'Right'
            need(108<=int(approach[0]['gap'])<=116 and start==begin+36 and all((begin+a,forward) in pressed for a in (10,18,26)) and (begin+34,'Low_Kick') in pressed, 'Actual FFF LK input'+label)
        else:
            need(False,'Reached original distance'+label)
        first = 0xff878bf0 if side==1 else 0xff878b90
        comparisons = [r for r in items('COMPARE') if int(r['frame'])==start and first<=int(r['table'],16)<=first+32]
        need(len(comparisons)==3 and [int(r['table'],16) for r in comparisons]==[first+n*16 for n in range(3)] and all(r['wanted']==r['actual']==('7' if side==1 else '8') for r in comparisons), 'Original parser directions'+label)
        need(wraps[0]['age']=='179' and int(wraps[0]['frame'])==start+179 and wraps[0]['pc']=='FF8CDC50', 'Original winner completion'+label)
        need(stops[0]['frame']=='5198' and stops[0]['damage']=='322' and stops[0]['wins']=='2' and int(stops[0]['wrap'])==start+179 and any(r['mode']=='3' and int(r['frame'])>start+179 for r in items('MODE')) and not items('CACHE_OVERWRITE'), 'Continue without softlock/reset/cache overwrite'+label)
        table_address = f'{native(0xfbf40):08X}'
        control_name = 'kitana_p1' if side==1 else 'liu_kang_p2'
        control_log = ROOT/f'audit_v1098_kung_lao_{control_name}_split_native_trace/run.log'
        historical = json.loads((ROOT/'audit_v1105_split_grammar_checkpoint/checkpoint.json').read_text())
        need(digest(control_log)==historical['inputHashes'][str(control_log)], 'Hash-pinned original same-slot timing reference'+label)
        pins[str(control_log)] = digest(control_log)
        original_tables = [r for tag,r in previous.prior.rows(control_log.read_text(encoding='utf-8-sig'),'MK2_STOCK_HEAD_V921') if tag in ('TABLE_ENTER','TABLE_RETURN') and r['table']=='FF8CF110']
        need(len(original_tables)==2 and original_tables[0]['age']==original_tables[1]['age'], 'Original slot-phase reference'+label)
        lookup_age = int(original_tables[0]['age'])
        table_enters = [r for r in items('TABLE_ENTER') if r['table']==table_address]
        table_returns = [r for r in items('TABLE_RETURN') if r['table']==table_address]
        need(len(table_enters)==len(table_returns)==1, 'One actual relocated native split lookup'+label)
        for row in table_enters+table_returns:
            need(row['id']==str(identity) and row['actor']==action['victim_actor'] and row['main']==action['victim_main'] and int(row['age'])==lookup_age and int(row['frame'])==start+lookup_age, 'Actual original same-slot lookup phase/true owner'+label)
        need(bool(table_returns) and table_returns[0]['value']==f'{native(0xfbec0+fighter*48):08X}', 'Native lookup returns own stream for real ID'+label)
        state = [r for r in grammar.records(text,'MK2_SPLIT_V1098_STATE') if r['id']==identity]
        need(len(state)==38 and all(r['pc']==r['at']+16 and r['writes']==0 and r['assistance']=='none' for r in state), 'Complete original victim fetch trace'+label)
        addresses = (0xff8cecb0,0xff8cece0,0xff8cede0,0xff8cef00,0xff8cefb0,0xff8cf030,0xff842630,0xff842650,0xff842690,0xff8426b0)
        by_at = {at:[r for r in state if r['at']==at] for at in addresses}
        need([len(by_at[at]) for at in addresses]==[1,1,1,1,1,1,8,8,8,8], 'Native constructor and seven paired poses plus zero'+label)
        if any(not by_at[at] for at in addresses):
            continue
        entry,lookup,seed = [by_at[at][0] for at in addresses[:3]]
        stance = 0xff000920+fighter*0x20000
        need(entry['a9']==0 and lookup['a9']==stance and seed['a9']==stance and lookup['a0']==0xff000000+fighter*0x20000, 'Own ordinary main0 only seeds second actor'+label)
        stance_at = (stance-0xfe800000)//8
        need(seed['words9'].split(',')[0]==f'{struct.unpack_from("<I",payload,stance_at)[0]:08X}', 'Original own stance seed retained'+label)
        stream = native(0xfbec0+fighter*48)
        words = struct.unpack_from('<12I',payload,0x1c3bc0+fighter*48)
        restored = by_at[0xff8cf030][0]
        physical,other,main = restored['actor'],restored['other'],restored['main']
        half = stream+128
        need(physical!=other and restored['other_id']==identity and physical==int(action['victim_actor'],16) and main==int(action['victim_main'],16) and restored['a9']==restored['a11']==half, 'Both true actors restore identical own half stream'+label)
        before,after = by_at[0xff8cef00][0],by_at[0xff8cefb0][0]
        need(before['other']==other and after['actor']==other and (before['other_flags']^after['flags'])==16, 'Only native X mirror toggled'+label)
        steps = [by_at[at] for at in addresses[6:]]
        first_age = steps[0][0]['age']
        need(first_age==lookup_age+90 and all(r['age']==first_age for at in addresses[:6] for r in by_at[at]), 'Original constructor-phase timing'+label)
        for n,rows in enumerate(zip(*steps)):
            a,b,c,d = rows
            cursor = half+n*32
            need(a['actor']==physical and a['other']==other and c['actor']==d['actor']==other and all(r['id']==identity and r['main']==main for r in rows), 'True IDs/owners at half '+str(n)+label)
            need(a['a9']==a['a11']==c['a9']==d['a11']==cursor and b['a9']==d['a9']==cursor+32 and b['a11']==cursor, 'Independent paired stream advancement '+str(n)+label)
            need(a['age']==first_age+6*n and all(r['frame']==a['frame'] for r in rows), 'Native six-field timing '+str(n)+label)
            need((a['flags']^a['other_flags'])&16==16 and a['words9']==a['words11'] and a['words9'].split(',')[0]==f'{words[n+4]:08X}', 'Mirrored same group/zero '+str(n)+label)
            need(d['sp']==a['sp']-64 and d['st']==b['st'], 'Original stack/status '+str(n)+label)
        need((directory/'guest_maincpu.bin').read_bytes()==guest,'Whole guest exact bounded split integration'+label)
        need((directory/'native_split_gfx.bin').read_bytes()==graphics,'Actual initialized source-encoded graphics'+label)
        own = {source:asset for source,asset in assets.items() if asset['fighter']==name}
        queues = {(r['frame'],r['cursor'],r['source']):r for tag,r in art if tag=='QUEUE'}
        dmas = [r for tag,r in art if tag=='DMA' and int(r['source'],16) in own]
        seen,actors = set(),set()
        for dma in dmas:
            asset = own[int(dma['source'],16)]
            q = queues.get((dma['frame'],dma['cursor'],dma['source']))
            need(q is not None and dma['queue_match']=='1','Bound native FIFO/DMA'+label)
            if q is None:
                continue
            need(q['id']==str(identity) and int(q['actor'],16) in (physical,other) and int(q['physical'],16)==int(q['owner'],16)==physical and int(q['main'],16)==main, 'Own halves rendered by true native actors'+label)
            need(q['y']==q['floor'] and int(q['floor'])==int(q['stageY'])-(134+fighter), 'Native actor floor'+label)
            ground = int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-(int(q['displayY'])&256)
            need((int(dma['y'])&255)+int(dma['height'])-1==ground and [int(dma['width']),int(dma['height'])]==asset['size'], 'Own actual raster floor/dimensions'+label)
            need(int(q['pose'],16)==asset['group'],'Own group pointer, no foreign-body substitution'+label)
            seen.add((int(q['actor'],16),asset['pose']))
            actors.add(int(q['actor'],16))
        expected_seen = {(physical,n) for n in range(10)}|{(other,n) for n in range(3,10)}
        need(seen==expected_seen and actors=={physical,other},'Every initial pose and both seven-half sequences'+label)
        dumps = {int(r['source'],16):r for tag,r in art if tag=='PALETTE_DUMP'}
        matches = []
        for tag,snap in art:
            source = int(snap.get('source','0'),16)
            if tag!='POSE_SNAPSHOT' or source not in own:
                continue
            dma = next((r for r in dmas if r['frame']==snap['queued_frame'] and int(r['source'],16)==source and r['fifo_actor']==snap['actor_pose'].split('_')[0]),None)
            need(dma is not None and int(snap['frame'])==int(snap['queued_frame'])+1,'Presented native picture chronology'+label)
            if dma is None:
                continue
            asset = own[source]
            palette_path = directory/dumps[source]['file']
            raw = np.asarray(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
            palette = np.stack(((raw>>16)&255,(raw>>8)&255,raw&255),axis=1)
            used_pens = np.unique(asset['indices']);used_pens = used_pens[used_pens!=0]
            need(np.max(np.abs(palette[used_pens].astype(int)-asset['colors'][used_pens].astype(int)))<=1, 'Actual own normal costume palette'+label)
            picture = directory/'snap'/f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
            score,count = previous.pixel_score(picture,asset['indices'],palette,dma)
            matches.append(dict(actor=dma['fifo_actor'],pose=asset['pose'],score=score,visibleChromaticPixels=count,picture=str(picture)))
            pins[str(palette_path)],pins[str(picture)] = digest(palette_path),digest(picture)
        strong = {(int(m['actor'],16),m['pose']) for m in matches if m['score']>=0.5 and m['visibleChromaticPixels']>=8}
        need(strong==expected_seen,'Actual displayed pixels for all seventeen actor/pose pairs'+label)
        cases[case] = dict(victim=name,slot=side,firstHalfAge=first_age,nativeWrapAge=179,
                           ownedDMAs=len(dmas),physicalActor=f'{physical:08X}',secondActor=f'{other:08X}',pixelMatches=matches)
        for file in ('run.log','result.json','guest_maincpu.bin','native_split_gfx.bin'):
            pins[str(directory/file)] = digest(directory/file)
        for file in (directory/'snap').rglob('*.png'):
            pins[str(file)] = digest(file)
    need(len(cases)==4,'Both owned characters in both real physical slots')
    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases,inputHashes=pins,
                scope='Normal Dead Pool only: both true characters/slots, native split state/timing/ground/palette and measured displayed pixels',
                sourceTransitionExact=True,main0Replaced=False,originalVictimTaskPreserved=True,
                sameNativeMirroredHalfStream=True,alternateCostumesAccepted=False,
                bloodCostumeInvarianceAccepted=False,allArenasAccepted=False,
                currentOtherFatalityRegressionsAccepted=False,fullPortAccepted=False)


if __name__=='__main__':
    if OUT.exists():
        raise ValueError('Preserve evidence')
    report = verify()
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
