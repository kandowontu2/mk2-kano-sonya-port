"""Qualify ACTIVE cursor pixels; do not excuse confirmed victory-pose occlusion."""
import inspect
import qualify_native_anchor_cursor_pixels as original

def verify(ram):
    source=inspect.getsource(original.verify)
    before="sample=[f for f in frames if f['header']['label']in('highlight','highlight_blink','cursor_trace_long')]"
    after=before[:-1]+" and int(f['header']['frame'])<int(frames[0]['header']['frame'])-8+220]"
    replacements=((before,after),('len(sample)>=24','len(sample)>=18'),
        ("'Complete three observed native blink windows, not a single lucky screenshot'",
         "'Both observed ACTIVE blink windows before P2 confirmation; post-confirmation overlap is an OPEN issue'"),
        ('for x in (*range(0,5),398,399)','for x in range(0,5)'),
        ("'Native exposed background strips do not shift when the new poses animate'",
         "'Actual uncovered LEFT-margin backdrop stays fixed during ACTIVE selection only'"),
        ('exactStableBackgroundPixels=len(bg_points)','exactStableLeftMarginBackgroundPixels=len(bg_points)'),
        ('finiteBothOwnNativePortraitBlinkNumbersPoseAndRegistrationAccepted=True',
         'finiteBothActiveOwnNativePortraitBlinkNumbersPoseAndRegistrationAccepted=True'),
        ('actualCases=cases,inputHashes=pins','actualCases=cases,inputHashes=pins,postConfirmationOwnKanoArmOverSonyaPortraitObserved=True,postConfirmationOcclusionNeedsStockReference=True,wholePortraitOcclusionLifecycleAccepted=False'))
    for before,after in replacements:
        original.need(source.count(before)==1,'Unique active-scope boundary: '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),OUT=original.capture.ROOT/'audit_native_anchor_active_cursor_pixels_checked',__file__=__file__)
    exec(compile(source,__file__+'::active_pixels_with_confirmed_overlap_explicitly_open','exec'),scope)
    return scope['verify'](ram)
