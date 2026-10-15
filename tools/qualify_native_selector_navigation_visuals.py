"""Bind24 actually viewed native navigation fields to the terminal edge proof."""
import json
from pathlib import Path
import qualify_native_selector_navigation as native

ROOT=native.ROOT
OUT=ROOT/'audit_native_selector_navigation_visuals_checked'
VIEWED=json.loads(r'''{
  "right": [
    {
      "index": 2,
      "header": {
        "seq": "3",
        "label": "edge_p2_9_right",
        "frame": "776",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "4B9C394A2DD483B5FA37C32E1EFEA30179A663B90BF478A1C29C36B04FF0A5F4"
    },
    {
      "index": 4,
      "header": {
        "seq": "5",
        "label": "edge_p2_18_right",
        "frame": "788",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "08C01BDE60C046067EB40C1A5A997DA480B9234AC4E2A7AF71BE7590EA45AC1B"
    },
    {
      "index": 6,
      "header": {
        "seq": "7",
        "label": "edge_p1_9_right",
        "frame": "812",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "5ECB2C44FF324BCA5525E6AD2697B40263A97B2BAA9EAE7BE89994257AF66D94"
    },
    {
      "index": 8,
      "header": {
        "seq": "9",
        "label": "edge_p1_18_right",
        "frame": "824",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "1D5EF53A4AB877AC39B41662721CF6049637C7272940A4746ECA279605688591"
    },
    {
      "index": 26,
      "header": {
        "seq": "27",
        "label": "edge_p1_17_right",
        "frame": "1124",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "B178957905A030A1F5D63AA4C29418AFBDD70D021C276F61BE1B8EF0E53E1801"
    },
    {
      "index": 28,
      "header": {
        "seq": "29",
        "label": "edge_p2_17_right",
        "frame": "1184",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "634EA8CB8D3571D8BB5544A7F71C3B2FA8C3C5783C90857CD9DB1949BD7E3BD7"
    }
  ],
  "left": [
    {
      "index": 3,
      "header": {
        "seq": "4",
        "label": "edge_p1_17_left",
        "frame": "788",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "777D349F910274A4A4D3F891163D4BA511E515C6865CF0017EDD613AFF8A315C"
    },
    {
      "index": 8,
      "header": {
        "seq": "9",
        "label": "edge_p2_17_left",
        "frame": "824",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "A3FA04ED048BA81FB798F32E81A88B07D380B5EB110B319C6110487C16BB4614"
    },
    {
      "index": 21,
      "header": {
        "seq": "22",
        "label": "edge_p1_9_left",
        "frame": "1028",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "CC483D1DACC26344D2B8C1876076900072B225AB638458657CD608D1D4B3E888"
    },
    {
      "index": 27,
      "header": {
        "seq": "28",
        "label": "edge_p2_18_left",
        "frame": "1124",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "BDFFC56B934D25BC251B66B5519C61E386286F74E8F351255A66C932BAD58931"
    },
    {
      "index": 28,
      "header": {
        "seq": "29",
        "label": "edge_p1_18_left",
        "frame": "1184",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "7E00F967D6891D889DB72DF646535CF07994B120E1AAEC9257CE9A18FB69C448"
    },
    {
      "index": 31,
      "header": {
        "seq": "32",
        "label": "native_match_intro",
        "frame": "1648",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "1454E933A9CC235F509BC851AE77312C0FBEFFCE3FE3A2E039AF5883DF6FC0D3"
    }
  ],
  "down": [
    {
      "index": 2,
      "header": {
        "seq": "3",
        "label": "edge_p2_9_down",
        "frame": "776",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "89806DECF5287D9DB1D1EB75894114369417199218C294E546A87A36F7D1E6E2"
    },
    {
      "index": 19,
      "header": {
        "seq": "20",
        "label": "edge_p1_9_down",
        "frame": "980",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "7B1387041751E22911F0A26AA5BD6E76582725AA4B2F150B75B9BF2B7F2DD2C5"
    },
    {
      "index": 22,
      "header": {
        "seq": "23",
        "label": "edge_p2_17_down",
        "frame": "1016",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "7DB2BFB9E5255F7E310E9B3C0115B330C3E99C914F195E9BA745A57BF6755280"
    },
    {
      "index": 26,
      "header": {
        "seq": "27",
        "label": "edge_p1_17_down",
        "frame": "1100",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "906B360C2D949564F57224C1B4AD66192B3E742303AC792849F348757FC976A1"
    },
    {
      "index": 27,
      "header": {
        "seq": "28",
        "label": "edge_p2_18_down",
        "frame": "1136",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "F13D5779405E11D4885EF988719BF9F7ECB82C4EE7E5D1F2CFC3043675B57B84"
    },
    {
      "index": 28,
      "header": {
        "seq": "29",
        "label": "edge_p1_18_down",
        "frame": "1172",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "A78A853462A23793388B127BA33066D6E35E4D4791CCA29B53D255E518F2C5EF"
    }
  ],
  "up": [
    {
      "index": 3,
      "header": {
        "seq": "4",
        "label": "edge_p1_17_up",
        "frame": "800",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "24194579184257CB27307474AEBCF16A7734ED81A399E6F22A463EEE9F2BF5C7"
    },
    {
      "index": 10,
      "header": {
        "seq": "11",
        "label": "edge_p2_17_up",
        "frame": "872",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "D8FE7F6F15FE375B683190D3C6106FD7B91C99F28FC9989B6E6A8856CE4B763F"
    },
    {
      "index": 13,
      "header": {
        "seq": "14",
        "label": "edge_p1_18_up",
        "frame": "920",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "2A050CB521677F998D4B912101A593BD0A2865144508A3A3BEFAD852A4E5F571"
    },
    {
      "index": 18,
      "header": {
        "seq": "19",
        "label": "edge_p2_18_up",
        "frame": "1004",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "1BD864CE60611FBF0DA9A5C4BA6A7E77CA40C7B1D53977827A1D688A395DE01E"
    },
    {
      "index": 29,
      "header": {
        "seq": "30",
        "label": "css_exit",
        "frame": "1367",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "0830C4F3BCF1D57F58C4FCEB768D6867E9178C5DCE69B2318BCB63D262CE1D80"
    },
    {
      "index": 31,
      "header": {
        "seq": "32",
        "label": "native_match_intro",
        "frame": "1648",
        "width": "400",
        "height": "254",
        "bytes": "406400",
        "writes": "0",
        "assistance": "none"
      },
      "SHA256": "1454E933A9CC235F509BC851AE77312C0FBEFFCE3FE3A2E039AF5883DF6FC0D3"
    }
  ]
}''')

