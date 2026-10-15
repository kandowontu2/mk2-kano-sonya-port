"""Review actual original allocation epochs, not reused pointer labels.

Accept original emitter/particle reference only. No port/build/release
acceptance, no inferred cleanup for transition-interrupted objects, and
no claim about requested600/750rasters the identity gate did not capture.
"""
import gzip
import json
import re
import struct
from collections import Counter
from pathlib import Path

import capture_native_kano_laser_effect_lifetime_scope as capture
import qualify_native_kano_laser_effect_assets_camera as source

ROOT=capture.ROOT
INPUT=ROOT/'audit_native_kano_laser_effect_lifetime_scope'
OUT=ROOT/'audit_native_kano_laser_effect_lifetime_review'
need,sha=capture.reference.need,capture.reference.sha


def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
            if line.startswith('MK3_SECONDARY_'+tag+' ')]


def contract(text,donor):
    births=rows(text,'EFFECT_BORN');fields=rows(text,'EFFECT_FIELD')
    by_epoch={row['epoch']:row for row in births}
    need(len(by_epoch)==len(births)==477,'Actual unique477allocationepochs, not guessed objects in memory')
    emitters=[r for r in births if r['kind']=='emitter'];smoke=[r for r in births if r['kind']=='smoke']
    need([(int(r['age']),int(r['mode'],16)) for r in emitters]==[(102,2),(162,3)] and len(smoke)==475,
         'Original contact/body/shake timings launch two exact2/3particle emitters')
    ticks=rows(text,'EFFECT_EMIT');expected_ticks=Counter()
    for row in emitters:
        own=[r for r in ticks if r['epoch']==row['epoch']]
        need([int(r['age']) for r in own]==list(range(int(row['age']),515,4)) and
             all(int(r['count'])==int(row['mode'],16) and r['victim']==row['saved_actor'] for r in own),
             'Every original4fieldtick uses actual true victim and its saved2/3count through winner')
        for tick in own:expected_ticks[int(tick['age'])]+=int(tick['count'])
        own_fields=[r for r in fields if r['epoch']==row['epoch']]
        need([int(r['age']) for r in own_fields]==list(range(int(row['age'])+1,519)) and
             all(r['active']=='1' and r['type']=='0018' for r in own_fields[:-1]) and
             own_fields[-1]['active']=='0' and own_fields[-1]['free']=='1',
             'Both real original emitters survive winner and stop at native scene task teardown, not bone burst')
    need(Counter(int(r['age']) for r in smoke)==expected_ticks,'Every actual475smoke birth matches full source emitter schedule')
    colors=struct.unpack_from('<16H',donor,(0xffcd6540-0xff800000)//8+2)
    expected_colors=','.join(f'{c:04X}' for c in colors)
    complete=[];interrupted=[];palette_checks=0;pending_palette=[];observed_free=0
    ends=rows(text,'EFFECT_ANIMATION_END');deletes=rows(text,'EFFECT_OBJECT_DELETE');retired=rows(text,'EFFECT_RETIRED')
    masses=rows(text,'EFFECT_MASS');ignored_late=[]
    for born in smoke:
        epoch=born['epoch'];start=int(born['age']);own=[r for r in fields if r['epoch']==epoch]
        active=[r for r in own if r['active']=='1']
        expected_end=min(start+20,517)
        need([int(r['age']) for r in active]==list(range(start+1,expected_end+1)) and
             all(r['kind']=='smoke' and r['type']=='0019' and r['lists']=='1,0,0' and r['actor_free']=='0' for r in active),
             'Every active original smoke field belongs to its actual allocated19task/real rendered object')
        for field in active:
            if field.get('colors')!=expected_colors:
                need(start==102 and int(field['age'])==103 and epoch in ('2','3'),
                     'Only first two known pre-transfer palette queue boundary observations differ')
                pending_palette.append(dict(epoch=epoch,age=103,colors=field.get('colors')))
            else:palette_checks+=1
            vx=int(field['vx'],16);vx=vx-0x100000000 if vx&0x80000000 else vx
            vy=int(field['vy'],16);vy=vy-0x100000000 if vy&0x80000000 else vy
            need(-0x1ffff<=vx<=0x20000 and -0x3ffff<=vy<=-0x10000,
                 'Actual source signedX and negativeY velocities: +/-2 and -1..-4 pixels/field')
        life_ends=[r for r in ends if r['epoch']==epoch and int(r['age'])<=expected_end]
        life_retired=[r for r in retired if r['epoch']==epoch and int(r['age'])<=expected_end]
        ignored_late.extend(r for r in retired if r['epoch']==epoch and int(r['age'])>expected_end)
        if start+20<=517:
            need(len(life_ends)==len(life_retired)==1 and int(life_ends[0]['age'])==start+20 and
                 life_ends[0]['fields']=='20' and life_retired[0]['fields']=='20' and
                 any(r['epoch']==epoch and int(r['age'])==start+20 and r['actor']==life_ends[0]['actor'] for r in deletes),
                 'Every one of450completeparticles calls actual object/palette delete then retires after exactly20fields')
            complete.append(epoch)
            final=[r for r in own if r['active']=='0']
            if final:
                need(final[-1]['free']=='1' and final[-1]['actor_free']=='1' and final[-1]['lists']=='0,0,0',
                     'Observed unreused completed object/task is actually free and no longer rendered')
                observed_free+=1
        else:
            need(not life_ends and not life_retired and any(r['epoch']==epoch and r['age']=='517' and
                r['type']=='0019' and r['mask']=='00008000' for r in masses),
                 'Last25realparticles interrupted by original native scene transition, not normal20fieldcleanup')
            interrupted.append(epoch)
    need(len(complete)==450 and len(interrupted)==25 and len(pending_palette)==2 and palette_checks==9273,
         'Whole450normal+25transitioninterruptedreference, all9273settledhardwarepalettefields')
    for emitter in emitters:
        need(any(r['epoch']==emitter['epoch'] and r['age']=='517' and r['type']=='0018' for r in masses),
             'Both emitters removed by actual native scene teardown')
    frames=rows(text,'RGB_DIGEST')
    need(len(frames)==25 and frames[-1]['stage']=='action_age_480' and
         not any(r['stage'] in ('action_age_600','action_age_750') for r in frames),
         'Actual25fullrasters only; later identity-gated rasters are absent, not accepted')
    return dict(emitterBirths=emitters,emitterTicks=len(ticks),particleBirths=475,
        completeParticles=450,completeParticleFields=20,transitionInterruptedParticles=25,
        sceneMassDeleteAge=517,emitterPostDeleteObservationAge=518,
        settledGreyPaletteFields=palette_checks,initialPendingPaletteTransfers=pending_palette,
        completedFreeTopologyObserved=observed_free,ignoredReusedEpochRetirements=len(ignored_late),
        actualRGBFrames=frames,actualRGBFramesViewed=25,
        visualObservation='Both original smoke emitters remain during bone burst/winner/fatality lettering through480. Individual grey particles naturally expire20fields; original mass task teardown at517.',
        sourceBounds=dict(signedXOffset=[-31,32],yOffset=[0,111],signedXVelocity=[-0x1ffff,0x20000],negativeYVelocity=[-0x3ffff,-0x10000]))


def main():
    need(not OUT.exists(),'Fresh immutable reference review')
    OUT.mkdir()
    report=json.loads((INPUT/'report.json').read_text());stage=json.loads((source.OUT/'report.json').read_text())
    need(report['passed'] and report['nativeExit']==0 and report['originalWholeGuestMatched'] and
         all(sha(p)==h for p,h in report['inputHashes'].items()) and
         stage['passed'] and all(sha(p)==h for p,h in stage['inputHashes'].items()),
         'Actual native original reference and complete current source evidence conserved')
    text=gzip.open(INPUT/'run.log.gz','rt').read();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    result=contract(text,donor);faults=[]
    for name,old,new in (('early_emitter','age=102 kind=emitter','age=100 kind=emitter'),
        ('short_particle','born=102 fields=20','born=102 fields=19'),
        ('wrong_palette','colors=0000,1CE7,18C6','colors=0000,1CE6,18C6'),
        ('wrong_scene_delete','age=517 kind=emitter','age=516 kind=emitter')):
        need(old in text,'Negative fault actual boundary: '+name)
        try:contract(text.replace(old,new,1),donor)
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Fault admitted: '+name)
    paths=[Path(__file__),INPUT/'report.json',INPUT/'run.log.gz',INPUT/'executed_sources.json.gz',
        source.OUT/'report.json',ROOT/'mk3/mk3-maincpu.bin',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    accepted=dict(passed=True,originalSmokeLifecycleReferenceAccepted=True,nativePortRuntimeAccepted=False,
        fullPortAcceptance=False,referenceContract=result,negativeFaultsRejected=faults,
        originalNaturalIntegrationRequirements=stage['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=stage['originalRemainingWorkGroups'],goalStatus='active',
        inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        latestPlayableChanged=False,limitations=['Only original earned Kano versus Sonya reference; no port acceptance.',
            'Scene-interrupted25objects were still in old render list at518; post-transition object clearance not observed here.',
            'No600/750actualrasters: identity gate suppresses later screenshots, so no post-continue visual acceptance.',
            'Original smoke lives until native scene cleanup, NOT only until164bone burst or196winner.',
            'Full action/audio/victim/CPU/arena/combined acceptance and all14requirements/sixremaininggroups remain.'])
    (OUT/'report.json').write_text(json.dumps(accepted,indent=2)+'\n')
    print(json.dumps(dict(passed=True,originalReferenceOnly=True,particles=475,completed=450,
        transitionInterrupted=25,settledPaletteFields=9273,fullPortAcceptance=False)))


if __name__=='__main__':main()
