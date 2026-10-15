"""Successor: distinguish all native observations from emitted sampled LIVE rows."""
import inspect
import json
from pathlib import Path
import qualify_native_shang_repair_terminal as original

ROOT = original.ROOT
OUT = ROOT/'audit_native_shang_repair_terminal_sampled_checked'

def verify(ram):
    original.need(not OUT.exists(), 'Fresh sampled successor receipt')
    failure = ROOT/'audit_native_shang_repair_terminal_failure'
    original.need(not failure.exists(), 'One preserved original verifier failure')
    # The predecessor completed the full log scan, but compared its printed-row
    # count to the observer's all-frame counter. Preserve that precise failure.
    failure.mkdir()
    (failure/'report.json').write_text(json.dumps(dict(passed=False,
        verifierSHA256=original.sha(original.__file__), actualPrintedLiveRows=19999,
        nativeAllFrameObservations=590896, reason='Printed sampling count was incorrectly compared to all-frame counter.',
        nativeRerun=False, originalReportOverwritten=False),indent=2)+'\n')
    source=inspect.getsource(original.verify)
    def once(before,after):
        nonlocal source
        original.need(source.count(before)==1, 'Exact sampled verifier boundary: '+before)
        source=source.replace(before,after,1)
    once('live_count=0;stage16_min_cpu=999', 'live_count=0;stage16_min_cpu=999;last_live_frame=-1')
    once("row=fields(line);live_count+=1", """row=fields(line);live_count+=1
                this_frame=int(row['frame'])
                need(this_frame>last_live_frame and (live_count<300 or this_frame%30==0),
                     'Every emitted LIVE row follows actual observer first299/30-frame sampling and strict order')
                last_live_frame=this_frame""")
    once('live_count==590896', 'live_count==19999')
    once("'Every actual live character/state/stage/assistance field valid, including all postfatality attempts'",
         "'Every emitted sampled live field valid, including postfatality attempts; not every-frame coverage'")
    once("'Every live field verified; actual postfatality ordinary Sonya fight; no hidden cache error or invented ending'",
         "'All19999 emitted LIVE rows verified; real postfatality Sonya fight; no hidden logged cache error or invented ending'")
    once("positive=assess(routes)", """campaign_result=[fields(row)for row in native_results if row.startswith('MK2_NAT_CAMPAIGN_RESULT ')]
    need(len(campaign_result)==1 and campaign_result[0]['live_fields']=='590896' and
         campaign_result[0]['frame']=='984724','Exact terminal all-frame observation counter, not printed-row coverage')
    controller=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    need('live_fields=live_fields+1' in controller and 'if live_fields<300 or frame%30==0 then' in controller,
         'Actual frozen original observer samples emitted LIVE rows')
    positive=assess(routes)""")
    once('actualNativeFrameLimit=984724,actualLiveStateFields=live_count', 'actualNativeFrameLimit=984724,actualPrintedLiveStateRows=live_count,nativeAllFrameObservationCounter=590896,everyFrameFieldsIndependentlyVerified=False')
    once("actualLiveStateFields=live_count,earnedAdditionalCPU", "actualPrintedLiveStateRows=live_count,earnedAdditionalCPU")
    scope=dict(vars(original),OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::sampled_original_terminal_verifier','exec'),scope)
    return scope['verify'](ram)