def verify(ram):
    need,sha=native.need,native.sha
    need(not OUT.exists() and not native.capture.startup.initial.identity.census(),'Fresh actual visual proof, all native games terminal')
    proof_path=native.OUT/'report.json'
    proof=json.loads(proof_path.read_text())
    need(proof==ram['navigationReport'] and proof['passed'] and
         proof['freshBothSlotsAll14CellsAllFourSinglePulseDirectionsAccepted'] and
         proof['actualDirectionalEdges']==112 and len(proof['actualFaultsRejected'])==672 and
         not proof['fullPortAcceptance'],'Actual complete finite physical-navigation proof')
    pins=dict(proof['inputHashes']);count=0
    for direction,selected in VIEWED.items():
        held=ram['cases'][direction]
        need(held['process'].poll()==0 and held['terminal']['nativeExit']==0,'Same original native handles remain actually terminal')
        for row in selected:
            actual=held['images'][row['index']]
            need(actual['header']==row['header'] and actual['SHA256']==row['SHA256'] and
                 native.digest(actual['raw'])==row['SHA256'] and
                 actual['image'].tobytes()==native.Image.frombytes('RGB',(400,254),actual['raw'],'raw','BGRX').tobytes(),
                 'Every actually viewed complete native raster/header/decoded field bound exactly')
            count+=1
    need(count==24,'All24 actually reviewed fields, not merely planned screenshots')
    for path in (Path(__file__),proof_path,ROOT/'tools/read_native_selector_navigation.py',
                 ROOT/'tools/read_native_selector_navigation_remote.py',ROOT/'tools/read_native_anchor_ui_remote.py'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All original accepted inputs/reports/readers immutable')
    report=dict(passed=True,actualHumanViewedCurrentNativeFrames=VIEWED,actualViewedNativeFrameCount=count,
        freshBothSlotAll112DirectionalEdgesAccepted=True,
        finiteOwnCellsBlockedEdgesDiagonalDownAndReptileSonyaRoundTripVisualsAccepted=True,
        ownPreviewActorsAndNativeNumberRegistrationsAccepted=True,
        observedSelectionObjectsClearedAtVersusAndCombat=True,
        finiteCurrentArmoryIntroOwnFeetAndFloorShadowsVisible=True,
        heldButtonRepeatAccepted=False,selectionAcrossContinuesAccepted=False,
        fullEveryFrameTransitionRasterAccepted=False,fullGroundShadowMatrixAccepted=False,
        audioAccepted=False,allMovesAccepted=False,allFinishersAccepted=False,
        fullTowerEndingFreshJoinAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['navigationVisualReport']=report
    print(json.dumps(dict(passed=True,actualViewedNativeFrames=count,
        actualDirectionalEdges=112,fullPortAcceptance=False)),flush=True)
    return report

