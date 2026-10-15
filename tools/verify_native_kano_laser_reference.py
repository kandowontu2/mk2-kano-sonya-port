"""Check the actual ordinary-input original laser reference, not the port.

Accepts whole native rasters in RAM. No game launch or guest mutation here.
The immutable run receipt remains transport-only; this is a separate finite
original-action receipt, explicitly not second-finisher implementation.
"""
import copy
import gzip
import hashlib
import json
import re
from pathlib import Path
import capture_native_secondary_kano_reference as transport
import audit_native_secondary_finisher_reference as reference

ROOT = reference.ROOT
RUN = ROOT/'audit_native_secondary_kano_source_distance'
OUT = ROOT/'audit_native_kano_laser_reference_checked'


def need(value, message):
    if not value:
        raise ValueError(message)


def rows(text):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line), tag=line.split()[0])
            for line in text.splitlines() if line.startswith('MK3_SECONDARY_')]


def inspect(data, images):
    def tagged(name):
        return [r for r in data if r['tag'] == 'MK3_SECONDARY_'+name]
    all_observations = [r for r in data if r['tag'] not in
                        ('MK3_SECONDARY_GUEST_DIGEST', 'MK3_SECONDARY_RGB_DIGEST')]
    need(all(r.get('writes') == '0' and r.get('assistance') == 'none' for r in all_observations),
         'Actual passive controller explicitly reports no guest assistance throughout')
    need(len(tagged('GUEST_DIGEST')) == 1 and tagged('GUEST_DIGEST')[0]['sha256'] ==
         '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
         'Full actually initialized original guest conserved')
    selected = tagged('SELECTED')
    need(len(selected) == 1 and selected[0]['frame'] == '3800' and selected[0]['ids'] == '0,1',
         'Genuine original physical-player Kano and Sonya selection')
    zero = tagged('ROUND_ZERO')
    need([int(r['frame']) for r in zero] == [4296, 5166] and
         all(r['hp'] == '166,0' and r['ids'] == '0,1' for r in zero),
         'Both actually physically earned native rounds, no health staging')
    health = tagged('HEALTH')
    need(all(r['pc'] in ('FF9503C0', 'FF9503F0', 'FFA5D5A0', 'FFA96760',
                        'FFA96790', 'FFA969F0', 'FFA96A90') for r in health),
         'Actual native health store PCs only')
    losses = [r for r in health if r['at'] == '010615F0' and
              int(r['after']) < int(r['before']) <= 166 and int(r['frame']) <= 5166]
    need(len([r for r in losses if r['after'] == '0']) == 2 and
         all(r['pc'] == 'FFA5D5A0' for r in losses),
         'Actual combat damage routine earned both knockouts')
    spacing, entry = tagged('COMMAND_SPACING'), tagged('OWN_ENTRY')
    need(len(spacing) == len(entry) == 1 and spacing[0]['frame'] == '5253' and
         spacing[0]['finish'] == '3' and spacing[0]['ids'] == '0,1' and
         spacing[0]['x'] == '753,898', 'Actual physical retreat reached145pixel command gap')
    need(entry[0]['frame'] == '5295' and entry[0]['ids'] == '0,1' and
         entry[0]['hp'] == '166,0' and entry[0]['finish'] == '3' and
         entry[0]['x'] == '748,898' and entry[0]['pc'] == 'FF9B5CE0',
         'Actual first original Kano action entered at150pixel gate distance')
    command = [r for r in tagged('INPUT') if 5253 <= int(r['frame']) <= 5296]
    expected = [(str(frame), name) for name, first in
                [('lp', 5263), ('block', 5273), ('block', 5283), ('hk', 5293)]
                for frame in range(first, min(first+4, 5296))]
    need([(r['frame'], r['field']) for r in command] == expected,
         'Actual chronological LP/Block/Block/HK physical fields, no injected guard/history')
    code = tagged('CODE')
    chain = ['FF991F70', 'FF992EE0', 'FF993160', 'FF9931F0', 'FF993760',
             'FF992090', 'FF998750', 'FF9B5CD0']
    at_entry = [r for r in code if r['frame'] == '5295']
    need([r['at'] for r in at_entry if r['at'] in chain] == chain and
         all(r['pc'] == f'{int(r["at"],16)+16:08X}' for r in code),
         'Actual instruction fetch chain validates history, range, native finish gate and first performer')
    need(any(r['at'] == 'FFA5EF10' and r['a9'] == '00000003' for r in code),
         'Actual performer used owned original special3 animation')
    need(any(r['at'] == 'FF9B62C0' and r['a8'] == '010394B0' for r in code),
         'Actual independent victim process entered original laser reaction')
    fields = tagged('FIELD')
    need(len(fields) == 451 and [int(r['age']) for r in fields] == list(range(1,452)),
         'All451 actual consecutive action-to-win fields, not sampled stability')
    need(all(int(r['frame']) == 5295+int(r['age']) and r['ids'] == '0,1' and
             r['hp'] == '166,0' and r['own'] == '010396C0' and r['victim'] == '010394B0'
             for r in fields), 'Actual players, HP and actor allocation remain genuine through native win')
    need(all(r['finish'] in ('3', '1') for r in fields) and
         fields[-1]['finish'] == '1', 'Original native finish-to-win transition, not a frozen finish flag')
    phase = {int(r['age']): r for r in fields}
    expected_poses = {21:'FF831520',49:'FF831580',53:'FF8315E0',
                      189:'FF831580',193:'FF831520',197:'FF82E3A0',233:'FF82E800'}
    need(all(phase[age]['poses'].split(',')[0] == pose for age, pose in expected_poses.items()),
         'Actual original laser performer choreography and its own win animation')
    need(phase[69]['poses'].split(',')[1] == 'FF83ED00' and
         all(r['poses'].split(',')[1] == 'FF83ED00' for r in fields[68:]),
         'Actual Sonya native main64 reaction starts69 and persists through win')
    objects = [r for r in tagged('OBJECT') if r['actor'] == '01032970']
    need(len(objects) == 30 and objects[0]['age'] == '33' and objects[-1]['age'] == '183' and
         all(r['x'] == '748' and r['y'] == '102' for r in objects),
         'Distinct observed native laser object, not either fighter actor')
    groups = {f'{int(r["group"],16):08X}' for r in json.loads(
        (ROOT/'audit_native_secondary_finisher_reference/report.json').read_text())['originalUnusedAssets'][0]['references']}
    need(all(r['pose'] in groups for r in objects),
         'All observed laser-object groups belong to the already imported original special3')
    digests = tagged('RGB_DIGEST')
    need(len(digests) == len(images) == 15, 'All15 whole actual native frames supplied in RAM')
    for actual, image in zip(digests, images):
        header = image['header']
        need(actual['stage'] == header['stage'] and actual['frame'] == header['frame'] and
             header['width'] == '400' and header['height'] == '254' and
             len(image['pixels']) == 406400 and actual['sha256'] == header['sha256'] ==
             hashlib.sha256(image['pixels']).hexdigest().upper(),
             'Whole native RGB buffer, declared dimensions and frozen digest match')
    stop = tagged('STOP')
    need(len(stop) == 1 and stop[0]['frame'] == '5746' and stop[0]['own_action_observed'] == '1' and
         stop[0]['zeros'] == '2', 'Original same controller planned exit after complete recorded action')
    return dict(twoPhysicallyEarnedRounds=True, commandGap=145, entryGap=150,
                entryFrame=5295, consecutiveNativeFields=451,
                nativeWinFirstAge=min(int(r['age']) for r in fields if r['finish'] == '1'),
                observedLaserObjectChanges=len(objects), ownSpecialAnimationIndex=3,
                actualNativeFramesReviewed=15, originalActionObserved=True)


