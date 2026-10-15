"""Record unmatched actual body commands, not just the matching subset."""
import prepare_bounded_native_late_sole_dma_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.old.old.prior.ROOT/'audit_bounded_native_sole_unmatched_preparation'
tail=scope['TAIL'];marker='    if not part then return end'
assert tail.count(marker)==1
replacement=r'''
    if not part then
        local source_part,cw,ch=-1,0,0
        for index=0,11 do
            local row=cache+index*112;local graphic=selection_p:read_u32(row)
            if graphic==0 then break end
            if graphic==source then source_part=index;cw=selection_p:read_u16(row+0x20);ch=selection_p:read_u16(row+0x30);break end
        end
        print(string.format('MK2_BOUNDED_SOLE_UNMATCHED frame=%d age=%d slot=%d id=%d source=%08X width=%d height=%d command=%04X x=%d y=%d cache_source_part=%d cache_width=%d cache_height=%d pc=%08X writes=0',
            selection_frame,age,slot,s.id,source,w,h,command,reg(4)&0x3ff,reg(5)&0x1ff,source_part,cw,ch,
            manager.machine.devices[':maincpu'].state.PC.value))
        return
    end'''
scope['TAIL']=tail.replace(marker,replacement,1)
exec(compile(old.old.old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
