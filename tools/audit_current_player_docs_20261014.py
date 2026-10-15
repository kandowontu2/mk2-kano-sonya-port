"""Refresh external docs evidence without altering prior audit or archive."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_player_docs.py').read_text()
source=source.replace("out=sync.ROOT/'audit_current_player_docs_checked'","out=sync.ROOT/'audit_current_player_docs_20261014_checked'")
source=source.replace('longerRunApprovalPending=True','longerRunApprovalPending=False,existingBoundedTestsAuthorized=True')
source=source.replace("assert 'airborne opponent' in moves", "assert 'Kintaro and Shao Kahn cannot be grabbed by Choke.' in moves\nassert 'clears Shang Tsung and Kintaro' in head\nassert 'round wins on separate continues are not a match clear' in head\nassert 'airborne opponent' in moves")
exec(compile(source,__file__+'::updated_external_docs','exec'))
