"""Exact current host/native identities, bounded in-RAM native-frame transport."""
import inspect
from pathlib import Path
import read_live_shang_drain_frames as original

ROOT=original.ROOT
REMOTE=ROOT/'tools/read_live_shang_anchor_frames_remote.py'
OUT=ROOT/'audit_native_shang_drain_anchors_campaign'

def run():
    source=inspect.getsource(original.run)
    def once(before,after):
        nonlocal source
        assert source.count(before)==1
        source=source.replace(before,after,1)
    once("r'shang_(?:shrink_id(?:17|18)_age|victim_provenance_age)\\d+\\.png'", "r'[a-z0-9_]+\\.png'")
    once("wanted['ProcessId']==31336 and wanted['ParentProcessId']==30848", "wanted['ProcessId']==32016 and wanted['ParentProcessId']==3232 and wanted['createdUnix']==1791725473.170991")
    once("r['ProcessId']==30848", "r['ProcessId']==3232")
    once("host['ParentProcessId']==35304", "host['ParentProcessId']==18840 and host['createdUnix']==1791725456.132396")
    once('tools/capture_native_shang_owned_drain_campaign.py', 'tools/capture_native_shang_drain_anchors_campaign.py')
    scope=dict(vars(original),ROOT=ROOT,REMOTE=REMOTE,OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::read_only_current_actual_host_native_binding','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
