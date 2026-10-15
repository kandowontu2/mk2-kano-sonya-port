"""Exact full twelve-match conservation gate on the original new live handle.

No Liu win, ending, art, audio or whole-port acceptance follows from this.
Every preceding physical/native category, paid loss and earned win remains.
"""
import hashlib
import inspect
import json
import re
from pathlib import Path
import qualify_native_subzero_ring_preceding_campaign as original
import run_native_sonya_liu_early_leg_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_liu_early_leg_preceding_campaign_checked'
START = 391498
OPPONENTS = [17,11,7,4,0,18,3,9,2,10,5,8]
OLD = capture.previous.OUT
EXPECTED_ROWS = 1001809
EXPECTED_SHA = 'A5EED9E32C6CAA84C547B8815C97B7D631EAC53F724DA1A7557A1CC676BD5D6C'


def validators():
    body = inspect.getsource(original.compare)
    once = capture.original.once
    for before, after in (
        ('list(range(11))','list(range(12))'),
        ("chosen[0]['ids'].split(',')))[:11]", "chosen[0]['ids'].split(',')))[:12]"),
        ('for stage in range(11):','for stage in range(12):'),
        ('if stage < 10 else START','if stage < 11 else START'),
        ('completedOpponents=11','completedOpponents=12'),
        ('pre-SubZero','pre-Liu'),
        ('eleven true defeated','twelve true defeated'),
        ('stage0..10','stage0..11')):
        body = once(body,before,after)
    scope = dict(vars(original), START=START, OPPONENTS=OPPONENTS)
    exec(compile(inspect.getsource(original.prefix),__file__+'::whole_all_category_prefix','exec'),scope)
    exec(compile(body,__file__+'::whole_two_round_native_conservation_extended_to_twelve','exec'),scope)
    return scope['prefix'], scope['compare']


def run():
    need(not OUT.exists(), 'Fresh full twelve-match receipt, no failed result overwritten')
    paths = [capture.SOURCE/'report.json',
             ROOT/'audit_native_subzero_guard_pressure_preceding_campaign_checked/report.json',
             ROOT/'audit_native_subzero_guard_pressure_earned_clear_phase_bound_checked/report.json',
             ROOT/'audit_native_sonya_liu_original_policy_preserved/report.json',
             ROOT/'audit_native_sonya_liu_original_policy_retirement/report.json']
    source, preceding, clear, failed, retired = [json.loads(p.read_text()) for p in paths]
    guest_path = capture.OUT/'guest_memory_proof.json'
    identity_path = capture.OUT/'native_identity.json'
    pins_path = capture.OUT/'input_hashes_before.json'
    guest, identity, before = [json.loads(p.read_text()) for p in (guest_path,identity_path,pins_path)]
    census = original.census
    need(source['passed'] and source['sourceOnlyAccepted'] and
         preceding['passed'] and preceding['accepted']['completeOriginalRows']==785698 and
         clear['passed'] and clear['finiteNativeSonyaSubZeroClearAccepted'] and
         failed['preservationPassed'] and not failed['passed'] and retired['passed'] and
         guest['everyActualByteComparedInRAM'] and guest['bytes']==1048576 and
         guest['sha256']==preceding['currentWholeGuestSHA256'] and
         identity['ProcessId']==10800 and identity['ParentProcessId']==33348 and
         identity['createdUnix']==1791711060.8420143 and identity in census.census(),
         'Actual original child birth/path/parent/full command/current guest and full twelve prior earned fights')
    pins = dict(before)
    for proof in (source,preceding,clear,failed,retired):
        need(not proof['fullPortAcceptance'], 'Every prerequisite remains finite')
        for path,digest in proof['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest), 'Frozen complete evidence: '+path)
            pins[path]=digest
    lines = original.reader.complete_lines(capture.OUT/'run.log.gz')
    need(not any(line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')) for line in lines),
         'Same entire stream has no observed native cache corruption')
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines
                        if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    entered = [r for r in parse('STAGE') if r['stage']=='12']
    need(len(entered)==1 and entered[0]['frame']==str(START) and entered[0]['schedule']=='FFFA3000' and
         any(int(r['frame'])>=START+120 and r['stage']=='12' and r['human']=='18:18' and r['cpu']=='1:1'
             for r in parse('LIVE')), 'Actual Liu admission and subsequent true Sonya/Liu fields, not predicted progress')
    prefix, compare = validators()
    expected = prefix(original.reader.complete_lines(OLD/'run.log.gz'))
    need(len(expected)==EXPECTED_ROWS and hashlib.sha256(''.join(expected).encode()).hexdigest().upper()==EXPECTED_SHA,
         'Entire independently inventoried original successful twelve-match stream')
    actual = prefix(lines)
    positive = compare(actual,expected)
    need(positive['completeOriginalRows']==EXPECTED_ROWS and positive['completedOpponents']==12 and
         len(positive['completeAllObservedCategoryInventory'])==28,
         'Complete native/physical twelve-match inventory, not just shared favorable categories')
    faults = []
    for tag in positive['completeAllObservedCategoryInventory']:
        key = 'MK2_NAT_CAMPAIGN_'+tag+' '
        index = next(i for i,line in enumerate(actual) if line.startswith(key))
        need('writes=0' in actual[index], 'All observed physical/native categories unassisted')
        for description,bad in (
            ('changed actual record',actual[:index]+[actual[index].replace('writes=0','writes=1',1)]+actual[index+1:]),
            ('omitted actual record',actual[:index]+actual[index+1:])):
            try: compare(bad,expected)
            except ValueError as error: faults.append(dict(category=tag,fault=description,rejectedBy=str(error)))
            else: raise ValueError('Altered preceding native campaign accepted')
    need(len(faults)==56 and compare(actual,expected)==positive and identity in census.census(),
         'All category changes/omissions reject; complete positive and same live handle revalidated')
    for path in (Path(__file__).resolve(),Path(original.__file__),Path(capture.__file__),
                 Path(original.reader.__file__),*paths,guest_path,identity_path,pins_path,OLD/'run.log.gz'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==digest for p,digest in pins.items()), 'Every pin unchanged after finite full prefix gate')
    report = dict(passed=True,finiteCurrentFirstTwelveEarnedFightsByExactConservationAccepted=True,
        actualLiveNativeIdentity=identity,accepted=positive,actualObservedLiuAdmission=entered[0],
        allObservedCategoryFaultsRejected=faults,currentWholeGuestSHA256=guest['sha256'],
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        growingCurrentLogNotPinnedAsTerminal=True,exactCompletedPrefixBoundBySHA256=True,
        currentLiuClearAccepted=False,fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,
        artworkAccepted=False,audioAccepted=False,fullPortAcceptance=False,newBuilds=0,newNativeBoots=0,
        newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,originalNativePID=identity['ProcessId'],completedOpponents=12,
                         completeOriginalRows=len(actual),categoryFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':
    run()
