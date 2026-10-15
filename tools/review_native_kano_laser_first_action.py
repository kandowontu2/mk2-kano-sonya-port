"""Finite earned P1 action review; never promote a transport pass to fidelity.

All eighteen whole native rasters were viewed from the same terminal trial's
RAM host. The baseline emitter tap counts LOOP visits, not allocations, and
same-frame pointer reuse prevents some topology assertions. Preserve that
observer limitation and require a successor allocation-epoch trial.
"""
import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port')
INPUT=ROOT/'audit_native_kano_laser_action_p1'
OUT=ROOT/'audit_native_kano_laser_first_action_review'

def need(value,message):
    if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
            if line.startswith('MK2_LASER_'+tag+' ')]

def contract(text):
    entries=rows(text,'ENTRY');contacts=rows(text,'CONTACT');winners=rows(text,'WINNER')
    need(len(entries)==len(contacts)==len(winners)==1,'One actual own action/contact/winner')
    entry,contact,winner=entries[0],contacts[0],winners[0]
    need(entry['side']=='1' and entry['age']=='0' and entry['hp']=='161,0' and entry['gap']=='149',
         'Genuinely earned P1 finish against zero-health opponent at legal149gap')
    history=[r for r in rows(text,'HISTORY') if r['frame']==entry['frame']]
    need([r['wanted'] for r in history]==['3','2','2','1'] and
         all(r['wanted']==r['actual'] for r in history) and
         [int(r['tick']) for r in history]==[785,777,769,761],
         'Actual native press history HK,Block,Block,LP inside forty-tick window')
    command=next(r for r in rows(text,'COMMAND_READY'))
    start=int(command['frame']);inputs=[r for r in rows(text,'INPUT') if start<=int(r['frame'])<=int(entry['frame'])]
    want=[(start+age+d,key) for age,key in ((10,'Low_Punch'),(18,'Block'),(26,'Block'),(34,'High_Kick')) for d in range(3)]
    need([(int(r['frame']),r['key']) for r in inputs]==want and all(r['slot']=='1' for r in inputs),
         'Actual physical LP,Block,Block,HK presses, with Block released before HK')
    fields=rows(text,'FIELD')
    need(len(fields)==902 and all(r['writes']=='0' and r['assistance']=='none' for r in fields),
         'Both actual bodies observed every field0..450, no guest assistance')
    for slot,ident,actor,main,bank,hp in ((1,17,entry['actor'],entry['main'],'0202','161'),
        (2,18,entry['victim'],entry['victim_main'],'0303','0')):
        own=[r for r in fields if int(r['slot'])==slot]
        need([int(r['age']) for r in own]==list(range(451)) and
             all(r['id']==r['roster']==str(ident) and r['actor']==actor and r['main']==main and
                 r['bank']==bank and r['hp']==hp for r in own),
             'True actor/main/roster/palette/health identities stay intact through winner450')
    victim=[r for r in fields if r['slot']=='2']
    need(contact['age']=='69' and contact['actor']==entry['victim'] and contact['main']==entry['victim_main'] and
         contact['id']=='18' and all(r['pose']=='FE83ED00' for r in victim[69:]),
         'Real native next-field handoff uses true Sonya own laser-hit composite, not a proxy')
    cleanup=rows(text,'CLEANUP')
    need(any(r['kernel']=='FF838F60' and r['age']=='164' and r['a0']==entry['victim'] for r in cleanup) and
         any(r['kernel']=='FF83F930' and r['age']=='164' and r['a0']==entry['victim_main'] and r['a7']=='FF841EC0' for r in cleanup),
         'Actual victim body hidden and its true main parked at burst164')
    need(all(int(r['body'],16)&0x20 for r in victim[164:]) and
         len({(r['x'],r['y']) for r in victim[164:]})==1,'Hidden victim never reappears or resumes shake')
    bones=[r for r in rows(text,'TASK') if r['kind']=='bone']
    need(len(bones)==32 and all(r['age']=='164' and r['actor']==entry['victim'] and r['type']=='010C' for r in bones),
         'Actual32own paired bone initializers from true victim at164')
    need(winner['age']=='196' and winner['main']==entry['main'] and
         all(r['child']=='00000000' for r in fields if r['slot']=='1' and int(r['age'])>=196) and
         all(any(r['kernel']==kernel and r['age']=='196' and r['job']==entry['main'] for r in cleanup)
             for kernel in ('FF83EFD0','FF840450','FF80E0E0')),
         'On-time native winner196 and actual owned beam object/cache cleanup')
    need(not rows(text,'OVERRUN'),'No observed native body-cache overwrite into live character state')
    frames=rows(text,'RGB_DIGEST');ages=[1,21,48,68,72,100,102,132,162,164,170,196,200,240,300,450,600,750]
    need([int(r['age']) for r in frames]==ages and all(r['bytes']=='406400' and r['width']=='400' and r['height']=='254' for r in frames),
         'All18complete actual400x254rasters, including continue scene')
    mode=rows(text,'MODE');need(any(r['age']=='620' and r['mode']=='3' for r in mode),'Actual natural continue transition620')
    need(rows(text,'STOP')[0]['age']=='750' and rows(text,'RESULT')[0]['age']=='751','Same trial retained750fields then natural native terminal')
    return dict(entry=entry,contact=contact,winner=winner,boneInitializers=32,actualFrames=frames,
        actualFramesViewed=18,continueTransitionAge=620,observedStableIdentityThroughAge=450,
        visualObservation='True Kano laser and red Sonya recoil, grey smoke, own bones, native Kano winner/FATALITY lettering. No full-screen white flash. At750 the continue panels are present; this is not an unobscured render-list clearance proof.')

