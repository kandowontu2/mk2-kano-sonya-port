"""Current input-only stock control for original CPU uppercut ordering."""
from verify_cpu_air_runtime import matched_launch, need
from verify_cpu_recovery import rows, rows_prefix
from verify_cpu_action_flow import original_instructions, verify_followup


def verify(folder):
    meta, log, original = matched_launch(folder, 'mk2ks_cpu_action_transition_v3_probe.lua',
                                         'run_cpu_action_transition_v3_probe.ps1')
    original_instructions(original)
    cold = rows_prefix(log, 'MK2_P1CPU_COLD_LIVE ')
    select = rows_prefix(log, 'MK2_P1CPU_SELECT_RESULT ')
    need(len(cold) == len(select) == 1, 'Single cold stock campaign')
    c, s = cold[0], select[0]
    need(c['cpu_id'] == s['initial_cpu'] == 3 and c['stage'] == 0 and
         c['schedule'] == 0xfffa3480 and c['human_id'] == s['human_id'] == 18 and
         s['human'] == c['human'] == meta['player'] == 'sonya' and s['errors'] == 0 and
         s['checks'] == 39 and 700 < s['css'] < s['exit'] < s['live'] == c['frame'] and
         all(r['writes'] == 0 and r['assistance'] == 'none' for r in (c, s)),
         'Actual stock Baraka versus selected Sonya, no identity/stage assistance')
    fields = rows(log, 'STOCK_FIELD')
    need(fields, 'Actual stock match fields')
    result = rows(log, 'STOCK_END')
    need(len(result) == 1 and result[0]['clear'] > result[0]['start'] > c['frame'],
         'Stock control finishes after actual attack cleanup, not KO timeout')
    done = result[0]
    proof = verify_followup(log, fields[0]['actor'], fields[0]['main'], 3,
                            c['frame'], done['start'], 'STOCK_FIELD')
    need(done['clear'] == proof['clear'] and done['frame'] == done['clear'] + 30 and
         fields[-1]['frame'] == done['frame'] and done['initial_cpu'] == 3 and
         done['writes'] == 0 and done['assistance'] == 'none', 'Actual bounded terminal stock control')
    return dict(passed=True, uppercut=proof, real_block_input=True,
                scope='one_current_stock_CPU_Baraka_uppercut_full_ordered_native_recovery_not_all_stock_moves_or_KO',
                whole_character_integration_complete=False)
