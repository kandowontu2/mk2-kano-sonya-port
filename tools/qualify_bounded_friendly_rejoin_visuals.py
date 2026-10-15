"""Pin eight reviewed transition samples without whole-transition claims."""
import json
from PIL import Image
from qualify_bounded_friendly_rejoin import validate_rejoin
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_friendly_rejoin_visuals_checked'
assert not out.exists()
reports=[]
total=0
for kind in ('friendship','babality'):
    prefix='MK2_FRIEND_' if kind=='friendship' else 'MK2_NATIVE_BABY_'
    for fighter in ('kano','sonya'):
        case=sync.ROOT/f'audit_bounded_rejoin_visual_{kind}_{fighter}_p1_runtime'
        baseline=sync.ROOT/f'audit_bounded_rejoin_both_selectors_{kind}_{fighter}_p1_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        lua=sync.ROOT/f'audit_bounded_friendly_rejoin_visuals_preparation/{kind}.lua'
        assert terminal['observerSha256'].lower()==sync.sha(lua).lower()
        assert not (case/'stderr.log').read_text().strip()
        text=(case/'run.log').read_text()
        validate_rejoin(text,prefix,17 if fighter=='kano' else 18,1)
        actual=[line for line in text.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'REJOIN_VISUAL_SAVED')]
        expected=[line for line in (baseline/'run.log').read_text().splitlines() if line.startswith(prefix)]
        assert actual==expected,'Sampling changed observed mechanics'
        images=list((case/'snap').rglob('*.png'))
        assert len(images)==2
        samples=[]
        for path in images:
            with Image.open(path) as image: assert image.size==(400,254)
            total+=path.stat().st_size
            samples.append({'path':str(path),'sha256':sync.sha(path),'bytes':path.stat().st_size})
        reports.append({'fighter':fighter,'kind':kind,'side':1,'manualReview':'Native selection and new-match samples have no prior friendly-finisher baby/bubble/banner or selection portraits over arena; new match has expected added bodies and names.','samples':samples,'terminal':terminal})
out.mkdir()
(out/'report.json').write_text(json.dumps({'finiteViewedSamples':8,'totalPngBytes':total,'mechanicsUnchanged':True,'everyTransitionFieldAcceptance':False,'p2VisualAcceptance':False,'audioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
print(f'PASS: eight viewed P1 transition samples, {total} PNG bytes; not every-field/P2/audio certification')
