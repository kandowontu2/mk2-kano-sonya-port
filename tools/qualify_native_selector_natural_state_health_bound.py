"""Existing exact Win32 host census; whole original state/HP gate unchanged."""
from pathlib import Path

path = Path(__file__).with_name('qualify_native_selector_natural_state_health.py')
source = path.read_text()
changes = (
    ('import psutil', 'import os, sys\nimport read_live_shang_drain_frames as transport\nimport capture_current_subzero_audio_v6213 as artifact'),
    ("    host = psutil.Process()\n    need(host.pid == 38752 and host.ppid() == 40316 and\n         host.create_time() == 1791734919.6266766 and\n         host.cmdline()[1:] == ['-B', 'tools/capture_native_selector_special_shadow.py'],",
     "    host = next(p for p in transport.census_hosts() if p['ProcessId'] == os.getpid())\n    need(host['ProcessId'] == 38752 and host['ParentProcessId'] == 40316 and\n         host['createdUnix'] == 1791734919.6266766 and\n         Path(host['ExecutablePath']).resolve() == Path(sys.executable).resolve() and\n         host['CommandLine'] == '\"' + sys.executable + '\" -B tools/capture_native_selector_special_shadow.py',"),
    ('(expected_pid, host.pid, expected_birth)', "(expected_pid, host['ProcessId'], expected_birth)"),
    ("capture.prior.current.prior.save(OUT / 'report.json', report)", "artifact.save(OUT / 'report.json', report)"),
)
for before, after in changes:
    assert source.count(before) == 1, 'Exact original host or artifact boundary only'
    source = source.replace(before, after, 1)
exec(compile(source, str(path) + '::host_and_saver_bound_successor', 'exec'))
