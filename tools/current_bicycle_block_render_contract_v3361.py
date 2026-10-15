"""Whole original native renderer, explicit blocked proof/physical-role routing."""
import inspect
from types import SimpleNamespace
import verify_native_cpu_bicycle_round_render_v3130 as original
import verify_current_bicycle_block_display_state_v3359 as state
import native_cpu_bicycle_hit_contract_v3317 as poses

need=state.need

def verify(side):
    need(side in (1,2),'Actual physical attacking human slot')
    source=inspect.getsource(original.verify)
    substitutions=[
        ("name,build,player=CASES[key];CASE=ROOT/name;victim_id=state.original.HUMANS[player]",
         "name,build,player=CASES[key];CASE=ROOT/name;victim_id=17;side=int(key[-1])"),
        ("assert proof['passed']and proof['actualCandidateBicycleMissAccepted']",
         "assert proof['passed']and proof['actualBothPhysicalSlotsBlockedChipAndRecoveryAccepted']"),
        ("assert meta['player']==player", "assert meta['victim']=='kano' and meta['side']==side"),
        ("assert typed==proof['cases'][key]['phase']",
         "assert typed['actualPhase']=={k:v for k,v in proof['cases'][side-1].items()if k!='case'}"),
        ("assert pair['damage']==0 and not pair['allCPUAccepted']",
         "assert pair['damage']==3 and not pair['allCPUAccepted']"),
        ("CASE/'input_sources/mk2ks_native_cpu_bicycle_display_v3105.lua'",
         "CASE/'input_sources/tree/mk2ks_human_bicycle_block_display_v3356.lua'"),
        ("assert \"dofile('mk2ks_physical_p2_cpu_square_trace_v3104.lua')\"in observer",
         "assert \"dofile('mk2ks_human_bicycle_block_trace_v3345.lua')\"in observer"),
        ("ids=(victim_id,18);anchors={17:134,18:135}",
         "ids=(18,victim_id)if side==1 else(victim_id,18);anchors={17:134,18:135}"),
        ("and r[f'state{s}']==(1 if s==1 else 0)","and r[f'state{s}']==1"),
        ("bicycle.POSES<=held[2]", "bicycle.POSES<=held[side]"),
        ("bicycle.POSES<=visible[2]", "bicycle.POSES<=visible[side]"),
        ("{(1,victim_id),(2,18)}", "{(1,ids[0]),(2,ids[1])}"),
    ]
    for before,after in substitutions:
        need(source.count(before)==1,'Exactly one declared blocked proof/physical routing change: '+before)
        source=source.replace(before,after)
    begin=source.index('    required={');end=source.index('    image=bytearray',begin)
    before=source[begin:end]
    need(before.endswith("    assert required<={Path(p).name for p in meta['input_hashes']}\n"),
         'Only original fixture-specific metadata requirement block adapts')
    source=source[:begin]+"""    required={'mk2ks_human_special_negative_v9.lua','mk2ks_human_bicycle_block_trace_v3345.lua',
        'mk2ks_human_bicycle_block_display_v3356.lua','run_current_bicycle_block_display_v3357.ps1',
        '34010gfx.hxx','34010ops.hxx','mk2-maincpu.bin','mk3-maincpu.bin'}
    assert required<={Path(p).name for p in meta['input_hashes']}
"""+source[end:]
    begin=source.index("    terminal=state.original.rows(log,'RESULT')");end=source.index('    expected=list',begin)
    before=source[begin:end]
    need("if first_live and frame>=first_live+1800 then manager.machine:exit();return end"in before and
         "terminal==state.original.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ')[0]['frame']+1800"in before,
         'Only CPU-fixture-specific exit provenance replaces with actual unchanged two-human exit')
    source=source[:begin]+"""    terminal=negative.rows(log,'RESULT')[0]['frame']
    driver=(CASE/'input_sources/tree/mk2ks_human_special_negative_v9.lua').read_text()
    assert "if f==160 then log('FINAL');screen:snapshot('special_final.png');manager.machine:exit()end"in driver
    assert terminal==negative.rows(log,'RESULT')[0]['followup']+160 and terminal>pair['ready']+30
"""+source[end:]
    def phase(log,guest):
        actual=state.phase(log,guest,side)
        return dict(actualPhase=actual,start=actual['start'],ready=actual['regain'],damage=3,allCPUAccepted=False)
    namespace=dict(vars(original))
    namespace.update(negative=state.negative,
       bicycle=SimpleNamespace(verify=phase,POSES=set(poses.INTRO)|set(poses.BIKE_CYCLE[:7])),
       model=SimpleNamespace(OUT=state.OUT,capture=SimpleNamespace(assembly=state.current.assembly)),
       CASES={'current_p'+str(side):(f'audit_v3358_current_bicycle_block_display_p{side}_kano','new','kano')})
    exec(compile(source,__file__+'::whole_original_renderer_blocked_physical_routing','exec'),namespace)
    return namespace['verify']('current_p'+str(side))
