"""Current regular-pose shadows and unchanged UI, not full port acceptance."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
import inspect_ground_presentation as presentation

ROOT=presentation.ROOT
NAME='diagnostic_v437_camera_native_floor_shadow'
EXE='EB058EBE47311DA2DE94CA7398391A5792F03CDD2F5C2C6129F35EB377521004'
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
    folder=ROOT/f'audit_v438_ground_{fighter}_p{side}'
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
    folder=ROOT/f'audit_v439_shadow_ui_{fighter}_p{side}'
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

def verify():
    return {'passed':True,'candidate':NAME,'executable_sha256':EXE,'payload_sha256':PAYLOAD,
            'ground':[verify_case(f,s) for f,s in CASES],
            'ui':[verify_ui(f,s) for s in (1,2) for f in ('kano','sonya')],
            'fullPortAcceptance':False,'pending':'KO/flat poses, all arenas, moves/interruptions/victims, full tower/continue/finishers/endings/audio, final matching launcher/ZIP'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
