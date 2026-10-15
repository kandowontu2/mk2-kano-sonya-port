"""Correct prelaunch Lua wrapper binding; whole same distinct guard policy."""
import inspect
from pathlib import Path
import capture_native_selector_cpu_projectile_pcm_startup as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE,OUT=original.BASE,original.OUT
LUA=ROOT/'mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua'
KEY='cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct'
RAM_CASES=original.RAM_CASES;NATIVE_HANDLES=original.NATIVE_HANDLES
COMPLETED=original.COMPLETED;AUDIO=original.AUDIO
SCOPE=None

def execute(state,preflight=False):
    global SCOPE
    old_base=original.ROOT/'mk2ks_native_selector_cpu_projectile_pcm_startup_base.lua'
    need('and p:read_u16(0x01060e50)==17 then' not in old_base.read_text(),
         'Original nested wrapper cannot satisfy natural observer substitution; no native launched')
    scope=dict(vars(original),LUA=LUA,KEY=KEY,__file__=__file__,SCOPE=None)
    for function in (original.prepare,original.execute):
        exec(compile(inspect.getsource(function),__file__+'::whole_original_'+function.__name__,'exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
