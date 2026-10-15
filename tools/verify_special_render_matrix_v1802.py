"""Complete bounded positive eight-special body/shadow/continuous-clear matrix.

Two human slots, original Sub-Zero victim, arena zero, one earned command per
fixture; plus both airborne square-wave contacts. Not all victims/arenas,
interrupts, repeated moves, artistic grounding, audio or whole-game acceptance.
"""
import json
from pathlib import Path
from verify_human_special_phases_v1767 import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1802_special_full_render_matrix_checked'

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    pins={};cases=[]
    def pin(path,h=None):
        path=str(Path(path).resolve());expected=h or sha(path)
        if path in pins:assert pins[path]==expected,'Conflicting immutable pin'
        else:assert sha(path)==expected,'Changed captured evidence '+path;pins[path]=expected
    for move in('knife','ball','blade','choke','ring','square','bicycle','leg'):
        for side in(1,2):
            stem=ROOT/f'audit_v1800_human_{move}_p{side}_render'
            rpath=Path(str(stem)+'_checked')/'report.json';cpath=Path(str(stem)+'_continuity_checked')/'report.json'
            if move=='ball':
                stem=ROOT/f'audit_v1806_human_ball_p{side}_render'
                rpath=ROOT/f'audit_v1807_human_ball_p{side}_render_checked/report.json'
                cpath=ROOT/f'audit_v1809_human_ball_p{side}_continuity_checked/report.json'
                if side==2:rpath=ROOT/'audit_v1811_human_ball_p2_render_checked/report.json'
            if move=='leg'and side==1:
                stem=ROOT/'audit_v1796_human_leg_p1_render'
                rpath=ROOT/'audit_v1797_human_leg_p1_render_checked/report.json'
                cpath=ROOT/'audit_v1799_human_leg_p1_continuity_checked/report.json'
            cases.append((stem,rpath,cpath,move,side,False))
    for side in(1,2):
        stem=ROOT/f'audit_v1800_human_square_air_p{side}_render'
        cases.append((stem,Path(str(stem)+'_checked')/'report.json',Path(str(stem)+'_continuity_checked')/'report.json','square',side,True))
    records=[]
    for folder,rpath,cpath,move,side,air in cases:
        r=json.loads(rpath.read_text());c=json.loads(cpath.read_text());pin(rpath);pin(cpath)
        assert r['passed']and c['passed']and r['move']==move and r['side']==side and r['air']==air
        assert r['candidate']=='diagnostic_v1597_native_ground_throw'
        n=r['exactConsecutiveScanouts']
        assert r['exactNativeReplayedPasses']==c['continuousExactPreBuffers']==c['continuousExactFlips']==n
        assert not r['heldOriginalScanouts']and c['oneInitialBaseOnly']and not c['laterBuffersUsedAsAnchors']and not c['guestWrites']
        assert c['shiftLoads']==c['shiftFills']==n+1 and c['nativeShiftTransfers']==127*(n+1)
        assert r['currentPositiveConsecutiveNativeRenderAccepted']and not r['fullPortAcceptance']and not c['fullPortAcceptance']
        for report in(r,c):
            for p,h in report['inputHashes'].items():pin(p,h)
        records.append(dict(move=move,side=side,air=air,frames=n,nativeCompositeDraws=r['actualPhysicalCompositeDraws'],
          sourceBoundNativeClippedParts=r.get('sourceBoundNativeClippedParts',0),nativeLowOrFullyCulledBodyFrames=r.get('nativeLowOrFullyCulledBodyFrames',[]),
          shadowCopies=r['nativeShadowCopies'],shadowComponents=r['nativeShadowComponents'],
          nativeShiftTransfers=c['nativeShiftTransfers'],nativeOwnedPaletteChecks=r['fullOwnedPaletteChecks'],
          renderReport=str(rpath),renderReportSHA=pins[str(rpath.resolve())],continuityReport=str(cpath),continuityReportSHA=pins[str(cpath.resolve())]))
    upath=ROOT/'audit_v1810_continuous_erase_units_checked/report.json';u=json.loads(upath.read_text());pin(upath)
    assert u['passed']and u['mutationCount']==18 and u['mutationsInMemoryOnly']and not u['guestWrites']
    for p,h in u['sourceHashes'].items():pin(p,h)
    baseline=Path(u['baselineReport']);pin(baseline,u['baselineHash'])
    pin(__file__)
    report=dict(passed=True,candidate='diagnostic_v1597_native_ground_throw',cases=records,fixtureCount=len(records),
      consecutiveFullScenes=sum(r['frames']for r in records),sourceBoundBodyDraws=sum(r['nativeCompositeDraws']for r in records),
      exactNativeShadowCopies=sum(r['shadowCopies']for r in records),nativeShiftTransfers=sum(r['nativeShiftTransfers']for r in records),
      sourceBoundNativeClippedParts=sum(r['sourceBoundNativeClippedParts']for r in records),
      nativeOwnedPaletteChecks=sum(r['nativeOwnedPaletteChecks']for r in records),negativeContinuityCasesRejected=18,
      allEightSpecialsBothSlotsPositiveRasterShadowAndEraseAccepted=True,airborneSquareBothSlotsAccepted=True,
      allVictimArenaDefenseRepeatedMoveAcceptance=False,universalArtisticGroundingAcceptance=False,audioAcceptance=False,
      fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
