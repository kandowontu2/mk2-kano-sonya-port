"""Finite current selector/confirmation/ladder visuals, with original MK2 reference."""
import json
from pathlib import Path
import qualify_native_selector_layers_ui as current

ROOT,need,sha,digest=current.ROOT,current.need,current.sha,current.digest
OUT=ROOT/'audit_native_selector_layers_visuals_checked'
REVIEWED={
 'sonya_p1_kano_p2_two_confirm370':{
  1:'4C49A7B87C8ED96F61A242DE16EF9EE6E463DFC928A2D7367ABFC439AB1B65A5',
  6:'7E7A21BF7AF3AAC4AE86CFE673A2BFA6B5FF15B7FECF061A991C7A45ECAD0E59',
  19:'85329D2C89FAA0237DC56D3963F23BD42F2B45BEE2EB9136B555E9D1B99FEE86',
  23:'774DB2C78F3B3E80D30CAF4DA732E3D7F8DA8676E9E514594C3FE90BA4F6BC8B',
  27:'ABDA1E8488CD75FC79CFEFEACC3C8105DB45A304BE455FF8FD9E989B96A868A6',
  38:'2D30BC9D86541FB32453578A9ABE226DEC142CA3A1A3C519117D455EC6624747'},
 'kano_p1_sonya_p2_two_confirm370':{
  1:'C7C0D34771304D310B9CD176B6B2A286F22910C719ECA1D38310A58EF5EEFC1E',
  6:'CD77105C9E3ECAB8531DE57A37E5687183FEB5476472A1CCFB98DEB7A45BE77D',
  11:'DECF00999BCB3028CEE3BAACE2ED25A0403B6EA64B5FA370631EABDC13042E10',
  19:'FCD098BC48364378E59660CBD21052A7DB845B5D646CD3797199BDFAA798F113',
  23:'5E03D47E23D81D9FAB56B813BC2F01B8D27613D39955D000331E5BB3FC370166',
  27:'84FC00D271AD538B8648FCE9D040BA364491A714A55C14F9E992278A8C448FA7'},
 'kano_p1_stock_p2_ladder_confirm96':{
  18:'8DB90D07B068562BA982D26451BEF6DECC014C2B4450A25BAD9596CC37120ED2',
  19:'2ED4291C5DFF023D7BB609C416862B0070681C2753A1B579554F229A06A41772',
  25:'AED29A3960641EE54082F67076BF39D7574754D9158735647B4CD5689A973E38',
  30:'13E6DB4FB4B5BDD80C3E0EFB09D2769772B61210E3687F0F25D1391B4D17268F',
  35:'512ED5ECFCF9F0FB1C6A626A1B10B5F78EE4F74733729469003041ED138939BB',
  39:'EE82C082A35D7171A0A910F0FA0F81F28E7C060FFA757A6E8D1B66051D52C95F'},
 'sonya_p1_stock_p2_ladder_confirm96':{
  18:'42525D5176578503CB4FDC006C1D3B6BDB04E1812BAF4A012D550251A8C0A9D8',
  19:'B45DBD974F02E6EA508365A53B9255F289F4096796C36E59D0BEEC55AEF7AD59',
  25:'C4846A6DB95ECFCCFF02F9611B16DF4657DF9582C27C199E02FF384532B6500E',
  30:'74B85EC94B49482669F214BCFB044152DC9F8D972BB0C9A97D1EDD9A7502D2B5',
  35:'49D28137A60D47246F73F1D2F1AE7593F44C5858E594E6D57F265343FB6CDA3F',
  40:'E707BA35C539BD6E27A729AC79F8FE2EA51B84598E32A0B797535AB207095721'}}
CLASSIC_VIEWED={
 19:'0411A3BFD2D81BF8DE0CBB785D4FAF1DEC2C1DD9364C55255BBA25E9512B48B4',
 20:'19FC64FC00F4C553A62978DE741B667A750FCED7FD4C4C6E5B5279775952D37C',
 21:'CFDDAEDC6300B4B7CC81F05D44C9142DB92E223C15DDD960E5C9DEB38EF44A93',
 25:'CFDDAEDC6300B4B7CC81F05D44C9142DB92E223C15DDD960E5C9DEB38EF44A93',
 30:'896BCF7E93200ACD0696065E423DF60D567059343826870128B5C59105A05AC9',
 35:'9EED4D076033E28DC0701D545A3AB1335A71252CE1D79E13FC58652965CE3CC7'}

