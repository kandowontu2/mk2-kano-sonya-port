"""Preserve full comparison rules; use an available explicit JSON serializer."""
import inspect,json
from pathlib import Path
import qualify_native_selector_exit_stock_comparison as prior

STOCK_OUT=prior.ROOT/'audit_native_selector_exit_stock_reference_saved_checked'
OUT=prior.ROOT/'audit_native_selector_exit_stock_comparison_saved_checked'

def save(path,value):
    prior.need(not path.exists(), 'Do not overwrite an existing receipt')
    path.write_text(json.dumps(value,indent=2)+'\n')

scope=dict(vars(prior),STOCK_OUT=STOCK_OUT,OUT=OUT,__file__=__file__,save=save,comparison_original=prior)
for function in (prior.execute_stock,prior.execute_layers):
    source=inspect.getsource(function)
    before='original.capture.original.save('
    prior.need(source.count(before)==1, 'Only unavailable serializer changes')
    source=source.replace(before,'save(',1)
    before='for p in (Path(__file__).resolve(),VIEWS,'
    prior.need(source.count(before)==1, 'Exact executed comparison provenance boundary')
    source=source.replace(before,"for p in (Path(__file__).resolve(),Path(comparison_original.__file__).resolve(),comparison_original.STOCK_OUT/'failure.json',VIEWS,",1)
    exec(compile(source,__file__+'::'+function.__name__+'::whole_original_gate_available_serializer','exec'),scope)
execute_stock=scope['execute_stock']
execute_layers=scope['execute_layers']
