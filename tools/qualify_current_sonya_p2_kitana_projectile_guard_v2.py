"""Correct wrapper's preparation pin; preserve wall-censored target-unobserved verdict."""
from pathlib import Path
wrapper=Path(__file__).with_name('qualify_current_sonya_p2_kitana_projectile_guard.py').read_text()
marker="exec(compile(source,__file__,'exec'))";assert wrapper.count(marker)==1
adapt="""
source=source.replace('audit_current_sonya_p2_kitana_ring_spacing_preparation/campaign.lua','audit_current_sonya_p2_kitana_projectile_guard_preparation/campaign.lua')
source=source.replace('audit_current_sonya_p2_kitana_projectile_guard_checked','audit_current_sonya_p2_kitana_projectile_guard_v2_checked')
source=source.replace('report=dict(passed=True,','report=dict(passed=True,targetKitanaEncounterObserved=bool(fights),targetPolicyUntested=not bool(fights),')
source=source.replace("('passed','ringPlans'", "('passed','targetPolicyUntested','ringPlans'")
"""
wrapper=wrapper.replace(marker,adapt+'\n'+marker)
exec(compile(wrapper,__file__,'exec'))
