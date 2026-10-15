"""Before-boot missing stock renderer: unchanged controls plus actual row ledger."""
import ast,inspect,json,re,subprocess,sys
from pathlib import Path
import qualify_scorpion_secondary_scene_source_v4595 as previous
ROOT,need,sha,NAME,current=previous.ROOT,previous.need,previous.sha,previous.NAME,previous.current
OUT=ROOT/'audit_v4641_stock_scorpion_secondary_source_checked'
LUA,CONTROL=previous.LUA,previous.CONTROL
source_boundary=previous.source_boundary

def main():
    need(not OUT.exists(),'Fresh before-boot missing stock renderer qualification')
    positive=source_boundary();actual=(ROOT/LUA).read_text();faults=[]
    for label,before,after in [('proxy_attacker','a.id==10 and victim.id==identity','a.id==1 and victim.id==identity'),
      ('wrong_native_action','local action_entry=0xff8bbfe0','local action_entry=0xff8bc000'),
      ('changed_controller','mk2ks_scorpion_secondary_state_ram_v4534.lua','mk2ks_stock_fatality_v1021.lua'),
      ('guest_write',"assert(not source:match(':write_[%w_]+%s*%('))","p:write_u16(0x01060e50,1)\nassert(not source:match(':write_[%w_]+%s*%('))")]:
        changed=actual.replace(before,after,1);need(changed!=actual,'Actual non-vacuous inherited role/source fault')
        try:previous.observer_source(changed)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted native role source fault: '+label)
        previous.observer_source(actual)
    import run_stock_scorpion_secondary_native_scene_v4639 as capture
    generated=capture.collector()
    need('errors'in generated.__code__.co_varnames and 'scene_errors'in generated.__code__.co_varnames,
         'Full generated stderr handle and native model error list remain distinct')
    keywords=[value for value in generated.__code__.co_consts if isinstance(value,tuple)]
    need(any(set(('MK2KS_STAGE_OUT','MK2KS_STAGE_SIDE','MK2KS_STAGE_WINNER'))<=set(value)for value in keywords),
         'Every original renderer metadata role/output environment key provided')
    need(generated.__globals__['stock']is capture.stock and generated.__globals__['source']is sys.modules[__name__],
         'Actual generated collector bound to fresh stock preflight and qualified native row/font ledger')
    # The stock ledger qualification retains entire557 native fields, source
    # routines,13 actual phase/row/font faults and original two bitmap faults.
    stock_path=ROOT/'audit_v4638_stock_kitana_scorpion_secondary_renderer_checked/report.json'
    stock=json.loads(stock_path.read_text())
    need(stock['passed']and stock['completeNativeRendererWindowAccepted']and stock['exactConsecutiveNativeRendererFields']==557 and
         stock['originalFinalDuplicateRowRegisterPhaseSourceProven']and stock['originalCommandPostSkipRegisterSourceProven']and
         stock['allStockSolidDMAOperationsExplicitlyAccounted']and len(stock['actualPipelineAndStockShadowFaultsRejected'])==13 and
         len(stock['actualPixelFaultsRejected'])==2 and not stock['completeCurrentVsStockRendererMatrixAccepted'],
         'Actual original stock row/font/register/source/fault/window proof, not full matrix acceptance')
    need(all(sha(p)==h for p,h in stock['inputHashes'].items()),'Every actual stock proof input unchanged before boot')
    old_path=previous.OUT/'report.json';old=json.loads(old_path.read_text())
    need(old['passed']and all(sha(p)==h for p,h in old['inputHashes'].items()),'Entire existing source/model/graphics/callback proof unchanged')
    files={Path(__file__).resolve(),Path(capture.__file__),Path(previous.__file__),Path(capture.previous.__file__),stock_path,old_path}
    files.update(map(Path,stock['inputHashes']));files.update(map(Path,old['inputHashes']))
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path and Path(path).resolve().is_relative_to(ROOT/'tools'):files.add(Path(path).resolve())
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    report=dict(positive,actualSourceFaultsRejected=faults,generatedStderrAndSceneErrorLocalsDistinct=True,
      everyRequiredRendererEnvironmentKeyPresent=True,actualGeneratedCollectorUsesQualifiedStockRowFontLedger=True,
      missingContext=dict(fighter='liu_kang',physicalVictimSlot=2,identity=1),
      originalStockKitanaWholeRendererAlreadyQualified=True,fullNativeRendererMatrixAccepted=False,
      inputHashes={str(p.resolve()):sha(p)for p in files},fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
