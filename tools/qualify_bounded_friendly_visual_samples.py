"""Pin the twelve viewed samples; do not certify mislabeled clearing frames."""
import json
from PIL import Image
from qualify_bounded_current_friendships import validate as validate_friend
from qualify_bounded_current_babalities import validate as validate_baby
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_friendly_visual_samples_checked'
assert not out.exists()
reports=[]
total=0
for kind in ('friendship','babality'):
    validator=validate_friend if kind=='friendship' else validate_baby
    for fighter in ('kano','sonya'):
        case=sync.ROOT/f'audit_bounded_visual_{kind}_{fighter}_p1_runtime'
        original=sync.ROOT/f'audit_bounded_current_{kind}_{fighter}_p1_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        assert not (case/'stderr.log').read_text().strip()
        text=(case/'run.log').read_text()
        validator(text,fighter,1)
        prefix='MK2_FRIEND_' if kind=='friendship' else 'MK2_NATIVE_BABY_'
        lines=[line for line in text.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'VISUAL_SAVED')]
        baseline=[line for line in (original/'run.log').read_text().splitlines() if line.startswith(prefix)]
        assert lines==baseline, 'Visual sampling changed controller/mechanics observations'
        images=list((case/'snap').rglob('*.png'))
        assert len(images)==3
        samples=[]
        for path in images:
            with Image.open(path) as image: assert image.size==(400,254)
            total+=path.stat().st_size
            samples.append({'path':str(path),'sha256':sync.sha(path),'bytes':path.stat().st_size})
        reports.append({'fighter':fighter,'kind':kind,'side':1,'manualReview':'Expected own action/baby and names visible; no selection portraits over arena. Late sample labelled post_scene is still cinematic, NOT clearing proof.','samples':samples,'terminal':terminal})
out.mkdir()
(out/'report.json').write_text(json.dumps({'finiteViewedSamples':12,'totalPngBytes':total,'mechanicsUnchanged':True,'completeAnimationAcceptance':False,'transitionClearingAcceptance':False,'audioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
print(f'PASS: twelve viewed finite samples, {total} PNG bytes; scene clearing/audio not certified')
