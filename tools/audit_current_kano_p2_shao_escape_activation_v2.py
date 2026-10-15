"""Zero escape attempts is distinct from rejected jump input or broken character."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_kano_p2_shao_escape_activation.py').read_text()
source=source.replace('audit_current_kano_p2_shao_escape_activation_checked','audit_current_kano_p2_shao_escape_activation_v2_checked')
source=source.replace('assert plans and entries','assert not plans and not entries # actual retained trace has neither; preserve v1 incorrect assumption')
source=source.replace('passedFiniteActivationChecks=True,','passedFiniteActivationChecks=True,noPhysicalEscapeAttemptObserved=True,failedJumpInputClaimSupported=False,')
exec(compile(source,__file__+'::zero_attempt_scope','exec'))
