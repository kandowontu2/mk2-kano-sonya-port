"""Finish the actual capture comparison without replaying the terminal game."""
import json
import traceback
from pathlib import Path
import capture_native_selector_sonya_pressure_palette as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_palette_bound_checked'
FAILURE=capture.OUT/'failure.json'


def execute():
    need(not OUT.exists(), 'Fresh immutable actual comparison successor')
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error']==
         "ValueError('The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()')" and
         sha(capture.__file__)=='6CAEF14BB6EF8325F80827C861EE2E052F8002F9ED9741063A7E749B3D9BAB93',
         'Actual array-comparison failure and executed source preserved')
    handle=capture.NATIVE_HANDLES[capture.KEY]
    need(handle['process'].poll()==0 and handle['identity']['ProcessId']==35924 and
         not capture.parent.original.census.identity.census(),
         'Same actual35924 terminal handle, never restart for checker failure')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    native=json.loads((folder/'result.json').read_text())
    need(native['passed'] and native['nativeExit']==0, 'Original whole native capture already passed')
    parent=json.loads(capture.parent.OUT.read_text());pins=dict(parent['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()) and capture.sync.verify()['passed'],
         'Whole earlier source/current evidence and source sync unchanged')
    previous=capture.previous
    tags=('MK2_EFFECT_','MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_',
          'MK2_CPU_OVERLAP_','MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_',
          'MK2_STARTUP_PROJECTILE_','MK2_SONYA_HORIZONTAL_','MK2_MAUDIO_',
          'MK2_TOMB_MIX_','MK2_BBAUDIO_PCM_DIGEST ','MK2_NATIVE_DAC_RAM_DIGEST ','MK2_HPHASE_')
    old_text=previous.RAM_CASES[previous.KEY][1]
    need([s for s in text.splitlines() if s.startswith(tags)]==
         [s for s in old_text.splitlines() if s.startswith(tags)],
         'Every original effect/control/health/choice/shadow/audio event identical')
    old_images=previous.RAM_CASES[previous.KEY][2]
    need(images.keys()==old_images.keys() and len(images)==143 and all(
        images[k].shape==old_images[k].shape and images[k].dtype==old_images[k].dtype and
        images[k].tobytes()==old_images[k].tobytes() for k in images),
        'Every whole actual sparse RGB raster and shape/dtype identical')
    for key in ('pcmChunks','pcmHeaders','dacChunks','dacHeaders','rom'):
        need(capture.AUDIO[capture.KEY][key]==previous.AUDIO[previous.KEY][key],
             'Whole actual sound evidence identical: '+key)
    need(all('MK2_PAL_'+tag+' ' in text for tag in ('WRITE','OWNER','CACHE','RESULT')),
         'Actual missing palette stores and owner assignments present')
    for p in (Path(__file__),Path(capture.__file__),capture.LUA,FAILURE,
              *(p for p in folder.rglob('*') if p.is_file())):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,
            'No executed source/original failure/current evidence rewritten');pins[key]=h
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        originalCapture=native,actualSparseRGBRasters=143,actualArrayComparisonFailurePreserved=True,
        allOriginalNativeEventsIdentical=True,allOriginalPCMandDACBytesIdentical=True,
        inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        paletteReferenceArithmeticAccepted=False,allHiddenPaletteOwnersAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,
        newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    return value


def safe_execute():
    try:return execute()
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual comparison successor failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
