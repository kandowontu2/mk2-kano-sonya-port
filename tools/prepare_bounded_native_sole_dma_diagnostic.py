"""Preserve zero-match probe; observe a bounded inventory of actual commands."""
import prepare_bounded_native_sole_dma_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.prior.ROOT/'audit_bounded_native_sole_dma_diagnostic_preparation'
scope['TAIL']+=r'''
local sole_diag_count=0
local sole_diag_tap=selection_p:install_write_tap(0x01a80000,0x01a800ff,
    'bounded native DMA register inventory',function(at,data,mask)
    if not first_live or selection_frame-first_live>40 or sole_diag_count>=64 then return end
    sole_diag_count=sole_diag_count+1
    local function reg(n)return selection_p:read_u16(0x01a80000+n*16)end
    print(string.format('MK2_BOUNDED_DMA_DIAGNOSTIC frame=%d age=%d at=%08X data=%04X mask=%04X source=%08X width=%d height=%d palette=%04X pc=%08X writes=0',
        selection_frame,selection_frame-first_live,at,data&0xffff,mask&0xffff,reg(2)|(reg(3)<<16),reg(6),reg(7),reg(8),manager.machine.devices[':maincpu'].state.PC.value))
end)
emu.register_stop(function()
    assert(sole_diag_tap,'Diagnostic tap retained')
    print(string.format('MK2_BOUNDED_DMA_DIAGNOSTIC_TERMINAL events=%d writes=0',sole_diag_count))
end)
'''
exec(compile(old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
