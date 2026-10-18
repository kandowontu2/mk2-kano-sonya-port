"""Verify the finite current demonstration set, without copying large assets."""
import csv
import hashlib
import json
import sys
from pathlib import Path
import zipfile
from verify_finisher_roms import verify
from refresh_stage_videos import verify_capture

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(with_normals=False):
    cases=[('special/'+kind,'stock_wolf_2219_video_'+kind) for kind in
           ('ball','blade','choke','leg','bike','square','knife','ring')]
    cases += [('lethal/'+kind,'stock_wolf_2219_lethal_video_'+kind) for kind in ('extract','laser','kiss','bubble')]
    cases += [(f'{kind}/{actor}',f'stock_wolf_2219_nonlethal_video_{kind}_{actor}')
              for kind in ('friend','baby') for actor in (17,18)]
    cases += [(f'{kind}/{actor}',f'stock_wolf_2219_stage_video_{kind}_{actor}_p1')
              for kind in ('deadpool','tomb') for actor in (17,18)]
    cases += [(f'pit/{actor}',f'stock_wolf_2219_pit_video_filtered_pit_{actor}_p1') for actor in (17,18)]
    cases += [(f'morph/{actor}',f'stock_wolf_2219_morph_video_{actor}') for actor in (17,18)]
    if with_normals:
        from refresh_normal_videos import plan as normal_plan
        cases += [(f'normal/{actor}/{label}',name) for name,actor,label,_ in normal_plan('stock_wolf_2219_normal_video')]
    assert len(cases)==len(set(key for key,_ in cases))==len(set(run for _,run in cases))==(58 if with_normals else 24)
    return cases

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()

def main(with_normals=False):
    cases=[]
    for key,name in plan(with_normals):
        run=BASE/name
        receipt=json.loads((run/'execution.json').read_text())
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==sha(run/'autoboot.lua')
        assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
        with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
        video=json.loads((run/'FINISHER_VIDEO.json').read_text())
        clip=Path(video['file'])
        assert clip==run/'native_finisher_v2.mp4'
        assert sha(clip)==video['SHA256'] and clip.stat().st_size==video['bytes']
        assert video['fullVideoAndAudioDecodePassed'] and video['nativeAudio']
        assert video['observerSHA256']==receipt['controllerSHA256']
        with (run/'finisher_capture.csv').open() as stream:rows=list(csv.DictReader(stream))
        frames=[int(r['frame']) for r in rows]
        assert frames==list(range(video['firstGuestFrame'],video['firstGuestFrame']+video['frames']))
        kind=key.split('/')[0]
        if kind in ('deadpool','tomb','pit'):verify_capture(run,kind)
        if kind in ('special','morph'):
            proof=json.loads((run/('CAPTURED_HIT_QUALIFICATION.json' if kind=='special' else 'CAPTURED_MORPH_QUALIFICATION.json')).read_text())
            assert proof['clipSHA256']==video['SHA256']
        if kind=='normal':
            proof=json.loads((run/'CAPTURED_NORMAL_QUALIFICATION.json').read_text())
            assert proof['clipSHA256']==video['SHA256'] and proof['twoStanceRecoveryObserved']
        cases.append(dict(key=key,run=name,file=str(clip),SHA256=video['SHA256'],
                          bytes=video['bytes'],frames=video['frames'],
                          receiptSHA256=sha(run/'execution.json'),captureSHA256=sha(run/'finisher_capture.csv')))
    report=dict(scope='Finite current native demonstrations, not full campaigns or all-frame audiovisual acceptance',
                cases=cases,totalBytes=sum(c['bytes'] for c in cases),
                allCurrent26ROMBytesVerified=True,fullPortVerified=False,releaseReady=False)
    (PORT/('NATIVE_VIDEO_CATALOG_FULL_2219.json' if with_normals else 'NATIVE_VIDEO_CATALOG_2219.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('Verified',len(cases),'current clips;',report['totalBytes'],'bytes; no media copies created.')

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--with-normals'])
    main(bool(sys.argv[1:]))
