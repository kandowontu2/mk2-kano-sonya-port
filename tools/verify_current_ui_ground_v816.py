"""Current both-slot selection/ladder/name and bounded Dead Pool grounding/shadows.

Complete fixed captured raster passes, native compressed-row copies and true-ID
UI flow. Not all arenas/moves/finisher phases, full towers/endings or release.
"""
import argparse
import json
from pathlib import Path
import re
import inspect_current_ground_shadow_v811 as ground
import inspect_native_idle_feet_v635_v2 as baseline_model
from verify_native_idle_feet_v635 import check_presentation
import verify_native_ui_flow_v814 as ui
import verify_native_candidate_v798 as candidate

need=candidate.need

def check_ground(value,fighter,side):
    check_presentation(value,fighter,side)
    need(value['native_shadow_row_stream_verified'] and value['native_shadow_components']>=900
         and value['native_shadow_copies']>20000,'Full actual native compressed shadow cadence')
    need(all(r['owned_shadow_mismatches']==0 and r['native_shadow_pen_black']
             and r['owned_shadow_pixels'][side]>100 for r in value['records']),
         'Visible original black-pen owned shadows in every retained mobility raster')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();root,output=args.root.resolve(),args.output.resolve()
    need(not output.exists(),'Do not overwrite proof')
    tracked,ground_reports,ui_reports={},{},{}
    def track(path,wanted=None):
        path=Path(path);actual=candidate.digest(path)
        need(wanted is None or actual==wanted,'Changed executed/proof input: '+str(path))
        tracked[str(path.resolve())]=actual
    track(Path(__file__))
    for module in (ground,baseline_model,ui,candidate):track(Path(module.__file__))
    # Pin transitive original pixel decoder, latch, grounding and UI consumers.
    for name in ('inspect_ground_presentation.py','inspect_natural_arena_floor_v602.py',
                 'verify_native_floor_display_v602.py','verify_native_idle_feet_v635.py',
                 'verify_cpu_air_gate.py','verify_cpu_air_runtime.py','verify_p2_campaign.py'):
        track(root/'tools'/name)
    track(root/'mk2/mk2-maincpu.bin',ui.ORIGINAL_SHA)
    track(root/'roms/mk2ks/mk2ks.ui',ui.UI_SHA)
    build_path=root/candidate.NAME/'build-info.json';track(build_path)
    build=json.loads(build_path.read_text())
    need(build['executable_sha256']==candidate.EXE and build['payload_sha256']==candidate.PAYLOAD,'Current matched candidate')
    def launch(folder,fighter,side,observer,runner):
        metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        need(metadata['exit_code']==0 and metadata['candidate']==candidate.NAME
             and metadata['executable_sha256']==candidate.EXE and metadata['payload_sha256']==candidate.PAYLOAD
             and metadata['fighter']==fighter and metadata['side']==side and metadata['assistance']=='none'
             and before==metadata['input_hashes'],'Exact terminal cold launch')
        need(all(before.get(path)==value for path,value in build['input_hashes'].items()),'All executed build inputs pinned')
        for path,value in before.items():
            track(path,value)
            if Path(path).suffix in ('.lua','.ps1','.json'):track(folder/'input_sources'/Path(path).name,value)
        source=(folder/'input_sources'/observer).read_text()
        need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',source),'Observer cannot write gameplay state')
        run=(folder/'input_sources'/runner).read_text()
        need('-nocheat' in run,'Cheat-disabled launch')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback|INVALID',log,re.I),'No runtime or ownership error')
        for path in folder.rglob('*'):
            if path.is_file():track(path)
        return log
    for fighter in ('kano','sonya'):
        for side in (1,2):
            name=f'{fighter}_p{side}'
            folder=root/f'audit_v815_ground_shadow_{name}'
            log=launch(folder,fighter,side,'mk2ks_ground_shadow_v815_probe.lua','run_ground_shadow_v815_probe.ps1')
            terminal=ground.rows(log,'RESULT')
            need(len(terminal)==1 and terminal[0]['terminalAge']==480,'Complete mobility observation')
            fields=ground.rows(log,'FIELD')
            need(len(fields)==962 and [(r['age'],r['slot'])for r in fields]==[(age,slot)for age in range(481)for slot in (1,2)],'Every owned physical mobility field')
            anchors={17:134,18:135,4:133}
            for r in fields:
                identity=(17 if fighter=='kano'else 18)if r['slot']==side else 4
                need(r['id']==r['roster']==identity and r['owner']==r['actor'] and r['state']==1
                     and r['hp']==161 and r['floor']==r['stageY']-anchors[identity],'Native IDs/owner/full health/physical floor')
            value=ground.inspect(folder);check_ground(value,fighter,side)
            reference=root/f'audit_v810_ground_{name}'
            reference_log=launch(reference,fighter,side,'mk2ks_ground_presentation_v9_probe.lua','run_ground_presentation_v9_probe.ps1')
            tags=('INPUT','FIELD','PART','OWNER','SNAP','RESULT')
            timeline=lambda text:[line for line in text.splitlines()if any(line.startswith('MK2_GROUND_'+tag+' ')for tag in tags)]
            need(timeline(log)==timeline(reference_log),'Expanded shadow observation altered native movement/state chronology')
            baseline=baseline_model.inspect(reference);check_presentation(baseline,fighter,side)
            for snap in ground.rows(log,'SNAP'):
                need((folder/'snap'/snap['file']).read_bytes()==(reference/'snap'/snap['file']).read_bytes(),
                     'Read-only shadow observer changed captured pixels')
            ground_reports[name]=value
            ui_folder=root/f'audit_v813_ui_{name}'
            ui_log=launch(ui_folder,fighter,side,'mk2ks_native_ui_flow_v2_probe.lua','run_native_ui_flow_v813.ps1')
            ui_reports[name]={**ui.verify_log(ui_log,fighter,side),'rendered':ui.render(ui_folder,ui_log,fighter,side)}
    # Failed v812 capture is retained explicitly, not accepted or substituted.
    failed={}
    for fighter in ('kano','sonya'):
        for side in (1,2):
            folder=root/f'audit_v812_ground_shadow_{fighter}_p{side}'
            for path in (folder/'run.log',folder/'result.json',folder/'input_sources/mk2ks_ground_shadow_v812_probe.lua'):track(path)
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            dm=[r for r in ground.rows(log,'DMA')if 0x10000000<=r['source']<0x1a000000 and r['command']&15==8]
            comp=ground.rows(log,'SHADOW_COMPONENT')
            need(len(comp)<len(dm),'Failed observer history no longer incomplete')
            failed[f'{fighter}_p{side}']={'actual_shadow_copies':len(dm),'recorded_cache_rows':len(comp),'accepted':False}
    output.mkdir()
    report={'passed':True,'candidate':candidate.NAME,'ground_cases':ground_reports,'ui_cases':ui_reports,
        'sampled_ground_frames':sum(r['samples']for r in ground_reports.values()),
        'native_owned_shadow_copies':sum(r['native_shadow_copies']for r in ground_reports.values()),
        'boundedCurrentGroundShadowAcceptance':True,'boundedCurrentUiFlowAcceptance':True,
        'allArenaFloorAcceptance':False,'fullPortAcceptance':False,'checked_inputs':tracked,'failed_v812_preserved':failed,
        'scope':__doc__}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ('sampled_ground_frames','native_owned_shadow_copies','boundedCurrentGroundShadowAcceptance','boundedCurrentUiFlowAcceptance','fullPortAcceptance')}))
if __name__=='__main__':main()
