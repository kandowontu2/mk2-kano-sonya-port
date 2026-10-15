"""Keep the whole actual passive-cause failure and retire only its RAM host.

No game failure is promoted to success. All thirteen earlier earned fights,
the entire old preservation contract, original source/log and29 RAM rasters
remain accounted. No build/ROM/raw-media/ZIP copies or broad cleanup.
"""
import inspect
import seal_native_sonya_shang_cache_failure as original
import capture_native_sonya_shang_cache_cause as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
GAME,PARENT=2008,35228
OUT=ROOT/'audit_native_sonya_shang_actual_cause_preserved'
RETIRED=ROOT/'audit_native_sonya_shang_actual_cause_retirement'


def functions():
    body=inspect.getsource(original.prepare)
    for before,after in (
        ('audit_native_liu_early_leg_preceding_campaign_checked/report.json',
         'audit_native_shang_cause_preceding_campaign_checked/report.json'),
        ('1791711060.8420143','1791713685.8643436'),
        ("preceding['accepted']['completedOpponents']==12","preceding['accepted']['completedOpponents']==13"),
        ("preceding['accepted']['completeOriginalRows']==1001809","preceding['accepted']['completeOriginalRows']==1009959"),
        ('full twelve-match conservation','full thirteen-match conservation'),
        ('len(raw)==28','len(raw)==29'),
        ("result['actualNativeRGBFrameCallbacks']==467","result['actualNativeRGBFrameCallbacks']==468"),
        ("result['nativeRGBBytesComparedInRAM']==189788800","result['nativeRGBBytesComparedInRAM']==190195200"),
        ('bounded28 raw/PIL','bounded29 raw/PIL'),
        ('actualNativeRGBFrameCallbacks=467,nativeRGBBytesComparedInRAM=189788800',
         'actualNativeRGBFrameCallbacks=468,nativeRGBBytesComparedInRAM=190195200'),
        ('earlierTwelveExactConservationAccepted=True,liuEarnedClearIndependentVerificationPending=True',
         'earlierThirteenExactConservationAccepted=True,liuEarnedClearIndependentVerificationPending=False')):
        need(body.count(before)==1,'One whole original preservation boundary: '+before)
        body=body.replace(before,after,1)
    retire_body=inspect.getsource(original.retire)
    need(retire_body.count('=28')==4,'All four original RAM release receipt counters retained')
    retire_body=retire_body.replace('=28','=29')
    scope=dict(vars(original),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)
    exec(compile(body,__file__+'::whole_original_failure_preservation_actual_cause','exec'),scope)
    exec(compile(retire_body,__file__+'::whole_original_exact_host_retirement_29','exec'),scope)
    return scope


def prepare(ram):return functions()['prepare'](ram)


def retire():return functions()['retire']()


if __name__=='__main__':retire()
