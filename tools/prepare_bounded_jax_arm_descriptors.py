"""Current guest scalar arm descriptor reads, no RAM dumps or writes."""
import json
import verify_native_source_sync as sync

TAIL=r'''
emu.register_frame(function()
 if frame~=1 then return end
 for ident=17,18 do
  local stream=0xff800000+(0xfb980+(ident-17)*48+24)*8
  for index=0,5 do
   local descriptor=p:read_u32(stream+index*32)
   if index==5 then assert(descriptor==0) else
    assert(descriptor>=0xff800000)
    print(string.format('MK2_ARM_DESCRIPTOR id=%d index=%d pointer=%08X width=%d height=%d source=%08X flags=%04X palette=%08X terminator=%04X writes=0 assistance=none',ident,index,descriptor,p:read_u16(descriptor),p:read_u16(descriptor+16),p:read_u32(descriptor+64),p:read_u16(descriptor+96),p:read_u32(descriptor+112),p:read_u16(descriptor+144)))
   end
  end
 end
end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arms_finisher_preparation'
    out=sync.ROOT/'audit_bounded_jax_arm_descriptors_preparation';assert not out.exists();out.mkdir()
    target=out/'prepared_observer.lua';target.write_text((old/'prepared_observer.lua').read_text()+TAIL)
    runner=(old/'run_sonya.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace('audit_bounded_sonya_jax_arms_finisher_runtime','audit_bounded_jax_arm_descriptors_runtime')
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
