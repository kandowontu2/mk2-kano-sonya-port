"""Fresh bounded census after executed cleanup and updated package, not arithmetic."""
from pathlib import Path
source = Path(__file__).with_name('census_cleanup_candidates_20261015.py')
text = source.read_text()
old = "out = R/'audit_cleanup_candidate_census_20261015'"
assert text.count(old) == 1
text = text.replace(old, "out = R/'audit_after_cleanup_and_package_census_20261015'")
exec(compile(text, str(source), 'exec'))
