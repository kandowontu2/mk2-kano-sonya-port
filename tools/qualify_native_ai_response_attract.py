"""Actual native attract identity/pictures only; does not finish the port."""
import hashlib
import json
import re
import struct
from pathlib import Path
import numpy as np
import decode_native_picture as decoder
import native_ai_response_context as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_ATTRACT_'+tag+' ')]

def qualify(c):
    out=c['folder']/'native_ai_attract_runtime.json'
    need(not out.exists(),'Fresh actual runtime receipt')
    report=json.loads((c['folder']/'report.json').read_text())
    need(report['passed'] and c['guestCount']==1 and len(c['battleGfx'])==1 and c['terminal']['nativeExit']==0,'Same full cold native job actually terminal and every guest byte matched')
    need(not rows(c['text'],'RESET') and not rows(c['text'],'ERROR_ENTRY'),'No native reset or executed stock error loop anywhere in the complete cold attract run')
    inputs=rows(c['text'],'INPUT')
    need([(int(r['frame']),r['button'],int(r['value'])) for r in inputs]==[(f,'HighPunch',1) for f in range(300,304)]+[(304,'HighPunch',0)],'Only normal factory-screen High Punch and release; no paid selection or demo assistance')
    counters=rows(c['text'],'COUNTER')
    need(counters and all(r['writes']=='0' and r['assistance']=='none' for r in counters),'Whole passive native counter history')
    roster=current.ROSTER
    rotations=[]
    previous=None
    for r in counters:
        identity=int(r['id'])
        need(identity in roster,'Every native counter ID belongs to typed ordinary14 roster')
        if r['pc']=='FF84A460' and previous is not None:
            need(identity==roster[(roster.index(previous)+1)%14],'Actual native biography rotates with real IDs and no boss/proxy gap')
            rotations.append(r)
        previous=identity
    need({17,18}.issubset({int(r['id']) for r in rotations}),'Both new real biographies reached naturally without inputs')
    demos=rows(c['text'],'DEMO_OWNER')
    demo_records=[]
    for r in demos:
        slot=int(r['slot']);identity=int(r['id'])
        need(identity in (17,18) and int(r[f'p{slot}_roster'])==identity==int(r[f'p{slot}_id']) and
             r[f'p{slot}_actor']==r[f'p{slot}_owner'] and int(r[f'p{slot}_hp'])>0,
             'Real live native CPU construction and actor/Main ownership, not labels or stale attract fields')
        demo_records.append(r)
    need({17,18}.issubset({int(r['id']) for r in demo_records}),'Both new true CPU fighters reached without identity/health/RNG writes')
    picture_rows=rows(c['text'],'PICTURE')
    need({54,55}.issubset({int(r['row']) for r in picture_rows}),'Both native own-photo pointers reached shared decoder')
    photo_records=[]
    battle=c['battleGfx'][0]
    for identity in (17,18):
        pointer=struct.unpack_from('<I',c['guest'],0xf4900+(54+identity-17)*4)[0]
        at=(pointer-0x07200000)//8
        image,decoded=decoder.decode(battle,at)
        need(image.size==(138,158),'Genuine full native battle/biography photo geometry')
        palette=np.frombuffer(battle,dtype='<u2',count=decoded['palette_count'],offset=at+8)
        rgb5=np.stack(((palette>>10)&31,(palette>>5)&31,palette&31),axis=1)
        colors=((rgb5<<3)|(rgb5>>2)).astype(np.uint8)
        photo=colors[np.asarray(image)]
        candidates=[r for r in c['rgbFrames'] if r['header']['stage']==f'bio_{identity}_delay_180']
        need(len(candidates)==1,'One entire original native biography raster at completed presentation phase')
        record=candidates[0]
        need(hashlib.sha256(record['pixels']).hexdigest().upper()==record['header']['sha256'],'Full unchanged captured native raster')
        screen=np.frombuffer(record['pixels'],dtype=np.uint8).reshape(254,400,4)[:,:,[2,1,0]]
        need(np.array_equal(screen[22:180,29:167],photo),'All21804 genuine own photo pixels at exact stock biography position, no crop/overlay/scale')
        photo_records.append(dict(identity=identity,header=record['header'],pointer=f'{pointer:08X}',
            position=[29,22],matchedPixels=21804,decodedPhotoSHA256=hashlib.sha256(photo.tobytes()).hexdigest().upper()))
    fields=rows(c['text'],'FIELD')
    need(fields and int(fields[-1]['frame'])>120000 and len(rows(c['text'],'RESULT'))==1,'Complete bounded forty-minute logical cold native run, not an early favorable snapshot')
    frozen=[r for r in fields if int(r['frame'])>23000]
    stalled=bool(frozen) and all((r['mode'],r['counter'],r['p1_roster'],r['p1_action'],r['p2_action'],r['p1_hp'],r['p2_hp'])==('1','18','18','771','8','161','161') for r in frozen)
    complete_cycle=set(roster).issubset({int(r['id']) for r in rotations})
    states=rows(c['text'],'DEMO_STATE')
    live_records={}
    for identity in (17,18):
        records=[]
        for row in states:
            for slot in (1,2):
                if int(row[f'p{slot}_roster'])==identity==int(row[f'p{slot}_id']) and row[f'p{slot}_actor']==row[f'p{slot}_owner']:
                    records.append(dict(frame=int(row['frame']),slot=slot,id=identity,action=int(row[f'p{slot}_action']),
                        hp=int(row[f'p{slot}_hp']),opponentHP=int(row[f'p{3-slot}_hp']),actor=row[f'p{slot}_actor'],main=row[f'p{slot}_main']))
        need(len(records)>20 and len({r['action'] for r in records})>4 and
             any(0<r['hp']<161 or 0<r['opponentHP']<161 for r in records),
             'Both true added CPU fighters actually advance through multiple actions and health-changing combat')
        live_records[str(identity)]=dict(samples=len(records),actions=sorted({r['action'] for r in records}),
            minimumHP=min(r['hp'] for r in records),minimumOpponentHP=min(r['opponentHP'] for r in records),
            first=records[0],last=records[-1])
    responses=rows(c['text'],'AI_RESPONSE')
    for identity in (17,18):
        matches=[r for r in responses if int(r['id'])==identity]
        need(len(matches)==1,'Both real added CPU IDs naturally reach the repaired response dispatcher')
        row=matches[0]
        table=0xff800000+0xf3910*8
        need(row['pc']=='FF83B850' and int(row['table'],16)==int(row['a1'],16)==table and
             int(row['at'],16)==table+identity*32 and row['low']=='9BA0' and row['mask']=='FFFF' and
             any(row[f'p{slot}_actor']==row['a8']==row[f'p{slot}_owner'] and
                 row[f'p{slot}_main']==row['a13'] and int(row[f'p{slot}_id'])==identity for slot in (1,2)),
             'Actual live-ID read reaches owned valid FF9B9BA0 continuation, not ED9A0D3F instructions')
    old_pair=[r for r in states if r['p1_roster']=='18' and r['p2_roster']=='4']
    same_pair_advanced=bool(old_pair) and len({(r['p1_action'],r['p2_action'],r['p1_hp'],r['p2_hp']) for r in old_pair})>10
    need(any(r['pc']=='FF84A460' and int(r['frame'])>22631 and int(r['id'])==0 for r in rotations),
         'Native attract scheduler leaves the formerly blocked Sonya demo and wraps the real fourteen roster')
    result=dict(passed=complete_cycle and not stalled,
        actualLiveCPUCombat=live_records,actualRepairedResponseDispatch=responses,
        originalSonyaFailureNativeDispatchRepaired=True,originalSonyaKitanaPairNaturallyObservedAdvancing=same_pair_advanced,
        executedNativeErrorEntries=rows(c['text'],'ERROR_ENTRY'),nativeBiographyAndPublishedDemoIDsAccepted=True,nativeOwnBiographyPhotosAccepted=True,
        completeNativeAttractCycleAccepted=complete_cycle and not stalled,
        actualSonyaP1DemoStall=dict(observed=stalled,unchangedFieldSamples=len(frozen),firstField=frozen[0] if frozen else None,lastField=frozen[-1] if frozen else None),
        fullPortAcceptance=False,allAttractAudioAccepted=False,manualPresentationReviewPending=True,
        nativeTerminal=c['terminal'],physicalBootInputFields=inputs,wholeGuestBytesCompared=len(c['guest']),
        actualRotations=rotations,actualTrueDemoOwners=demo_records,exactOwnPhotoFrames=photo_records,
        observedBiographyIDs=sorted({int(r['id']) for r in rotations}),nativeLastField=fields[-1],
        inputHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(decoder.__file__)):sha(decoder.__file__)},
        goalStatus='active',publicBuildPromoted=False)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(biographiesAndPublishedIDsAccepted=True,exactOwnPhotoPixels=43608,trueDemoOwners=len(demo_records),attractCycleAccepted=result['completeNativeAttractCycleAccepted'],actualSonyaDemoStalled=stalled,lastField=fields[-1]['frame'],fullPortAcceptance=False)))
    return result

