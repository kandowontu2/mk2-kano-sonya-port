"""Verify existing clean sound inputs, then independently stage the new pop."""
import contextlib
import io
import json
from pathlib import Path
import time
import sys
import extend_dcs_kano_pop as stage
ball=sys.argv[1:]==['--ball']
chicken=sys.argv[1:]==['--chicken']
assert sys.argv[1:] in ([],['--ball'],['--chicken'])
if ball:
    import extend_dcs_kano_ball as stage
stage_name='DCS_KANO_BALL_INPUTS.json' if ball else 'DCS_KANO_POP_INPUTS.json'
previous_name='DCS_KANO_POP_INPUTS.json' if ball else 'DCS_KISS_INPUTS.json'
region='KSKB' if ball else 'KSKP'
clip_count=12 if ball else 11
if chicken:
    import extend_dcs_chicken as stage
    stage_name='DCS_CHICKEN_INPUTS.json';previous_name='DCS_KANO_BALL_INPUTS.json';clip_count=16
from build_arm_rip_assets import sha

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
CLEAN=BASE/'clean_program'
CURRENT=BASE/'mk2-rebuild-main'
receipt_path=PORT/'CLEAN_SOUND_INPUTS.json'
inputs=json.loads(receipt_path.read_text())
prior=json.loads((PORT/'CLEAN_SOUND_QUALIFICATION.json').read_text())
assert prior['cleanSoundRebuildByteIdentical']
for name,digest in inputs['sourcePCM_SHA256'].items():
    assert sha((CLEAN/'soundp/SNDS'/name).read_bytes())==digest
for relative,digest in inputs['originalInputSHA256'].items():
    if relative not in ('MK2.LOC','MK2.PLS'):assert sha((CLEAN/'soundp'/relative).read_bytes())==digest
for item in prior['soundROMs']:assert sha((CLEAN/'soundp'/item['file']).read_bytes())==item['SHA256']
assert sha((CLEAN/'soundp/MK2.PLS').read_bytes())==inputs['playlistStages'][previous_name]
stage.DEST=CLEAN/'soundp';stage.OUT=CLEAN/'dcs_manifest'
with contextlib.redirect_stdout(io.StringIO()):stage.main()
new=json.loads((stage.OUT/stage_name).read_text())
working=json.loads((PORT/'generated_dcs'/stage_name).read_text())
assert new['stagedPlaylistSHA256']==working['stagedPlaylistSHA256']
if chicken:
    assert [clip['pcmSHA256'] for clip in new['clips']]==[clip['pcmSHA256'] for clip in working['clips']]
    assert all(not (stage.DEST/f'SNDS/{clip["region"]}.CMP').exists() for clip in new['clips'])
else:
    assert new['pcmSHA256']==working['pcmSHA256']
    assert not (stage.DEST/f'SNDS/{region}.CMP').exists()
(CLEAN/'SNDBUILD.BAT').write_bytes((CURRENT/'SNDBUILD.BAT').read_bytes())
own=list((stage.DEST/'SNDS').glob('*.SND'));assert len(own)==clip_count
inputs['playlistStages'][stage_name]=new['stagedPlaylistSHA256']
inputs.update(ownClipsRegenerated=clip_count,existingCleanDirectoryReused=True,
    newClipIndependentlyRegenerated=True,ownCompressedSamplesImported=False,
    existingSoundROMsImported=False,priorSoundOutputsVerifiedBeforeRebuild=True,
    freshBuildNotBeforeEpoch=time.time(),buildScriptSHA256=sha((CLEAN/'SNDBUILD.BAT').read_bytes()),
    sourcePCM_SHA256={p.name:sha(p.read_bytes()) for p in own})
receipt_path.write_text(json.dumps(inputs,indent=2)+'\n')
print(f'Verified previous clean inputs; independently staged clip{clip_count}. Awaiting clean sound build.')
