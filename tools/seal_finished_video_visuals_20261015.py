"""Seal the actual final Sonya image review after independent AV completion."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_finished_video_delivery_20261015'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()

def main():
    target=OUT/'root_visual_completion.json';assert not target.exists()
    report=json.loads((OUT/'report.json').read_text());assert report['passed'] and report['allFourActualAVFilesDecoded']
    assert len(report['requestedVideos'])==4 and report['sonyaActualNativeLogMatchesQualifiedBenchmark']
    final=ROOT/'video_sonya_final_20261015'
    names=['review_actual_selection.png','review_ladder.png','review_first_fight.png','review_shao.png','review_ending1.png','review_ending2.png']
    images=[dict(file=name,sha256=sha(final/name)) for name in names]
    for item in report['requestedVideos']:assert sha(Path(item['file']))==item['sha256']
    review=dict(passed=True,supersedesPendingVisualFlagIn='report.json',AVReportSHA256=sha(OUT/'report.json'),imagesActuallyViewed=images,observations=dict(selection='Dedicated native Sonya portrait with player2 number and border; selected Sonya body visible.',ladder='Native Sonya ladder portrait; selector body/player-number art not overlaid on the ladder.',firstFight='Actual Sonya mirror with distinct native palette and Sonya lifebar names.',shao='Actual Shao body defeated, Sonya wins and correct Sonya winner body.',ending1='Sonya own portrait and narrative about escaping Shao empire and finding Jax.',ending2='Sonya own agency portrait and narrative about warning commanders and forming an agency; existing small native top-edge black rectangle retained, not edited out.'),reviewScope='Six sampled real final-recording images, not a claim of manual review of every frame. Aspect fix was H264/container metadata only; no gameplay frame or audio edits.',showcaseVisualReviewAlreadySealed=True,allRequestedVideoRequirementsSatisfied=True,remainingRequiredWork=[],allRecordingAndEncodingProcessesTerminal=True)
    target.write_text(json.dumps(review,indent=2)+'\n')
    lines=['FINISHED VIDEO DELIVERY - 2026-10-15','',
      'COMPLETE MOVE SHOWCASES:18chapters each, native audio, labels below game.',
      'videos_showcase_20261015/kano_complete_showcase/Kano_Complete_Moves_and_Finishers_VERIFIED.mp4',
      'videos_showcase_20261015/sonya_complete_showcase/Sonya_Complete_Moves_and_Finishers.mp4','',
      'FULL CURRENT-BUILD PLAYTHROUGHS:both bosses and both own ending pages.',
      'video_kano_full_20261015/Kano_full_playthrough.mp4 (22m58.55s;6paidlosses/continues)',
      'video_sonya_final_20261015/Sonya_full_playthrough.mp4 (53m51.57s;30paidlosses/continues)','',
      'Full games are automated native-control runs. All losses/continues retained.',
      'No health/AI/difficulty/RNG/state edits, cheats or fabricated winning cuts.',
      'Both full games have correct4:3 display metadata. All four AV files decoded.',
      'Showcases cover every special, fatality, Friendship, Babality, DeadPool/',
      'Tomb/PitII finish, listed shared basic and both Shang morph commands.',
      'Actual Sonya native log matches the qualified full campaign exactly.',
      'Temporary WAV/video-only and label-render intermediates removed; no archive.','',
      'Proof: audit_finished_video_delivery_20261015/report.json and',
      'audit_finished_video_delivery_20261015/root_visual_completion.json.','',
      'PUBLIC CODE: https://github.com/kandowontu2/mk2-kano-sonya-port',
      'Source-only: exact15file emulator overlay, upstream diff, tooling/history,',
      'change/build/test/video documentation. No ROMs, ripped media or binaries.','']
    (ROOT/'VIDEO_DELIVERY_2026-10-15.txt').write_text('\n'.join(lines))
    print(target)

if __name__=='__main__':main()
