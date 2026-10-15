"""Same retained reader; remote debug execution has no __file__ binding."""
from pathlib import Path
path = Path(__file__).with_name('read_native_selector_cpu_projectile_pcm_frames.py')
source = path.read_text()
before = "'tools/read_native_selector_cpu_projectile_pcm_frames_remote.py'"
assert source.count(before) == 1
source = source.replace(before, "'tools/read_native_selector_cpu_projectile_pcm_frames_bound_remote.py'", 1)
exec(compile(source, str(path) + '::bound_remote_successor', 'exec'))
