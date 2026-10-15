"""Same live current native handle: conserve the complete earned eleven fights.

The target strategy is new, but all preceding original physical/native rows
must equal the independently qualified Mileena campaign, including every
health, winner, continue and opponent-specific action/decision record. This
does not qualify Sub-Zero, bosses, endings, art, sound or the whole port.
"""
import gzip
import hashlib
import json
import re
from pathlib import Path
import native_process_census_v6647 as census
import check_native_scorpion_guard_first_five_prefix as reader
import run_native_sonya_subzero_ring_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT / 'audit_native_subzero_ring_preceding_campaign_checked'
OLD = ROOT / 'audit_native_paired_stumble_mileena_guard'
START = 304271
OPPONENTS = [17, 11, 7, 4, 0, 18, 3, 9, 2, 10, 5]


def prefix(lines):
    result = []
    for line in lines:
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            frame = re.search(r'\bframe=(\d+)\b', line)
            need(frame is not None, 'Every original campaign row has its actual native field')
            if int(frame[1]) < START:
                result.append(line)
    return result


def compare(actual, expected):
    need(actual == expected, 'All original pre-SubZero physical/native records identical, no dropped favorable or unfavorable rows')
    parsed = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line))
                          for line in actual if line.startswith('MK2_NAT_CAMPAIGN_' + tag + ' ')]
    stages, wins, losses = (parsed(tag) for tag in ('STAGE', 'WIN', 'LOSS'))
    need([int(row['stage']) for row in stages] == list(range(11)) and
         all(row['schedule'] == 'FFFA3000' for row in stages), 'Every actual earned preceding stage0..10 retained')
    chosen = [row for row in parsed('ROM') if row['list'] == 'FFFA3000']
    need(len(chosen) == 1 and list(map(int, chosen[0]['ids'].split(',')))[:11] == OPPONENTS,
         'Exact original native schedule and eleven true defeated opponent IDs')
    for stage in range(11):
        end = int(stages[stage+1]['frame']) if stage < 10 else START
        last_loss = max([int(row['frame']) for row in losses if row['stage'] == str(stage) and int(row['frame']) < end]
                        + [int(stages[stage]['frame'])])
        earned = [row for row in wins if row['stage'] == str(stage) and row['slot'] == '1' and
                  last_loss < int(row['frame']) < end]
        need(len(earned) == 2 and all(row['id'] == '18' and row['pc'] == 'FF8296B0' and
             int(row['health'].split(',')[0]) > int(row['health'].split(',')[1]) for row in earned),
             'Each opponent follows two real own native rounds in one successful attempt, never accumulated paid losses')
    tags = sorted({line.split(' ', 1)[0][len('MK2_NAT_CAMPAIGN_'):] for line in actual})
    return dict(completeOriginalRows=len(actual), exclusiveNativeBoundary=START,
                prefixSHA256=hashlib.sha256(''.join(actual).encode()).hexdigest().upper(),
                completedTrueOpponentIDs=OPPONENTS, completedOpponents=11,
                completeAllObservedCategoryInventory={tag:len(parsed(tag)) for tag in tags},
                originalCPU_IDRows=0)


