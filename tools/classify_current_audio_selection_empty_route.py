"""Parser omits empty values; explicitly verify the raw empty-route transcript."""
from pathlib import Path
source=Path(__file__).with_name('classify_current_audio_selection_transition.py').read_text()
old="'route':continued['path']"
assert source.count(old)==1
source=source.replace(old,"'route':continued.get('path','')")
source=source.replace("assert continued['continue']==loss['frame'] and continued['number']=='2'", "assert continued['continue']==loss['frame'] and continued['number']=='2'\nassert 'number=2 initial=18 target=18 path= continue=4206' in (folder/'run.log').read_text()")
source=source.replace('audit_current_audio_selection_transition_classification','audit_current_audio_selection_empty_route_classification')
exec(compile(source,__file__+'::verified empty route','exec'))
