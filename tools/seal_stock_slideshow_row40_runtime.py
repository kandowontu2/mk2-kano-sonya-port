"""Finite reviewed geometry/provenance; no full-port acceptance claim."""
import gzip
import hashlib
import inspect
import json
from pathlib import Path
import numpy as np
from PIL import Image
import qualify_stock_slideshow_row40_runtime as model


def geometry(image,photo,origin):
    matches=model.locate_photo(image,photo)
    model.need(matches==[origin],'Complete source photo at original native caller coordinates')
    return matches[0]


def seal(c):
    folder=c['folder']
    report=json.loads((folder/'native_stock_row40_regression.json').read_text())
    model.need(report['passed'] and report['resetRouteAccepted'] and not report['fullPortAcceptance'],
               'Actual finite successful replay, never whole-port/release acceptance')
    header=report['actualHeader']
    address=int(header['A10'],16)
    origin=[(address&0xfff)//8,address>>12]
    model.need(address==0x160e8 and origin==[29,22], 'Original caller picture destination')
    photo,_=model.photo_oracle()
    reviewed=[]
    for i,delay in ((41,20),(42,60),(43,180)):
        frame=c['rgbFrames'][i]
        model.need(frame['header']['stage']==f'stock_row40_visible{delay}.png' and
                   hashlib.sha256(frame['pixels']).hexdigest().upper()==frame['header']['sha256'],
                   'Entire actually viewed native RGB frame unchanged')
        image=np.asarray(Image.frombytes('RGB',(400,254),frame['pixels'],'raw','BGRX'))
        if delay==20:
            model.need(np.all(image==0),'Entire actually viewed early clearing page black')
        else:geometry(image,photo,origin)
        reviewed.append(frame['header'])
    faults=[]
    for label,bad in (('one actual photo pixel',image.copy()),('actual raster shifted one pixel',np.roll(image,1,axis=1))):
        if label=='one actual photo pixel':bad[origin[1]+79,origin[0]+69,0]^=1
        try:geometry(bad,photo,origin)
        except ValueError as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Actual native raster geometry fault accepted')
    archived={}
    files=(Path(model.__file__),Path(model.current.__file__),Path(model.source.__file__),
           Path(model.original.__file__),Path(model.original.prior.__file__),Path(model.decoder.__file__),
           Path(inspect.getsourcefile(model.locate_photo)),Path(__file__).resolve())
    for path in files:
        raw=path.read_bytes()
        archived[str(path.resolve())]=dict(sha256=hashlib.sha256(raw).hexdigest().upper(),text=raw.decode('utf-8'))
    archive=folder/'executed_runtime_qualification_sources.json.gz'
    model.need(not archive.exists(),'Fresh whole executed checker archive')
    with gzip.open(archive,'wt',encoding='utf-8') as f:json.dump(archived,f)
    result=dict(passed=True,actuallyViewedNativeFrames=reviewed,nativePhotoOrigin=origin,
                completeOriginalPhotoPixelsPerVisibleFrame=21804,exactNativeGeometryFaultsRejected=faults,
                observation='Native20-field clearing page black; complete original Johnny Cage biography visible at60/180fields with matching native name/frame/text. No selector artwork or picture shift.',
                entireExecutedQualificationSources=len(archived),archiveSHA256=model.current.sha(archive),
                originalFailedVisualCheckerPreserved=(folder/'executed_failed_visual_checker.json.gz').exists(),
                nativeResetRouteAccepted=True,fullPortAcceptance=False,publicPlayableChanged=False,
                newRawMedia=0,newROMCopies=0,newZIPs=0)
    path=folder/'native_stock_row40_visual_geometry.json'
    model.need(not path.exists(),'Fresh finite actual visual review')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(nativePictureGeometryAccepted=True,actualRasterFaultsRejected=2,
                         actuallyViewedFrames=3,newRawMedia=0,fullPortAcceptance=False)))
    return result
