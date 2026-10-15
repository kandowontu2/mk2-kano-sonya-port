"""Full native Sub-Zero Leg Grab body/shadows, including stock raw reaction.

Entire original entry/body/actor/projection/pen/cadence/ROM/fault gate retained.
Only the exact native10x48 stock raw reaction gains source-derived original
signed-header scanning. No imported raw stream or arbitrary raw sprite allowed.
"""
import copy,inspect,json
from pathlib import Path
import verify_current_subzero_special_shadow_v5302 as context
import verify_special_shadow_v5141 as original
import native_stock_raw_shadow_scanner_v5315 as scanner
ROOT,need,sha=context.ROOT,context.need,context.sha
def replace_once(text,before,after):
    need(text.count(before)==1,'Exact sole source substitution: '+before)
    return text.replace(before,after,1)
def bindings():
    main=context.bindings()
    previous=main.__globals__['check']
    source=inspect.getsource(original.check)
    source=replace_once(source,'ids={side:identity,3-side:4}','ids={side:identity,3-side:8}')
    start="  if not c&128:\n"
    end="  need(t['compressedRowStreamVerified']and t['streamFormat']=='compressed6','Every imported shadow stream remains strictly compressed')"
    need(source.count(start)==source.count(end)==1,'Unique complete old stock raw branch and strict imported compressed gate')
    a,b=source.index(start),source.index(end)
    old=source[a:b]
    source=source[:a]+"  if not c&128:\n   if graphic==0x01457742:\n"+''.join(' '+line+'\n'for line in old.splitlines()[1:])+"   decoded[key]=stock_raw_starts(graphic,w,h,c,gfx,t);continue\n"+source[b:]
    source=replace_once(source,
      "originalStockSmallRawStreams=[k for k,t in streams.items()if not num(t,'command')&128]",
      "originalStockSmallRawStreams=[k for k,t in streams.items()if not num(t,'command')&128 and num(t,'height')==6],originalStockRawReactionStreams=[k for k,t in streams.items()if not num(t,'command')&128 and num(t,'height')==48],originalStockRawReactionNativeScannerRowsSourceBound=True")
    scope=dict(previous.__globals__,stock_raw_starts=scanner.stock_raw_starts)
    exec(compile(source,__file__+'::entire_original_native_shadow_gate_plus_exact_stock_raw_source','exec'),scope)
    check=scope['check']
    source=replace_once(inspect.getsource(original.main),
      'audit_v5142_special_shadow_{args.move}_p{args.side}_checked',
      'audit_v5318_current_stock_raw_reaction_shadow_{args.move}_p{args.side}_sub_zero_checked')
    source=replace_once(source," need(all(sha(p)==h for p,h in pins.items()),'Every final source/evidence/native input stable')",
      " faults.extend(raw_faults(b,guest,payload,gfx,check))\n need(all(sha(p)==h for p,h in pins.items()),'Every final source/evidence/native input stable')")
    def reconstruct(pins):
        qualified=ROOT/'audit_v5316_original_stock_raw_shadow_scanner_source_checked/report.json'
        proof=json.loads(qualified.read_text())
        need(proof['passed']and proof['sourceOnly']and proof['currentOriginalShadowKernelByteExact']and
          proof['originalUnconditionalHeaderAndSignedWidthAdvanceQualified']and
          all(sha(p)==h for p,h in proof['inputHashes'].items()),
          'Entire original native scanner disassembly/whole ROM/current kernel qualified before comparing actual rows')
        for p in (Path(__file__),Path(context.__file__),Path(scanner.__file__),qualified):pins[str(p.resolve())]=sha(p)
        return main.__globals__['reconstruct'](pins)
    scope=dict(main.__globals__,__file__=__file__,check=check,reconstruct=reconstruct,raw_faults=raw_faults)
    exec(compile(source,__file__+'::entire_original_all11faults_plus6actual_stock_raw_faults','exec'),scope)
    return scope['main']
def raw_faults(b,guest,payload,gfx,check):
    need(b['move']=='leg','This actual new context only, not arbitrary raw body admission')
    rawindex=next(i for i,t in enumerate(b['streams'])if t['graphic']=='0251F2DC'and t['command']in('6000','6010'))
    projection=next(t for t in b['rows']['MK2_HPHASE_PROJECTION']if t['graphic']=='0251F2DC')
    rows=b['rows']['MK2_HPHASE_SHADOW_DMA']
    indices=[i for i,t in enumerate(rows)if t['frame']==projection['frame']and t['cache_row']==projection['row']]
    need(len(indices)==13,'Exact native48quarterheight plus duplicate-tail reaction copies observed')
    tests=[]
    for label,key,value in (
      ('actual_raw_ROM_bytes_wrong','sha256','0'*64),
      ('actual_raw_falsely_compressed','compressedRowStreamVerified',True),
      ('actual_raw_descriptor_width_changed','width','11'),
      ('actual_raw_fake_compressed_row_proof','actualRowStarts',[0])):
        bad=copy.deepcopy(b);need(bad['streams'][rawindex][key]!=value,'Every raw fault changes an actual record')
        bad['streams'][rawindex][key]=value;tests.append((label,bad))
    for label,index,key,value in (
      ('actual_raw_intermediate_source_wrong',indices[1],'source',f"{int(rows[indices[1]]['source'],16)^1:08X}"),
      ('actual_raw_duplicate_tail_wrong',indices[-1],'source',f"{int(rows[indices[-1]]['source'],16)^1:08X}")):
        bad=copy.deepcopy(b);need(bad['rows']['MK2_HPHASE_SHADOW_DMA'][index][key]!=value,'Every native raw row fault is an actual change')
        bad['rows']['MK2_HPHASE_SHADOW_DMA'][index][key]=value;tests.append((label,bad))
    faults=[]
    for label,bad in tests:
        try:check(bad,guest,payload,gfx)
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual stock raw source-row fault accepted: '+label)
    need(check(b,guest,payload,gfx)['originalStockRawReactionNativeScannerRowsSourceBound'],
      'Complete untouched actual native control restored after every real raw-source fault')
    return faults
if __name__=='__main__':bindings()()
