"""Bounded current fix checkpoint with explicit historical/current evidence."""
import argparse
import json
import re
import sys
from pathlib import Path
import inspect_current_pit_raster_v680_v3 as inspection
from verify_native_candidate_v680 import ROOT,NAME,matched,matched_reference
from verify_native_pit_scene_v680_v1 import need,digest,rows

def report():
    evidence=ROOT/'audit_v682_pit_initial_verification'
    render_path=evidence/'verification_v3.json'
    rom_path=ROOT/'audit_v684_pit_guest_rom_integrity/verification.json'
    render=json.loads(render_path.read_text());rom=json.loads(rom_path.read_text())
    need(render['passed']and rom['passed']and render['candidate']==NAME,'Both focused native fix/whole-ROM proofs pass')
    inputs={**render['inputHashes'],**rom['inputHashes']}
    for path,sha in inputs.items():need(digest(path)==sha,'Verified input changed: '+path)
    ui=[]
    for name,(fighter,side,reference_name)in inspection.CASES.items():
        folder=ROOT/name;reference=ROOT/reference_name
        matched(folder,inputs);matched_reference(reference,inputs)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        proof=render['cases'][name]['native_state'];start=proof['pit_enter']
        files=[]
        # These are the exact recorder's snapshot triggers, not a convenient
        # filename union or nearest-image search. Match every pre-Pit case.
        for row in rows(log,'SELECT'):
            for age in (130,146):
                if int(row['frame'])+age<start:files.append(f"campaign_selection_{row['number']}_{age}.png")
        for row in rows(log,'FIGHT'):
            if int(row['frame'])<start:files.append(f"campaign_fight_selection{row['selection']}_stage{row['stage']}.png")
        for row in rows(log,'LOSS'):
            if int(row['frame'])<start:files.append(f"campaign_loss_{row['number']}.png")
        need(len(files)>=20 and len(files)==len(set(files)),'Complete unambiguous actual pre-Pit selection/fight/loss snapshot set')
        for file in files:
            a=folder/'snap'/file;b=reference/'snap'/file
            need(a.read_bytes()==b.read_bytes(),'Every recorded pre-Pit UI/fight/loss image unchanged: '+file)
            inputs[str(a)]=digest(a);inputs[str(b)]=digest(b)
        ui.append(dict(fighter=fighter,human_slot=side,snapshots=len(files),files=files,
                       scope='All saved input-only pre-Pit selected-avatar/first-fight/loss snapshots byte-identical to matched v635; not every cursor route/ladder or all arenas'))
    regression=evidence/'regression_initial.log'
    text=regression.read_text(encoding='utf-8-sig')
    need(re.search(r'Ran 41 tests in ',text)and re.search(r'^OK\s*$',text,re.M)and
         not re.search(r'FAILED|FAIL|ERROR|Traceback',text),'Forty-one actual current regression tests pass')
    launcher=evidence/'latest_launcher_verifyroms.log'
    need('1 romsets found, 1 were OK.'in launcher.read_text(encoding='utf-8-sig'),'Actual latest CMD resolves one valid ROM set')
    rootcmd=ROOT/'PLAY_LATEST_TEST_BUILD.cmd';candidatecmd=ROOT/NAME/'PLAY_TEST_BUILD.cmd'
    need(NAME+'\\PLAY_TEST_BUILD.cmd'in rootcmd.read_text(),'Latest CMD points to exact checked test candidate')
    command=candidatecmd.read_text()
    need(NAME+'\\mkport_candidate.exe'in command and NAME+'\\roms;roms'in command and
         '-nocheat'in command and all('set '+prefix in command for prefix in ('MK2KS_','MK2_TRACE_','MK2_RANGE_','MK2_P2_')),
         'Correct candidate-first ROM/isolated settings and diagnostic environment cleanup')
    extra=[render_path,rom_path,regression,launcher,rootcmd,candidatecmd,
           ROOT/'STATUS_2026-10-02_PIT_INITIAL_CACHE.md',ROOT/'tools/test_pit_initial_cache_v680.py',
           ROOT/'tools/build_native_candidate_v2.ps1',ROOT/NAME/'build.log']
    for path in extra:inputs[str(path)]=digest(path)
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(ROOT/'tools')and path.suffix=='.py':inputs[str(path)]=digest(path)
    for directory in ('audit_v680_pre_pit_initial_cache','audit_v682_pit_initial_verification','audit_v683_pit_native_audio_sonya_p2','audit_v684_pit_guest_rom_integrity'):
        for path in (ROOT/directory).rglob('*'):
            if path.is_file():inputs[str(path)]=digest(path)
    # Explicitly include rejected recorder/checker sources and logs, without
    # treating their partial runs, missing samples or errors as passes.
    for name in ('audit_v675_current_pit_raster_kano_p1','audit_v675_current_pit_raster_sonya_p2',
                 'audit_v676_current_pit_raster_kano_p1','audit_v676_current_pit_raster_sonya_p2',
                 'audit_v677_current_pit_raster_kano_p1','audit_v677_current_pit_raster_sonya_p2',
                 'audit_v679_current_pit_render_audio_checked_inputs'):
        directory=ROOT/name
        for path in directory.iterdir():
            if path.is_file()and path.suffix in ('.log','.json'):inputs[str(path)]=digest(path)
        if(directory/'input_sources').is_dir():
            for path in (directory/'input_sources').iterdir():
                if path.is_file():inputs[str(path)]=digest(path)
    for name in ('mk2ks_natural_pit_raster_v635_v1.lua','mk2ks_natural_pit_raster_v635_v2.lua','mk2ks_natural_pit_raster_v635_v3.lua',
                 'tools/inspect_current_pit_raster_v635_v1.py','tools/inspect_current_pit_raster_v680_v1.py',
                 'tools/inspect_current_pit_raster_v680_v2.py','tools/inspect_natural_pit_saved_passes_v680_v1.py'):
        path=ROOT/name;inputs[str(path)]=digest(path)
    return dict(passed=True,candidate=NAME,native_initial_cache_fix_verified=True,
                actual_native_preloads=sum(len(c['native_state']['episodes'])for c in render['cases'].values()),
                first_scene_display_fields=662,independently_replayed_fields=658,byte_exact_preserved_native_flash_fields=4,
                body_draws=sum(c['body']['body_draws']for c in render['cases'].values()),
                synchronized_native_stereo_frames=sum(c['audio']['stereo_frames']for c in render['cases'].values()),
                guest_ROM_changed_bytes=rom['changed_bytes'],regression_tests=41,pre_Pit_ui_preservation=ui,
                evidence_reports=[str(render_path),str(rom_path)],inputHashes=inputs,fullPortAcceptance=False,
                scope='Native first-Pit pose/cache fix, current captured scenes and exact limited preservation; individual finishers/all cinematics/full towers/bosses/endings/art/audio/broad regression/release still required')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    need(not args.output.exists(),'Never overwrite evidence');proof=report()
    args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({k:v for k,v in proof.items()if k not in ('inputHashes','pre_Pit_ui_preservation')},indent=2))
