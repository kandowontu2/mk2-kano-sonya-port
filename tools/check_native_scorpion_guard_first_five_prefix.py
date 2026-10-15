"""Finite SAME live handle prefix comparison; no new replay or campaign pass.

All twelve original categories retained, including zero CPU_ID records.
The independently qualified original nine-fight chronology is the oracle.
Only first five earned advances on the new live handle can be credited.
"""
import gzip
import hashlib
import json
import re
from pathlib import Path
import capture_native_paired_stumble_scorpion_guard as current
import inspect_native_campaign_progress as progress

ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT / 'audit_native_scorpion_guard_first_five_prefix_checked'
OLD = ROOT / 'audit_native_paired_stumble_regular_guard'
CUTOFF_EXCLUSIVE = 142740
TAGS = ('LIVE','STAGE','SELECT_ID','WIN','LOSS','HEALTH','ROM','STATE','SELECT','INPUT','SPECIAL','CPU_ID')


def complete_lines(path):
    lines = []
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        try:
            for line in stream:
                if line.endswith('\n'): lines.append(line)
        except EOFError:
            pass  # An active gzip member has no trailer yet; not a terminal.
    return lines


def prefix(lines):
    tags = tuple('MK2_NAT_CAMPAIGN_'+tag+' ' for tag in TAGS)
    result = []
    for line in lines:
        if line.startswith(tags):
            found = re.search(r'\bframe=(\d+)\b', line)
            need(found is not None, 'Every original physical/native record has an observed field')
            if int(found[1]) < CUTOFF_EXCLUSIVE: result.append(line)
    return result


def compare(actual, expected):
    need(actual == expected, 'Entire observed input/identity/health/winner/selection/stage chronology matches, no favorable rows dropped')
    stages = [dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in actual if l.startswith('MK2_NAT_CAMPAIGN_STAGE ')]
    need([int(q['stage']) for q in stages] == list(range(6)) and
         all(q['schedule']=='FFFA3000' for q in stages),
         'Actual cold first five earned advances, mirror reached but not credited as complete')
    return dict(prefixRows=len(actual), cutoffExclusive=CUTOFF_EXCLUSIVE,
        actuallyObservedFinalPrefixField=max(int(re.search(r'\bframe=(\d+)\b',l)[1]) for l in actual),
        completedOpponents=['Kano','Jax','Raiden','Kitana','Kung Lao'],
        completedTrueOpponentIDs=[17,11,7,4,0], reachedStage=5,
        completeOriginalInventory={tag:sum(l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ') for l in actual) for tag in TAGS},
        wholePrefixSHA256=hashlib.sha256(''.join(actual).encode()).hexdigest().upper())


def run():
    need(not OUT.exists(), 'Fresh finite live-prefix receipt')
    nine_path = ROOT / 'audit_native_sonya_first_nine_ladder_fights_checked/report.json'
    nine = json.loads(nine_path.read_text())
    source_path = current.SOURCE / 'report.json'
    source = json.loads(source_path.read_text())
    guest_path = current.OUT / 'guest_memory_proof.json'
    guest = json.loads(guest_path.read_text())
    native_path = current.OUT / 'native_identity.json'
    native = json.loads(native_path.read_text())
    current_pins_path = current.OUT / 'input_hashes_before.json'
    current_pins = json.loads(current_pins_path.read_text())
    need(nine['passed'] and nine['finiteFirstNineLadderProgressionAccepted'] and not nine['fullPortAcceptance'] and
         source['passed'] and source['sourceOnlyAccepted'] and source['physicalBranchPriorityChanges']==1 and
         source['timingChanges']==0 and guest['everyActualByteComparedInRAM'] and guest['bytes']==1048576 and
         guest['sha256']==nine['currentWholeGuestSHA256'] and
         all(sha(p)==h for report in (nine,source) for p,h in report['inputHashes'].items()) and
         all(sha(p)==h for p,h in current_pins.items()),
         'Actual entire current initialized guest and whole immutable original qualified chronology bound')
    need(native in progress.census.census(), 'Same actual native birth/path/parent/command remains live, not a timeout restart')
    lines = complete_lines(current.OUT/'run.log.gz')
    need(not any(l.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')) for l in lines),
         'No observed corruption in actual current prefix')
    latest = max(int(re.search(r'\bframe=(\d+)\b',l)[1]) for l in lines if l.startswith('MK2_NAT_CAMPAIGN_LIVE '))
    need(latest >= CUTOFF_EXCLUSIVE+120, 'Same stream has genuinely advanced past the fixed complete-prefix boundary')
    expected = prefix(complete_lines(OLD/'run.log.gz'))
    actual = prefix(lines)
    need(len(actual)==181259, 'Entire independently inventoried 181259-row actual prefix')
    positive = compare(actual,expected)
    faults = []
    for tag in TAGS:
        indices = [i for i,l in enumerate(actual) if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
        if not indices:
            need(tag=='CPU_ID', 'Only explicitly absent original CPU_ID category inapplicable')
            continue
        i = indices[len(indices)//2]
        for label,bad in (
            ('actual native/physical record changed',actual[:i]+[actual[i].replace('writes=0','writes=1',1)]+actual[i+1:]),
            ('actual native/physical record omitted',actual[:i]+actual[i+1:])):
            try: compare(bad,expected)
            except ValueError as error: faults.append(dict(tag=tag,record=i,fault=label,rejectedBy=str(error)))
            else: raise ValueError('Altered actual live-prefix record admitted')
    need(len(faults)==22 and compare(actual,expected)==positive and native in progress.census.census(),
         'All non-vacuous category changes/omissions reject; whole positive and same live handle revalidated')
    pins = dict(current_pins)
    for p in (nine_path,source_path,guest_path,native_path,current_pins_path,
              Path(__file__).resolve(),Path(current.__file__).resolve(),Path(progress.__file__).resolve()):
        pins[str(p)] = sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'All actual executed inputs still unchanged after prefix gate')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteSuccessorFirstFiveLadderProgressionAccepted=True,
        actualLiveNativeIdentity=native,accepted=positive,actualCategoryFaultsRejected=faults,
        explicitUnobservedCPU_IDFaultCategory=True,wholeCurrentGuestSHA256=guest['sha256'],
        originalNaturalIntegrationRequirements=nine['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=nine['originalRemainingWorkGroups'],
        fullTowerAccepted=False,ScorpionPolicyRuntimeAccepted=False,endingAccepted=False,freshJoinAccepted=False,
        artAccepted=False,audioAccepted=False,allFinishersAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteSuccessorFirstFiveLadderProgressionAccepted=True,
        actualNativePID=native['ProcessId'],prefixRows=len(actual),actualCategoryFaultsRejected=len(faults),
        fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual original live-prefix check outcome')
        OUT.mkdir(); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
