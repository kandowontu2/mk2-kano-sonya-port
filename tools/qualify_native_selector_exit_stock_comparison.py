"""Retained stock exit and current native ladder teardown, without new games.

The exact comparison is the two 80px side backdrops (40,640 RGB pixels),
not the different native inner grid or character-specific ladder portraits.
"""
import hashlib,json,os,re
from pathlib import Path
import qualify_native_selector_layers_ui as original

ROOT=original.ROOT
STOCK_OUT=ROOT/'audit_native_selector_exit_stock_reference_checked'
OUT=ROOT/'audit_native_selector_exit_stock_comparison_checked'
VIEWS=ROOT/'audit_native_selector_exit_stock_actual_views.json'
need,sha=original.need,original.sha
EXPECTED='2FEE793645DBEF08F9429B8CF23DB405810107B4CEAF1A10B5E9313F8BF9A468'

def outer(image):
    return image.crop((0,0,80,254)).tobytes()+image.crop((320,0,400,254)).tobytes()

def whole_frames(held,records):
    need(held['process'].poll()==0 and held['identity']==held['report']['actualNativeIdentity'], 'Same original terminal native handle')
    frames=held['images']
    need(len(frames)==len(records), 'Entire original raster inventory')
    for f,r in zip(frames,records):
        need(f['header']==r['header'] and original.digest(f['raw'])==f['SHA256']==r['SHA256'], 'Every complete original BGRX digest')
        need(f['image'].tobytes()==original.capture.original.Image.frombytes('RGB',(400,254),f['raw'],'raw','BGRX').tobytes(), 'Every pixel decoded from its original raw scanout')

