"""Same whole freeze/source/shadow matrix, exact ordered DMA key indexing.

Preserve interrupted6202, all actual native captures and all original checks.
Index every original eligible DMA once instead of repeatedly rescanning it.
Equal duplicate report/part inventories share one in-memory list before
deepcopy; JSON sources remain unchanged and every actual part remains checked.
"""
from pathlib import Path
adapter_source=Path(__file__).with_name('qualify_current_normal_freeze_v6202.py')
outer=adapter_source.read_text()
outer=outer.replace('audit_v6206_current_normal_subzero_freeze_checked','audit_v6209_current_normal_subzero_freeze_checked')
anchor="scope=dict(__name__='original_complete_freeze_predicates',__file__=str(PRIOR))"
assert outer.count(anchor)==1,'Exact full original source predicate execution'
repair='''
before=" copies=rows['MK2_NORMAL_FREEZE_DMA'];counts=defaultdict(int);raw_stock=[];checked_copies=0;own_copies=0"
need(source.count(before)==1,'Original complete DMA inventory')
source=source.replace(before,before+"\\n copy_index=defaultdict(list)\\n for d in copies:\\n  if num(d,'pc')in(0xff8015a0,0xff801610):copy_index[num(d,'frame'),num(d,'cache_row')].append(d)",1)
before="  actual=[d for d in copies if (num(d,'frame'),num(d,'cache_row'))==key and num(d,'pc')in(0xff8015a0,0xff801610)]"
need(source.count(before)==1,'Exact original eligible tuple/PC predicate and native row order')
source=source.replace(before,"  actual=copy_index[key]",1)
before=" return dict(fighter=fighter,side=side,report=report,folder=folder,report_path=report_path,rows=rows,parts=parts)"
need(source.count(before)==1,'Exact complete native report and part transport')
source=source.replace(before," need(report['actualShadowParts']==parts,'Every duplicate logical native report/part entry identical before RAM aliasing')\\n report['actualShadowParts']=parts\\n"+before,1)
'''
outer=outer.replace(anchor,repair+'\n'+anchor,1)
before="pins={str(p.resolve()):sha(p)for p in(PRIOR,Path(__file__),Path(current.__file__),Path(scanner.__file__))}"
assert outer.count(before)==1,'All executed source and actual interruption records preserved'
outer=outer.replace(before,"pins={str(p.resolve()):sha(p)for p in(PRIOR,adapter_source,ROOT/'audit_v6207_current_normal_freeze_verifier_interruption/report.json',Path(__file__),Path(current.__file__),Path(scanner.__file__))}",1)
exec(compile(outer,__file__+'::complete_native_ordered_DMA_index','exec'),globals())