def verify(ram):
    need(not OUT.exists() and not current.census.census(),'Fresh finite visual receipt; all original native games terminal')
    finite_path=current.OUT/'report.json';finite=json.loads(finite_path.read_text())
    need(finite==ram['finiteLayerUIReport'] and finite['passed'] and len(finite['actualFaultsRejected'])==32 and
         finite['finiteConfirmedPhotoPixelOcclusionAndNativeNumberLayeringAccepted'] and not finite['fullPortAcceptance'],
         'Exact four standard/two confirmed current native gates, not transport alone')
    classic_path=ROOT/'audit_native_classic_selector_reference_loaded/report.json'
    classic=json.loads(classic_path.read_text())
    need(classic['passed'] and classic['nativeExit']==0 and classic['driver']=='mk2' and
         classic['actualUnmodifiedFullStockProgramSHA256']=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Actual separate original MK2 reference binds every original1MiB program byte')
    pins=dict(finite['inputHashes']);viewed={};active_equal={}
    for case,records in REVIEWED.items():
        held=ram['cases'][case];need(held['process'].poll()==0,'Same original native handle terminal')
        viewed[case]=[]
        for index,wanted in records.items():
            frame=held['images'][index]
            need(frame['SHA256']==wanted==digest(frame['raw']) and
                 frame['image'].tobytes()==current.capture.original.Image.frombytes('RGB',(400,254),frame['raw'],'raw','BGRX').tobytes(),
                 'Each human-reviewed exact full native raster unchanged')
            viewed[case].append(dict(index=index,header=frame['header'],SHA256=wanted))
        if case.endswith('370'):
            old_case=case.removesuffix('_confirm370')
            old_path=ROOT/'audit_native_anchor_ui_ram'/old_case/'report.json';old=json.loads(old_path.read_text())
            need(all(held['images'][i]['SHA256']==old['actualNativeRasters'][i]['SHA256']for i in (1,6)),
                 'Actual complete active highlight/blink RGB unchanged, including backdrop/registration/pose')
            active_equal[case]=[dict(index=i,SHA256=held['images'][i]['SHA256'])for i in (1,6)]
            pins[str(old_path.resolve())]=sha(old_path)
    for index,wanted in CLASSIC_VIEWED.items():
        need(classic['actualNativeRasters'][index]['SHA256']==wanted,'Original stock transition reference actually viewed')
    # All four sheets were inspected: native 1/2/borders/poses and confirmed
    # hands behind new top photos; old CSS photos/poses/numbers disappear at
    # the ladder boundary; only the correct small own ladder icon remains.
    # The original mk2 reference independently exhibits the same category of
    # first-transition-field grid/palette flash. No pixel-identical whole first
    # field claim is made: the extra palettes change its uninitialized colors.
    for proof in (classic,):
        for p,h in proof['inputHashes'].items():need(sha(p)==h and (p not in pins or pins[p]==h),'All actual classic reference inputs unchanged');pins[p]=h
    for p in (Path(__file__),finite_path,classic_path,ROOT/'tools/read_native_selector_layers_ui.py',
              ROOT/'tools/read_native_selector_layers_ui_remote.py',ROOT/'tools/read_native_classic_selector_reference.py',
              ROOT/'tools/read_native_classic_selector_reference_remote.py'):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All current/reference source/ROM/observation pins unchanged')
    report=dict(passed=True,finiteCurrentOwnSelectionConfirmationAndLadderVisualsAccepted=True,
        actualHumanReviewedCurrentNativeFrames=viewed,actualHumanReviewedOriginalStockFrames=CLASSIC_VIEWED,
        currentActiveWholeRGBEqualsPredecessor=active_equal,
        ownNumbersOneAndTwoAndNativeBlinkBordersActuallyViewed=True,ownPreviewPosesAnimateWithoutBackdropShiftInViewedPhases=True,
        confirmedOwnRaisedArmNoLongerOverlaysTopPortrait=True,correctSmallOwnLadderIconsActuallyViewed=True,
        CSSPortraitPoseNumberAbsentAtObservedLadderBoundary=True,bothTrueOwnNativeMatchEntriesAccepted=True,
        firstTransitionGridPaletteFlashAlsoObservedInOriginalStockGame=True,
        firstTransitionFieldPixelIdenticalToStockClaimed=False,fullEveryFrameTransitionRasterAccepted=False,
        allNavigationEdgesAccepted=False,allContinuesLaddersCinematicsAccepted=False,
        fullGroundShadowMatrixAccepted=False,audioAccepted=False,allMovesAccepted=False,allFinishersAccepted=False,
        fullTowerAccepted=False,fullPortAcceptance=False,inputHashes=pins,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['finiteVisualLayerReport']=report
    print(json.dumps(dict(passed=True,currentNativeFramesViewed=24,originalStockFramesViewed=6,finiteSelectionLadderVisualsAccepted=True,fullPortAcceptance=False)),flush=True)
    return report