def execute_stock(ram):
    need(os.getpid()==37792 and not STOCK_OUT.exists(), 'Original stock host, immutable new receipt')
    report=ram['report'];path=ROOT/'audit_native_classic_selector_reference_loaded/report.json'
    need(json.loads(path.read_text())==report and report['passed'] and report['nativeExit']==0 and report['driver']=='mk2', 'Actual stock terminal report unchanged')
    need(report['actualUnmodifiedFullStockProgramSHA256']=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23', 'Whole unmodified stock program captured, not a port reference')
    pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Original complete stock source and ROM proof intact')
    whole_frames(ram,report['actualNativeRasters'])
    views=json.loads(VIEWS.read_text())['stock']
    need(views['actualNativeIdentity']==ram['identity'] and [f['index']for f in views['selectedFrames']]==[19,20,21], 'Three actually inspected original stock exit/blank/ladder callbacks')
    for f in views['selectedFrames']:
        need(f['header']==ram['images'][f['index']]['header'] and f['SHA256']==ram['images'][f['index']]['SHA256'], 'Viewed stock callback bound to whole original pixel digest')
    value=outer(ram['images'][19]['image'])
    need(len(value)==121920 and hashlib.sha256(value).hexdigest().upper()==EXPECTED, 'Whole exact independently observed stock side backdrop')
    for p in (Path(__file__).resolve(),VIEWS,path,ROOT/'tools/read_native_classic_selector_reference.py',ROOT/'tools/read_native_classic_selector_reference_remote.py',ROOT/'tools/read_native_anchor_ui.py',ROOT/'tools/read_native_anchor_ui_remote.py'):
        pins[str(p)]=sha(p)
    STOCK_OUT.mkdir()
    result=dict(passed=True,actualNativeIdentity=ram['identity'],actualHostPID=os.getpid(),wholeUnmodifiedStockROM=report['actualUnmodifiedFullStockProgramSHA256'],
        allOriginalRastersVerified=len(ram['images']),actuallyViewedCallbacks=views['selectedFrames'],sideBackdropSHA256=EXPECTED,sideBackdropRGBBytes=121920,
        blankFrameSHA256=ram['images'][20]['SHA256'],inputHashes=pins,newNativeGames=0,newRawMediaFiles=0)
    original.capture.original.save(STOCK_OUT/'report.json',result)
    print('PASS original stock43 rasters/three viewed exit callbacks/exact side backdrop',flush=True)
    return result

def execute_layers(ram):
    need(os.getpid()==39892 and not OUT.exists(), 'Original current UI host; immutable new receipt')
    stock_path=STOCK_OUT/'report.json';stock=json.loads(stock_path.read_text())
    need(stock['passed'] and all(sha(p)==h for p,h in stock['inputHashes'].items()), 'Actual independently retained stock proof intact')
    positive_path=original.OUT/'report.json';positive=json.loads(positive_path.read_text())
    need(positive==ram['finiteLayerUIReport'] and positive['passed'] and len(positive['actualFaultsRejected'])==32,
         'Entire preceding six-case native UI/layer/teardown and32-fault proof unchanged')
    need(all(sha(p)==h for p,h in positive['inputHashes'].items()), 'Complete source/compiled/current cold-window pins intact')
    views=json.loads(VIEWS.read_text());accepted={}
    for fighter,descriptor in (('kano','FFFF2A00'),('sonya','FFFF2B00')):
        case=fighter+'_p1_stock_p2_ladder_confirm96';held=ram['cases'][case]
        disk=json.loads((original.capture.OUT/case/'report.json').read_text())
        need(disk==held['report'] and disk['nativeExit']==0, 'Same untouched native UI result')
        whole_frames(held,disk['actualNativeRasters'])
        assessed=original.previous.assess(disk['nativeControllerResults'])
        need(assessed['MK2KS_EXIT_RESULT']['pass']=='true', 'Whole original physical exit/combat/identity/name/leak/stability contract')
        selected=views[fighter]['selectedFrames']
        need([r['index']for r in selected]==[19,21,39] and views[fighter]['actualNativeIdentity']==held['identity'], 'Only actually viewed exit/ladder/HUD callbacks claimed')
        for r in selected:
            need(r['header']==held['images'][r['index']]['header'] and r['SHA256']==held['images'][r['index']]['SHA256'], 'Actual inspected native whole pixels bound')
        value=outer(held['images'][19]['image'])
        need(len(value)==stock['sideBackdropRGBBytes'] and hashlib.sha256(value).hexdigest().upper()==stock['sideBackdropSHA256'], 'All40,640 side backdrop pixels exactly stock, including cleared added-icon locations')
        need(held['images'][20]['SHA256']==stock['blankFrameSHA256'], 'Entire following clear screen exactly stock, no retained added portrait/pose')
        depths={};done={}
        for line in held['text']:
            if line.startswith('MK2_ANCHOR_UI_DEPTH '):
                r=original.previous.fields(line);depths.setdefault(int(r['seq']),[]).append(r)
            elif line.startswith('MK2_ANCHOR_UI_DEPTH_COMPLETE '):
                r=original.previous.fields(line);done[int(r['seq'])]=r;depths.setdefault(int(r['seq']),[])
        need(set(depths)==set(done)==set(range(len(held['images']))) and all(int(done[i]['count'])==len(depths[i])for i in depths), 'Every complete native list, including empty teardown lists')
        exit_frame=int(assessed['MK2KS_EXIT_RESULT']['exit']);hud_frame=int(held['images'][39]['header']['frame'])
        checked=[]
        for i,f in enumerate(held['images']):
            if exit_frame<=int(f['header']['frame'])<hud_frame:
                need(all(r['descriptor']not in ('FFFF2800','FFFF2900','FFC09B30','FFC09BA0') and r['id']not in ('0011','0012')for r in depths[i]), 'Every observed exit/ladder list clears added CSS photos, native player marker and preview bodies')
                checked.append(i)
        portrait=[r for r in depths[21]if r['descriptor']==descriptor and r['x']=='0080'and r['y']=='005E']
        need(len(portrait)==1 and portrait[0]['id']=='0000', 'Correct dedicated native ladder descriptor at player portrait location, no fighter proxy')
        accepted[fighter]=dict(actualNativeIdentity=held['identity'],entireOriginalRasters=len(held['images']),actuallyViewedCallbacks=selected,
            exitSideBackdropPixelsExactlyStock=40640,wholeNextBlankScreenExactlyStock=True,nativeCSSObjectsAbsentAtCallbacks=checked,
            actualNativeLadderDescriptor=portrait[0],entirePhysicalControllerResult=assessed)
    pins=dict(positive['inputHashes']);pins.update(stock['inputHashes'])
    for p in (Path(__file__).resolve(),VIEWS,positive_path,stock_path,ROOT/'tools/read_native_selector_layers_ui.py',ROOT/'tools/read_native_selector_layers_ui_remote.py'):
        pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'All existing compiled/source/runtime evidence unchanged')
    OUT.mkdir();result=dict(passed=True,goalStatus='active',thisGoalTurnClassification='progress',actualCases=accepted,inputHashes=pins,
        suspectedPurpleExitBackdropIsStockBehavior=True,entireInnerGridStockEqualityClaimed=False,finiteNativeLadderTeardownAndDedicatedPlayerPortraitAccepted=True,
        allCampaignLaddersAccepted=False,allVisualsAccepted=False,fullPortAcceptance=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False)
    original.capture.original.save(OUT/'report.json',result)
    print('PASS retained Kano/Sonya stock-exact side backdrop/blank screen/native ladder icons/teardown/real match contracts; full port remains active',flush=True)
    return result
