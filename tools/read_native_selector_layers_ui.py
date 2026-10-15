"""View only the exact original successor UI host's terminal native rasters."""
import inspect
import read_native_anchor_ui as original

def run():
    source=inspect.getsource(original.run)
    changes=(
        ("profile_records={'delayed':(27800,29688,1791726178.3294525,'capture_native_anchor_ui_ram.py'),\n                     'standard':(12004,16360,1791726301.6143703,'capture_native_anchor_ui_standard_ram.py')}",
         "profile_records={'layers':(39892,18304,1791729346.34943,'capture_native_selector_layers_ui_ram.py')}"),
        ("('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')",
         "('kano_p1_sonya_p2_two_confirm96','sonya_p1_kano_p2_two_confirm96','kano_p1_stock_p2_ladder_confirm96','sonya_p1_stock_p2_ladder_confirm96','kano_p1_sonya_p2_two_confirm370','sonya_p1_kano_p2_two_confirm370')"),
        ("'tools/read_native_anchor_ui_remote.py'","'tools/read_native_selector_layers_ui_remote.py'"))
    for before,after in changes:
        assert source.count(before)==1,(before,source.count(before))
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::same_terminal_ui_layers_host','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
