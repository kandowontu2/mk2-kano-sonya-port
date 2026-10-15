"""Same complete4670 bounded native probe with corrected executable preflight."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=(ROOT/'tools/run_ending_clear_beam_probe_ram_v4670.py').read_text()
for before,after in(
  ('qualify_ending_clear_beam_source_v4671','qualify_ending_clear_beam_source_v4675'),
  ('audit_v4672_ending_clear_beam_source_checked','audit_v4677_ending_clear_beam_source_checked'),
  ('audit_v4673_{fighter}_ending_clear_beam_probe_ram','audit_v4678_{fighter}_ending_clear_beam_probe_ram'),
  ('audit_v4674_kano_ending_clear_beam_probe_observed','audit_v4679_kano_ending_clear_beam_probe_observed')):
    assert source.count(before)==1;source=source.replace(before,after)
scope=dict(__name__='qualified_clear_capture_4676',__file__=__file__)
exec(compile(source,__file__+'::whole4670_corrected_preflight_only','exec'),scope)
globals().update({key:value for key,value in scope.items()if not key.startswith('__')})
if __name__=='__main__':main()
