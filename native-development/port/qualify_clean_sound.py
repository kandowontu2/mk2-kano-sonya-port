"""Byte-compare clean original-tool sound rebuild, including own PCM inputs."""
import hashlib
import json
from pathlib import Path

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
CLEAN=BASE/'clean_program'
CURRENT=BASE/'mk2-rebuild-main'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
inputs=json.loads((PORT/'CLEAN_SOUND_INPUTS.json').read_text())
assert not inputs['ownCompressedSamplesImported'] and not inputs['existingSoundROMsImported']
assert (CLEAN/'SP_OK.TXT').read_text().strip()=='DONE'
assert not (CLEAN/'SPFAIL.TXT').exists()
for name,digest in inputs['sourcePCM_SHA256'].items():
    data=(CLEAN/'soundp/SNDS'/name).read_bytes()
    assert sha(data)==digest
    assert data==(CURRENT/'soundp/SNDS'/name).read_bytes()
assert len(inputs['sourcePCM_SHA256'])==inputs['ownClipsRegenerated']
last_stage='DCS_KANO_POP_INPUTS.json' if 'DCS_KANO_POP_INPUTS.json' in inputs['playlistStages'] else 'DCS_KISS_INPUTS.json'
if 'DCS_KANO_BALL_INPUTS.json' in inputs['playlistStages']:last_stage='DCS_KANO_BALL_INPUTS.json'
if 'DCS_CHICKEN_INPUTS.json' in inputs['playlistStages']:last_stage='DCS_CHICKEN_INPUTS.json'
assert sha((CLEAN/'soundp/MK2.PLS').read_bytes())==inputs['playlistStages'][last_stage]
if 'freshBuildNotBeforeEpoch' in inputs:
    assert sha((CLEAN/'SNDBUILD.BAT').read_bytes())==inputs['buildScriptSHA256']
    for name in inputs['sourcePCM_SHA256']:
        assert (CLEAN/'soundp/SNDS'/Path(name).with_suffix('.CMP')).stat().st_mtime>=inputs['freshBuildNotBeforeEpoch']-2
for relative,digest in inputs['originalInputSHA256'].items():
    if relative=='MK2.LOC':continue  # Original-tool generated placement output.
    if relative=='MK2.PLS':continue  # Authored extensions verified above.
    assert sha((CLEAN/'soundp'/relative).read_bytes())==digest
results=[]
for chip in range(2,6):
    name=f'U{chip}.ROM'
    clean=(CLEAN/'soundp'/name).read_bytes()
    current=(CURRENT/'soundp'/name).read_bytes()
    if 'freshBuildNotBeforeEpoch' in inputs:
        assert (CLEAN/'soundp'/name).stat().st_mtime>=inputs['freshBuildNotBeforeEpoch']-2
    assert len(clean)==len(current)==1048576
    results.append(dict(file=name,SHA256=sha(clean),currentSHA256=sha(current),identical=clean==current))
report=dict(scope=f"{inputs['ownClipsRegenerated']} own WAVs regenerated, recompressed and linked with original DCS tools",
    inputReceiptSHA256=sha((PORT/'CLEAN_SOUND_INPUTS.json').read_bytes()),
    ownPCMInputsByteIdentical=True,originalCMPInputsVerified=439,soundROMs=results,
    cleanSoundRebuildByteIdentical=all(result['identical'] for result in results),
    finalMixAccepted=False,sourceVoiceProvenanceFullyReviewed=False,fullRebuildVerified=False,
    gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'CLEAN_SOUND_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['cleanSoundRebuildByteIdentical'],'Investigate clean sound ROM mismatch'
