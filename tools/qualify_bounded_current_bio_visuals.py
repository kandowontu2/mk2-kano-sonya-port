"""Four inspected bio/demo checkpoints, unchanged natural scalar trace."""
import json,re
import verify_native_source_sync as sync
import qualify_bounded_current_attract_bios as prior

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_bounded_current_bio_visual_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_current_bio_visual_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    lua=sync.ROOT/'audit_bounded_current_bio_visual_preparation/attract.lua'
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
    lines=[l for l in text.splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
    baseline=sync.ROOT/'audit_bounded_current_attract_long_runtime/run.log'
    assert [l for l in lines if not l.startswith('MK2_LIGHT_ATTRACT_VISUAL_SAVED ')]==[l for l in baseline.read_text().splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
    rows=[(l.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in lines]
    proof=prior.gate(rows)
    saved=[r for t,r in rows if t=='VISUAL_SAVED']
    assert [r['label'] for r in saved]==['17_early','17_late','18_early','18_late']
    for r in saved:
        ident,phase=r['label'].split('_')
        assert int(r['frame'])==proof[ident]['frame']+(100 if phase=='early' else 1100)
    pngs=sorted(folder.rglob('*.png'))
    assert {p.name for p in pngs}=={'bio_'+r['label']+'.png' for r in saved} and len(pngs)==4
    size=sum(p.stat().st_size for p in pngs);assert size<=1024*1024
    assert not any(p.suffix.lower() in ('.bin','.wav') for p in folder.rglob('*'))
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,nativeBios=proof,
        originalScalarTraceUnchanged=True,pngBytes=size,
        images={str(p):sync.sha(p) for p in pngs},
        inspectedCheckpointReview='Viewed all four actual native images. Early screenshots: own Kano/Sonya portraits, centered yellow own names, properly broken readable story text inside stock biography panels. Late screenshots: native Kano-versus-Cage and Sonya-versus-Kitana CPU demos, correct visible bodies and labels, no leftover biography panels/portraits. Four checkpoints only, not entire pixel/audio/demo lifecycle acceptance.',
        fullBioVisualAudioAccepted=False,fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,inspectedImages=4,pngBytes=size,fullPortAcceptance=False)))

if __name__=='__main__':main()
