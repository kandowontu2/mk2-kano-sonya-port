"""Four inspected native checkpoints bound to unchanged earned-action traces."""
import json,re
import verify_native_source_sync as sync
import qualify_morphed_victims_secondary_pairs as pairs
import qualify_morphed_secondary_body_retirement as body

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_morphed_sonya_orb_visual_checked';assert not out.exists()
    lua=sync.ROOT/'audit_morphed_sonya_orb_visual_preparation/finishers.lua'
    cases={};total=0;gate=pairs.make_gate('sonya',18,'FFD7B000')
    for side in (1,2):
        folder=sync.ROOT/f'audit_morphed_sonya_orb_visual_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['observerSha256']==sync.sha(lua)
        assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
        assert not (folder/'stderr.log').read_text().strip()
        text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
        lines=[l for l in text.splitlines() if l.startswith('MK2_STOCK_HEAD_V921_')]
        original=sync.ROOT/f'audit_morphed_victim_secondary_sonya_sonya_p{side}_runtime/run.log'
        original_lines=[l for l in original.read_text().splitlines() if l.startswith('MK2_STOCK_HEAD_V921_')]
        assert [l for l in lines if not l.startswith('MK2_STOCK_HEAD_V921_VISUAL_SAVED ')]==original_lines
        rows=[(l.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in lines]
        proof=gate(rows,'sonya',18,side,[]);hide=body.body_gate(rows,'sonya',18,side)
        saved=[r for t,r in rows if t=='VISUAL_SAVED'];assert [r['age'] for r in saved]==['155','185']
        images=sorted(folder.rglob('*.png'));assert len(images)==2
        assert {p.name for p in images}=={'orb_155.png','orb_185.png'}
        assert not any(p.suffix.lower() in ('.bin','.wav') for p in folder.rglob('*'))
        size=sum(p.stat().st_size for p in images);assert size<=512*1024;total+=size
        cases[str(side)]=dict(proof=proof,bodyHide=hide,terminal=terminal,
            completeOriginalScalarTraceEqual=True,
            screenshotHashes={str(p):sync.sha(p) for p in images},pngBytes=size,
            visualReview='Viewed both actual PNGs: own transformed Sonya body inside orb at155; no remaining full victim body during burst at185. Performer remains own Sonya. Native edge cropping retained; no broad full-effect/art claim.')
    assert total<=1024*1024
    report=dict(passed=True,cases=cases,pngBytes=total,sourceSync=source_sync,
        fullEffectArtAccepted=False,fullPortAcceptance=False,
        scope='Four manually inspected bounded Sonya orb transformed-victim checkpoints on both player sides, tied to the entire unchanged earned-action scalar trace, true IDs and original body-hide mask. Not continuous pixels, all motion/palette/effect retirement/audio, other victims/arenas or full release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,inspectedImages=4,pngBytes=total,fullPortAcceptance=False)))

if __name__=='__main__':main()
