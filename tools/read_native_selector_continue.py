"""Exact original paid-continue host, bounded RAM-only native scanout viewer."""
import inspect
import read_native_anchor_ui as original


def run():
    source=inspect.getsource(original.run)
    changes=(("profile_records={'delayed':(27800,29688,1791726178.3294525,'capture_native_anchor_ui_ram.py'),\n                     'standard':(12004,16360,1791726301.6143703,'capture_native_anchor_ui_standard_ram.py')}",
              "profile_records={'continue':(40856,39948,1791732779.396103,'capture_native_selector_continue.py')}"),
             ("('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')",
              "('kano_p1_to_sonya','sonya_p1_to_kano','kano_p2_to_sonya','sonya_p2_to_kano')"),
             ('0<=n<80','0<=n<200'),
             ("'tools/read_native_anchor_ui_remote.py'","'tools/read_native_selector_continue_remote.py'"))
    for before,after in changes:
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::exact_original_paid_continue_terminal_host','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