def main():
    need(not OUT.exists(),'Fresh immutable finite review')
    run=json.loads((INPUT/'report.json').read_text());stage_path=ROOT/'audit_native_kano_laser_action_routes_source/report.json'
    stage=json.loads(stage_path.read_text())
    need(run['passed'] and run['transportOnlyAccepted'] and run['nativeExit']==0 and run['wholeGuestMatched'] and
         run['nativeRGBFrames']==18 and not run['errors'] and not run['finisherAccepted'] and
         all(sha(p)==h for p,h in run['inputHashes'].items()) and stage['passed'] and
         all(sha(p)==h for p,h in stage['inputHashes'].items()),'Actual trial/source/whole guest conserved; no full finisher acceptance inferred')
    text=gzip.open(INPUT/'run.log.gz','rt').read();result=contract(text);faults=[]
    for name,old,new in (('wrong_history','wanted=3 actual=3 tick=785','wanted=3 actual=2 tick=785'),
        ('proxy_identity','id=18 roster=18 hp=0','id=0 roster=18 hp=0'),
        ('late_victim_hide','age=164 writes=0 assistance=none kernel=FF838F60','age=165 writes=0 assistance=none kernel=FF838F60'),
        ('late_winner','MK2_LASER_WINNER frame=3242 side=1 age=196','MK2_LASER_WINNER frame=3242 side=1 age=197')):
        need(old in text,'Actual negative-fault boundary '+name)
        try:contract(text.replace(old,new,1))
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Fault admitted '+name)
    paths=[Path(__file__),INPUT/'report.json',INPUT/'run.log.gz',INPUT/'executed_sources.json.gz',stage_path]
    report=dict(passed=True,finiteEarnedP1KanoLaserActionAccepted=True,fullFinisherAccepted=False,
        nativeEffectLifetimeAccepted=False,fullPortAcceptance=False,actionContract=result,negativeFaultsRejected=faults,
        observerLimitations=['Baseline emitter task entry is also its loop target:243visits are NOT243allocationepochs.',
            'Some retired task/object/cache addresses are reused before frame-end. Pointer-only EPOCH_END cannot prove every old allocation was active/free.',
            'Scene-interrupted particle/cache/palette clearance requires successor passive epoch observers.',
            'Missing white flash/screen shake/source sound; no sound-none audio acceptance.',
            'Only P1 Kano versus Sonya in this arena; other slot/stock victims/CPU/fallback/full regression still required.'],
        originalNaturalIntegrationRequirements=stage['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=stage['originalRemainingWorkGroups'],goalStatus='active',
        previousGoalTurnClassification='no progress: user requested status; authoritative native report inspected but no acceptance work completed',
        inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False)
    need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteActionOnly=True,framesViewed=18,negativeFaults=len(faults),fullFinisherAccepted=False)))

if __name__=='__main__':main()
