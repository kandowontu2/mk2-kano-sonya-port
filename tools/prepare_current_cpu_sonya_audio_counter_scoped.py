"""Use this case's generic physical strategy branch, not later mirror wrapper."""
from pathlib import Path
code=Path(__file__).with_name('prepare_current_cpu_sonya_audio_counter.py').read_text()
code=code.replace("needle='   if leg_tactic and other.roster==18 then'",'''needle="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"''')
code=code.replace('   elseif leg_tactic and other.roster==18 then','   elseif (leg_tactic or strategy==\'lowkick\'or strategy==\'throw\') and other.roster~=12 and other.roster~=13 then')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
