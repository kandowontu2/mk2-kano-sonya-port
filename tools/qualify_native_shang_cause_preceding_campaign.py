"""Conserve all thirteen earned fights before the passive Shang trace.

The later actual failure remains a failure. No boss/ending/art/audio or
whole-port acceptance follows from exact preceding input conservation.
"""
import hashlib
import inspect
import json
import re
from pathlib import Path
import qualify_native_subzero_ring_preceding_campaign as original
import capture_native_sonya_shang_cache_cause as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_shang_cause_preceding_campaign_checked'
START=394481
OPPONENTS=[17,11,7,4,0,18,3,9,2,10,5,8,1]
OLD=capture.previous.OUT
EXPECTED_ROWS=1009959


def validators():
    body=inspect.getsource(original.compare)
    for before,after in (
        ('list(range(11))','list(range(13))'),
        ("chosen[0]['ids'].split(',')))[:11]","chosen[0]['ids'].split(',')))[:13]"),
        ('for stage in range(11):','for stage in range(13):'),
        ('if stage < 10 else START','if stage < 12 else START'),
        ('completedOpponents=11','completedOpponents=13'),
        ('pre-SubZero','pre-Shang'),
        ('eleven true defeated','thirteen true defeated'),
        ('stage0..10','stage0..12')):
        body=capture.original.once(body,before,after)
    scope=dict(vars(original),START=START,OPPONENTS=OPPONENTS)
    exec(compile(inspect.getsource(original.prefix),__file__+'::whole_all_category_prefix','exec'),scope)
    exec(compile(body,__file__+'::whole_two_round_native_conservation_thirteen','exec'),scope)
    return scope['prefix'],scope['compare']


def run():
    need(not OUT.exists(),'Fresh full thirteen-match receipt, no failed outcome overwritten')
    paths=[capture.SOURCE/'report.json',
           ROOT/'audit_native_liu_early_leg_preceding_campaign_checked/report.json',
           ROOT/'audit_native_liu_early_leg_earned_clear_checked/report.json',
           ROOT/'audit_native_sonya_shang_cache_failure_preserved/report.json',
           ROOT/'audit_native_sonya_shang_cache_failure_retirement/report.json']
    source,twelve,liu,failed,retired=[json.loads(p.read_text()) for p in paths]
    guest_path=capture.OUT/'guest_memory_proof.json'
    identity_path=capture.OUT/'native_identity.json'
    before_path=capture.OUT/'input_hashes_before.json'
    guest,identity,before=[json.loads(p.read_text()) for p in (guest_path,identity_path,before_path)]
    need(source['passed'] and source['sourceOnlyAccepted'] and twelve['passed'] and
         twelve['accepted']['completeOriginalRows']==1001809 and liu['passed'] and
         liu['finiteNativeSonyaLiuClearAccepted'] and liu['completeTargetRows']==8150 and
         liu['accepted']['ownSuccessfulRoundFrames']==[392352,393931] and
         failed['preservationPassed'] and not failed['passed'] and retired['passed'] and
         guest['everyActualByteComparedInRAM'] and guest['bytes']==1048576 and
         guest['sha256']==twelve['currentWholeGuestSHA256'] and
         identity['ProcessId']==2008 and identity['ParentProcessId']==35228 and
         identity['createdUnix']==1791713685.8643436 and identity in original.census.census(),
         'Same original actual child birth/path/parent/full command, whole guest and all prior thirteen earned fights')
    pins=dict(before)
    for proof in (source,twelve,liu,failed,retired):
        need(not proof['fullPortAcceptance'],'Every prior finite requirement remains finite')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'Every frozen input unchanged: '+p)
            pins[p]=h
    lines=original.reader.complete_lines(capture.OUT/'run.log.gz')
    for line in lines:
        if line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')):
            q=dict(re.findall(r'(\w+)=([^\s]+)',line))
            need(int(q.get('frame',q.get('observer_callback','-1')))>=START,
                 'No corruption before the qualified prefix; do not hide a later real failure')
    parsed=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines
                       if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    entered=[q for q in parsed('STAGE') if q['stage']=='14']
    need(len(entered)==1 and entered[0]['frame']==str(START) and entered[0]['schedule']=='FFFA3000' and
         any(int(q['frame'])>=START+120 and q['stage']=='14' and q['human']=='18:18' and q['cpu']=='6:6'
             for q in parsed('LIVE')),'Actual Shang admission and later true Sonya/Shang owned fields')
    prefix,compare=validators()
    old_lines=original.reader.complete_lines(OLD/'run.log.gz')
    expected=prefix(old_lines)
    earlier=[line for line in expected if int(re.search(r'\bframe=(\d+)\b',line)[1])<391498]
    target=[line for line in expected if int(re.search(r'\bframe=(\d+)\b',line)[1])>=391498]
    need(len(expected)==EXPECTED_ROWS and len(earlier)==1001809 and len(target)==8150 and
         hashlib.sha256(''.join(earlier).encode()).hexdigest().upper()==twelve['accepted']['prefixSHA256'] and
         hashlib.sha256(''.join(target).encode()).hexdigest().upper()==liu['completeTargetSHA256'],
         'Entire independent twelve-prefix plus complete previously qualified actual Liu window')
    actual=prefix(lines)
    positive=compare(actual,expected)
    need(positive['completeOriginalRows']==EXPECTED_ROWS and positive['completedOpponents']==13 and
         len(positive['completeAllObservedCategoryInventory'])==28,'All preceding native/physical categories, not a favorable subset')
    faults=[]
    for tag in positive['completeAllObservedCategoryInventory']:
        key='MK2_NAT_CAMPAIGN_'+tag+' '
        i=next(i for i,line in enumerate(actual) if line.startswith(key))
        need('writes=0' in actual[i],'Every real observed category unassisted')
        for name,bad in (
            ('changed actual record',actual[:i]+[actual[i].replace('writes=0','writes=1',1)]+actual[i+1:]),
            ('omitted actual record',actual[:i]+actual[i+1:])):
            try:compare(bad,expected)
            except ValueError as error:faults.append(dict(category=tag,fault=name,rejectedBy=str(error)))
            else:raise ValueError('Altered preceding campaign accepted')
    need(len(faults)==56 and compare(actual,expected)==positive and identity in original.census.census(),
         'All category changes/omissions rejected and same original handle still live')
    for p in (Path(__file__).resolve(),Path(original.__file__),Path(original.reader.__file__),Path(capture.__file__),
              *paths,guest_path,identity_path,before_path,OLD/'run.log.gz'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Whole original sources/pins intact after finite gate')
    report=dict(passed=True,finiteFirstThirteenEarnedFightsByExactConservationAccepted=True,
        actualLiveNativeIdentity=identity,accepted=positive,actualObservedShangAdmission=entered[0],
        allObservedCategoryFaultsRejected=faults,currentWholeGuestSHA256=guest['sha256'],
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        growingCurrentLogNotPinnedAsTerminal=True,exactCompletedPrefixBoundBySHA256=True,
        laterCorruptionNotRelabeledAsSuccess=True,shangClearAccepted=False,fullTowerAccepted=False,
        endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,completedOpponents=13,completeOriginalRows=len(actual),
                         categoryFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':run()
