"""Match actual renderer palette masking; preserve zero-match predecessor."""
import prepare_bounded_native_sole_dma_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.prior.ROOT/'audit_bounded_native_sole_dma_palette_preparation'
tail=scope['TAIL']
before='local palette=reg(8);local slot='
assert tail.count(before)==1
tail=tail.replace(before,'local palette=reg(8)&0x7f00;local slot=',1)
scope['TAIL']=tail
exec(compile(old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
