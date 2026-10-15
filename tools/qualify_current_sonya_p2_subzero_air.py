"""Finite16k air-policy chronology and exact whole opening trace."""
from pathlib import Path
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 old=chronology.load(sync.ROOT/'audit_current_sonya_p2_mirror_guard_runtime/run.log')
 new=chronology.load(sync.ROOT/'audit_current_sonya_p2_subzero_air_runtime/run.log')
 cutoff=int(old['STAGE'][1]['frame'])
 assert new['STAGE'][1]==old['STAGE'][1]
 for tag in set(old)|set(new):
  if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
  assert [r for r in old.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in new.get(tag,[]) if int(r['frame'])<cutoff]
 code=Path(__file__).with_name('qualify_current_sonya_p2_mirror_guard_native_wins.py').read_text()
 code=code.replace('audit_current_sonya_p2_mirror_guard_','audit_current_sonya_p2_subzero_air_')
 code=code.replace("code=code.replace('existing leg-grab controls'", "code=code.replace(\"'30000'\",\"'16000'\")\n    code=code.replace('existing leg-grab controls'")
 code=code.replace('historical physical mirror guard/leg sequence; existing leg elsewhere','actual grounded/flight-aware jumpkick policy for SubZero8; exact opening mirror route retained; existing leg elsewhere')
 exec(compile(code,__file__+'::native chronology','exec'),{'__name__':'__main__','__file__':__file__})
