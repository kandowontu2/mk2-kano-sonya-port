"""Do not accept decoded overlap when its final RGB does not match."""
from pathlib import Path
import qualify_bounded_idle_shadow_coverage as prior

source=Path(prior.__file__).read_text()
source=source.replace("assert r['match']=='1' and r['cover_pc']=='FF804640'", "assert r['cover_pc']=='FF804640'",1)
source=source.replace('                covered+=1','                if r[\'match\']==\'1\':covered+=1\n                else:unresolved+=1',1)
source=source.replace('allUnresolvedHaveNoObservedBodyCoverage=True','unmatchedDecodedOverlapsRemainUnresolved=True',1)
source=source.replace("'Actual DMA LRSKIP and banked clipping registers for remaining source points'", "'Actual DMA clipping/row skips and display timing for all remaining source points, including unmatched decoded body overlaps'",1)
scope=dict(prior.__dict__,__name__='finite_successor',__file__=__file__)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
