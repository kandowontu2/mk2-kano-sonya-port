"""Freeze a bounded native memory repair and explicitly retain fidelity gaps."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Preserve existing checkpoint')
    accepted=ROOT/'audit_v865_reptile_native_overrun_checked/verification.json'
    units=ROOT/'audit_v866_reptile_native_overrun_units/result.json'
    proof=json.loads(accepted.read_text());tests=json.loads(units.read_text())
    if not(proof['passed']and proof['native_table_overrun_repair_proven']and
           not proof['full_native_reptile_art_acceptance']and not proof['full_port_acceptance']and
           tests['passed']and tests['methods']==13):raise ValueError('Exact bounded repair and unit gate required')
    candidate=ROOT/'diagnostic_v860_native_reptile_victims'
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    for name,sha in build['input_hashes'].items():
        if digest(Path(name))!=sha:raise ValueError('Current build input changed: '+name)
    paths=[accepted,units,candidate/'build-info.json',candidate/'mkport_candidate.exe',
           candidate/'roms/mk2ks/mk2ks.mdata',ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',
           ROOT/'mame-mkp/mkport.exe',ROOT/'PLAY_CURRENT_V786_TEST_BUILD.cmd',
           ROOT/'PLAY_LATEST_TEST_BUILD.cmd',ROOT/'PLAY_MK2_KANO_SONYA.cmd',Path(__file__),
           ROOT/'tools/verify_reptile_campaign_v865.py',ROOT/'tools/test_reptile_campaign_v866.py',
           ROOT/'tools/verify_reptile_campaign_v862.py',ROOT/'tools/inspect_detached_heads_v863.py',
           ROOT/'tools/build_native_candidate_v2.ps1',ROOT/'STATUS_2026-10-02_REPTILE_NATIVE_OVERRUN.md']
    for name in ('audit_v858_sonya_p2_cache_failure','audit_v859_pre_reptile_victim_fix',
                 'audit_v861_sonya_p2_reptile_replay','audit_v862_reptile_first_observer_checked',
                 'audit_v863_original_detached_head_candidates','audit_v864_sonya_p2_reptile_replay',
                 'audit_v865_reptile_native_overrun_checked','audit_v866_reptile_native_overrun_units'):
        paths.extend(p for p in(ROOT/name).rglob('*')if p.is_file())
    paths.extend(Path(name)for name in proof['inputHashes'])
    paths=list(dict.fromkeys(paths));pinned={str(p):digest(p)for p in paths}
    if (digest(candidate/'mkport_candidate.exe')!=build['executable_sha256']or
        digest(candidate/'roms/mk2ks/mk2ks.mdata')!=build['payload_sha256']):
        raise ValueError('Candidate executable/payload changed')
    if digest(ROOT/'mame-mkp/mkport.exe')!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':
        raise ValueError('Installed build was not restored')
    report={'passed':True,'candidate':candidate.name,'nativeReptileTableOverrunRepairAcceptance':True,
            'actualSonyaP2ReplayAcceptance':True,'actualKanoReptileFatalityAcceptance':False,
            'nativeReptileFinisherArtAcceptance':False,'fullPortAcceptance':False,
            'unassistedTowerClearAcceptance':False,'productionAndLaunchersUnchanged':True,
            'guestChangedBytes':123,'samePreFaultNativeRecords':37537,'postFaultSonyaFights':8,
            'nativeHealthStores':13659,'nativeFinisherSnapshots':16,'unitMethods':13,
            'failedObserverGatePreserved':'audit_v862_reptile_first_observer_checked',
            'priorCheckpointNotUpgradedToNewBuild':'audit_v847_current_cpu_campaign_launcher_checkpoint',
            'remaining':['Correct detached-head and headless victim art/palettes for both fighters',
                         'Reptile fatality victims in both physical slots, including Kano runtime proof',
                         'Complete native towers/bosses/endings and remaining whole-port regression',
                         'Final release launcher/ZIP after full acceptance'],
            'pinCount':len(pinned),'inputHashes':pinned}
    args.output.mkdir();(args.output/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))

if __name__=='__main__':main()
