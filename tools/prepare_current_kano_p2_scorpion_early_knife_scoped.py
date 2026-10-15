"""Preserve failed ambiguous matcher; select Scorpion-only exact condition."""
from pathlib import Path
source=Path(__file__).with_name('prepare_current_kano_p2_scorpion_early_knife.py').read_text()
source=source.replace("'other.hp<=33 and ready'","'elseif other.hp<=33 and ready then'")
source=source.replace("'other.hp<=55 and ready'","'elseif other.hp<=55 and ready then'")
exec(compile(source,__file__+'::scorpion_only_condition','exec'))
