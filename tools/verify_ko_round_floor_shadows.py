"""Actual five-hit KO/round-two evidence, not full natural-character acceptance."""
import hashlib
import json
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image
import inspect_ground_presentation as p

ROOT=p.ROOT
NAME='diagnostic_v456_ko_round_floor_shadow'
OLD='diagnostic_v447_unclipped_body_floor_shadow'
EXE='2731D2D965477251F19E1E8496480588C59BA521DDC3DD4AE55C3FD14D7DDB0A'
OLD_EXE='8B4DA232C575F0983C17CDF5CEC3338C416765000718D28BBEBA3AA17102811B'
PAYLOAD='82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'
CASES=[(f,s) for s in (1,2) for f in ('kano','sonya','sub_zero')]

def need(value,label):
    if not value:raise ValueError(label)

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest().upper()

@lru_cache(maxsize=None)
def read(folder):return (folder/'run.log').read_text(encoding='utf-8-sig')

def rgb(path):return np.asarray(Image.open(path).convert('RGB'))

def matched(folder,current=True):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    name,exe=(NAME,EXE) if current else (OLD,OLD_EXE)
    need(result['exit_code']==0 and result['candidate']==name and result['assistance']=='none','Matched unassisted terminal launch')
    need(result['executable_sha256']==exe and result['payload_sha256']==PAYLOAD,'Matched executable/payload')
    for path,sha in json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig')).items():
        need(digest(path)==sha,'Frozen launch input changed: '+path)
    build=json.loads((ROOT/name/'build-info.json').read_text(encoding='utf-8-sig'))
    for path,sha in build['input_hashes'].items():
        actual=Path(path)
        if digest(actual)!=sha:actual=ROOT/name/'input_sources'/actual.name
        need(digest(actual)==sha,'No matched frozen build input: '+path)
    need(digest(ROOT/name/'mkport_candidate.exe')==exe,'Matched executable bytes')
    need(digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.h')==
         '8BA30B7AA635EA1FD68CF46697560E58BA7E3FC7A2C760C0881414836FBFD4D5','Original video-header ABI')

def foreground(folder,parent_log):
    matched(folder)
    observed=read(folder)
    for tag in ('FIELD','PART','INPUT','DMA','DMA_CACHE','GFX','HEALTH','KO','ROUND_RESET','NEXT_READY','INVALID','RESULT'):
        need(p.rows(observed,tag)==p.rows(parent_log,tag),'Independent observer preserves actual '+tag+' records')
    need(not p.rows(observed,'SNAP'),'Supplemental observer does not replace actual screenshots')
    last_body={};lines=observed.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('MK2_GROUND_DMA '):
            d=p.rows(line,'DMA')[0]
            if d['command']&15==2 and 0x10000000<=d['source']<0x1a000000:last_body[d['frame']]=i
    positions=[i for i,line in enumerate(lines) if line.startswith('MK2_GROUND_FG_DMA ')]
    # KO blood also uses palette 0500, unlike the earlier single-uppercut case.
    # Include every independently captured non-fighter object drawn afterwards;
    # source geometry, per-draw colors and the original image prove visibility.
    records=[r for i,r in zip(positions,p.rows(observed,'FG_DMA'))
             if i>last_body.get(r['frame'],-1)]
    need(records and all(len(r['colors'].split(','))==256 for r in records),
         'Every actual foreground DMA has its own captured palette, including blood palette changes')
    colors={}
    buffers={r['key']:r for r in p.rows(observed,'FG_GFX')};decoded={};byframe={}
    for d in records:byframe.setdefault(d['frame'],[]).append(d)
    def render(frame):
        image=np.zeros((512,512,3),dtype=np.uint8);mask=np.zeros((512,512),dtype=bool)
        for d in byframe.get(frame,[]):
            need(d['scaleX']==d['scaleY']==256,'Actual unscaled native foreground')
            key=f"{d['source']:08X}_{d['command']:04X}_{d['width']}_{d['height']}"
            if key not in decoded:decoded[key]=p.decode(d,buffers)
            indices=decoded[key];ys,xs=np.where(indices!=0)
            x=d['x']+(-xs if d['command']&16 else xs);y=(d['y']+(-ys if d['command']&32 else ys))&511
            inside=(x>=0)&(x<512)&(y<254)
            signature=d['colors']
            if signature not in colors:
                colors[signature]=np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in signature.split(',')],dtype=np.uint8)
            image[y[inside],x[inside]]=colors[signature][indices[ys[inside],xs[inside]]]
            mask[y[inside],x[inside]]=True
        return image[:254,56:456],mask[:254,56:456]
    return render

