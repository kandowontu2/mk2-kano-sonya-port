"""Validate the complete authored sound-playlist chain before current checks."""
import hashlib
import json
from pathlib import Path

PORT=Path(__file__).resolve().parent
STAGES=('DCS_INPUTS.json','DCS_BIKE_INPUTS.json','DCS_ANNOUNCER_INPUTS.json',
        'DCS_KISS_INPUTS.json','DCS_KANO_POP_INPUTS.json','DCS_KANO_BALL_INPUTS.json','DCS_CHICKEN_INPUTS.json')

def verify_latest_playlist():
    previous=None
    for name in STAGES:
        stage=json.loads((PORT/'generated_dcs'/name).read_text())
        if previous is not None:
            assert stage['previousPlaylistSHA256']==previous,f'Broken sound stage: {name}'
        previous=stage['stagedPlaylistSHA256']
    path=PORT.parent/'baseline/mk2-rebuild-main/soundp/MK2.PLS'
    assert hashlib.sha256(path.read_bytes()).hexdigest().upper()==previous
    return previous
