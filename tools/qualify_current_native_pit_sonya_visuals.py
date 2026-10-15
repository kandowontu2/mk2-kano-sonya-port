"""Retain complete earned gate and byte-exact reciprocal scalar baseline."""
import inspect
from pathlib import Path
import qualify_current_native_pit_case as native
import qualify_current_native_pit_visuals as visual

def main():
    code=inspect.getsource(native.gate)
    code=code.replace("r['side']=='1'","r['side']=='2'").replace("r['winner']=='kano'","r['winner']=='sonya'").replace("'17,18'","'18,17'")
    code=code.replace("=='17'","=='TEMP'").replace("=='18'","=='17'").replace("=='TEMP'","=='18'")
    context=dict(vars(native));exec(compile(code,__file__+'::reciprocal gate','exec'),context)
    code=Path(visual.__file__).read_text().replace('from qualify_current_native_pit_case import load,gate','from qualify_current_native_pit_case import load')
    code=code.replace('audit_current_native_pit_visual_kano_p1','audit_current_native_pit_visual_sonya_p2')
    code=code.replace('audit_current_native_pit_longkick_kano_p1_runtime','audit_current_native_pit_longkick_sonya_p2_runtime')
    code=code.replace('KanoP1/SonyaP2','SonyaP2/KanoP1')
    exec(compile(code,__file__+'::reciprocal visual','exec'),{'__name__':'__main__','gate':context['gate']})

if __name__=='__main__':main()
