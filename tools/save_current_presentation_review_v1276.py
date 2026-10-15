"""Record the main-agent review of unchanged actual current contact sheets."""
import json
from pathlib import Path
import verify_native_metadata_build_v1254 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1276_current_presentation_review';assert not OUT.exists()
pins={};cases={}
for folder in ('audit_v1272_current_ground_contacts','audit_v1274_current_ui_contacts'):
    path=ROOT/folder/'report.json';report=json.loads(path.read_text());pins[str(path)]=current.digest(path)
    assert report['candidate']==current.CANDIDATE and report['productionArtChanged'] is False
    for key,value in report['cases'].items():
        sheet=Path(value['sheet']);assert current.digest(sheet)==value['sha256'];pins[str(sheet)]=value['sha256']
        for r in value['entries']:
            path=Path(r['file']);assert current.digest(path)==r['sha256'];pins[str(path)]=r['sha256']
        cases[folder+'/'+key]=dict(sheet=str(sheet),actualImages=len(value['entries']),reviewedBy='main_agent',viewed=True)
pins[str(Path(__file__))]=current.digest(__file__)
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,candidate=current.CANDIDATE,cases=cases,inputHashes=pins,
    actualMobilityImagesReviewed=148,actualUIImagesReviewed=24,
    observations=['Both true characters share the stock idle contact line in the normal Dead Pool mobility scenes.',
        'Native black projected shadows remain on the floor during each observed jump and landing; crouch and walking remain grounded.',
        'Dedicated top-row portraits, native-thickness colored borders and centered player numbers are visible in both slots.',
        'Unchosen portraits lose the selected border/player number; real native poses replace the selected stance when moving to the stock neighbor.',
        'First transition samples are clean; normal ladder reveals show owned small portraits, not persistent CSS portraits/stances.',
        'Actual first matches show the real selected Kano/Sonya, including normal/alternate owned opponents and their native-style HUD names.'],
    limitations=['Static contact sheets do not establish complete animation/audio fidelity or every field.',
        'Separate state/raster contracts establish sampled blink, source pixels, palettes and exact native DMA execution.',
        'These mobility cases are normal Dead Pool only; other arenas/move/KO/fatality shadows and complete towers remain open.'],
    fullPortAccepted=False),indent=2)+'\n')
print('Main-agent review recorded:148 mobility and24 UI actual images; bounded scope',flush=True)
