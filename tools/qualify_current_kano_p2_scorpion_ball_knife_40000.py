"""Direct true-ID chronology gate plus unchanged prior32k record prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_liu_standing.py').read_text()
source=source.replace('audit_current_kano_p2_liu_standing','audit_current_kano_p2_scorpion_ball_knife_40000')
source=source.replace('audit_current_kano_p2_subzero_low_knife_runtime','audit_current_kano_p2_scorpion_ball_knife_runtime')
source=source.replace("if tag not in ('KANO_P2_LIU_DAMAGE','KANO_P2_LIU_STANDING'):","if tag not in ('HOST_BOUND','RESULT'):")
source=source.replace("int(r['frame'])<8510","int(r['frame'])<32000")
source=source.replace("records['RESULT'][0]['frame']=='20000'","records['RESULT'][0]['frame']=='40000'")
source=source.replace('priorEarnedPrefixUnchangedThrough=8509','priorEarnedPrefixUnchangedThrough=31999')
source=source.replace('proof=gate(rows)',"proof=gate(rows)\nproof['scorpionOwnRoundWins']=[r for r in rows['WIN'] if r['stage']=='6' and r['slot']=='2']\nproof['scorpionMatchCleared']=7 in proof['earnedStages']")
exec(compile(source,__file__+'::native_campaign_gate','exec'))
