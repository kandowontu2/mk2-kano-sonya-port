"""Clarify sampled throw role; preserve first audit with ambiguous label."""
from pathlib import Path
import audit_current_reptile_controller_failures as base

if __name__=='__main__':
    code=Path(base.__file__).read_text()
    code=code.replace("sync.ROOT/'audit_current_reptile_controller_failures'","sync.ROOT/'audit_current_reptile_controller_failures_cpu'")
    code=code.replace('sparseThrowFields','sparseCpuThrowFields')
    code=code.replace("r['actions'].split(',')[0]=='1287'","r['actions'].split(',')[1]=='1287'")
    exec(compile(code,str(Path(base.__file__))+' [explicit CPU role]','exec'),{'__name__':'__main__'})
