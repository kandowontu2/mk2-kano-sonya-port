"""Add later sparse fields to avoid treating airborne stock samples as stance."""
import prepare_bounded_native_sole_dma_palette_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.old.prior.ROOT/'audit_bounded_native_late_sole_dma_preparation'
tail=scope['TAIL'];marker='if age~=8 and age~=16 and age~=24 and age~=32 then return end'
assert tail.count(marker)==2
tail=tail.replace(marker,'if age~=8 and age~=16 and age~=24 and age~=32 and age~=80 and age~=96 and age~=112 then return end')
scope['TAIL']=tail
exec(compile(old.old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
