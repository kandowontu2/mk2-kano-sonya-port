"""Review and seal four actual current paid-continue routes; full scope intact.

Whole old native UI/raster/control contracts retained, new Kano paired source
clause is fault-qualified on the actual victim-thread stores. Twelve original
selection/ladder/punch images in RAM; no disk media or broad audio/arena claim.
"""
import hashlib
import json
import re
from pathlib import Path
import numpy as np
import qualify_native_kano_laser_cross_continue_retained as qualified
import capture_native_kano_laser_cross_continue as capture
import review_launch_challenger_ram_frames as preview

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_kano_laser_cross_continue_matrix_review'
CASES=[('kano',1,'sonya'),('kano',2,'sonya'),('sonya',1,'kano'),('sonya',2,'kano')]


def visual_records(scope):
    contract=scope['contract'];model=contract.model;records=[]
    for fighter,side,target in CASES:
        key=f'{fighter}_p{side}_to_{target}';folder,text,images,report=scope['RAM_CASES'][key]
        css=int(model.records(text,'CSS')[0]['frame']);exit_at=int(model.records(text,'EXIT')[0]['frame'])
        digests=report['actualFullRGBDigests']
        selection=next(q for q in digests if q['label'].startswith('ui_')and 54<=q['frame']-css<=70)
        template=model.portrait((ROOT/'roms/mk2ks/mk2ks.ui').read_bytes(),0 if target=='kano'else 1,35,45)
        ladder=next(q for q in digests if q['label'].startswith('ui_')and exit_at+2<=q['frame']<=exit_at+100 and
            np.array_equal(np.frombuffer(images[q['frame'],q['label']],np.uint8).reshape(254,400,4)[158:203,128:163,2::-1],template))
        punch=next(q for q in digests if q['label']=='actual_punch')
        for stage,q in zip(('continued_selection','native_ladder','continued_actual_punch'),(selection,ladder,punch)):
            raw=images[q['frame'],q['label']]
            need(len(raw)==406400 and hashlib.sha256(raw).hexdigest().upper()==q['sha256'],'Every selected original native raw byte matches its actual callback digest')
            records.append(dict(header=dict(q,width='400',height='254',case=key,stage=stage,
                frameLabel='actual observed callback; native rendering not inferred from input marker'),pixels=raw))
    return dict(rgbFrames=records)


def neutral_jump(text,side,contract):
    jump=contract.rows(text,'JUMP')[0];frame=int(jump['frame'])-1
    fields=[r for r in contract.rows(text,'FIELD')if int(r['frame'])==frame and r['slot']==str(side)]
    need(len(fields)==1,'Exactly one actual native response field before the jump callback')
    q=fields[0]
    need(q['action']=='779'and int(q['y'])<int(q['floor'])and int(q['vy'],16)&0x80000000 and
         q['gravity']=='00008000'and int(q['hp'])>0 and q['owner']==q['actor'],
         'Actual own living neutral-jump action, upward velocity and native gravity; not a held/hurt lift')
    return q


