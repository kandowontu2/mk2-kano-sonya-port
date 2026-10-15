"""Missing stock Liu P2 full native Scorpion-secondary renderer window.

Keep entire4594 physical/guest/renderer/retirement/palette/pixel/fault gates.
Use original stock row/font ledger rather than own-art-only shadow marker.
No repeated added-victim context, guest/control/build changes or raw writes.
"""
import inspect,json,subprocess,traceback
from pathlib import Path
import run_scorpion_secondary_native_scene_v4594 as previous
import qualify_stock_scorpion_secondary_native_scene_v4640 as source
import verify_stock_scorpion_secondary_renderer_v4637 as stock
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def collector():
    text=inspect.getsource(previous.collector)
    changes=[
      ('audit_v4597_scorpion_secondary_{fighter}_p{side}_native_scene_ram',
       'audit_v4642_scorpion_secondary_{fighter}_p{side}_native_scene_ram'),
      ("need(scene.groups['FLOOR_QUEUE']and scene.groups['SHADOW_COMPONENT'],'Actual body FIFO and native compressed-shadow components, not metadata-only claims')",
       "need(scene.groups['FLOOR_QUEUE']and stock.stock_shadow_rows(text),'Actual native owned FIFO and source-bound original stock shadow row/font ledger, not own-art-only markers')"),
      ("nativeShadowComponents=len(scene.groups['SHADOW_COMPONENT'])",
       'actualOriginalStockShadowRowDMAs=len(stock.stock_shadow_rows(text))'),
      ('namespace=dict(vars(original),__file__=__file__,source=source,model=model,np=np)',
       'namespace=dict(vars(original),__file__=__file__,source=source,model=model,np=np,stock=stock)')]
    for before,after in changes:
        need(text.count(before)==1,'Only fresh missing stock leaf and declared stock evidence type substitution: '+before)
        text=text.replace(before,after,1)
    scope=dict(vars(previous),__file__=__file__,source=source,stock=stock)
    exec(compile(text,__file__+'::entire4594_missing_original_stock_renderer','exec'),scope)
    return scope['collector']()

def run():
    report=collector()(('liu_kang',2))
    folder=Path(report['capture']);baseline=ROOT/'audit_v4552_scorpion_secondary_liu_kang_p2_native_state_ram'
    need(json.loads((folder/'native_rgb_digests.json').read_text())==json.loads((baseline/'native_rgb_digests.json').read_text()),
         'Every original62 native stock physical-controller RGB digest exactly unchanged')
    prefixes=('MK2_STOCK_HEAD_V921_','MK2_SSECOND_')
    select=lambda text:[line for line in text.splitlines()if line.startswith(prefixes)]
    need(select((folder/'run.log').read_text())==select((baseline/'run.log').read_text()),
         'Every original stock physical/native state/health/release/cooperative callback/guest/RGB/retirement event byte-exact')
    for p in (baseline/'native_rgb_digests.json',baseline/'run.log',Path(__file__).resolve()):
        report['inputHashes'][str(p)]=sha(p)
    report.update(everyOriginalStockControllerNativeEventAndRGBUnchanged=True,
                  completeCurrentVsStockRendererMatrixAccepted=False,fullPortAcceptance=False,scope=__doc__)
    need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All source/capture/native/public bytes unchanged')
    return report

if __name__=='__main__':
    out=ROOT/'audit_v4643_scorpion_secondary_liu_kang_p2_native_scene_checked'
    need(not out.exists(),'Fresh immutable missing original stock renderer result')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
