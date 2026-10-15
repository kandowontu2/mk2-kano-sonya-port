"""Exclude the native raised victory hand from the claimed uncovered background."""
import inspect
import qualify_native_anchor_cursor_pixels as original

def verify(ram):
    source=inspect.getsource(original.verify)
    replacements=(
        ("for x in (*range(0,5),398,399)","for x in range(0,5)"),
        ("'Native exposed background strips do not shift when the new poses animate'",
         "'Actual uncovered native LEFT-margin background pixels remain fixed; right raised hand is foreground, not backdrop'"),
        ('exactStableBackgroundPixels=len(bg_points)','exactStableLeftMarginBackgroundPixels=len(bg_points)'),
        ('actualCases=cases,inputHashes=pins','actualCases=cases,inputHashes=pins,earlierBackgroundProbeFailurePreserved=True,earlierProbeIncludedNativeSonyaRaisedHandAtRightmost16Pixels=True'))
    for before,after in replacements:
        original.need(source.count(before)==1,'Unique actual uncovered-pixel scope correction: '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),OUT=original.capture.ROOT/'audit_native_anchor_cursor_uncovered_pixels_checked',__file__=__file__)
    exec(compile(source,__file__+'::actual_uncovered_pixels_not_native_foreground','exec'),scope)
    return scope['verify'](ram)
