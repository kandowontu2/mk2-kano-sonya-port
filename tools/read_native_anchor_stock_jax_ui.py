"""View the existing, terminal stock Jax reference without starting another game."""
import inspect
import read_native_anchor_ui as original

def run():
    source=inspect.getsource(original.run)
    replacements=(
        ("profile_records={'delayed':(27800,29688,1791726178.3294525,'capture_native_anchor_ui_ram.py'),\n                     'standard':(12004,16360,1791726301.6143703,'capture_native_anchor_ui_standard_ram.py')}",
         "profile_records={'stock':(38904,37020,1791727181.9141426,'capture_native_anchor_ui_stock_jax_ram.py')}"),
        ("('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')", "('sonya_p1_jax_p2_two',)"),
        ("'tools/read_native_anchor_ui_remote.py'", "'tools/read_native_anchor_stock_jax_ui_remote.py'"))
    for before,after in replacements:
        assert source.count(before)==1,(before,source.count(before))
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::same_terminal_stock_reference','exec'),scope)
    scope['run']()

if __name__=='__main__':run()
