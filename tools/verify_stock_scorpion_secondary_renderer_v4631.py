"""Fresh stock proof with explicit complete generated contract source binding.

Keep the frozen4629 native final-row correction. Compile the declared stock
contract text directly rather than introspecting a synthetic filename.
"""
import inspect,json,subprocess,traceback
from pathlib import Path
import verify_stock_scorpion_secondary_renderer_v4629 as previous
ROOT,need,sha,CASE=previous.ROOT,previous.need,previous.sha,previous.CASE
OUT=ROOT/'audit_v4632_stock_kitana_scorpion_secondary_renderer_checked'
stock_shadow_rows=previous.stock_shadow_rows
scope=dict(vars(previous.previous),__file__=__file__,stock_shadow_rows=stock_shadow_rows)
exec(compile(previous.previous.text,__file__+'::entire_declared_stock_contract','exec'),scope)
need(scope['contract'].__globals__['stock_shadow_rows']is stock_shadow_rows,
     'Generated stock contract actually bound to source-qualified native final duplicate-row phase')
exec(compile(inspect.getsource(previous.previous.verify),__file__+'::whole4625_stock_verify','exec'),scope)
namespace=dict(vars(previous),__file__=__file__,scope=scope,stock_shadow_rows=stock_shadow_rows,previous=previous)
exec(compile(inspect.getsource(previous.verify),__file__+'::whole4629_native_final_row_proof','exec'),namespace)
verify=namespace['verify']

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable explicitly source-bound original stock qualification')
    try:
        report=verify()
        report['inputHashes'][str(Path(__file__).resolve())]=sha(__file__)
        report['inputHashes'][str(Path(previous.__file__))]=sha(previous.__file__)
        need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual original/current source byte unchanged')
        report['explicitWholeGeneratedStockContractSourceBinding']=True
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
