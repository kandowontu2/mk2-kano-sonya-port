"""Same12 actual admission/control mutations, bound to true Kano17 evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_smoke_control_faults.py').read_text()
for old,new in (
    ('audit_current_sonya_toasty_72_cadence_runtime','audit_current_kano_smoke_64_cadence_runtime'),
    ('audit_current_sonya_toasty_72_cadence_checked','audit_current_kano_smoke_64_cadence_checked'),
    ('audit_current_sonya_smoke_control_faults_checked','audit_current_kano_smoke_control_faults_checked'),
    ("prior['admission']['completeSameRoundControls']","prior['controls']['completeSameRoundControls']"),
    ('currentNaturalSonyaSmokeAdmissionAndFiniteControlsPassed','currentNaturalKanoSmokeAdmissionAndFiniteControlsPassed'),
):
    assert old in source,old
    source=source.replace(old,new)
old="exec(compile(ast.Module(body=definitions,type_ignores=[]),__file__+'::'+name,'exec'))"
assert source.count(old)==1
source=source.replace(old,"""code='\\n'.join(ast.unparse(n) for n in definitions)
    code=code.replace("r['winner'] == 'sonya'", "r['winner'] == 'kano'")
    code=code.replace("'18,4'", "'17,4'").replace("'18,14'", "'17,14'")
    code=code.replace("fights[0]['human'] == '18'", "fights[0]['human'] == '17'")
    exec(compile(code,__file__+'::same_native_Kano_gate','exec'))""")
old="rows=load(folder/'run.log')"
assert source.count(old)==1
source=source.replace(old,"""whole=load(folder/'run.log')
end=int(whole['SECRET_COMPLETE'][0]['frame'])
rows={tag:[r for r in group if int(r['frame'])<=end] for tag,group in whole.items()}""")
exec(compile(source,__file__+'::same_actual_Kano_control_faults','exec'))