def lifecycle(log,fighter,side):
    fields=p.rows(log,'FIELD');identity={'kano':17,'sonya':18,'sub_zero':8}[fighter]
    need(len(fields)==4104,'Both participants observed across 2053 fields except native teardown')
    for r in fields:
        need(r['id']==r['roster']==(identity if r['slot']==side else 4) and r['state']==1 and r['owner']==r['actor'],
             'True identity/controller/Main ownership throughout KO and next round')
    ko=p.rows(log,'KO');reset=p.rows(log,'ROUND_RESET');ready=p.rows(log,'NEXT_READY');end=p.rows(log,'RESULT')
    need(len(ko)==len(reset)==len(ready)==len(end)==1 and ko[0]['age']==1425 and reset[0]['age']==1812 and ready[0]['age']==1992,
         'Actual KO, native round reset, and next-round readiness')
    hits=[r for r in p.rows(log,'HEALTH') if r['frame']<ko[0]['frame'] and r['before']>r['after']]
    need([(r['before'],r['after']) for r in hits]==[(161,121),(121,81),(81,41),(41,1),(1,0)] and
         all(r['slot']==side and r['pc']==0xff836700 for r in hits),'Five genuine native uppercut damage writes')
    winner=[r for r in fields if r['mode']==5]
    need(len(winner)==608 and all(r['winner']==3-side for r in winner),'Actual native winner scene')
    for slot in (1,2):
        samples=[r for r in fields if r['slot']==slot and r['frame']>=ready[0]['frame']]
        need(len(samples)==61 and all(r['mode']==2 and r['hp']==161 and r['y']==r['floor'] and r['vx']==r['vy']==r['gravity']==0 for r in samples),
             'Both real fighters grounded and healthy for 61 next-round fields')
    need(p.rows(log,'INVALID')==[dict(frame=end[0]['ready']+1732,fighter=fighter,side=side,writes=0,assistance='none',age=1732)],
         'Only the native one-field round teardown; no match softlock')
    need(end[0]['terminalAge']==2052 and end[0]['nextReady']==ready[0]['frame'],'Clean actual next-round terminal')
    return fields

@lru_cache(maxsize=None)
def original_report(fighter,side):
    # Original body pixels, not the candidate/mutation, choose the displayed DMA field.
    return p.inspect(ROOT/f'audit_v457_ko_round_{fighter}_p{side}',shift=56)

