"""Preserve original whitelist failure; classify exactly native CMOS metadata.

The original native map shares01400000..0141ffff TMS bits as nvram:16384 bytes.
Only its exact generated file is admitted, no general extensionless-file or
ROM/media exception. Every original source/hash/compression assertion retained.
"""
import inspect
import json
from pathlib import Path
import seal_native_selector_sonya_pressure_snapshot as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_metadata_storage_checked.json'
FAILURE=ROOT/'audit_native_selector_sonya_pressure_snapshot_storage_failure.json'


def execute(visual_notes=None):
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed']and failure['sourceSHA256']==sha(previous.__file__)and
         failure['sourceSHA256']=='CB1DF0EBC14863566E8BCE2F6CCA67650458C15815574367FA8F4D4BBDF3DFBE'and
         not previous.OUT.exists()and not failure['compressionExecuted'],
         'Actual original storage-source rejection preserved, no game or drawing check failure')
    folder=previous.capture.RAM_CASES[previous.capture.KEY][0]
    native_nvram=(folder/'nvram/mk2ks/nvram').resolve()
    map_source=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    code=map_source.read_text()
    need('map(0x01400000, 0x0141ffff).rw(FUNC(midtunit_state::midtunit_cmos_r), FUNC(midtunit_state::midtunit_cmos_w)).share("nvram");'in code and
         'NVRAM(config, "nvram", nvram_device::DEFAULT_ALL_0);'in code and
         native_nvram.is_relative_to(previous.capture.BASE.resolve())and native_nvram.is_file()and
         native_nvram.stat().st_size==(0x0141ffff-0x01400000+1)//8==16384,
         'Exact normal native CMOS file, size bound to current compiled TMS-bit memory map')
    source=inspect.getsource(previous.execute)
    def once(before,after):
        nonlocal source
        need(source.count(before)==1,'One exact original storage classification/source inventory boundary')
        source=source.replace(before,after,1)
    once("files.add(capture.LUA.resolve())","files.add(capture.LUA.resolve());files.update((Path(previous.__file__).resolve(),FAILURE,map_source))")
    once("p.suffix.lower()in ('.py','.lua','.json','.gz','.log','.cfg')",
         "(p.suffix.lower()in ('.py','.lua','.json','.gz','.log','.cfg','.cpp')or p==native_nvram)")
    once('publicPlayableChanged=False)',
         'publicPlayableChanged=False,originalStorageWhitelistFailurePreserved=True,'
         "nativeCMOSFile=dict(path=str(native_nvram),bytes=16384,sha256=sha(native_nvram)))")
    scope=dict(vars(previous),OUT=OUT,__file__=__file__,previous=previous,FAILURE=FAILURE,map_source=map_source,native_nvram=native_nvram)
    exec(compile(source,__file__+'::whole_original_storage_exact_source_defined_native_CMOS_metadata','exec'),scope)
    value=scope['execute'](visual_notes)
    need(value['passed']and value['sourceExactSavedPassCPUAndDMAReplayPassed']and
         value['actualReplayedPasses']==1746 and value['wholeExactPassVRAMWords']==457703424 and
         value['completeCurrentScanoutBindingPassed']and value['exactCurrentDisplayedPixels']==182880000,
         'All original whole1800 scanouts and1746 complete pass positives retained through exact storage seal')
    return value
