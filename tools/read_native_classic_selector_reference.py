"""Exact original unmodified stock reference host; native rasters remain in RAM."""
import inspect
import read_native_anchor_ui as original

def run():
    source=inspect.getsource(original.run)
    changes=(
        ("profile_records={'delayed':(27800,29688,1791726178.3294525,'capture_native_anchor_ui_ram.py'),\n                     'standard':(12004,16360,1791726301.6143703,'capture_native_anchor_ui_standard_ram.py')}",
         "profile_records={'classic':(37792,34228,1791729958.8748436,'capture_native_classic_selector_reference_loaded.py')}"),
        ("('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')", "('liu_kang_p1_stock_ladder',)"),
        ("'tools/read_native_anchor_ui_remote.py'", "'tools/read_native_classic_selector_reference_remote.py'"))
    for before,after in changes:
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::exact_original_classic_host','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
