"""All13 actual preceding fights on the coordinate successor, no selected subset."""
import inspect
import qualify_native_shang_drain_preceding_campaign as original
import capture_native_shang_drain_anchors_campaign as capture

OUT=capture.ROOT/'audit_native_shang_anchor_preceding_campaign_checked'

def run():
    source=inspect.getsource(original.run)
    for before,after in (
        ('audit_native_shang_drain_startup_successor/report.json','audit_native_shang_drain_anchors_startup/report.json'),
        ("identity['ProcessId']==31336 and identity['ParentProcessId']==30848", "identity['ProcessId']==32016 and identity['ParentProcessId']==3232"),
        ('1791721342.2271461','1791725473.170992')):
        capture.need(source.count(before)==1,'Unique current full preceding-gate binding: '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),capture=capture,OUT=OUT,__file__=__file__)
    exec(compile(inspect.getsource(original.actual_state),__file__+'::same_actual_native_identity_or_original_wait_receipt','exec'),scope)
    exec(compile(source,__file__+'::all_original_rows_categories_and_earned_rounds','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
