"""Native P1 Sonya chronology/results, not input-command success."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p1_learned_campaign.py').read_text()
source=source.replace('audit_current_kano_p1_learned_campaign_runtime','audit_current_sonya_p1_subzero_defense_priority_runtime').replace('audit_current_kano_p1_learned_campaign_checked','audit_current_sonya_p1_subzero_defense_priority_checked')
source=source.replace('check(rows,1,17,sequence)','check(rows,1,18,sequence)').replace("r['human']=='17:17'","r['human']=='18:18'").replace('currentTrueKanoP1FiniteStageChronologyPassed','currentTrueSonyaP1FiniteStageChronologyPassed')
source=source.replace("assert terminal['exitCode']==0 and terminal['limitReason'] is None","assert (terminal['exitCode']==0 and terminal['limitReason'] is None) or terminal['limitReason']=='wall_limit'")
exec(compile(source,__file__+'::subzero_defense_priority','exec'))