def main(capture):
    need(not OUT.exists() and not transport.census() and not reference.native.census(),
         'Fresh finite original receipt; no native games live')
    record = json.loads((RUN/'report.json').read_text())
    need(record['passed'] and record['nativeExit'] == 0 and record['originalWholeGuestMatched'] and
         record['actualWindowsIdentity']['ProcessId'] == 123164 and
         record['actualWindowsIdentity']['ParentProcessId'] == 178652 and
         record['actualWindowsIdentity']['createdUnix'] == 1791615650.8108082 and
         all(reference.sha(p) == h for p,h in record['inputHashes'].items()),
         'Actually executed original native PID/parent/creation, normal exit and frozen whole provenance')
    with gzip.open(RUN/'run.log.gz','rt') as stream:
        text = stream.read()
    need(text == capture['text'], 'RAM capture corresponds to the exact frozen original trace')
    data = rows(text)
    accepted = inspect(data, capture['rgbFrames'])
    faults = []
    mutations = [
        ('selection_identity','SELECTED',0,'ids','0,0'),
        ('earned_round_health','ROUND_ZERO',1,'hp','166,1'),
        ('command_distance','COMMAND_SPACING',0,'x','835,901'),
        ('performer_entry','OWN_ENTRY',0,'pc','FF9B12F0'),
        ('physical_command','INPUT',next(i for i,r in enumerate([x for x in data if x['tag']=='MK3_SECONDARY_INPUT']) if r['frame']=='5263'),'field','hk'),
        ('continuous_field_frame','FIELD',200,'frame','5500'),
        ('continuous_actor_identity','FIELD',200,'ids','0,0'),
        ('continuous_actor_pointer','FIELD',200,'own','010394B0'),
        ('continuous_health','FIELD',200,'hp','166,1'),
        ('native_pose','FIELD',52,'poses','FF831520,FF83B8C0'),
        ('victim_pose','FIELD',119,'poses','FF8315E0,FF83B800'),
        ('independent_laser_geometry','OBJECT',0,'x','898'),
        ('planned_stop','STOP',0,'own_action_observed','0'),
    ]
    for name, tag, index, key, value in mutations:
        wrong = copy.deepcopy(data)
        target = [r for r in wrong if r['tag']=='MK3_SECONDARY_'+tag][index]
        target[key] = value
        try:
            inspect(wrong, capture['rgbFrames'])
        except ValueError as error:
            faults.append(dict(name=name, rejected=str(error)))
        else:
            raise ValueError('Original runtime fault admitted: '+name)
    damaged = copy.deepcopy(capture['rgbFrames'])
    damaged[10]['pixels'] = bytes([damaged[10]['pixels'][0]^1])+damaged[10]['pixels'][1:]
    try:
        inspect(data, damaged)
    except ValueError as error:
        faults.append(dict(name='actual_native_raster_byte', rejected=str(error)))
    else:
        raise ValueError('Whole original raster fault admitted')
    scope = json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text(encoding='utf-8-sig'))
    paths = [Path(__file__), RUN/'report.json', RUN/'run.log.gz', RUN/'process.json',
             ROOT/'audit_native_kano_secondary_input/report.json',
             ROOT/'audit_native_secondary_finisher_reference/report.json',
             ROOT/'tools/review_native_current_attract_ram.py',
             ROOT/'audit_native_kano_laser_checker_failure/report.json',
             ROOT/'audit_native_kano_laser_checker_failure/failed_executed_checker_source.json.gz',
             ROOT/'audit_native_kano_laser_checker_failure_2/report.json',
             ROOT/'audit_native_kano_laser_checker_failure_2/failed_executed_sources.json.gz']
    pins = {str(p.resolve()): reference.sha(p) for p in paths}
    report = dict(passed=True, originalFiniteActionReferenceAccepted=True,
                  portSecondFatalityImplemented=False, fullAudioAccepted=False,
                  fullPortAcceptance=False, accepted=accepted,
                  actualWindowsIdentity=record['actualWindowsIdentity'], nativeExit=0,
                  actualNativeFrameHeaders=[r['header'] for r in capture['rgbFrames']],
                  actualFrameReview=dict(pages=3, all15WholeFramesActuallyViewed=True,
                      observations=['Actual original Kano and Sonya bodies selected and fought.',
                                    'At source-correct distance, native Kano eye laser stretches to Sonya.',
                                    'Victim reddens, skeleton/body breaks apart, Kano returns to his own win pose.',
                                    'This is the original MK3 reference, not an MKII port preview.']),
                  faultRejections=faults, inputHashes=pins,
                  originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                  limitations=['Finite Kano0 versus Sonya1 reference in original MK3 only.',
                               'Palette values were captured on pose changes, not every palette update.',
                               'Sound packet trace exists, but no complete PCM/audio acceptance.',
                               'Native win handoff observed; following rematch/ladder cleanup not exercised.',
                               'Other victim identities and the MKII implementation remain unproved.'],
                  newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
                  gameSourceChanged=False,latestPlayableChanged=False,goalStatus='active',
                  nextAction='Port the genuinely distinct owned eye-laser performer, victim main64/red-palette/bone effects and native win cleanup; map Sonya original second input/effect separately.')
    need(len(report['originalNaturalIntegrationRequirements'])==14 and
         len(report['originalRemainingWorkGroups'])==6, 'Full original14+6 scope retained')
    need(all(reference.sha(p)==h for p,h in pins.items()), 'Actual executed checker dependencies frozen')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(OUT/'executed_checker_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump({str(Path(__file__).resolve()):dict(sha256=reference.sha(__file__),text=Path(__file__).read_text())},stream)
    print(json.dumps(dict(passed=True, originalReference=accepted, rejectedFaults=len(faults),
                          portSecondFatalityImplemented=False)))
    return report
