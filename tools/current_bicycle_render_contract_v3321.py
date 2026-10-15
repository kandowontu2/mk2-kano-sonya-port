"""Original complete native renderer; explicit hit proof/source-path adaptation."""
import inspect
from types import SimpleNamespace
import verify_native_cpu_bicycle_round_render_v3130 as original
import native_cpu_bicycle_hit_contract_v3317 as phase
import current_jump_capture_contract_v3310 as capture
import verify_current_cpu_launch_jump_v3319 as model
need=capture.need

def verify():
    source=inspect.getsource(original.verify)
    substitutions=[
        ("assert proof['passed']and proof['actualCandidateBicycleMissAccepted']", "assert proof['passed']and proof['actualNativeBicycleContactDamageAndSeparateRecoveryAccepted']"),
        ("assert typed==proof['cases'][key]['phase']", "assert typed==proof['case']['phase']"),
        ("assert pair['damage']==0 and not pair['allCPUAccepted']", "assert pair['damage']==22 and not pair['allCPUAccepted']"),
        ("assert bicycle.POSES<=held[2],'All actual original startup and full cycling bicycle poses executed'", "assert bicycle.POSES<=held[2],'All actual original startup and full cycling bicycle poses executed'\n    assert set(bicycle.VICTIM_POSES)<=held[1],'All six original owned paired victim poses executed'"),
        ("for pose in bicycle.POSES:", "for pose in sorted(set(bicycle.POSES)|set(bicycle.VICTIM_POSES)):"),
        ("assert bicycle.POSES<=visible[2],'Every startup and cycling bicycle pose has an exact visible scanout'", "assert bicycle.POSES<=visible[2],'Every startup and cycling bicycle pose has an exact visible scanout'\n    assert set(bicycle.VICTIM_POSES)<=visible[1],'Every original paired victim pose has an exact visible scanout'"),
    ]
    for before,after in substitutions:
        need(source.count(before)==1,'Exactly one declared renderer proof/phase change: '+before)
        source=source.replace(before,after)
    # Original driver/observer bodies are separately checked in their entirety
    # by the capture contract. These references select their actual frozen copies.
    paths={
        'mk2ks_native_cpu_bicycle_display_v3105.lua':'mk2ks_native_cpu_bicycle_display_v3305.lua',
        'mk2ks_native_cpu_mobility_boundary_v3106.lua':'mk2ks_native_cpu_mobility_boundary_v3306.lua',
        'mk2ks_physical_p2_cpu_continuation_v3095.lua':'mk2ks_physical_p2_cpu_continuation_v3300.lua',
        'mk2ks_physical_p2_cpu_round_trace_v3101.lua':'mk2ks_physical_p2_cpu_round_trace_v3301.lua',
        'mk2ks_physical_p2_cpu_overlap_trace_v3102.lua':'mk2ks_physical_p2_cpu_overlap_trace_v3302.lua',
        'mk2ks_physical_p2_cpu_choice_trace_v3103.lua':'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
        'mk2ks_physical_p2_cpu_square_trace_v3104.lua':'mk2ks_physical_p2_cpu_square_trace_v3304.lua',
    }
    for before,after in paths.items():
        need(before in source,'Actual retained original snapshot reference: '+before)
        source=source.replace(before,after)
    namespace=dict(vars(original))
    namespace.update(bicycle=phase,model=SimpleNamespace(OUT=model.OUT,capture=capture),
                     CASES={'current_kano':(model.CASE,'new','kano')})
    exec(compile(source,__file__+'::complete_original_native_renderer_with_hit_proof','exec'),namespace)
    return namespace['verify']('current_kano')
