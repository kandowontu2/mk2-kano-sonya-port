"""Whole4527 progress checkpoint; bounded complete progress records, not a tail.

4527's small text tail sometimes holds only dense native knife observations
and therefore contains no LIVE record. This is not a native-job failure.
Keep that executed source unchanged. Preserve every native/live/source/scope
gate, changing only the read-only progress extraction and fresh output leaf.
"""
import inspect
from pathlib import Path
import save_ending_video_pending_progress_v4527 as original
ROOT,need=original.ROOT,original.need
OUT=ROOT/'audit_v4532_ending_video_live_full_scope_checkpoint'

def main():
    source=inspect.getsource(original.main)
    before="""    with(CASE/'run.log').open('rb')as f:
        f.seek(max(0,(CASE/'run.log').stat().st_size-16384));tail=f.read(16384).decode('utf-8',errors='replace')
    live=[line for line in tail.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_LIVE ')]"""
    after="""    snapshot_bytes=(CASE/'run.log').stat().st_size
    live=[];native_error=False
    with(CASE/'run.log').open('rb')as f:
        while True:
            binary=f.readline()
            if not binary or f.tell()>snapshot_bytes:break
            line=binary.decode('utf-8',errors='strict')
            if line.startswith('MK2_NAT_CAMPAIGN_LIVE '):live=[line.strip()]
            if re.search(r'LUA ERROR|Lua error|stack traceback|fatal error|access violation',line):native_error=True
    tail='LUA ERROR'if native_error else''
    pin(ROOT/'tools/save_ending_video_pending_progress_v4527.py')"""
    need(source.count(before)==1,'Only declared small-tail versus bounded complete-record extraction repair')
    source=source.replace(before,after,1)
    before="current3836EndingContinuousVideoSourcePreflightAccepted=True,"
    after="""current3836EndingContinuousVideoSourcePreflightAccepted=True,
      priorPendingCheckpointSourceFailure=dict(source=str(ROOT/'tools/save_ending_video_pending_progress_v4527.py'),
        condition='The fixed16KiB tail contained only dense native knife observations and no LIVE record; its no-progress-record gate rejected. No native failure or terminal state was inferred.',
        correction='Read only complete records within one actual byte-size snapshot, retaining every original fresh live-CIM/true-ID/source/scope gate. Executed4527 source preserved.'),"""
    need(source.count(before)==1,'Record exact non-native checkpoint extraction correction')
    source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__,OUT=OUT)
    exec(compile(source,__file__+'::whole4527_complete_record_extraction_only','exec'),scope)
    return scope['main']()

if __name__=='__main__':main()
