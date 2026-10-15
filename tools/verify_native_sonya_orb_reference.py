"""Finite physically earned original Sonya orb reference, not a port claim."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import verify_native_kano_laser_reference as shared

ROOT=shared.ROOT
RUN=ROOT/'audit_native_secondary_sonya_source_distance'
OUT=ROOT/'audit_native_sonya_orb_reference_checked'
need=shared.need


def inspect(data,images):
    def tagged(name):return [r for r in data if r['tag']=='MK3_SECONDARY_'+name]
    observations=[r for r in data if r['tag']not in
                  ('MK3_SECONDARY_GUEST_DIGEST','MK3_SECONDARY_RGB_DIGEST')]
    need(all(r.get('writes')=='0'and r.get('assistance')=='none'for r in observations),
         'Entire actual original controller remains physical-input/passive-observation only')
    need(len(tagged('GUEST_DIGEST'))==1 and tagged('GUEST_DIGEST')[0]['sha256']==
         '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
         'Complete actual original initialized program unchanged')
    selected=tagged('SELECTED')
    need(len(selected)==1 and selected[0]['frame']=='3800'and selected[0]['ids']=='1,0',
         'Actual original Sonya player2 versus Kano player1 selected')
    zero=tagged('ROUND_ZERO')
    need([int(r['frame'])for r in zero]==[4179,4928] and
         all(r['hp']=='166,0'and r['ids']=='1,0'for r in zero),
         'Two actual physically earned Sonya rounds')
    health=tagged('HEALTH')
    need(all(r['pc']in('FF9503C0','FF9503F0','FFA5D5A0','FFA96760',
                      'FFA96790','FFA969F0','FFA96A90')for r in health),
         'Actual native health store PCs, not assisted HP writes')
    loss=[r for r in health if r['at']=='01060A40'and
          int(r['after'])<int(r['before'])<=166 and int(r['frame'])<=4928]
    need(len([r for r in loss if r['after']=='0'])==2 and
         all(r['pc']=='FFA5D5A0'for r in loss),'Both actual knockouts earned by the native combat contact routine')
    spacing,entry=tagged('COMMAND_SPACING'),tagged('OWN_ENTRY')
    need(len(spacing)==len(entry)==1 and spacing[0]['frame']=='5050'and
         spacing[0]['x']=='540,315'and spacing[0]['ids']=='1,0'and spacing[0]['finish']=='3',
         'Actual physical retreat reached225pixel original command distance')
    need(entry[0]['frame']=='5092'and entry[0]['ids']=='1,0'and
         entry[0]['x']=='544,315'and entry[0]['hp']=='166,0'and
         entry[0]['pc']=='FF9AE0C0'and entry[0]['finish']=='3',
         'Actual original second Sonya performer entered at229pixel distance')
    expected=[]
    for frame in range(5050,5093):
        if 5056<=frame:expected.append((str(frame),'block'))
        if 5089<=frame:expected.append((str(frame),'run'))
        for field,first in [('up',5060),('up',5070),('right',5080),('down',5090)]:
            if first<=frame<first+4:expected.append((str(frame),field))
    command=[r for r in tagged('INPUT')if 5050<=int(r['frame'])<=5093]
    need([(r['frame'],r['field'])for r in command]==expected,
         'Actual Block, Up/Up/Back/Down and final Run fields, without injected history')
    chain=['FF991F70','FF9923B0','FF993160','FF9931F0','FF993760',
           'FF992090','FF9987E0','FF9AE0B0']
    code=tagged('CODE')
    need([r['at']for r in code if r['frame']=='5092'and r['at']in chain]==chain and
         all(r['pc']==f'{int(r["at"],16)+16:08X}'for r in code),
         'Actual original history, held-mask, distance, finish gate and second selector fetch chain')
    need(any(r['at']=='FFA5EF10'and r['a9']=='00000002'for r in code)and
         any(r['at']=='FFA5EF10'and r['a9']=='00000004'for r in code)and
         any(r['at']=='FF9AE5D0'and r['a9']=='FF83F3C0'for r in code),
         'Actual shared kiss performer2 and genuinely distinct owned special4 orb task')
    fields=tagged('FIELD')
    need(len(fields)==451 and [int(r['age'])for r in fields]==list(range(1,452)),
         'All451 consecutive native action-to-win fields')
    need(all(int(r['frame'])==5092+int(r['age'])and r['ids']=='1,0'and
             r['hp']=='166,0'and r['own']=='010394B0'and r['victim']=='010396C0'
             for r in fields),'Actual distinct actors and character identities retained across complete recorded action')
    need(all(r['finish']in('3','2')for r in fields)and fields[-1]['finish']=='2',
         'Original finish flag becomes physical winner slot2, not character1 or a frozen3')
    phase={int(r['age']):r for r in fields}
    expected_poses={21:'FF8402C0',24:'FF840340',27:'FF8403C0',30:'FF840440',
                    33:'FF8404C0',36:'FF840540',39:'FF8405C0',42:'FF840640',
                    45:'FF8406C0',48:'FF840740',51:'FF8407A0',198:'FF83D500',241:'FF83D760'}
    need(all(phase[age]['poses'].split(',')[0]==pose for age,pose in expected_poses.items()),
         'Actual eleven original performer groups followed by Sonya own win animation')
    need(phase[118]['poses'].split(',')[1]=='FF8294A0'and
         phase[157]['poses'].split(',')[1]=='FF825280'and
         all(r['poses'].split(',')[1]=='FF840280'for r in fields[168:]),
         'Actual original Kano spin/reaction then transparent victim handoff, not another fighter body')
    palettes=tagged('PALETTE_FIELD')
    need(len(palettes)==902 and [(int(r['age']),int(r['side']))for r in palettes]==
         [(age,side)for age in range(1,452)for side in(1,2)],
         'Both actual palette banks observed every field,902 observations')
    for p in palettes:
        field=phase[int(p['age'])];side=int(p['side'])
        need(p['actor']==('010394B0'if side==1 else'010396C0')and
             int(p['bank'],16)==(int(field['bank'].split(',')[side-1],16)&0x7f00)and
             len(p['colors'].split(','))==64 and
             all(len(c)==4 and 0<=int(c,16)<=65535 for c in p['colors'].split(',')),
             'Entire real64word native palette for the actual actor/bank')
    need([len({r['colors']for r in palettes if r['side']==str(side)})for side in(1,2)]==[1,3],
         'Actual performer palette conserved and three original victim palette phases recorded')
    orb=[r for r in tagged('OBJECT')if r['actor']=='01034A70']
    need(len(orb)==36 and orb[0]['age']=='54'and orb[-1]['age']=='165'and
         (orb[0]['pose'],orb[0]['x'],orb[0]['y'])==('FF83FDA0','576','87')and
         any(r['age']=='114'and r['x']=='498'and r['y']=='87'for r in orb)and
         any(r['age']=='117'and r['x']=='138'and r['y']=='102'for r in orb),
         'Actual independent original orb grows, travels and wraps the native victim')
    source=json.loads((ROOT/'audit_native_secondary_finisher_reference/report.json').read_text())
    groups={r['group']for r in source['originalUnusedAssets'][2]['references']}
    need(all(r['pose']in groups for r in orb),
         'All observed orb groups belong to the already imported distinct special4')
    digest=tagged('RGB_DIGEST')
    need(len(digest)==len(images)==15,'All15 actual whole native rasters available in RAM')
    for actual,image in zip(digest,images):
        h=image['header']
        need(h['frame']==actual['frame']and h['stage']==actual['stage']and
             h['width']=='400'and h['height']=='254'and len(image['pixels'])==406400 and
             h['sha256']==actual['sha256']==hashlib.sha256(image['pixels']).hexdigest().upper(),
             'Entire original native raster and frozen actual digest match')
    stop=tagged('STOP')
    need(len(stop)==1 and stop[0]['frame']=='5543'and stop[0]['own_action_observed']=='1'and
         stop[0]['zeros']=='2','Same original controller planned normal exit after recorded action')
    return dict(twoPhysicallyEarnedRounds=True,physicalSlot=2,commandGap=225,entryGap=229,
                entryFrame=5092,consecutiveNativeFields=451,continuousPaletteBankObservations=902,
                nativeWinFirstAge=min(int(r['age'])for r in fields if r['finish']=='2'),
                observedIndependentOrbChanges=36,performerAnimationIndex=2,effectAnimationIndex=4,
                actualNativeFramesReviewed=15,originalActionObserved=True)


def main(capture):
    need(not OUT.exists()and not shared.transport.census()and not shared.reference.native.census(),
         'Fresh finite original reference receipt, no live native games')
    record=json.loads((RUN/'report.json').read_text())
    need(record['passed']and record['nativeExit']==0 and record['originalWholeGuestMatched']and
         record['actualWindowsIdentity']['ProcessId']==102192 and
         record['actualWindowsIdentity']['ParentProcessId']==183112 and
         record['actualWindowsIdentity']['createdUnix']==1791616299.8372784 and
         all(shared.reference.sha(p)==h for p,h in record['inputHashes'].items()),
         'Actual original PID/parent/path/creation normal exit and complete frozen executed provenance')
    with gzip.open(RUN/'run.log.gz','rt')as stream:text=stream.read()
    need(text==capture['text'],'Exact RAM original trace matches the immutable actual run')
    data=shared.rows(text);accepted=inspect(data,capture['rgbFrames']);faults=[]
    mutations=[('player_slot_identity','SELECTED',0,'ids','0,1'),
        ('earned_round','ROUND_ZERO',1,'hp','166,1'),('distance','COMMAND_SPACING',0,'x','400,315'),
        ('original_performer','OWN_ENTRY',0,'pc','FF9AF2F0'),('held_command','INPUT',
         next(i for i,r in enumerate([r for r in data if r['tag']=='MK3_SECONDARY_INPUT'])if r['frame']=='5089'and r['field']=='run'),'field','lp'),
        ('continuous_field','FIELD',200,'frame','5292'),('native_identity','FIELD',200,'ids','0,0'),
        ('native_hp','FIELD',200,'hp','166,1'),('performer_pose','FIELD',50,'poses','FF8402C0,FF82A540'),
        ('victim_pose','FIELD',168,'poses','FF8407A0,FF82A380'),
        ('palette_bank','PALETTE_FIELD',200,'bank','0700'),
        ('palette_actor','PALETTE_FIELD',200,'actor','010396C0'),
        ('palette_words','PALETTE_FIELD',200,'colors','0000'),
        ('orb_geometry','OBJECT',0,'x','315'),('planned_stop','STOP',0,'own_action_observed','0')]
    for name,tag,index,key,value in mutations:
        wrong=copy.deepcopy(data);[r for r in wrong if r['tag']=='MK3_SECONDARY_'+tag][index][key]=value
        try:inspect(wrong,capture['rgbFrames'])
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Original Sonya runtime fault admitted: '+name)
    damaged=copy.deepcopy(capture['rgbFrames']);damaged[11]['pixels']=bytes([damaged[11]['pixels'][0]^1])+damaged[11]['pixels'][1:]
    try:inspect(data,damaged)
    except ValueError as error:faults.append(dict(name='actual_native_raster_byte',rejected=str(error)))
    else:raise ValueError('Original whole Sonya raster fault admitted')
    source=json.loads((ROOT/'audit_native_secondary_finisher_reference/report.json').read_text())
    paths=[Path(__file__),Path(shared.__file__),RUN/'report.json',RUN/'run.log.gz',RUN/'process.json',
           ROOT/'audit_native_sonya_secondary_input/report.json',
           ROOT/'audit_native_kano_laser_reference_checked/report.json',
           ROOT/'tools/review_native_current_attract_ram.py']
    pins={str(p.resolve()):shared.reference.sha(p)for p in paths}
    report=dict(passed=True,originalFiniteActionReferenceAccepted=True,
        portSecondFatalityImplemented=False,fullAudioAccepted=False,fullPortAcceptance=False,
        accepted=accepted,actualWindowsIdentity=record['actualWindowsIdentity'],nativeExit=0,
        actualNativeFrameHeaders=[r['header']for r in capture['rgbFrames']],
        actualFrameReview=dict(pages=3,all15WholeFramesActuallyViewed=True,
            observations=['Actual original Sonya P2 earned two wins versus genuine Kano P1.',
                          'Source-correct command activates the owned magenta orb, distinct from fire kiss.',
                          'Actual orb surrounds the victim, who breaks apart; native Sonya wins text follows.',
                          'This is original MK3, not an implemented MKII port variant.']),
        faultRejections=faults,inputHashes=pins,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
        limitations=['Finite original Sonya1 versus Kano0 and stage only.',
                     'Sound packets captured, but no full PCM/audio acceptance.',
                     'Native physical winner2 handoff observed; following rematch cleanup not exercised.',
                     'MKII has no Run; its second input and all action/effect/victim code still need implementation.'],
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        gameSourceChanged=False,latestPlayableChanged=False,goalStatus='active',
        nextAction='Use both physically verified original variants to implement genuine distinct owned MKII finishers; conserve existing original choices, use MKII input/scheduler/victim/effect ownership and verify normal transitions.')
    need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
         'Full original14+6 scope retained')
    need(all(shared.reference.sha(p)==h for p,h in pins.items()),'Complete actual checker source/provenance conserved')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(OUT/'executed_checker_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({str(Path(__file__).resolve()):dict(sha256=shared.reference.sha(__file__),source=Path(__file__).read_text())},stream)
    print(json.dumps(dict(passed=True,originalReference=accepted,rejectedFaults=len(faults),portSecondFatalityImplemented=False)))
    return report
