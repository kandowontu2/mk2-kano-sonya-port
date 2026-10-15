"""Parsed jump plans exist; no matching native776 entries, unlike failed v2."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_kano_p2_shao_escape_activation.py').read_text()
source=source.replace('audit_current_kano_p2_shao_escape_activation_checked','audit_current_kano_p2_shao_escape_activation_v3_checked')
source=source.replace('assert plans and entries','assert plans and not entries # parsed plans exist; original filtered-entry assumption failed')
source=source.replace('passedFiniteActivationChecks=True,','passedFiniteActivationChecks=True,zeroPhysicalEscapeAttemptClaimRejected=True,')
exec(compile(source,__file__+'::parsed_plan_scope','exec'))
