"""Correlate observed native uppercut entry to recorded physical punish cycles."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
baseline=sync.ROOT/'audit_current_kano_kitana_close_guard_runtime/run.log'
tight=sync.ROOT/'audit_current_kano_kitana_tight_punish_runtime/run.log'
rows=chronology.load(baseline);other=chronology.load(tight)
attempts=rows['KANO_KITANA_CLOSE_PUNISH']
links=[]
for entry in rows['KANO_CLOSE_NATIVE_UPPER']:
    recent=[r for r in attempts if 0<=int(entry['frame'])-int(r['frame'])<23]
    assert recent
    attempt=recent[-1]
    assert entry['actor']==entry['owner'] and entry['id']=='17'
    links.append(dict(nativeFrame=int(entry['frame']),punishMarkerFrame=int(attempt['frame']),
                      controllerCycleAge=13+int(entry['frame'])-int(attempt['frame']),
                      attemptGap=int(attempt['gap']),nativeEntry=entry))
assert len(links)==3 and not other.get('KANO_CLOSE_NATIVE_UPPER')
report=dict(passedCorrelation=True,baselineSHA256=sync.sha(baseline),tightSHA256=sync.sha(tight),
 nativeEntries=links,tightNativeEntries=0,
 scope='Correlation to recorded age13 marker. Does not prove exact input-parser read time or crouch counter. Native entry may follow the HP edge by a field.',
 nextAction='Preserve observed later HP opportunities; directly inspect crouch readiness if trying to shorten the release window.',
 fullPortAccepted=False)
out=sync.ROOT/'audit_current_kano_uppercut_timing'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
