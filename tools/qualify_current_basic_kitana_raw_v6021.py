"""Whole ordinary state/body/shadow/fault matrix including real stock knockback.

Admit only original Kitana11x40 raw sprite0144AB50 using the already qualified
whole original unconditional signed shadow scanner. Do not relabel it compressed,
accept generic imported raw assets, fit pointers to DMA or discard victim fields.
"""
import inspect,json,traceback,types
from pathlib import Path
import qualify_current_basic_contact_scope_v6018 as contacts
import native_stock_raw_shadow_scanner_v5315 as stock
ROOT,need,sha=contacts.ROOT,contacts.need,contacts.sha
OUT=ROOT/'audit_v6022_current_ordinary_kitana_raw_checked'
physical=contacts.walking.prior

def raw_scanner():
 source=inspect.getsource(stock.stock_raw_starts)
 before='graphic==0x0251f2dc and width==10 and height==48'
 need(source.count(before)==1,'One finite original stock descriptor guard adaptation')
 source=source.replace(before,'graphic==0x0144ab50 and width==11 and height==40',1)
 source=source.replace('original Sub-Zero10x48 raw reaction sprite','original Kitana11x40 raw knockback sprite')
 scope=dict(stock.stock_raw_starts.__globals__)
 exec(compile(source,__file__+'::entire_original_signed_scanner_exact_Kitana11x40','exec'),scope)
 return scope['stock_raw_starts']

def bindings():
 original=physical.body
 source=inspect.getsource(original.check)
 before='  if not c&128:\n'
 after="""  if not c&128 and graphic==0x0144ab50:
   decoded[key]=kitana_raw_starts(graphic,w,h,c,gfx,t)
   continue
  if not c&128:
"""
 need(source.count(before)==1,'Only independently owned stock knockback stream added; all existing source/row/projection gates retained')
 source=source.replace(before,after,1)
 scope=dict(original.check.__globals__,kitana_raw_starts=raw_scanner())
 exec(compile(source,__file__+'::whole_native_body_shadow_gate_stock_knockback','exec'),scope)
 check=scope['check'];check.source=source
 proxy=types.SimpleNamespace(**dict(vars(original),check=check))
 binding=inspect.getsource(physical.bindings)
 before='source=inspect.getsource(body.check)';need(binding.count(before)==1,'Use actual generated whole check source, not misleading original-line inspection')
 binding=binding.replace(before,'source=body.check.source',1)
 scope=dict(physical.bindings.__globals__,body=proxy,state_gate=contacts.state_gate())
 exec(compile(binding,__file__+'::whole_original_ordinary_physical_kernel_binding','exec'),scope)
 return scope['bindings']()

def run():
 failed=contacts.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Only exact original Kitana11x6 raw hand'in failure['error'],'Retain actual previously unqualified stock knockback shadow counterexample')
 proof_path=ROOT/'audit_v5316_original_stock_raw_shadow_scanner_source_checked/report.json';proof=json.loads(proof_path.read_text())
 need(proof['passed']and proof['currentOriginalShadowKernelByteExact']and proof['originalUnconditionalHeaderAndSignedWidthAdvanceQualified']and
      all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual independent whole original ROM/opcode/signed scanner qualification still intact')
 scope=dict(contacts.run.__globals__,OUT=OUT,bindings=bindings,__file__=__file__)
 exec(compile(inspect.getsource(contacts.run),__file__+'::whole_contact_scope_matrix_and_all48_faults','exec'),scope)
 report=scope['run']()
 for p in(failed,proof_path,Path(stock.__file__).resolve(),Path(contacts.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(originalKitana11x40RawKnockbackShadowRowsAccepted=True,
               originalSignedUnconditionalScannerUsedWithoutPointerFitting=True,
               genericImportedRawSpriteAcceptance=False,retainedFailedStockRawKnockbackCoverage=str(failed))
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable exact stock-knockback ordinary matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
