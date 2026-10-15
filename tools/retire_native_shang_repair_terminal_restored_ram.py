"""Only retire old terminal RAM after the newer compiler restores mutable files."""
import inspect
import json
from pathlib import Path
import retire_native_shang_repair_terminal_ram as original

def retire(ram):
    root=original.checked.ROOT
    need=original.checked.original.need
    build=root/'diagnostic_native_shang_drain_anchors'
    restored=json.loads((build/'restoration.json').read_text(encoding='utf-8-sig'))
    cache=json.loads((build/'cache_retirement.json').read_text(encoding='utf-8-sig'))
    need(restored['passed'] and restored['native_build_exit']==0 and cache['passed'] and
         cache['nativeCompilerExit']==0 and cache['cacheAbsent'] and not(root/'mame-mkp/build/mingw-gcc').exists(),
         'Actual newer compiler terminal, original sources restored, temporary cache retired')
    need(all(original.checked.original.sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items()),
         'Every original user file/executable restored before old qualified pins are checked')
    source=inspect.getsource(original.retire)
    before='RAMDictionaryCleared=True,normalHostExitRequired=True'
    need(source.count(before)==1,'Unique successor RAM retirement provenance boundary')
    source=source.replace(before,"RAMDictionaryCleared=True,normalHostExitRequired=True,newCompilerTerminalRestorationChecked=True,earlierRetirementDeferredBecauseMutableSourceWasTemporarilyStaged=True,successorSourceSHA256=sha(__file__)",1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::original_terminal_retirement_after_actual_restoration','exec'),scope)
    return scope['retire'](ram)
