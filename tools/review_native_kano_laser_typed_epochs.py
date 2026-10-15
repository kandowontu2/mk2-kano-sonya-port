"""Both physical slots: actual laser action and normal grey particle cleanup.

Do not mistake native0109cache reuse for a live0201particle, or UI object
address reuse for stale debris. Transition-interrupted objects are not fully
accepted by this observer. Full action/audio/flash/roster regression remains.
"""
import gzip
import hashlib
import json
import re
import struct
import traceback
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port')
OUT=ROOT/'audit_native_kano_laser_typed_epochs_review'

def need(value,message):
    if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
            if line.startswith('MK2_LASER_'+tag+' ')]

def indexed(records,key='epoch'):
    result=defaultdict(list)
    for row in records:result[row[key]].append(row)
    return result

def signed(value):
    number=int(value,16)
    return number-0x100000000 if number&0x80000000 else number

def contract(text,side,colors):
    entry=rows(text,'ENTRY');contact=rows(text,'CONTACT');winner=rows(text,'WINNER')
    need(len(entry)==len(contact)==len(winner)==1,'One actual own action/contact/winner')
    entry,contact,winner=entry[0],contact[0],winner[0]
    need(entry['side']==str(side) and entry['age']=='0' and entry['hp']=='161,0' and entry['gap']=='149',
         'Earned real Kano finish at legal149gap')
    command=rows(text,'COMMAND_READY')[0];start=int(command['frame'])
    inputs=[r for r in rows(text,'INPUT') if start<=int(r['frame'])<=int(entry['frame'])]
    want=[(start+age+d,key) for age,key in ((10,'Low_Punch'),(18,'Block'),(26,'Block'),(34,'High_Kick')) for d in range(3)]
    need([(int(r['frame']),r['key']) for r in inputs]==want and all(r['slot']==str(side) for r in inputs),
         'Physical LP,Block,Block,HK with Block released at final button')
    history=[r for r in rows(text,'HISTORY') if r['frame']==entry['frame']]
    need([r['wanted'] for r in history]==['3','2','2','1'] and all(r['actual']==r['wanted'] for r in history) and
         [int(history[0]['tick'])-int(r['tick']) for r in history]==[0,8,16,24],
         'Actual native button-ring comparison, inside40tick source window')
    fields=rows(text,'FIELD')
    for slot,ident,actor,main,hp in ((side,17,entry['actor'],entry['main'],'161'),
        (3-side,18,entry['victim'],entry['victim_main'],'0')):
        own=[r for r in fields if r['slot']==str(slot) and int(r['age'])<=450]
        need([int(r['age']) for r in own]==list(range(451)) and
             all(r['id']==r['roster']==str(ident) and r['actor']==actor and r['main']==main and
                 r['hp']==hp and r['bank']==own[0]['bank'] and r['writes']=='0' and r['assistance']=='none' for r in own),
             'Every actual field through450 retains true body/main/roster/palette/health identity')
    need(contact['actor']==entry['victim'] and contact['main']==entry['victim_main'] and contact['id']=='18' and
         int(contact['age'])==(69 if side==1 else 68),'True victim handoff reflects actual native slot scheduling')
    victim=[r for r in fields if r['slot']==str(3-side) and int(contact['age'])<=int(r['age'])<=450]
    need(all(r['pose']=='FE83ED00' for r in victim),'Only true Sonya own laser-hit composite, not a proxy')
    cleanup=rows(text,'CLEANUP')
    need(any(r['kernel']=='FF838F60' and r['age']=='164' and r['a0']==entry['victim'] for r in cleanup) and
         any(r['kernel']=='FF83F930' and r['age']=='164' and r['a0']==entry['victim_main'] and r['a7']=='FF841EC0' for r in cleanup),
         'Actual true victim body hide and private native park at164')
    hidden=[r for r in victim if int(r['age'])>=164]
    need(all(int(r['body'],16)&0x20 for r in hidden) and len({(r['x'],r['y']) for r in hidden})==1,
         'Hidden victim stays hidden and local shake stops')
    need(winner['age']=='196' and winner['main']==entry['main'] and
         all(r['child']=='00000000' for r in fields if r['slot']==str(side) and 196<=int(r['age'])<=450),
         'On-time native Kano winner and owned beam release')
    need(not rows(text,'OVERRUN'),'No observed body-cache overwrite into live character state')
    births=rows(text,'TASK');need(len({r['epoch'] for r in births})==len(births),'Unique actual allocation epochs')
    emitters=[r for r in births if r['kind']=='emitter'];smoke=[r for r in births if r['kind']=='particle'];bones=[r for r in births if r['kind']=='bone']
    offset=1 if side==1 else 0
    need([(int(r['age']),int(r['count'])) for r in emitters]==[(102+offset,2),(162+offset,3)] and
         all(r['actor']==entry['victim'] and r['cache']=='00000000' for r in emitters),
         'Exactly two real independent emitters, not loop visits or victim-cache ownership')
    observations=indexed(rows(text,'EFFECT_FIELD'));ticks=indexed(rows(text,'EMIT'))
    retired=indexed(rows(text,'RETIRE'));mass=indexed(rows(text,'MASS'));terminal=indexed(rows(text,'TERMINAL_FIELD'))
    predicted=Counter()
    for born in emitters:
        epoch=born['epoch'];age=int(born['age']);own=ticks[epoch]
        need([int(r['age']) for r in own]==list(range(age,619,4)) and all(r['victim']==entry['victim'] and r['count']==born['count'] for r in own),
             'Complete source2/3particles every4fields, through winner until native scene teardown')
        for tick in own:predicted[int(tick['age'])]+=int(tick['count'])
        fs=observations[epoch]
        need([int(r['age']) for r in fs]==list(range(age,620)) and all(r['active']=='1' and r['type']=='0201' for r in fs[:-1]) and
             fs[-1]['active']=='0' and fs[-1]['free']=='1' and len(mass[epoch])==1 and mass[epoch][0]['age']=='619' and not retired[epoch],
             'Actual emitter task survives native winner and unlinks normally at scene619')
    need(Counter(int(r['age']) for r in smoke)==predicted and len(smoke)==(600 if side==1 else 605),
         'Every actual600/605particle birth matches both emitter schedules')
    complete=[];interrupted=[];pending=[];settled=0;unreused=0;reused=0
    by_cache_age=defaultdict(list)
    for r in smoke:by_cache_age[(r['cache'],r['age'])].append(r)
    for born in smoke:
        epoch=born['epoch'];age=int(born['age']);end=min(age+20,619);fs=observations[epoch]
        active=[r for r in fs if r['active']=='1']
        need([int(r['age']) for r in active]==list(range(age,end)) and all(r['type']=='0201' and r['actor']==born['actor'] and
             r['cache']==born['cache'] and r['cache_active']=='1' and r['lists']=='1,0,0' for r in active),
             'Every live particle field belongs to its actual20field allocation/render/cache epoch')
        for field in active:
            need(-0x1ffff<=signed(field['vx'])<=0x20000 and -0x3ffff<=signed(field['vy'])<=-0x10000,
                 'Actual grey particle X/Y source velocity ranges')
            need(field['pose']==f'{0xff800000+0xafc00*8+(int(field["life"])//4)*64:08X}',
                 'Complete native five-pose grey animation, four fields each')
            if field['colors']==colors:settled+=1
            else:
                need(epoch in ('2','3') and field['life']=='0' and field['age']==str(102+offset),
                     'Only two first-frame native queued palette transfers may be pending')
                pending.append(dict(epoch=epoch,age=field['age'],colors=field['colors']))
        if age+20<619:
            need(len(retired[epoch])==len(terminal[epoch])==1 and retired[epoch][0]['life']=='20' and not mass[epoch],
                 'Actual normal grey particle retirement after exactly20fields')
            for kernel,target in (('FF840450',born['actor']),('FF80E0E0',born['cache'])):
                need(any(r['kernel']==kernel and r['job']==born['job'] and r['actor']==born['actor'] and r['a0']==target and int(r['age'])==age+20 for r in cleanup),
                     'Normal particle invokes actual owned object/palette and cache delete before native retirement')
            final=terminal[epoch][0]
            if final['current_type']=='0109':
                need(final['active']=='1' and final['lists']=='1,0,0' and
                     any(r['actor']==born['actor'] for r in by_cache_age[(born['job'],str(age+20))]),
                     'Same-frame0109cache/new particle reuses retired addresses; never classify old0201task alive')
                reused+=1
            else:
                need(final['current_type']=='0201' and final['active']=='0' and final['free']=='1' and
                     final['cache_active']=='0' and final['lists']=='0,0,0','Unreused completed native object/cache/task no longer rendered or active')
                unreused+=1
            complete.append(epoch)
        else:
            need(not retired[epoch] and len(mass[epoch])==1 and mass[epoch][0]['age']=='619' and
                 mass[epoch][0]['type']=='0201' and mass[epoch][0]['mask']=='00008000' and
                 fs[-1]['age']=='619' and fs[-1]['active']=='0' and fs[-1]['cache_active']=='0',
                 'Final25particles interrupted by actual broad scene cleanup, not claimed normal20fieldretirement')
            interrupted.append(epoch)
    need(len(complete)==(575 if side==1 else 580) and len(interrupted)==25 and len(pending)==2,
         'Whole normal/interrupted native particle population reviewed')
    objects=indexed(rows(text,'OBJECT'))
    need(len(bones)==32 and all(r['age']=='164' and r['owner']==entry['victim'] and r['cache']=='00000000' and
         len(objects[r['epoch']])==1 and objects[r['epoch']][0]['actor']!=entry['victim'] and
         len(retired[r['epoch']])==1 for r in bones),'Actual32native bone allocations, real independent child identity, native retirement')
    scenes=rows(text,'SCENE');need(len(scenes)==42 and all(r['reused_pointer_active_hits']==r['reused_pointer_cache_hits']=='0'
         for r in scenes if int(r['age'])>=619),'No retained old effect task/cache address active after natural scene unlink through750')
    return dict(side=side,entry=entry,contact=contact,winner=winner,emitters=emitters,emitterTicks=sum(len(ticks[r['epoch']]) for r in emitters),
        particleBirths=len(smoke),normalParticles=len(complete),normalLifeFields=20,transitionInterruptedParticles=len(interrupted),
        normalUnreusedFreeTopology=unreused,normalProvenSameFrameCacheReuse=reused,settledActualGreyPaletteFields=settled,
        initialQueuedPaletteTransfers=pending,nativeBoneChildren=32,sceneTaskUnlinkAge=619,observedThroughAge=750,
        transitionObjectsFullyClearedAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable two-slot review');OUT.mkdir()
    try:
        stage_path=ROOT/'audit_native_kano_laser_action_routes_source/report.json';stage=json.loads(stage_path.read_text())
        need(stage['passed'] and all(sha(p)==h for p,h in stage['inputHashes'].items()),'Actual source qualification conserved')
        donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();colors=','.join(f'{c:04X}' for c in struct.unpack_from('<16H',donor,(0xffcd6540-0xff800000)//8+2))
        results=[];paths=[Path(__file__),stage_path,ROOT/'mk3/mk3-maincpu.bin',ROOT/'audit_native_kano_laser_first_action_review/report.json']
        for side in (1,2):
            folder=ROOT/f'audit_native_kano_laser_typed_epochs_p{side}';report=json.loads((folder/'report.json').read_text())
            need(report['passed'] and report['transportOnlyAccepted'] and not report['finisherAccepted'] and report['nativeExit']==0 and
                 report['wholeGuestMatched'] and not report['errors'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
                 'Same actual native handle terminal; whole guest/source/controller hashes conserved')
            text=gzip.open(folder/'run.log.gz','rt').read();result=contract(text,side,colors)
            baseline=ROOT/('audit_native_kano_laser_action_p1' if side==1 else 'audit_native_kano_laser_epochs_p2')
            baseline_text=gzip.open(baseline/'run.log.gz','rt').read()
            frames=rows(text,'RGB_DIGEST');prior_frames=rows(baseline_text,'RGB_DIGEST')
            need(len(frames)==18 and [(r['age'],r['sha256'],r['bytes']) for r in frames]==[(r['age'],r['sha256'],r['bytes']) for r in prior_frames],
                 'All18wholeactualnative rasters identical to each side already fully viewed in RAM')
            result['actualNativeFrames']=frames;result['wholeRastersIdenticalToViewedTrial']=str(baseline)
            results.append(result);paths.extend([folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz',baseline/'report.json',baseline/'run.log.gz'])
        faults=[]
        for name,old,new in (('short_particle','kind=particle job=0106D400 actor=0102FC10 life=20','kind=particle job=0106D400 actor=0102FC10 life=19'),
            ('wrong_grey_palette','colors=0000,1CE7,18C6','colors=0000,1CE6,18C6'),
            ('missing_cache_delete','kernel=FF80E0E0','kernel=FF80E0E1'),
            ('wrong_history','wanted=3 actual=3','wanted=3 actual=2')):
            text=gzip.open(ROOT/'audit_native_kano_laser_typed_epochs_p1/run.log.gz','rt').read();need(old in text,'Exact negative-fault boundary '+name)
            try:contract(text.replace(old,new,1),1,colors)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Fault admitted '+name)
        report=dict(passed=True,bothPhysicalSlotLaserActionAccepted=True,normalGreyParticleLifecycleAccepted=True,
            actualEmitterWinnerLifetimeAccepted=True,transitionObjectsFullyClearedAccepted=False,fullFinisherAccepted=False,fullPortAcceptance=False,
            runtimeCases=results,negativeFaultsRejected=faults,originalNaturalIntegrationRequirements=stage['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=stage['originalRemainingWorkGroups'],goalStatus='active',previousGoalTurnClassification='no progress: status only; next safe action was actual captured trial review',
            limitations=['Both slots only Kano versus true Sonya in this arena; no stock-victim/CPU/fallback acceptance.',
                'Bone objects normally rest on stage after their native task retires; not misclassified as leaked tasks.',
                'Last25particle objects still on old primary render list at619; no complete old object/palette reset/rejoin proof.',
                'SCENE old pointer render hits include reused UI allocations; never interpret them as live old debris.',
                'No native sound-none audio acceptance, white flash/screen shake still missing, full14+6acceptance unchanged.'],
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False)
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,slots=2,normalParticles=sum(r['normalParticles'] for r in results),settledGreyFields=sum(r['settledActualGreyPaletteFields'] for r in results),fullFinisherAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise

if __name__=='__main__':main()
