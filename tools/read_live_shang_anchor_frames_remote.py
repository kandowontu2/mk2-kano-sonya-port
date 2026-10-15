"""Read-only callback specialization for the existing coordinate-repair host."""
from pathlib import Path
_anchor_callback_source=Path(__file__).with_name('read_live_shang_drain_frames_remote.py').read_text()
def _anchor_once(before,after):
    global _anchor_callback_source
    assert _anchor_callback_source.count(before)==1
    _anchor_callback_source=_anchor_callback_source.replace(before,after,1)
_anchor_once('os.getpid()==30848 and process.pid==31336 and identity[\'createdUnix\']==1791721342.2271461',
             'os.getpid()==3232 and process.pid==32016 and identity[\'createdUnix\']==1791725473.170992')
_anchor_once("answer['nativePoll']=process.poll()", "answer['nativePoll']=process.poll();assert answer['nativePoll'] is None")
_anchor_once("n in request and (n.startswith('shang_shrink_') or n.startswith('shang_victim_provenance_'))", 'n in request')
exec(compile(_anchor_callback_source,__file__+'::existing_native_rasters_only','exec'))
