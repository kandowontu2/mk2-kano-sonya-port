"""Scope chord change to KungLao branch, preserve successful opening."""
from pathlib import Path
source=Path(__file__).with_name('prepare_current_sonya_p2_kunglao_immediate_leg.py').read_text()
source=source.replace("source=(base/'campaign.lua').read_text()","source=(base/'campaign.lua').read_text()\nstart=source.index('   elseif leg_tactic and other.roster==0 then\\n')\nend=source.index(\"   elseif fighter=='sonya' and side==2\",start)\nprefix,tail=source[:start],source[end:]\nsource=source[start:end]")
source=source.replace("assert ':write_' not in source", "source=prefix+source+tail\nassert ':write_' not in source")
exec(compile(source,__file__+'::scoped_successor','exec'))
