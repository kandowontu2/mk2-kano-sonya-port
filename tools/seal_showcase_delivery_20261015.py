"""Seal complete movelist coverage after root frame review and full AV decode."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'videos_showcase_20261015'
sp=importlib.util.spec_from_file_location('assembly',ROOT/'tools/assemble_move_showcases_20261015.py')
a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()

def main():
    receipt=BASE/'DELIVERY_VERIFICATION.json';assert not receipt.exists()
    cases=[];ff=shutil.which('ffmpeg')
    for fighter in ('kano','sonya'):
        folder=BASE/(fighter+'_complete_showcase')
        report=json.loads((folder/'verification.json').read_text())
        keys=['shang_'+fighter if x=='morph' else fighter+'_'+x for x in a.sequence(fighter)]
        assert report['passed'] and [x['key'] for x in report['chapters']]==keys and len(keys)==18
        clips=list(folder.glob('*.mp4'));assert len(clips)==1
        clip=clips[0];assert sha(clip)==report['finalSHA256']
        probe=report['probe'];video=next(x for x in probe['streams'] if x['codec_type']=='video')
        assert video['width']==800 and video['height']==680 and len(probe['chapters'])==18
        decode=subprocess.run([ff,'-v','error','-nostdin','-i',str(clip),'-map','0:v:0','-map','0:a:0','-f','null','NUL'],capture_output=True,timeout=30,creationflags=0x08000000)
        assert decode.returncode==0 and not decode.stderr
        assert not (folder/'labelled_intermediates').exists()
        cases.append(dict(fighter=fighter,file=str(clip),sha256=sha(clip),bytes=clip.stat().st_size,durationSeconds=float(probe['format']['duration']),chapters=keys,fullVideoAndAudioDecodePassed=True,rootLabelAndLayoutReview=str(folder/'review.png'),reviewImageSHA256=sha(folder/'review.png')))
    review={}
    for group in ('special','fatality','friendly','stage','basic','morph'):
        folder=BASE/('review_'+group)
        assert (folder/'sheet.png').is_file() and (folder/'index.json').is_file()
        review[group]=dict(sheetSHA256=sha(folder/'sheet.png'),index=json.loads((folder/'index.json').read_text()))
    # Explicit root observations from the sheets actually viewed this turn.
    observed=dict(specials='All8 actual effects/contact/recovery visible; airborne Square Wave observed.',fatalities='Skeleton extraction, laser burst, burning kiss and orb burst visible.',friendly='Both native babies; additional action frames show Kano bubble gum and Sonya gesture.',stage='Both added performers: DeadPool acid, Tomb ceiling impalement, Pit fall/impact and native retirement.',basic='Both actors uppercut/sweep/roundhouse/throw and standing/crouching guards visible.',morph='Native Shang-to-Kano/Sonya and restoration visible; HUD retains Shang name as native morph behavior.',finalLayout='Reviewed both labelled final screenshots: readable command bar below uncropped4:3 game picture.')
    receipt.write_text(json.dumps(dict(passed=True,scope='Complete full-movelist showcases, not full campaign completion',movelistSHA256=sha(ROOT/'MK2_KANO_SONYA_MOVES.txt'),characters=cases,rootSampledVisualReview=review,rootObserved=observed,entireFrameByFrameManualReviewClaimed=False,gameAndDifficultyChanged=False,guestStateWrites=False,sourceClipsRetained=True,labelledIntermediatesDeleted=True),indent=2)+'\n')
    print(json.dumps(cases,indent=2))

if __name__=='__main__':main()