def run():
    need(not OUT.exists(), 'Fresh finite full preceding-campaign receipt')
    source_path = capture.SOURCE / 'report.json'
    prior_path = ROOT / 'audit_native_mileena_guard_earned_clear_checked/report.json'
    retired_path = ROOT / 'audit_native_mileena_guard_losing_subzero_retirement/report.json'
    source, prior, retired = [json.loads(path.read_text()) for path in (source_path, prior_path, retired_path)]
    guest_path, identity_path, pins_path = (capture.OUT / name for name in
                                         ('guest_memory_proof.json', 'native_identity.json', 'input_hashes_before.json'))
    guest, identity, before = [json.loads(path.read_text()) for path in (guest_path, identity_path, pins_path)]
    need(source['passed'] and source['sourceOnlyAccepted'] and prior['passed'] and retired['passed'] and
         prior['finiteNativeSonyaMileenaClearAccepted'] and prior['actualObservedNextStage']['frame'] == str(START) and
         guest['everyActualByteComparedInRAM'] and guest['bytes'] == 1048576 and
         guest['sha256'] == prior['wholeCurrentGuestSHA256'] and identity['ProcessId'] == 30832 and
         identity['ParentProcessId'] == 14408 and identity['createdUnix'] == 1791703089.4675903 and
         identity in census.census(), 'Same actual live child birth/path/parent/full command and independently reconstructed current guest')
    pins = dict(before)
    for proof in (source, prior, retired):
        need(not proof['fullPortAcceptance'], 'Whole original objective remains open')
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest), 'Every frozen executed prerequisite unchanged')
            pins[path] = digest
    lines = reader.complete_lines(capture.OUT / 'run.log.gz')
    need(not any(line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ', 'MK2_MILEENA_CAMPAIGN_OVERRUN ')) for line in lines),
         'No observed native cache corruption in the same complete stream')
    stages = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in lines if line.startswith('MK2_NAT_CAMPAIGN_STAGE ')]
    entered = [row for row in stages if row['stage'] == '11']
    live = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in lines if line.startswith('MK2_NAT_CAMPAIGN_LIVE ')]
    need(len(entered) == 1 and entered[0]['frame'] == str(START) and entered[0]['schedule'] == 'FFFA3000' and
         any(int(row['frame']) >= START+120 and row['stage'] == '11' and row['human'] == '18:18' and
             row['cpu'] == '8:8' for row in live), 'Actual native SubZero admission and later owned fields, never predicted progress')
    expected = prefix(reader.complete_lines(OLD / 'run.log.gz'))
    actual = prefix(lines)
    positive = compare(actual, expected)
    faults = []
    for tag in positive['completeAllObservedCategoryInventory']:
        key = 'MK2_NAT_CAMPAIGN_' + tag + ' '
        index = next(i for i, line in enumerate(actual) if line.startswith(key))
        need('writes=0' in actual[index], 'All recorded old and new native/physical categories are unassisted')
        for description, bad in [('changed original record', actual[:index] + [actual[index].replace('writes=0', 'writes=1', 1)] + actual[index+1:]),
                                  ('omitted original record', actual[:index] + actual[index+1:])]:
            try:
                compare(bad, expected)
            except ValueError as error:
                faults.append(dict(category=tag, fault=description, rejectedBy=str(error)))
            else:
                raise ValueError('Altered preceding campaign accepted')
    need(compare(actual, expected) == positive and identity in census.census(), 'Whole positive and same native handle survive all category faults')
    for path in (Path(__file__).resolve(), Path(reader.__file__), Path(capture.__file__), source_path, prior_path,
                 retired_path, guest_path, identity_path, pins_path):
        pins[str(path.resolve())] = sha(path)
    need(all(sha(path) == digest for path, digest in pins.items()), 'Every source/report still frozen after complete finite gate')
    report = dict(passed=True, finiteCurrentFirstElevenEarnedFightsByExactConservationAccepted=True,
                  actualLiveNativeIdentity=identity, accepted=positive, actualObservedSubZeroAdmission=entered[0],
                  allObservedCategoryFaultsRejected=faults, currentWholeGuestSHA256=guest['sha256'],
                  currentSubZeroClearAccepted=False, fullTowerAccepted=False, endingAccepted=False,
                  freshJoinAccepted=False, artworkAccepted=False, audioAccepted=False, fullPortAcceptance=False,
                  originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=source['originalRemainingWorkGroups'], inputHashes=pins,
                  growingCurrentLogNotPinnedAsTerminal=True, exactCompletedPrefixBoundBySHA256=True,
                  newBuilds=0, newNativeBoots=0, newROMCopies=0, newRawMedia=0, newZIPs=0, goalStatus='active')
    OUT.mkdir(); (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, originalNativePID=identity['ProcessId'], completedOpponents=11,
                          completeOriginalRows=len(actual), categoryFaultsRejected=len(faults), fullPortAcceptance=False)), flush=True)
    return report


if __name__ == '__main__':
    run()
