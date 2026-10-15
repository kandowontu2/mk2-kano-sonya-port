"""Player-two successor: bind manually reviewed samples to baseline gameplay."""
from pathlib import Path
import verify_native_source_sync as sync

predecessor = Path(__file__).with_name('qualify_bounded_cross_grab_visual_review.py')
source = predecessor.read_text()
assert "_p1_runtime" in source
source = source.replace('audit_bounded_cross_grab_visual_review_checked',
                        'audit_bounded_p2_cross_grab_visual_review_checked')
source = source.replace('_p1_runtime', '_p2_runtime')
source = source.replace('Eight 400x254 P1 cross-grab PNG samples',
                        'Eight 400x254 P2 cross-grab PNG samples')
source = source.replace('pixel-exact alignment, P2 visuals,', 'pixel-exact alignment, all other visuals,')
source = source.replace('Expected character/victim pose, correct names, no selector overlays; no missing body or persistent grab pose observed in four samples.',
    'Expected character/victim pose, correct names and floor shadows, no selector overlays; no missing body or persistent grab pose observed in four samples. Choke recovery sample naturally crops Sonya at the left viewport edge. Recovered marker is not exact raster idle timing.')
source = source.replace('checkerSHA256=sync.sha(Path(__file__)),',
    'checkerSHA256=sync.sha(Path(__file__)), predecessorSHA256=sync.sha(predecessor),')
exec(compile(source, str(Path(__file__)), 'exec'))
