"""Explicit controlled native alternate palette branch, NOT natural selection."""
import json
import verify_native_split_blood_v1133 as proof

OUT=proof.ROOT/'audit_v1135_controlled_split_alternate_checked'
if OUT.exists():raise ValueError('Never overwrite controlled evidence')
report=proof.verify(controlled=True)
assert report['naturalAlternateSelectionAccepted'] is False
OUT.mkdir()
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
raise SystemExit(0 if report['passed'] else 1)
