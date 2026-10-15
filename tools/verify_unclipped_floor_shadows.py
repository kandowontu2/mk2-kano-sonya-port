"""Current regular-pose shadows and unchanged UI, not full port acceptance."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
import inspect_ground_presentation as presentation

ROOT=presentation.ROOT
NAME='diagnostic_v447_unclipped_body_floor_shadow'
EXE='8B4DA232C575F0983C17CDF5CEC3338C416765000718D28BBEBA3AA17102811B'
PAYLOAD='82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'
CASES=[(f,s) for s in (1,2) for f in ('kano','sonya','sub_zero')]

def need(value,label):
    if not value:raise ValueError(label)

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def matched(folder):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['candidate']==NAME and result['assistance']=='none','Current unassisted terminal launch')
    need(result['executable_sha256']==EXE and result['payload_sha256']==PAYLOAD,'Current executable/payload identity')
    inputs=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    for path,sha in inputs.items():need(digest(path)==sha,'Launch input changed: '+path)
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    for path,sha in build['input_hashes'].items():need(digest(path)==sha,'Build input changed: '+path)
    need(digest(ROOT/NAME/'mkport_candidate.exe')==EXE,'Current executable changed')
    need(digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.h')==
         '8BA30B7AA635EA1FD68CF46697560E58BA7E3FC7A2C760C0881414836FBFD4D5',
         'Video header matches the original ABI; no retained prototype lookup')

def verify_case(fighter,side,image_load=None):
    version=451 if fighter=='sonya' else 449
    folder=ROOT/f'audit_v{version}_unclipped_ground_{fighter}_p{side}'
    old=ROOT/f'audit_v427_ground_{fighter}_p{side}'
    matched(folder)
    log=(folder/'run.log').read_text(encoding='utf-8-sig');before=(old/'run.log').read_text(encoding='utf-8-sig')
    fields=presentation.rows(log,'FIELD');original=presentation.rows(before,'FIELD')
    need(fields==original,'Every observed native gameplay field unchanged')
    need(presentation.rows(log,'INPUT')==presentation.rows(before,'INPUT'),'Identical genuine selection/mobility inputs')
    need(len(fields)==962,'Full 481-field observation for both actual fighters')
    ids={1:17 if fighter=='kano' else 18 if fighter=='sonya' else 8,2:4}
    if side==2:ids={1:4,2:ids[1]}
    for row in fields:
        need(row['id']==row['roster']==ids[row['slot']] and row['state']==1 and row['owner']==row['actor'] and row['hp']==161,'True selected identity/Main ownership/undamaged gameplay')
    for slot in (1,2):
        samples=[r for r in fields if r['slot']==slot]
        need(max(r['floor']-r['y'] for r in samples)>=90,'Both genuine full jumps observed')
        need(samples[-1]['y']==samples[-1]['floor'] and samples[-1]['vx']==samples[-1]['vy']==samples[-1]['gravity']==0,'Both physically grounded after mobility')
        need(samples[-1]['x']!=samples[0]['x'],'Real walking displacement')
    report=presentation.inspect(folder,shift=56,image_load=image_load,comparison_folder=old)
    need(report['snapshots']==117,'All declared native-size snapshots')
    # The original foreground chains occlude jump pixels. Do not relax a
    # model-correlation threshold to hide that: compare every sampled opaque
    # body position against the identical pre-change capture, including chains.
    need(all(r['bodyPixelsBitExactBeforeAfter'] for r in report['records']),
         'Every opaque fighter/foreground body position bit-exact before/after')
    need(presentation.rows(log,'INVALID')==[] and report['terminal'][0]['terminalAge']==480,'Uninterrupted actual match to terminal observation')
    visible=[];changed=0;removed=0
    for rec in report['records']:
        path=folder/'snap'/rec['file']
        new=np.asarray(image_load(path) if image_load else Image.open(path).convert('RGB'))
        previous=np.asarray(Image.open(old/'snap'/rec['file']).convert('RGB'))
        need(new.shape==previous.shape==(254,400,3),'Native unscaled snapshots')
        difference=np.any(new!=previous,axis=2)
        if fighter=='sub_zero':
            need(not difference.any(),'Stock control frame changed')
            need(rec['nativeShadowPixels']==0,'Stock draw cannot acquire imported shadow')
        else:
            need(rec['nativeShadowPixels']>=50,'A full independently decoded visible floor silhouette')
            need(rec['nativeShadowScore']==1.0,'Every expected visible native floor-shadow pixel present')
            visible.append(rec['nativeShadowPixels'])
            black_new=np.all(new==0,axis=2);black_old=np.all(previous==0,axis=2)
            need(np.all((black_new|black_old)[difference]),'Non-shadow color/game art changed')
            need(not difference[:140].any(),'Unexpected high-screen/selection-style drawing')
            if rec['age'] in range(32,53) or rec['age']==480:
                need(rec['opaqueFootRows'][1]==rec['opaqueFootRows'][2]==228,
                     'Rendered native/Kitana soles share the stock ground contact row')
            changed+=int((difference&black_new).sum());removed+=int((difference&black_old).sum())
    if fighter!='sub_zero':need(changed>2000,'Previously missing silhouettes actually restored')
    return {'fighter':fighter,'side':side,'fields':len(fields),'snapshots':report['snapshots'],
            'addedShadowPixels':changed,'removedMisplacedShadowPixels':removed,
            'visibleShadowPixelsMin':min(visible) if visible else 0,'allExpectedNativeShadowPixels':fighter!='sub_zero',
            'stockSnapshotsBitExact':fighter=='sub_zero','minimumBodyScore':report['minimumBodyScore'],
            'scope':'regular_stance_both_jumps_crouch_walk_in_Goros_Lair_not_KO_or_all_arenas'}

def verify_ui(fighter,side,image_load=None):
    folder=ROOT/f'audit_v450_unclipped_ui_{fighter}_p{side}'
    old=ROOT/f'audit_v424_native_ui_{fighter}_p{side}'
    matched(folder)
    log=(folder/'run.log').read_text(encoding='utf-8-sig');before=(old/'run.log').read_text(encoding='utf-8-sig')
    need([line for line in log.splitlines() if line.startswith('MK2_UI_')]==
         [line for line in before.splitlines() if line.startswith('MK2_UI_')],
         'All original navigation/table/identity/ladder/live-field trace records unchanged')
    # Parse only our generic record syntax; no changes to the frozen v425 verifier.
    data=log.replace('MK2_UI_','MK2_GROUND_')
    live=presentation.rows(data,'LIVE')[0]['frame']
    modes={r['frame']:r['mode'] for r in presentation.rows(data,'OUTSIDE')}
    snapshots=presentation.rows(data,'SNAP');seen=set();prelive=0;names=0;intro=0
    reference_file=next(r['file'] for r in snapshots if r['frame']>=live)
    reference=np.asarray(Image.open(old/'snap'/reference_file).convert('RGB'))
    metal=np.zeros((254,400),dtype=bool)
    metal[25:45,18:185]=True;metal[25:45,211:378]=True
    metal&=(reference.max(2)-reference.min(2)<2)&(reference.max(2)>64)
    need(metal.sum()>400,'Complete original two-lifebar metal outline signature')
    for rec in snapshots:
        if rec['file'] in seen:continue
        seen.add(rec['file']);path=folder/'snap'/rec['file']
        new=np.asarray(image_load(path) if image_load else Image.open(path).convert('RGB'))
        previous=np.asarray(Image.open(old/'snap'/rec['file']).convert('RGB'))
        need(new.shape==previous.shape==(254,400,3),'Native UI capture size')
        arena=np.array_equal(previous[metal],reference[metal])
        if rec['frame']<live and not arena:
            need(np.array_equal(new,previous),'Selection/ladder presentation changed or acquired shadow')
            prelive+=1
        else:
            need(np.array_equal(new[27:44],previous[27:44]),'Lifebar names/stock shadow changed')
            names+=1
            if rec['frame']<live:
                # Mode 7 spans both ladder and arena setup. Only the full
                # canonical lifebar signature proves this is the arena intro.
                # Classify from the frozen original, never the new/mutated image.
                need(modes.get(rec['frame'])==7,'Original arena-intro state provenance')
                difference=np.any(new!=previous,axis=2)
                need(not difference[:140].any(),'Arena intro acquired selection art or shifted bodies')
                need(np.all((np.all(new==0,axis=2)|np.all(previous==0,axis=2))[difference]),
                     'Arena intro changed non-shadow art')
                intro+=1
    need(prelive>=100 and names>=8,'Full selection/ladder/first-match capture inventory')
    return {'fighter':fighter,'side':side,'preMatchSnapshotsBitExact':prelive,'lifebarCapturesBitExact':names,'actualArenaIntroCaptures':intro,
            'allNativeUiRecordsBitExact':True,'scope':'same_presentation_as_verified_v425_in_both_slots_not_full_tower'}

def foreground_frames(fighter,side,log):
    folder=ROOT/f'audit_v453_foreground_{fighter}_p{side}'
    matched(folder)
    observed=(folder/'run.log').read_text(encoding='utf-8-sig')
    for tag in ('FIELD','INPUT','DMA','DMA_CACHE','GFX','RESULT'):
        need(presentation.rows(observed,tag)==presentation.rows(log,tag),
             'Supplemental foreground observer preserves original actual '+tag+' records')
    need(presentation.rows(observed,'SNAP')==[],'Supplemental foreground observer does not replace actual image evidence')
    # Respect native draw order. Blood drawn BEFORE a fighter may correctly
    # be covered by its projection; blood/chain objects drawn AFTER it must
    # remain visible. Canonical ROM geometry alone cannot establish Z order.
    last_body={}
    lines=observed.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('MK2_GROUND_DMA '):
            d=presentation.rows(line,'DMA')[0]
            if d['command']&15==2 and 0x10000000<=d['source']<0x1a000000:
                last_body[d['frame']]=i
    positions=[i for i,line in enumerate(lines) if line.startswith('MK2_GROUND_FG_DMA ')]
    records=[r for i,r in zip(positions,presentation.rows(observed,'FG_DMA'))
             if r['palette'] in (0x1c00,0x400) and i>last_body.get(r['frame'],-1)]
    palettes=[r for r in presentation.rows(observed,'FG_PALETTE') if r['bank'] in (0x1c00,0x400)]
    need(records and len([r for r in palettes if r['bank']==0x1c00])==1,'Independent constant native foreground-chain palette and DMA records')
    colors={r['bank']:np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in r['colors'].split(',')],dtype=np.uint8) for r in palettes}
    need(len(colors)==len(palettes),'Foreground palettes unchanged during sampled reaction')
    buffers={r['key']:r for r in presentation.rows(observed,'FG_GFX')}
    decoded={}
    byframe={}
    for rec in records:byframe.setdefault(rec['frame'],[]).append(rec)
    def render(frame):
        rgb=np.zeros((512,512,3),dtype=np.uint8);mask=np.zeros((512,512),dtype=bool)
        for d in byframe.get(frame,[]):
            need(d['scaleX']==d['scaleY']==256,'Native unscaled foreground provenance')
            key=f"{d['source']:08X}_{d['command']:04X}_{d['width']}_{d['height']}"
            if key not in decoded:decoded[key]=presentation.decode(d,buffers)
            indices=decoded[key];sy,sx=np.where(indices!=0)
            xs=d['x']+(-sx if d['command']&16 else sx)
            ys=(d['y']+(-sy if d['command']&32 else sy))&511
            inside=(xs>=0)&(xs<512)&(ys>=0)&(ys<254)
            rgb[ys[inside],xs[inside]]=colors[d['palette']][indices[sy[inside],sx[inside]]]
            mask[ys[inside],xs[inside]]=True
        return rgb[:254,56:456],mask[:254,56:456]
    return render

def verify_reaction(fighter,side,image_load=None):
    folder=ROOT/f'audit_v448_unclipped_reaction_{fighter}_p{side}'
    old=ROOT/f'audit_v445_reaction_before_{fighter}_p{side}'
    matched(folder)
    baseline=json.loads((old/'result.json').read_text(encoding='utf-8-sig'))
    need(baseline['exit_code']==0 and baseline['candidate']=='diagnostic_v437_camera_native_floor_shadow' and
         baseline['executable_sha256']=='EB058EBE47311DA2DE94CA7398391A5792F03CDD2F5C2C6129F35EB377521004' and
         baseline['payload_sha256']==PAYLOAD and baseline['assistance']=='none','Matched actual pre-fix reaction launch')
    for path,sha in json.loads((old/'input_hashes_before.json').read_text(encoding='utf-8-sig')).items():
        need(digest(path)==sha,'Frozen pre-fix launch input changed: '+path)
    log=(folder/'run.log').read_text(encoding='utf-8-sig');before=(old/'run.log').read_text(encoding='utf-8-sig')
    fields=presentation.rows(log,'FIELD')
    need(fields==presentation.rows(before,'FIELD'),'Every actual reaction/health/physics field unchanged')
    need(presentation.rows(log,'INPUT')==presentation.rows(before,'INPUT'),'Identical genuine uppercut/selection inputs')
    need(len(fields)==882 and presentation.rows(log,'INVALID')==[],'Full uninterrupted 441-field reaction for both fighters')
    expected=17 if fighter=='kano' else 18 if fighter=='sonya' else 8
    for slot in (1,2):
        samples=[r for r in fields if r['slot']==slot]
        identity=expected if slot==side else 4
        need(all(r['id']==r['roster']==identity and r['state']==1 and r['owner']==r['actor'] for r in samples),
             'Real selected identity/controller/Main ownership throughout reaction')
        need(samples[0]['hp']==161 and samples[-1]['hp']==(121 if slot==side else 161),'Actual single 40-point uppercut hit; no health assistance')
        need(samples[-1]['y']==samples[-1]['floor'] and samples[-1]['vx']==samples[-1]['vy']==samples[-1]['gravity']==0,
             'Actual grounded physical recovery')
        if slot==side:
            need(max(r['floor']-r['y'] for r in samples)>175 and any(r['action']==1283 for r in samples),
                 'Real native uppercut launch and high airborne fall, not a missed button')
    report=presentation.inspect(folder,shift=56,image_load=image_load,comparison_folder=old)
    foreground=foreground_frames(fighter,side,log)
    need(report['snapshots']==211 and report['terminal'][0]['terminalAge']==440,'Every declared reaction capture and terminal')
    need(all(r['bodyPixelsBitExactBeforeAfter'] for r in report['records']),'Every sampled opaque body/foreground position unchanged')
    changed=0;flat=0;minimum=1.0;occluded=0
    buffers={r['key']:r for r in presentation.rows(log,'GFX')}
    palettes={r['bank']:np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in r['colors'].split(',')],dtype=np.uint8)
              for r in presentation.rows(log,'PALETTE')}
    draws={}
    for r in presentation.rows(log,'DMA'):draws.setdefault(r['frame'],[]).append(r)
    cache_rows=presentation.rows(log,'DMA_CACHE')
    parts=presentation.rows(log,'PART')
    flat_frames={r['frame'] for r in parts if r['slot']==side and r['width']>100 and r['height']<=45}
    for rec in report['records']:
        path=folder/'snap'/rec['file']
        new=np.asarray(image_load(path) if image_load else Image.open(path).convert('RGB'))
        previous=np.asarray(Image.open(old/'snap'/rec['file']).convert('RGB'))
        need(new.shape==previous.shape==(254,400,3),'Native reaction snapshots')
        difference=np.any(new!=previous,axis=2)
        if fighter=='sub_zero':
            need(not difference.any(),'Stock reaction frame changed')
            continue
        need(not difference[:140].any(),'Reaction changed high-screen body/HUD/art')
        need(np.all((np.all(new==0,axis=2)|np.all(previous==0,axis=2))[difference]),'Reaction changed non-shadow colors')
        fg_rgb,fg_mask=foreground(rec['dmaFrame'])
        # Classify visible chains from independently captured native DMA/ROM
        # colors and the frozen original image, never the candidate/mutation.
        visible=fg_mask&np.all(previous==fg_rgb,axis=2)
        need(np.array_equal(new[visible],previous[visible]),'Native foreground chain pixels changed')
        body,bodymask,slots,stock,native=presentation.render(draws[rec['dmaFrame']],buffers,palettes,
            fields,parts,cache_rows,{})
        expected_mask=native[:254,56:456]&~bodymask[:254,56:456];expected_mask[:44]=False
        occluded+=int((expected_mask&visible).sum());expected_mask&=~visible
        need(expected_mask.any() and np.all(new[expected_mask]==0),'Every independently decoded reaction floor-shadow pixel present')
        changed+=int(difference.sum())
        if rec['dmaFrame'] in flat_frames:flat+=1
    if fighter!='sub_zero':need(changed>1000 and flat>=4,'Both missing composite shadows and actual wide flat fall restored')
    return {'fighter':fighter,'side':side,'snapshots':211,'fields':882,'healthDamage':40,'groundedRecovery':True,
            'changedShadowPixels':changed,'flatPoseSnapshots':flat,'minimumNativeShadowScore':minimum,
            'independentlyVerifiedChainOcclusions':occluded,
            'opaqueBodiesBitExact':True,'stockSnapshotsBitExact':fighter=='sub_zero',
            'minimumBodyModelScoreDiagnosticOnly':report['minimumBodyScore'],
            'scope':'one_real_uppercut_launch_flat_fall_recovery_Goros_Lair_not_KO_or_all_arenas'}

def verify():
    return {'passed':True,'candidate':NAME,'executable_sha256':EXE,'payload_sha256':PAYLOAD,
            'ground':[verify_case(f,s) for f,s in CASES],
            'ui':[verify_ui(f,s) for s in (1,2) for f in ('kano','sonya')],
            'reactions':[verify_reaction(f,s) for f,s in CASES],
            'fullPortAcceptance':False,'pending':'KO/end-of-round poses, all arenas, moves/interruptions/victims, full tower/continue/finishers/endings/audio, final matching release launcher/ZIP'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
