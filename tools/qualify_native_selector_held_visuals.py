"""Bind twelve actually viewed held/reference fields and exact backdrop pixels."""
import json
from pathlib import Path
import numpy as np
import qualify_native_selector_navigation as native
import capture_native_selector_held as capture
ROOT=capture.ROOT
OUT=ROOT/'audit_native_selector_held_visuals_checked'
VIEWED=json.loads(r'''{
  "current": [
    {
      "index": 1,
      "header": {
        "seq": "2",
        "label": "held_age80",
        "frame": "781",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "8E5759937370724EA9D4129E7DB47574BC26375C11159B829744B6B605EEF5B0"
    },
    {
      "index": 2,
      "header": {
        "seq": "3",
        "label": "held_age96",
        "frame": "797",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "789A63A527126707483450049CC225C9F7FDB828C769E8F98F1450384D666A1D"
    },
    {
      "index": 3,
      "header": {
        "seq": "4",
        "label": "held_age112",
        "frame": "813",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "341BEFF58F626BAC2C01F57BDC58E7952E41F201A5236B8BB4CF8194865C47A7"
    },
    {
      "index": 4,
      "header": {
        "seq": "5",
        "label": "held_age128",
        "frame": "829",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "0063909E0EEB33F3AFF780EF74684ADCC496B55E47A5942CBDBCACC50AB73D53"
    },
    {
      "index": 11,
      "header": {
        "seq": "12",
        "label": "held_age360",
        "frame": "1061",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "814998BB72630C1C614D01BE9CBD0983898D9177599AD524FCBD9834702AC6C1"
    },
    {
      "index": 14,
      "header": {
        "seq": "15",
        "label": "match_intro",
        "frame": "1468",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "1454E933A9CC235F509BC851AE77312C0FBEFFCE3FE3A2E039AF5883DF6FC0D3"
    }
  ],
  "classic": [
    {
      "index": 1,
      "header": {
        "seq": "2",
        "label": "held_age80",
        "frame": "781",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "FD1BFAB84340FF7788193C2DEA598AA7E81D6B955586CABAB3B46B7DB48EF437"
    },
    {
      "index": 2,
      "header": {
        "seq": "3",
        "label": "held_age96",
        "frame": "797",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "EBE455FB90510C6A3734DC12A944667DEF7BE27E896849499CA509A13A425D47"
    },
    {
      "index": 3,
      "header": {
        "seq": "4",
        "label": "held_age112",
        "frame": "813",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "81DE9A92BB8125E2B6DC3BA08AC0FB0D783E1FD64BB652DBA8A43588AB444BAD"
    },
    {
      "index": 4,
      "header": {
        "seq": "5",
        "label": "held_age128",
        "frame": "829",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "C4711EBC0928D9C1B7CEC6B6BAE2D3BC02540437A79130CC2105DF5291B1932F"
    },
    {
      "index": 11,
      "header": {
        "seq": "12",
        "label": "held_age360",
        "frame": "1061",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "F489D084DC915D9D02C61BA512C301BED4BF952C19F27B574542DDEDA9AC4EF3"
    },
    {
      "index": 14,
      "header": {
        "seq": "15",
        "label": "match_intro",
        "frame": "1492",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "3E849C4387D0918BEA0D81C387F83C1C8042922B604D493E063CB4B6E2491A8C"
    }
  ]
}''')

def verify(ram):
    need,sha=native.need,native.sha
    need(not OUT.exists() and not capture.original.startup.initial.identity.census(),'Fresh visual proof, original native games terminal')
    proof_path=ROOT/'audit_native_selector_held_checked/report.json'
    proof=json.loads(proof_path.read_text())
    need(proof==ram['heldTimingReport'] and proof['passed'] and
         proof['finiteBothSlotsNativeHeldAndReleasedSelectionTimingAccepted'] and
         len(proof['actualFaultsRejected'])==2408 and not proof['fullPortAcceptance'],
         'Actual full finite current-versus-stock held/released timing proof')
    pins=dict(proof['inputHashes']);count=0;backdrops=[]
    for mode,rows in VIEWED.items():
        held=ram['cases'][mode]
        need(held['process'].poll()==0 and held['terminal']['nativeExit']==0,'Original same actual native handles terminal')
        for row in rows:
            actual=held['images'][row['index']]
            need(actual['header']==row['header'] and actual['SHA256']==row['SHA256'] and
                 native.digest(actual['raw'])==row['SHA256'] and
                 actual['image'].tobytes()==native.Image.frombytes('RGB',(400,254),actual['raw'],'raw','BGRX').tobytes(),
                 'Exact complete actual native fields already individually viewed')
            count+=1
    for index in (1,2):
        current=ram['cases']['current']['images'][index]
        stock=ram['cases']['classic']['images'][index]
        need(current['header']==stock['header'],'Same actual frame/label/size for shared stock selection phase')
        a=np.asarray(current['image']);b=np.asarray(stock['image'])
        mask=np.ones((254,400),dtype=bool)
        mask[20:98,20:82]=False;mask[20:98,320:382]=False
        need(int(mask.sum())==91928 and np.array_equal(a[mask],b[mask]),
             'ALL91928 pixels outside dedicated added portrait rectangles exactly equal original MK2, including both full pose backdrops, stock previews, cursor borders/numbers')
        backdrops.append(dict(index=index,frame=current['header']['frame'],exactOriginalPixels=91928,
            currentSHA256=current['SHA256'],originalStockSHA256=stock['SHA256'],
            originalComparedPixelSHA256=native.digest(b[mask].tobytes()),
            currentComparedPixelSHA256=native.digest(a[mask].tobytes())))
    need(count==12,'All twelve current/reference native fields actually reviewed')
    for path in (Path(__file__),proof_path,ROOT/'tools/read_native_selector_held.py',
                 ROOT/'tools/read_native_selector_held_remote.py'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All frozen actual native timing/models/logs/readers unchanged')
    report=dict(passed=True,actualHumanViewedNativeFields=VIEWED,actualReviewedFields=12,
        actualExactStockBackdropAndSharedPreviewComparisons=backdrops,
        finiteBothSlotsHeldReleasedOwnSelectionAndMatchVisualsAccepted=True,
        nativeHeldRepeatTimingMatchesOriginalMK2=True,
        noWholeScreenOrPoseBackdropShiftInComparedNativeFields=True,
        selectionAcrossContinuesAccepted=False,fullGroundShadowMatrixAccepted=False,
        audioAccepted=False,allMovesAccepted=False,allFinishersAccepted=False,
        fullTowerEndingFreshJoinAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['heldVisualReport']=report
    print(json.dumps(dict(passed=True,actualViewedFields=12,exactStockBackdropPixelsPerComparedField=91928,
        fullPortAcceptance=False)),flush=True)
    return report

