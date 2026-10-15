"""All independently inventoried Jax clap new non-body effect sources."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_effect_census import TAIL

DMA=r'''
local effect_mapping=p:install_write_tap(0x01a80010,0x01a8001f,'actual Jax clap effect DMA',function(at,data)
 if not ready or frame-ready<1 or frame-ready>188 or at~=0x01a80010 then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local source=reg(2)|(reg(3)<<16);if not clap_effect_sources[source]then return end
 print(string.format('MK2_CLAP_EFFECT_DMA frame=%d source=%08X width=%d height=%d x=%d y=%d command=%04X pc=%08X writes=0 assistance=none',frame,source,reg(6)&1023,reg(7)&1023,reg(4)&1023,reg(5)&511,data&65535,regs.PC.value))
end)
emu.register_stop(function()assert(effect_mapping)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_clap_body_pixels_preparation'
    out=sync.ROOT/'audit_bounded_jax_clap_effect_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_jax_clap_draw_census_checked/report.json').read_text());assert proof['passed']
    sources=set()
    for case in proof['results'].values():
        for actor in case['newNonphysicalActors'].values():sources.update(actor['sources'])
    assert len(sources)==32
    text=(old/'prepared_observer.lua').read_text()
    needle='local idle_owned={}';assert text.count(needle)==1
    table='local clap_effect_sources={'+','.join('[0x'+s+']=true' for s in sorted(sources))+'}\n'
    text=text.replace(needle,table+needle)
    needle='if a and a.actor==regs.A0.value then';assert text.count(needle)==1
    text=text.replace(needle,'if slot==1 and a and regs.A0.value>=0x01000000 and regs.A0.value<0x01100000 and regs.A0.value~=a.actor and p:read_u16(regs.A0.value+0x1f0)==0 and clap_effect_sources[regs.A11.value] then')
    needle='assert(not idle_owned[key]);idle_owned[key]={slot=slot,id=a.id,pose=a.pose}';assert text.count(needle)==1
    text=text.replace(needle,'local prior=idle_owned[key];if prior then prior.count=prior.count+1 else idle_owned[key]={slot=slot,id=a.id,pose=a.pose,count=1}end')
    needle='idle_owned[key]=nil';assert text.count(needle)==1
    text=text.replace(needle,'own.count=own.count-1;if own.count==0 then idle_owned[key]=nil end')
    text+=TAIL.replace('frame-action_start>174','frame-action_start>188')+DMA
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_jax_clap_body_pixels_runtime',f'audit_bounded_{fighter}_jax_clap_effect_pixels_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,effectSources=sorted(sources),observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
