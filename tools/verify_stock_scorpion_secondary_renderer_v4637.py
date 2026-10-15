"""Whole stock renderer: explicitly separate original font and floor row DMA.

Both use solid mode8. Original one-bit9008 text at FF804640 is not a floor
shadow. Keep every such operation in the whole pixel replay and account for
it separately, with source-bound graphics. No tolerance or dropped target.
"""
import inspect,json,re,subprocess,traceback
from pathlib import Path
import verify_stock_scorpion_secondary_renderer_v4625 as base
import verify_stock_scorpion_secondary_renderer_v4629 as final_row
import verify_stock_scorpion_secondary_renderer_v4633 as command_bits
ROOT,need,sha,CASE=base.ROOT,base.need,base.sha,base.CASE
OUT=ROOT/'audit_v4638_stock_kitana_scorpion_secondary_renderer_checked'
source=inspect.getsource(base.stock_shadow_rows)
changes=[
 ("int(r['a0'],16)==int(d['y'])","((int(r['a0'],16)+(d['pc']=='FF801610'))&511)==int(d['y'])"),
 ("r['a1']=='00000001'","int(r['a1'],16)==((int(d['command'],16)>>10)&3)"),
 ("native=[d for d in dmas if int(d['source'],16)<0x10000000 and int(d['command'],16)&15==8]",
  "solid=[d for d in dmas if int(d['source'],16)<0x10000000 and int(d['command'],16)&15==8]\n"
  "    fonts=[d for d in solid if d['command']=='9008']\n"
  "    need(all(d['pc']=='FF804640'and d['height']in ('11','15','16')and int(d['width'])>0 and d['palette']=='0000'and d['color']in ('1','2','15')and d['scaleX']==d['scaleY']=='256'and d['skip']=='0'for d in fonts), 'Every original one-bit solid text draw explicitly source/caller/shape bound, not silently excluded shadow DMA')\n"
  "    native=[d for d in solid if d['command']!='9008']\n"
  "    need(len(native)+len(fonts)==len(solid), 'Every stock-source solid DMA belongs to the explicit row/font ledger; all remain in whole pixel replay')")]
for before,after in changes:
    need(source.count(before)==1,'Only declared original stock operation semantics: '+before)
    source=source.replace(before,after,1)
namespace=dict(vars(base))
exec(compile(source,__file__+'::actual_original_row_and_font_ledger','exec'),namespace)
stock_shadow_rows=namespace['stock_shadow_rows']
scope=dict(vars(base),__file__=__file__,stock_shadow_rows=stock_shadow_rows)
exec(compile(base.text,__file__+'::entire_declared_stock_contract','exec'),scope)
need(scope['contract'].__globals__['stock_shadow_rows']is stock_shadow_rows,'Exact complete generated contract binding')
exec(compile(inspect.getsource(base.verify),__file__+'::whole_stock_verify','exec'),scope)
row_scope=dict(vars(final_row),__file__=__file__,scope=scope,stock_shadow_rows=stock_shadow_rows)
exec(compile(inspect.getsource(final_row.verify),__file__+'::whole_final_row_source_proof','exec'),row_scope)
bits_scope=dict(vars(command_bits),__file__=__file__,proof_scope=row_scope,stock_shadow_rows=stock_shadow_rows)
exec(compile(inspect.getsource(command_bits.verify),__file__+'::whole_command_bits_source_proof','exec'),bits_scope)

def verify():
    report=bits_scope['verify']()
    log=(CASE/'run.log').read_text();positive=stock_shadow_rows(log)
    fonts=[d for d in base.rows(log,'MK2_NAT_CAMPAIGN_FLOOR_DMA')if d['command']=='9008'and int(d['source'],16)<0x10000000]
    need(fonts,'Real native font operations in full win/continue window')
    d=fonts[0];lines=log.splitlines();index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_DMA ')and
                                              f"event={d['event']} "in line)
    before=lines[index];lines[index]=before.replace('pc=FF804640','pc=FF8015A0')
    need(lines[index]!=before,'Actual font-versus-floor operation caller fault')
    try:stock_shadow_rows('\n'.join(lines)+'\n')
    except ValueError as error:report['actualPipelineAndStockShadowFaultsRejected'].append(dict(label='font_mislabeled_as_floor_shadow',rejectedBy=str(error)))
    else:raise ValueError('Accepted font mislabeled as floor shadow')
    need(stock_shadow_rows(log)==positive,'All native original row/font positive restored')
    guest=base.state.source.current.expected();rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    first,last=(0xff804570-0xff800000)//8,(0xff804660-0xff800000)//8
    need(guest[first:last]==rom[first:last],'Original native font DMA dispatch byte-exact, not a port shadow hook')
    report.update(actualOriginalFontSolidDMAs=len(fonts),allStockSolidDMAOperationsExplicitlyAccounted=True,
                  fontDrawsNotOmittedFromWholePixelReplay=True,originalFontDMADispatchByteExact=True,
                  scope=__doc__)
    for p in (Path(__file__).resolve(),Path(base.__file__),Path(final_row.__file__),Path(command_bits.__file__)):
        report['inputHashes'][str(p)]=sha(p)
    need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every original/current input unchanged')
    return report

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable complete stock operation qualification')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
