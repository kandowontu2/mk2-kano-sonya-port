"""Pin real original CPU kick continuations; preserve all earlier captures."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_cpu_roundhouse_recovery as pair
import verify_cpu_roundhouse_flow as flow
from verify_cpu_air_runtime import NAME, EXE, PAYLOAD, SOURCE, matched_launch
from verify_cpu_air_gate import digest
from test_cpu_roundhouse_recovery import KANO, STOCK

ROOT=pair.ROOT
OUT=ROOT/'audit_v418_cpu_roundhouse_recovery_checked_inputs'


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    prior=ROOT/'audit_v413_cpu_action_recovery_checked_inputs'
    old=json.loads((prior/'input_hashes_before.json').read_text())
    earlier=json.loads((ROOT/'audit_v409_human_air_height_checked_inputs/input_hashes_before.json').read_text())
    for filename,expected in {**earlier,**old}.items():
        flow.need(digest(filename)==expected,'Previous frozen input changed: '+filename)
    proof=pair.verify(KANO,'kano')
    flow.need(proof['passed'],'Actual current choke and first kick acceptance')
    _,log,original=matched_launch(KANO,'mk2ks_cpu_roundhouse_v2_probe.lua','run_cpu_roundhouse_v2_probe.ps1')
    kicks=[flow.verify(log,at,original,late_miss=late)for at,late in ((2128,False),(2172,False),(2260,True))]
    _,stock_log,stock_original=matched_launch(STOCK,'mk2ks_cpu_roundhouse_v2_probe.lua','run_cpu_roundhouse_v2_probe.ps1')
    control=flow.verify(stock_log,1767,stock_original,3,'STOCK_FIELD')
    selected=pair.rows_prefix(stock_log,'MK2_P1CPU_SELECT_RESULT ')
    cold=pair.rows_prefix(stock_log,'MK2_P1CPU_COLD_LIVE ')
    flow.need(len(selected)==len(cold)==1 and selected[0]['errors']==0 and selected[0]['checks']==39 and
              selected[0]['human_id']==cold[0]['human_id']==18 and cold[0]['cpu_id']==3 and
              cold[0]['stage']==0 and cold[0]['schedule']==0xfffa3480,'Real original Baraka/P2 Sonya cold control')
    failed=ROOT/'audit_v416_cpu_roundhouse_kano604'
    failed_log=(failed/'run.log').read_text(encoding='utf-8-sig')
    flow.need('No space left on device' in failed_log and not pair.verify_log(failed_log,'kano')['passed'] and
              not(failed/'result.json').exists(),'Incomplete disk-full trace must never be accepted')
    failed_before=json.loads((failed/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    for filename,expected in failed_before.items():
        path=Path(filename)
        if path.suffix in ('.lua','.ps1','.json'):
            flow.need(digest(failed/'input_sources'/path.name)==expected,'Failed capture frozen source preserved')
    suites=[('test_cpu_roundhouse_recovery.py',49),('test_cpu_action_recovery.py',49),
            ('test_human_air_height.py',28),('test_cpu_air_runtime.py',34)]
    runs=[]
    for name,count in suites:
        process=subprocess.run([sys.executable,'tools/'+name],cwd=ROOT,capture_output=True,text=True)
        flow.need(process.returncode==0 and re.search(r'Ran '+str(count)+' tests',process.stdout+process.stderr),
                  'Exact current suite: '+name+'\n'+process.stdout+process.stderr)
        runs.append(process)
    files={ROOT/'tools/audit_cpu_roundhouse_recovery.py',ROOT/'tools/verify_cpu_roundhouse_flow.py',
           ROOT/'tools/verify_cpu_roundhouse_recovery.py',ROOT/'tools/test_cpu_roundhouse_recovery.py',
           ROOT/'mk2ks_cpu_action_transition_v4_probe.lua',ROOT/'tools/run_cpu_action_transition_v4_probe.ps1',
           ROOT/'mk2ks_cpu_roundhouse_followup_probe.lua',ROOT/'tools/run_cpu_roundhouse_followup_probe.ps1',
           ROOT/'mk2ks_cpu_roundhouse_v2_probe.lua',ROOT/'tools/run_cpu_roundhouse_v2_probe.ps1',
           prior/'input_hashes_before.json',prior/'tests.log',prior/'result.json',
           ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe'}
    for name,count in suites:files.add(ROOT/'tools'/name)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).resolve().parent==(ROOT/'tools').resolve():files.add(Path(filename).resolve())
    for glob in ('audit_v414_cpu_action_*','audit_v415_cpu_roundhouse_*','audit_v416_cpu_roundhouse_*',
                 'audit_v417_cpu_roundhouse_*',NAME):
        for folder in ROOT.glob(glob):files.update(p for p in folder.rglob('*')if p.is_file())
    hashes={str(p):digest(p)for p in sorted(files)}
    (OUT/'input_sources').mkdir(parents=True)
    for p in files:
        if p.parent in (ROOT,ROOT/'tools')and p.suffix in ('.py','.lua','.ps1'):
            shutil.copy2(p,OUT/'input_sources'/p.name)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    (OUT/'tests.log').write_text('\n'.join(p.stdout+p.stderr for p in runs))
    result=dict(passed=True,candidate=NAME,executable_sha256=EXE,payload_sha256=PAYLOAD,source_sha256=SOURCE,
                game_code_changed=False,Kano_choke_and_first_original_kick=proof,three_Kano_kicks=kicks,
                original_stock_roundhouse=control,original_instruction_pins=flow.instructions(original),
                native_Kano_kick_pose_fields=sum(p['native_pose_fields']for p in kicks),
                new_tests=49,repeated_current_tests=111,total_current_passing_tests=160,
                checked_inputs=len(hashes),unchanged_v413_inputs=len(old),unchanged_v409_inputs=len(earlier),
                failed_disk_full_capture_preserved=True,
                compiler_cache_removed=dict(path=str(ROOT/'mame-mkp/build/mingw-gcc/obj/x64/Release/emu.h.gch'),
                    bytes=212885742,sha256='26FFD1E5A3DD96CFA89DE32ECABBE99C9DE1B23049CF676177B4E8CCDF0CD211',
                    regenerable=True,source_assets_executables_and_frozen_evidence_not_removed=True),
                legacy_expected_source_guard_rejection_not_relabelled_pass=True,
                next_required='Both CPU projectile follow-ups, wider native CPU/KO and complete current UI/ladder/tower/finisher/art/audio acceptance, then matched launcher/ZIP delivery',
                production_not_promoted=True,whole_character_integration_complete=False,
                scope='current_choke_and_declared_blocked_original_CPU_roundhouse_continuations_full_counter_pose_chip_cleanup_not_all_CPU_actions_hits_KO_pixels_audio_or_goal')
    for filename,expected in {**earlier,**old,**hashes}.items():
        flow.need(digest(filename)==expected,'Input changed during audit: '+filename)
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in
        ('Kano_choke_and_first_original_kick','three_Kano_kicks','original_stock_roundhouse')},indent=2))


if __name__=='__main__':run()
