"""Immutable successor: add actual saved-owner reads and passive sound tap."""
import prepare_bounded_native_uppercut_probe as prior

OWNER_SOURCE = prior.ROOT/'mk2ks_native_selector_sonya_cpu_lowkick_owners.lua'
owner = OWNER_SOURCE.read_text()
marker = '-- Read actual saved driver arrays'
assert owner.count(marker)==1
owner = '-- Read actual saved driver arrays'+owner.split(marker,1)[1]
assert 'emu.register_sound_update' in owner
assert ':write_' not in owner and 'snapshot' not in owner
prior.OUT = prior.ROOT/'audit_bounded_native_uppercut_owners_preparation'
prior.TAIL += owner+r'''
local bounded_sound_tap=selection_p:install_write_tap(0x01d01030,0x01d0103f,
    'bounded passive private cue observation',function(at,data,mask)
    local word=data&0xffff
    if at==0x01d01030 and mask==0xffff and word>=0x6b00 and word<=0x6b03 then
        print(string.format('MK2_BOUNDED_CUE frame=%d seconds=%.12f word=%04X writes=0',selection_frame,emu.time(),word))
    end
end)
'''
if __name__=='__main__':
    prior.main()