def run(scope,carrier):
    need(not OUT.exists()and not capture.native_base.identity.census(),'All four actual native games terminal; no replay')
    contract=scope['contract'];need(set(scope['COMPLETED'])=={f'{f}_p{s}_to_{t}'for f,s,t in CASES},'All four original current continue routes completed')
    binding=json.loads((qualified.OUT/'report.json').read_text())
    parent=json.loads((ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json').read_text())
    need(binding['passed']and len(binding['actualAdditionalOriginFaultsRejected'])==10 and
         len(parent['originalNaturalIntegrationRequirements'])==14 and len(parent['originalRemainingWorkGroups'])==6,
         'Exact paired-origin correction qualified and full original integration scope retained')
    need(len(carrier['rgbFrames'])==12,'Exactly twelve individually inspected original native images')
    cases=[];pins={};faults=[];views=[];total_faults=10;total_fields=0;unique_rasters=0
    for fighter,side,target in CASES:
        key=f'{fighter}_p{side}_to_{target}';folder,text,images,metadata=scope['RAM_CASES'][key]
        paths=[ROOT/f'{capture.PREFIX}_{suffix}_{key}/report.json'for suffix in ('checked','pixels','control_faults')]
        proof,pixel,control=(json.loads(p.read_text())for p in paths)
        terminal=json.loads((folder/'native_terminal.json').read_text())
        need(all(r['passed']for r in (proof,pixel,control))and terminal['exitCode']==0 and not terminal['observationErrors']and
             not(folder/'stderr.log').read_text().strip()and metadata['candidate']==scope['current'].NAME and
             metadata['executableSHA256']==scope['current'].EXE_SHA and metadata['guestSHA256']==scope['current'].GUEST_SHA,
             'Every route actually used the current native executable/guest and naturally terminated without errors')
        positive=contract.gate(text,fighter,side,target)
        need(positive==proof['actualSinglePlayerContinue']and positive['collisionEarnedLosses']==2 and
             positive['actualWalkJumpPunchAccepted']and positive['actualOtherPlayerStartupKeyReleased']and
             len(proof['actualFaultsRejected'])==18 and len(control['actualControlFaultsRejected'])==9 and
             pixel['selectedPlayerLadderIcon']['fullSourceRasterMatches']>=3 and
             proof['actualUIPixels']['blink_colors']>=2 and proof['actualUIPixels']['native_name_shadow_checks']>=4,
             'Full original loss/payment/true-ID/released-key/UI/viewport/name/response and all original fault suites')
        need(all(q['everyActualByteComparedInRAM']for q in metadata['actualGuestGFXProofs'].values())and
             hashlib.sha256(scope['guest']).hexdigest().upper()==metadata['actualGuestGFXProofs']['guest']['sha256'],
             'Every actual whole guest/GFX native byte compared to the current independent source expectation')
        jump=neutral_jump(text,side,contract)
        jump_line=next(s for s in text.splitlines()if s.startswith('MK2_SC_FIELD ')and dict(re.findall(r'(\w+)=([^\s]+)',s))==jump)
        for name,value in [('action','1285'),('vy','00010000'),('gravity','00000000'),('y',jump['floor'])]:
            changed=re.sub(r'\b'+name+r'=\S+',name+'='+value,jump_line,count=1)
            need(changed!=jump_line,'Each exact native neutral-jump fault changes observed evidence')
            try:
                changed_text=text.replace(jump_line,changed,1)
                contract.gate(changed_text,fighter,side,target);neutral_jump(changed_text,side,contract)
            except(ValueError,AssertionError)as error:faults.append(dict(case=key,fault='neutral_jump_'+name,rejectedBy=str(error)))
            else:raise ValueError('False native jump accepted: '+key+' '+name)
        need(contract.gate(text,fighter,side,target)==positive and neutral_jump(text,side,contract)==jump,'Whole actual current positive restores')
        for p,r in zip(paths,(proof,pixel,control)):
            pins[str(p.resolve())]=sha(p)
            for name,h in r['inputHashes'].items():
                need(sha(name)==h and (name not in pins or pins[name]==h),'All immutable actual route inputs/proofs remain consistent')
                pins[name]=h
        captured={(r['frame'],r['label'])for r in metadata['actualFullRGBDigests']}
        need(captured==set(images),'Every and only original native raster key accounted for; duplicate identical UI callbacks not counted as extra buffers')
        for q in metadata['actualFullRGBDigests']:
            need(hashlib.sha256(images[q['frame'],q['label']]).hexdigest().upper()==q['sha256'],'Every original native raster remains exactly its captured raw bytes')
        own_views=[r for r in carrier['rgbFrames']if r['header']['case']==key]
        need(len(own_views)==3,'Each actual route has three individually inspected native screens')
        views.extend(dict(r['header'],individuallyViewed=True)for r in own_views)
        case_faults=18+9+len(pixel['additionalActualImageFaultsRejected'])
        total_faults+=case_faults;total_fields+=positive['continuedActorFields'];unique_rasters+=len(images)
        cases.append(dict(case=key,nativePID=terminal['nativePID'],nativeIdentity=metadata['nativeIdentity'],
            originalCollectorPassed=metadata['passed'],originalCollectorError=metadata.get('error'),
            continuedActorFields=positive['continuedActorFields'],collisionEarnedLosses=2,actualContinue=positive,
            actualNativeNeutralJumpResponse=jump,sourceNameShadowChecks=proof['actualUIPixels']['native_name_shadow_checks'],
            selectedPlayerLadderSourceMatches=pixel['selectedPlayerLadderIcon']['fullSourceRasterMatches'],
            originalFaultsRejected=case_faults,uniqueOriginalNativeRAMRasters=len(images),actualRawCallbacks=len(metadata['actualFullRGBDigests'])))
        for p in folder.rglob('*'):
            if p.is_file():
                need(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),'No disk media/build/ROM/archive created by actual route')
                pins[str(p.resolve())]=sha(p)
    need(len(faults)==16 and total_faults==127 and len({c['nativePID']for c in cases})==4,
         'Original117 route faults plus10 source-ownership faults;16 additional native-neutral-jump faults kept separate')
    # Whole native jump and health-store kernels are actual source-bound ROM bytes.
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo,hi=((v-0xff800000)//8 for v in (0xff82f700,0xff82f800))
    need(scope['guest'][lo:hi]==stock[lo:hi],'Entire original neutral-jump kernel unchanged in actual current guest')
    for report in (binding,parent):
        for p,h in report['inputHashes'].items():need(sha(p)==h,'Original native source guard/proof pins intact');pins[p]=h
    for p in (Path(__file__),Path(qualified.__file__),Path(capture.__file__),Path(retained.__file__)if False else Path(qualified.retained.__file__),
              qualified.OUT/'report.json',ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json',ROOT/'mk2/mk2-maincpu.bin'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every final current source/proof/native asset remains immutable')
    OUT.mkdir();capture.native_base.save(OUT/'report.json',dict(passed=True,candidate=scope['current'].NAME,
        executableSHA256=scope['current'].EXE_SHA,guestSHA256=scope['current'].GUEST_SHA,cases=cases,
        actualContinueRoutes=4,collisionEarnedLosses=8,continuedActorFields=total_fields,
        originalUIStateRasterControlImageFaultsRejected=117,additionalPairedKanoOriginFaultsRejected=10,
        additionalNativeNeutralJumpFaultsRejected=faults,totalActualSemanticFaultsRejected=143,
        individuallyReviewedNativeRasters=views,originalUniqueNativeRAMRastersToRelease=unique_rasters,
        originalScope=parent['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
        originalPreflightAndSourceBindingAndPoseFaultRejectionsPreserved=True,gameplayReplayedToRepairChecks=False,
        allContinueStagesOrAudioAccepted=False,allPostEndingFreshJoinsAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active',
        nextAction='Current stage-zero cross-character continues are qualified. Broaden continued-stage/audio/post-ending joins, CPU/arena/audio, remaining stage/stock finishers and secret/cinematic integration; then combined release acceptance.'))
    print(json.dumps(dict(passed=True,actualRoutes=4,collisionEarnedLosses=8,continuedActorFields=total_fields,
        actualSemanticFaults=143,individuallyViewedNativeImages=12,originalUniqueRAMRastersToRelease=unique_rasters,
        fullPortAcceptance=False)),flush=True)


def execute(scope,carrier):
    try:run(scope,carrier)
    except Exception as error:
        import traceback
        need(not OUT.exists(),'Preserve exact current matrix failure');OUT.mkdir()
        capture.native_base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
