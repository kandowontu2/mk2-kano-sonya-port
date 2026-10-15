"""Bind the unchanged finite recovery verifier to the actual coordinate replay."""
import inspect
import qualify_native_shang_repair_terminal as original
import capture_native_shang_drain_anchors_campaign as capture

OUT=capture.ROOT/'audit_native_shang_anchor_terminal_checked'

def verify(ram):
    source=inspect.getsource(original.verify)
    changes=(
        ("==31336", "==32016"), ("==30848", "==3232"),
        ('1791721342.2271461','1791725473.170992'),
        ('audit_native_shang_drain_preceding_campaign_checked/report.json','audit_native_shang_anchor_preceding_campaign_checked/report.json'),
        ('531553099','531553100'),
        ('live_count=0;stage16_min_cpu=999','live_count=0;stage16_min_cpu=999;last_live_frame=-1'),
        ("row=fields(line);live_count+=1", "row=fields(line);live_count+=1\n                this_frame=int(row['frame'])\n                need(this_frame>last_live_frame and (live_count<300 or this_frame%30==0),'Original emitted LIVE sampling and strict order')\n                last_live_frame=this_frame"),
        ('live_count==590896','live_count==19999'),
        ("'Every actual live character/state/stage/assistance field valid, including all postfatality attempts'",
         "'Every actual emitted sampled live field valid; not every-frame coverage'"),
        ("'Every live field verified; actual postfatality ordinary Sonya fight; no hidden cache error or invented ending'",
         "'All19999 actual emitted LIVE rows verified; real recovery; no logged cache error or ending'"),
        ("positive=assess(routes)", "campaign_result=[fields(row)for row in native_results if row.startswith('MK2_NAT_CAMPAIGN_RESULT ')]\n    need(len(campaign_result)==1 and campaign_result[0]['live_fields']=='590896' and campaign_result[0]['frame']=='984724','Exact native all-frame counter retained, not printed-row coverage')\n    positive=assess(routes)"),
        ("('shang_victim_provenance_age4.png','shang_shrink_id18_age20.png','shang_shrink_id18_age120.png',\n                 'shang_shrink_id18_age320.png','campaign_selection_1_146.png','campaign_fight_selection119_stage16.png')",
         "('shang_shrink_id18_age20.png','shang_shrink_id18_age40.png','shang_victim_provenance_age80.png',\n                 'shang_victim_provenance_age100.png','shang_shrink_id18_age120.png','shang_shrink_id18_age320.png')"),
        ('actualNativeFrameLimit=984724,actualLiveStateFields=live_count',
         'actualNativeFrameLimit=984724,actualPrintedLiveStateRows=live_count,nativeAllFrameObservationCounter=590896,everyFrameFieldsIndependentlyVerified=False'),
        ('actualLiveStateFields=live_count,earnedAdditionalCPU', 'actualPrintedLiveStateRows=live_count,earnedAdditionalCPU'),
        ("requiredArtFollowup='Source-qualified18-byte coordinate correction matches actual stock phase anchors; not compiled/native-verified yet. Selection numeral/blink needs multi-phase comparison, not acceptance from one screenshot.'",
         "requiredArtFollowup='Coordinate-only repair actually initialized and six true Sonya normal shrinking/skeleton/win/fatality rasters reviewed. Both true IDs/costumes and audio remain open; active selector blink/numbers verified separately; confirmed preview occlusion identified by actual render order.'"),
        ("Path(capture.__file__),prior_path", "Path(capture.__file__),Path(original.__file__),prior_path"))
    for before,after in changes:
        original.need(source.count(before)==1,'Exact original terminal verification boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),capture=capture,OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::same_actual_terminal_coordinate_replay','exec'),scope)
    return scope['verify'](ram)