def verify_case(fighter,side,image_load=None):
    folder=ROOT/f'audit_v458_ko_round_{fighter}_p{side}';old=ROOT/f'audit_v457_ko_round_{fighter}_p{side}'
    matched(folder);matched(old,False);log=read(folder);previous_log=read(old)
    for tag in ('FIELD','PART','INPUT','DMA','DMA_CACHE','GFX','HEALTH','KO','ROUND_RESET','NEXT_READY','INVALID','RESULT','SNAP'):
        need(p.rows(log,tag)==p.rows(previous_log,tag),'Every before/after native '+tag+' record unchanged')
    fields=lifecycle(log,fighter,side);report=original_report(fighter,side)
    need(report['snapshots']==268,'Complete native snapshot inventory')
    fg_version=464 if fighter=='sub_zero' and side==2 else 462
    fg=foreground(ROOT/f'audit_v{fg_version}_ko_foreground_{fighter}_p{side}',log)
    buffers={r['key']:r for r in p.rows(log,'GFX')}
    palettes={r['bank']:np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in r['colors'].split(',')],dtype=np.uint8) for r in p.rows(log,'PALETTE')}
    draws={}
    for d in p.rows(log,'DMA'):draws.setdefault(d['frame'],[]).append(d)
    parts=p.rows(log,'PART');caches=p.rows(log,'DMA_CACHE');modes={r['frame']:r['mode'] for r in fields}
    changed=occluded=winner_frames=flat_frames=0
    geometry=p.descriptor_geometry((ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes())
    for rec in report['records']:
        path=folder/'snap'/rec['file'];new=np.asarray(image_load(path) if image_load else rgb(path));previous=rgb(old/'snap'/rec['file'])
        need(new.shape==previous.shape==(254,400,3),'Native unscaled images')
        difference=np.any(new!=previous,axis=2)
        if fighter=='sub_zero':
            need(not difference.any(),'Stock KO/round-two image changed')
            continue
        mode=modes[rec['dmaFrame']]
        if mode!=5:
            need(not difference.any(),'Non-winner scene changed')
            continue
        winner_frames+=1
        body,bodymask,slots,stock,native=p.render(draws[rec['dmaFrame']],buffers,palettes,fields,parts,caches,geometry)
        opaque=bodymask[:254,56:456]
        need(np.array_equal(new[opaque],previous[opaque]),'Opaque body positions/colors changed')
        fg_rgb,fg_mask=fg(rec['dmaFrame']);visible=fg_mask&np.all(previous==fg_rgb,axis=2)
        need(np.array_equal(new[visible],previous[visible]),'Visible native foreground pixels changed')
        expected=native[:254,56:456]&~opaque;expected[:44]=False
        occluded+=int((expected&visible).sum());expected&=~visible
        need(expected.any() and np.all(new[expected]==0),
             f"Every decoded KO floor-shadow pixel present: age={rec['age']} dma={rec['dmaFrame']} missing={int((expected&np.any(new!=0,axis=2)).sum())}")
        need(not difference[:140].any(),'High-screen HUD/selection art changed')
        need(np.all(new[difference]==0),'Only newly black shadow pixels may change')
        need(not (difference&~expected).any(),'Change outside independently decoded shadow')
        changed+=int(difference.sum())
        if 1500<=rec['age']<=1660:flat_frames+=1
    if fighter!='sub_zero':need(changed>1000 and winner_frames>=70 and flat_frames>=30,'Actual KO falling and held corpse shadows restored')
    return dict(fighter=fighter,side=side,fields=len(fields),snapshots=268,genuineUppercuts=5,roundTwoGroundedFields=61,
                addedShadowPixels=changed,winnerSnapshots=winner_frames,heldCorpseSnapshots=flat_frames,foregroundOcclusions=occluded,
                nativeGameplayRecordsBitExact=True,stockWholeImagesBitExact=fighter=='sub_zero',
                scope='one_real_five_hit_KO_winner_scene_and_round_two_in_Goros_Lair_not_all_arenas_or_moves')

def verify_ui(fighter,side,image_load=None):
    folder=ROOT/f'audit_v459_ko_shadow_ui_{fighter}_p{side}';old=ROOT/f'audit_v450_unclipped_ui_{fighter}_p{side}'
    matched(folder)
    need([s for s in read(folder).splitlines() if s.startswith('MK2_UI_')]==
         [s for s in read(old).splitlines() if s.startswith('MK2_UI_')],'All original native UI records preserved')
    snaps=p.rows(read(folder).replace('MK2_UI_','MK2_GROUND_'),'SNAP');seen=set()
    for rec in snaps:
        if rec['file'] in seen:continue
        seen.add(rec['file']);path=folder/'snap'/rec['file']
        need(np.array_equal(np.asarray(image_load(path) if image_load else rgb(path)),rgb(old/'snap'/rec['file'])),
             'Whole selection/ladder/intro/name-shadow image changed')
    need(len(seen)>=160,'Complete actual selection-to-match capture inventory')
    return dict(fighter=fighter,side=side,wholeImagesBitExact=len(seen),allNativeRecordsBitExact=True,
                scope='same_verified_selection_ladder_first_match_presentation_not_full_campaign')

def verify():
    return dict(passed=True,candidate=NAME,executable_sha256=EXE,payload_sha256=PAYLOAD,
                ko=[verify_case(f,s) for f,s in CASES],ui=[verify_ui(f,s) for s in (1,2) for f in ('kano','sonya')],
                fullPortAcceptance=False,pending='All arenas/native shadow geometry, complete human/CPU moves and interrupts/victims, campaign/continue/bosses/finishers/endings/audio, final matching production launcher/ZIP')

if __name__=='__main__':print(json.dumps(verify(),indent=2))
