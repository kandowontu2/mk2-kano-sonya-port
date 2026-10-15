"""Same full true-ID/native chronology gate, exact prior20k progressing prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_liu_standing.py').read_text()
source=source.replace('audit_current_kano_p2_liu_standing','audit_current_kano_p2_campaign_32000')
source=source.replace('audit_current_kano_p2_subzero_low_knife_runtime','audit_current_kano_p2_liu_standing_runtime')
source=source.replace("if tag not in ('KANO_P2_LIU_DAMAGE','KANO_P2_LIU_STANDING'):","if tag not in ('HOST_BOUND','RESULT'):")
source=source.replace("int(r['frame'])<8510","int(r['frame'])<20000")
source=source.replace("records['RESULT'][0]['frame']=='20000'","records['RESULT'][0]['frame']=='32000'")
source=source.replace('priorEarnedPrefixUnchangedThrough=8509','priorEarnedPrefixUnchangedThrough=19999')
exec(compile(source,__file__+'::same_earned_campaign_gate','exec'))
