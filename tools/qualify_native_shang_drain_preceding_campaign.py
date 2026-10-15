"""Prove all thirteen earned preceding fights on the SAME repair replay.

Full original native/physical chronology, not a selected subset. This is only
a regression gate; Shang, endings, artwork, audio and whole-port remain open.
No launch, replay, gameplay mutation or raw media writes.
"""
import json
import re
from pathlib import Path

import capture_native_shang_owned_drain_campaign as capture
import qualify_native_shang_cause_preceding_campaign as original
import native_process_census_v6647 as census

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT / 'audit_native_shang_drain_preceding_campaign_checked'
START = original.START
OLD = ROOT / 'audit_native_sonya_shang_cache_cause'


def actual_state(identity):
    if identity in census.census():
        return dict(live=True, originalIdentityRevalidated=True)
    terminal_path = capture.OUT / 'native_terminal.json'
    need(terminal_path.exists(), 'Missing live identity is not permission to replay; need original actual wait receipt')
    terminal = json.loads(terminal_path.read_text())
    need(terminal['identity'] == identity and terminal['nativeExit'] == 0 and not census.census(),
         'Exact original native wait terminal; no replacement game')
    return dict(live=False, originalIdentityRevalidated=False, originalNativeWaitTerminal=terminal)


def run():
    need(not OUT.exists(), 'Fresh finite full preceding-campaign proof')
    paths = [capture.SOURCE/'report.json', ROOT/'audit_native_shang_cause_preceding_campaign_checked/report.json',
             ROOT/'audit_native_shang_drain_startup_successor/report.json',
             capture.OUT/'guest_memory_proof.json', capture.OUT/'initialized_windows_proof.json',
             capture.OUT/'native_identity.json', capture.OUT/'input_hashes_before.json']
    source, prior, startup, guest, windows, identity, before = [json.loads(p.read_text()) for p in paths]
    need(source['passed'] and source['unchangedWholeOriginalPhysicalInputs'] and
         source['allThirteenEarlierOpponentsRetained'] and prior['passed'] and
         startup['passed'] and startup['actualNativeInitializedWindowsAccepted'] and
         not startup['nativeGameplayRepairAccepted'] and guest['everyActualByteComparedInRAM'] and
         guest['bytes']==0x100000 and guest['sha256']==startup['actualWindowHashes']['high'] and
         windows['passed'] and windows['actualWindowHashes']==startup['actualWindowHashes'] and
         windows['actualWindowBytes']==dict(high=0x100000,owned=0x200000,graphics=65536) and
         identity['ProcessId']==31336 and identity['ParentProcessId']==30848 and
         identity['createdUnix']==1791721342.2271461,
         'Exact actual repair/cold game identity and all three independent initialized windows')
    before_state = actual_state(identity)
    pins = dict(before)
    for proof in (source, prior, startup):
        need(not proof['fullPortAcceptance'], 'Original whole-port scope remains open')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h), 'All frozen transitive inputs unchanged: '+p)
            pins[p]=h
    lines = original.original.reader.complete_lines(capture.OUT/'run.log.gz')
    parsed=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines
                       if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    entered=[q for q in parsed('STAGE') if q['stage']=='14']
    need(len(entered)==1 and entered[0]['frame']==str(START) and entered[0]['schedule']=='FFFA3000' and
         any(int(q['frame'])>=START+120 and q['stage']=='14' and q['human']=='18:18' and q['cpu']=='6:6'
             for q in parsed('LIVE')), 'Actually reached Shang after all preceding fights; no predicted admission')
    for line in lines:
        if line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')):
            fields=dict(re.findall(r'(\w+)=([^\s]+)',line))
            need(int(fields.get('frame',fields.get('observer_callback','-1')))>=START,
                 'No earlier corruption; later failures never hidden or relabeled')
    prefix, compare = original.validators()
    expected = prefix(original.original.reader.complete_lines(OLD/'run.log.gz'))
    need(len(expected)==1009959 and capture.corrected.digest(''.join(expected).encode())==
         prior['accepted']['prefixSHA256']=='0D4D38BFC644335304C62DF41265AF0014F779C4BED037ACE8ACD0D7BCDAD5E5',
         'Complete independently accepted actual original thirteen-fight oracle')
    actual = prefix(lines)
    positive = compare(actual, expected)
    need(positive==prior['accepted'] and positive['completedOpponents']==13 and
         len(positive['completeAllObservedCategoryInventory'])==28,
         'Every original row/category/native win and paid loss identical across actual repair')
    faults=[]
    for tag in positive['completeAllObservedCategoryInventory']:
        key='MK2_NAT_CAMPAIGN_'+tag+' '
        i=next(i for i,line in enumerate(actual) if line.startswith(key))
        need('writes=0' in actual[i], 'Actual category unassisted')
        for label,bad in [('changed row',actual[:i]+[actual[i].replace('writes=0','writes=1',1)]+actual[i+1:]),
                          ('omitted row',actual[:i]+actual[i+1:])]:
            try:compare(bad,expected)
            except ValueError as error:faults.append(dict(category=tag,fault=label,rejectedBy=str(error)))
            else:raise ValueError('Altered actual chronology accepted')
    need(len(faults)==56 and compare(actual,expected)==positive, 'All category changes/omissions rejected')
    after_state=actual_state(identity)
    for p in (Path(__file__).resolve(),Path(capture.__file__),Path(original.__file__),
              Path(original.original.__file__),Path(original.original.reader.__file__),
              *paths,OLD/'run.log.gz'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'All immutable actual sources/reports unchanged')
    report=dict(passed=True,finiteFirstThirteenEarnedFightsOnRepairByExactConservationAccepted=True,
        actualOriginalNativeIdentity=identity,originalNativeStateBefore=before_state,originalNativeStateAfter=after_state,
        accepted=positive,actualObservedShangAdmission=entered[0],allObservedCategoryFaultsRejected=faults,
        actualInitializedWindowHashes=windows['actualWindowHashes'],inputHashes=pins,
        growingCurrentLogNotPinnedAsTerminal=True,exactCompletedPrefixBoundBySHA256=True,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
        laterFailureNotRelabeledAsSuccess=True,shangClearAccepted=False,fullTowerAccepted=False,
        endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,originalNativePID=identity['ProcessId'],completedOpponents=13,
                         completeOriginalRows=len(actual),categoryFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':
    run()
