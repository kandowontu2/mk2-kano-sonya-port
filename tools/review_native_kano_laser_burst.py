"""Finite earned two-slot laser, smoke cleanup, and source burst timing review.

Retain the failed old velocity review and its strict source ranges unchanged.
No audio, stock-victim/CPU, interrupted-object reset, or full-port acceptance.
Full source and both new native raster inventories were visually inspected
in RAM, without writing raw media or modifying any executed input.
"""
import gzip
import hashlib
import json
import re
import struct
import traceback
from pathlib import Path
import review_native_kano_laser_typed_epochs as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_burst_review'
need,sha=prior.need,prior.sha


def rows(text,tag,original=False):
    prefix=('MK3_SECONDARY_' if original else 'MK2_LASER_')+tag+' '
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith(prefix)]


def uniform_digest(bgr):
    return hashlib.sha256(bytes((*bgr,0))*400*254).hexdigest().upper()


def original_contract(text):
    entry=rows(text,'OWN_ENTRY',True)
    need(len(entry)==1 and entry[0]['age']=='0' and entry[0]['ids']=='0,1' and entry[0]['hp']=='166,0',
         'Actual original own Kano versus Sonya, physically earned finish')
    stop=rows(text,'STOP',True)
    need(len(stop)==1 and stop[0]['zeros']=='2' and stop[0]['own_action_observed']=='1',
         'Two ordinary original rounds and actual original action')
    code=rows(text,'BURST_CODE',True)
    flash=[r for r in code if r['at'] in ('FFAA2880','FFAA2990')]
    need([(r['at'],r['age'],r['bg'],r['palette']) for r in flash]==
         [('FFAA2880','166','0000','0001'),('FFAA2990','172','FFFF','0000')],
         'Real original six-field flash coroutine entry and restoration')
    ctor=[r for r in code if r['at']=='FFAA2A20']
    need(len(ctor)==1 and ctor[0]['age']=='164' and ctor[0]['a11']=='000C0012',
         'Real original18-step12-pixel burst shake recipe')
    steps=[r for r in code if r['at']=='FFAA2B20']
    need([int(r['age']) for r in steps]==list(range(164,218,3)) and
         [r['a11'] for r in steps]==['0000000C' if n%2==0 else 'FFFFFFF4' for n in range(18)],
         'Every original shake step and source cadence observed')
    fields=rows(text,'BURST_FIELD',True)
    need([int(r['age']) for r in fields]==list(range(241)), 'Every original burst-global field')
    for r in fields:
        age=int(r['age'])
        if age>=164:
            need(r['bg']==('FFFF' if 166<=age<172 else '0000') and
                 r['palette']==('0000' if 166<=age<172 else '0001'), 'Original background/palette restore timing')
            want=0xfff4 if age<218 and ((age-164)//3)%2==0 else 0
            need(int(r['y'],16)==want,'Original complete18-step shake and final restoration')
    frames=rows(text,'RGB_DIGEST',True)
    action={int(r['stage'].rsplit('_',1)[1]):r for r in frames if r['stage'].startswith('action_age_')}
    need(len(frames)==36 and all(r['width']=='400' and r['height']=='254' and r['bytes']=='406400' for r in frames),
         'All36 whole actual source rasters, not screenshots/crops')
    need([age for age in range(164,178) if action[age]['sha256']==uniform_digest((255,255,255))]==list(range(169,173)),
         'Actual original pipeline has exactly four fully white fields169..172')
    need([age for age in range(164,178) if action[age]['sha256']==uniform_digest((0,0,0))]==[173,174],
         'Actual original pipeline has exactly two black-background recovery fields173..174')
    return dict(entry=entry[0],wholeActualRasters=frames,flashEnterAge=166,flashRestoreAge=172,
                visibleWholeWhiteAges=list(range(169,173)),uniformBackgroundRecoveryAges=[173,174],
                shakeStartAge=164,shakeEndAge=218,steps=18,cadenceFields=3,sourceBackgroundWord='0000')


def burst_contract(text,side):
    entry=rows(text,'ENTRY')[0]
    create=rows(text,'BURST_CREATE');worker=rows(text,'BURST_TASK')
    begin=rows(text,'FLASH_ENTER');restore=rows(text,'FLASH_RESTORE');retire=rows(text,'AUX_RETIRE')
    need(len(create)==len(worker)==len(begin)==len(restore)==1 and len(retire)==2,
         'One actual burst constructor/flash worker/entry/restoration, two auxiliary retirements')
    create,worker,begin,restore=create[0],worker[0],begin[0],restore[0]
    need(create['age']==worker['age']=='164' and create['actor']==worker['actor']==worker['owner']==entry['victim'] and
         create['id']==worker['id']=='18' and worker['type']=='0201' and create['main']==entry['main'],
         'Burst does not substitute a fighter or replace the actual performer main task')
    need(begin['age']=='166' and begin['life']=='2' and begin['actor']==entry['victim'] and
         begin['id']=='18' and begin['job']==worker['job'] and begin['sp']!=begin['private_sp'] and
         restore['age']=='172' and restore['job']==worker['job'] and restore['flash_fields']=='6' and
         restore['saved']==create['bg']=='0860' and restore['bg']=='FFFF' and restore['palette']=='0000',
         'Actual source-timed six-field coroutine uses native private continuation and saves the true background')
    flash=[r for r in retire if r['kind']=='flash'];quake=[r for r in retire if r['kind']=='quake']
    need(len(flash)==len(quake)==1 and flash[0]['age']=='172' and flash[0]['life']=='8' and
         flash[0]['job']==worker['job'] and flash[0]['bg']=='0860' and flash[0]['palette']=='0001',
         'Native flash returns and enters normal retirement with actual background and palette restored')
    need(quake[0]['age']=='218' and quake[0]['life']=='54' and quake[0]['steps']=='18' and
         quake[0]['initial_y32']==quake[0]['y32']==create['y32'],
         'Actual native shake restores its whole DWORD, including the neighbor WORD')
    steps=rows(text,'QUAKE_STEP')
    need([int(r['age']) for r in steps]==list(range(164,218,3)) and
         [int(r['step']) for r in steps]==list(range(1,19)) and
         [int(r['remaining']) for r in steps]==list(range(18,0,-1)) and
         all(r['job']==quake[0]['job'] and r['actor']==entry['victim'] and r['type']=='0103' for r in steps) and
         [r['amplitude'] for r in steps]==['0000000C' if n%2==0 else 'FFFFFFF4' for n in range(18)],
         'All18 actual native12-pixel steps, three fields each, in independent native quake task')
    fields=rows(text,'BURST_FIELD')
    need([int(r['age']) for r in fields]==list(range(301)),'Whole native burst global timeline0..300')
    initial=int(create['y32'],16)
    for r in fields:
        age=int(r['age'])
        if age>=164:
            need(r['bg']==('FFFF' if 166<=age<172 else create['bg']) and
                 r['palette']==('0000' if 166<=age<172 else '0001'),
                 'Every actual native background/palette field obeys exact source flash timing')
            want=(initial-12 if age<218 and ((age-164)//3)%2==0 else initial)&0xffffffff
            need(int(r['y32'],16)==want,'Every native DWORD shake field, cadence, and full restoration')
    frames=rows(text,'RGB_DIGEST');action={int(r['age']):r for r in frames}
    need(len(frames)==33 and all(r['width']=='400' and r['height']=='254' and r['bytes']=='406400' for r in frames),
         'All33 actual whole native rasters individually reviewed in RAM')
    need([age for age in range(164,177) if action[age]['sha256']==uniform_digest((255,255,255))]==list(range(169,173)),
         'Both-slot actual four-white-field render pipeline exactly matches original timing')
    # Native MK2 preserves its own stage background0860; the original MK3
    # reference uses0000. Never force black or claim cross-stage pixel identity.
    need([age for age in range(164,177) if action[age]['sha256']==uniform_digest((0,24,16))]==[173,174],
         'Two recovery fields restore actual native stage0860, not a forced MK3 black fill')
    return dict(side=side,constructor=create,flashWorker=worker,flashEnter=begin,flashRestore=restore,auxiliaryRetirements=retire,
        actualNativeRasters=frames,wholeWhiteAges=list(range(169,173)),stageBackgroundRecoveryAges=[173,174],
        nativeStageBackgroundWord='0860',nativeBackgroundBGR=[0,24,16],sourceTimingAccepted=True,
        crossStagePixelIdentityClaimed=False,actualWinnerAge=rows(text,'WINNER')[0]['age'])


def record(folder):
    report=json.loads((folder/'report.json').read_text())
    need(report['passed'] and report['transportOnlyAccepted'] and not report['finisherAccepted'] and
         report['nativeExit']==0 and not report['errors'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Same actual game handle terminal0; all executed source/asset/controller inputs conserved')
    return gzip.open(folder/'run.log.gz','rt').read()


def main():
    need(not OUT.exists(),'Fresh finite review, old failed receipts preserved');OUT.mkdir()
    try:
        stage_path=ROOT/'audit_native_kano_laser_burst_source/report.json';stage=json.loads(stage_path.read_text())
        need(stage['passed'] and stage['sourceOnlyAccepted'] and all(sha(p)==h for p,h in stage['inputHashes'].items()),
             'Actual built whole guest qualification conserved')
        old_failure=ROOT/'audit_native_kano_laser_typed_epochs_review/failure.txt'
        need('Actual grey particle X/Y source velocity ranges' in old_failure.read_text(),
             'Real previous width bug remains recorded; strict old contract was not weakened')
        original_folder=ROOT/'audit_native_kano_laser_original_burst_pipeline'
        original=original_contract(record(original_folder))
        donor_path=ROOT/'mk3/mk3-maincpu.bin';donor=donor_path.read_bytes()
        colors=','.join(f'{c:04X}' for c in struct.unpack_from('<16H',donor,(0xffcd6540-0xff800000)//8+2))
        results=[];texts={}
        paths=[Path(__file__),Path(prior.__file__),stage_path,donor_path,old_failure,
               ROOT/'audit_native_kano_laser_flash_shake_abi/report.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        for folder in [original_folder]+[ROOT/f'audit_native_kano_laser_burst_p{s}' for s in (1,2)]:
            paths.extend([folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz'])
        for side in (1,2):
            text=record(ROOT/f'audit_native_kano_laser_burst_p{side}');texts[side]=text
            life=prior.contract(text,side,colors);burst=burst_contract(text,side)
            results.append(dict(lifecycle=life,burst=burst))
        text=texts[1];faults=[]
        line=next(line for line in text.splitlines() if line.startswith('MK2_LASER_RETIRE ') and 'kind=particle ' in line and 'life=20 ' in line)
        mutations=[('short_particle',line,line.replace('life=20 ','life=19 ')),
            ('wrong_grey_palette','colors=0000,1CE7,18C6','colors=0000,1CE6,18C6'),
            ('missing_cache_delete','kernel=FF80E0E0','kernel=FF80E0E1'),
            ('wrong_history','wanted=3 actual=3','wanted=3 actual=2'),
            ('short_flash','flash_fields=6','flash_fields=5'),
            ('neighbor_corruption','initial_y32=0000FFF8 y32=0000FFF8','initial_y32=0000FFF8 y32=0001FFF8')]
        for name,old,new in mutations:
            need(old in text,'Exact actual negative-control boundary '+name)
            changed=text.replace(old,new,1)
            try:
                prior.contract(changed,1,colors);burst_contract(changed,1)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Fault admitted '+name)
        frame_line=next(line for line in text.splitlines() if line.startswith('MK2_LASER_RGB_DIGEST ') and 'age=169 ' in line)
        bad=text.replace(frame_line,frame_line.replace(uniform_digest((255,255,255)),uniform_digest((0,24,16))),1)
        try:burst_contract(bad,1)
        except ValueError as error:faults.append(dict(name='missing_actual_white_frame',rejected=str(error)))
        else:raise ValueError('Missing actual full white frame admitted')
        report=dict(passed=True,bothPhysicalSlotLaserActionAccepted=True,normalGreyParticleLifecycleAccepted=True,
            actualEmitterWinnerLifetimeAccepted=True,sourceBurstFlashTimingAccepted=True,actualNativeScreenShakeAccepted=True,
            transitionObjectsFullyClearedAccepted=False,audioAccepted=False,fullFinisherAccepted=False,fullPortAcceptance=False,
            originalRuntimeReference=original,runtimeCases=results,negativeFaultsRejected=faults,
            originalNaturalIntegrationRequirements=stage['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=stage['originalRemainingWorkGroups'],goalStatus='active',
            previousGoalTurnClassification='no progress: user status answer; this turn earned new original and player-two runtime evidence',
            limitations=['Only true Kano versus true Sonya in this native arena; other victims/CPU/fallback not accepted.',
                'Sound-none captures do not accept laser audio or native sound priority.',
                'Last25scene-interrupted smoke objects require full reset/rejoin object and palette proof.',
                'Original MK3 background0000 and native MK2 stage0860 intentionally differ; exact render timing, not cross-stage pixels, accepted.',
                'Auxiliary retirement entries observed; no separate post-retirement allocation-epoch audit for flash/quake.',
                'All original14requirements and6remaining work groups remain in scope; public CMD and ZIP unchanged.'],
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False)
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
             'Original full natural integration scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,slots=2,normalParticles=sum(r['lifecycle']['normalParticles'] for r in results),
            actualWhiteFields=4,actualStageRecoveryFields=2,nativeShakeFields=54,negativeFaultsRejected=len(faults),fullFinisherAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
