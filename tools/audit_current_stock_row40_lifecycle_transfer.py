"""Conserve accepted repaired biography lifecycle; do not relabel secret scope."""
import json,re,hashlib
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
old=R/'diagnostic_stock_slideshow_row40/input_sources/mame-mkp';new=R/'mame-mkp'
def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def clean(s):return re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S)
a=(old/'src/mame/midway/midtunit_m.cpp').read_text();b=(new/'src/mame/midway/midtunit_m.cpp').read_text()
start='constexpr unsigned ending_text_tables[2]';end='// The two-player BATTLE card'
x,y=section(a,start,end),section(b,start,end)
assert clean(x)==clean(y)
assert '0xff8f48f0), 41 * 4' in y and 'unsigned index = 41; index < 50' in y
equal={}
for f in ['src/mame/midway/mk2ks_native_picture.h','src/mame/midway/midtunit_v.cpp','src/mame/midway/midtunit_v.h','src/devices/cpu/tms34010/tms34010.cpp']:
 assert sync.sha(old/f)==sync.sha(new/f);equal[f]=sync.sha(new/f)
loader=lambda r:section((r/'src/mame/midway/midtunit.cpp').read_text(),'ROM_START( mk2ks )','ROM_END')
assert loader(old)==loader(new)
case='audit_natural_smoke_route_sonya_p2_stock_row40_repair_full_route'
reg=json.loads((R/case/'native_stock_row40_regression.json').read_text());vis=json.loads((R/case/'native_stock_row40_visual_geometry.json').read_text())
assert reg['passed'] and reg['resetRouteAccepted'] and vis['passed']
loaded=json.loads((R/'audit_current_loaded_stock_photo_pointers_checked/report.json').read_text());assert loaded['original41StockPhotoPointersExactlyLoaded'] and loaded['row40Preserved']
out=R/'audit_current_stock_row40_lifecycle_transfer_checked';assert not out.exists();out.mkdir()
report=dict(correctedBiographyComponentTransferAccepted=True,exactRepairedGeneratorIgnoringComments=True,unchangedRendererDecoderCPU=equal,unchangedROMLoader=True,currentLoadedAll41PointersAccepted=True,
 historicalActualLookupFrame=reg['actualLookup']['frame'],historicalActualHeader=reg['actualHeader']['A8'],historicalNativeDecoderReturnFrame=reg['actualNativeReturn']['frame'],historicalPostReturnFields=reg['postReturnFields'],historicalVisiblePhotoPixelsPerFrame=vis['completeOriginalPhotoPixelsPerVisibleFrame'],historicalGeometryFaults=vis['exactNativeGeometryFaultsRejected'],
 scope='Accepted repaired late JohnnyCage row40 biography native decode/return/visiblephoto lifecycle transfers at exact component level; current loaded41 pointers close pointer-install gap. Whole old secret controller route not transferred as whole new runtime; current Kano/Sonya secret return and paid reselect acceptance retained separately.',
 directCurrentRow40DecoderRuntimeObserved=False,lateResetReproductionRequiredForComponentProof=False,
 nextSmallOptionalRuntimeCheck='Input-free coldboot bounded passive row40 lookupFFFA4D00/PCFF8447E0→headerFF903640/A8=058B1BC0→returnFF844860 and watchdog progression+180fields. No secret replay prerequisite or forcedattract; classify NOTREACHED if biography not naturally selected within bound.',
 fullPortAccepted=False,inputHashes={case+'/native_stock_row40_regression.json':sync.sha(R/case/'native_stock_row40_regression.json'),case+'/native_stock_row40_visual_geometry.json':sync.sha(R/case/'native_stock_row40_visual_geometry.json')},sourceComponentSHA256=hashlib.sha256(clean(y).encode()).hexdigest().upper())
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(report=str(out/'report.json'),componentTransferAccepted=True,directCurrentLifecycle=False)))
