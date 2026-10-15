"""Show only this exact original terminal navigation host's RAM scanout."""
import inspect
import read_native_anchor_ui as original


def run():
    source=inspect.getsource(original.run)
    changes=(("profile_records={'delayed':(27800,29688,1791726178.3294525,'capture_native_anchor_ui_ram.py'),\n                     'standard':(12004,16360,1791726301.6143703,'capture_native_anchor_ui_standard_ram.py')}",
              "profile_records={'navigation':(42340,41868,1791730913.6030636,'capture_native_selector_navigation.py')}"),
             ("('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')",
              "('up','down','left','right')"),
             ("'tools/read_native_anchor_ui_remote.py'","'tools/read_native_selector_navigation_remote.py'"))
    for before,after in changes:
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::exact_original_terminal_navigation_host','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
