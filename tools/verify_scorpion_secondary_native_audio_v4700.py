"""Whole4698 native audio qualification with immediate dispatch attribution.

The original last selector interval also contains a later native direct packet.
Bind the first actual dispatch after each admission, retaining all28 packets,
all24 selectors and all4 explicitly unqualified direct callers. No native rerun.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=(ROOT/'tools/verify_scorpion_secondary_native_audio_v4698.py').read_text()
changes=[
 ('audit_v4699_scorpion_secondary_native_audio_checked','audit_v4701_scorpion_secondary_native_audio_checked'),
 ("        p=[r for r in packets if float(q['seconds'])<float(r['seconds'])<stop and r['a8']==call['a8']and r['a13']==call['a13']]\n        need(len(p)==1 and p[0]['frame']==call['frame']and int(p[0]['a3'],16)==word+slot,",
  "        later=[r for r in packets if float(q['seconds'])<float(r['seconds'])<stop]\n        need(later,'Actual immediate native dispatcher after admitted selector')\n        p=later[:1]\n        need(p[0]['a8']==call['a8']and p[0]['a13']==call['a13']and p[0]['frame']==call['frame']and int(p[0]['a3'],16)==word+slot,"),
 ("    extra=[p for p in packets if p not in [x['packet']for x in bound]]",
  "    need(len({tuple(sorted(x['packet'].items()))for x in bound})==24,'No native dispatch packet attributed twice')\n    extra=[p for p in packets if p not in [x['packet']for x in bound]]"),
 ("    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(original.__file__).resolve()):sha(original.__file__)}",
  "    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(original.__file__).resolve()):sha(original.__file__),str(ROOT/'tools/verify_scorpion_secondary_native_audio_v4698.py'):sha(ROOT/'tools/verify_scorpion_secondary_native_audio_v4698.py'),str(ROOT/'audit_v4699_scorpion_secondary_native_audio_checked/report.json'):sha(ROOT/'audit_v4699_scorpion_secondary_native_audio_checked/report.json')}"),
]
for before,after in changes:
    assert source.count(before)==1,before
    source=source.replace(before,after)
exec(compile(source,__file__+'::whole4698_immediate_dispatch_attribution','exec'),globals())
