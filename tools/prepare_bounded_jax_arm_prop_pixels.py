"""Source-bound detached arm props; native full-source clipping and scanout."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_effect_census import TAIL
from prepare_bounded_jax_clap_effect_pixels import DMA

PALETTE=r'''
local arm_palette=p:install_write_tap(0x01a80010,0x01a8001f,'native detached arm palette',function(at,data)
 if not ready or frame-ready<1 or frame-ready>147 or at~=0x01a80010 then return end
 local source=p:read_u16(0x01a80020)|(p:read_u16(0x01a80030)<<16)
 if not clap_effect_sources[source]then return end
 local victim=sample(side)
 print(string.format('MK2_ARM_PROP_PALETTE frame=%d source=%08X dma_bank=%04X victim_bank=%04X victim_id=%d victim_actor=%08X writes=0 assistance=none',frame,source,p:read_u16(0x01a80080)&0x7f00,victim.bank&0x7f00,victim.id,victim.actor))
end)
emu.register_stop(function()assert(arm_palette)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arms_body_pixels_preparation'
    out=sync.ROOT/'audit_bounded_jax_arm_prop_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_jax_arm_descriptors_checked/report.json').read_text());assert proof['passed']
    sources={r['source'] for rows in proof['descriptors'].values() for r in rows};assert len(sources)==10
    text=(old/'prepared_observer.lua').read_text()
    changes=[('local idle_owned={}','local clap_effect_sources={'+','.join('[0x'+s+']=true' for s in sorted(sources))+'}\nlocal idle_owned={}'),
        ('if a and a.actor==regs.A0.value then','if slot==1 and a and regs.A0.value>=0x01000000 and regs.A0.value<0x01100000 and regs.A0.value~=a.actor and p:read_u16(regs.A0.value+0x1f0)==0 and clap_effect_sources[regs.A11.value] then'),
        ('assert(not idle_owned[key]);idle_owned[key]={slot=slot,id=a.id,pose=a.pose}','local prior=idle_owned[key];if prior then prior.count=prior.count+1 else idle_owned[key]={slot=slot,id=a.id,pose=a.pose,count=1}end'),
        ('idle_owned[key]=nil','own.count=own.count-1;if own.count==0 then idle_owned[key]=nil end')]
    for before,after in changes:assert text.count(before)==1;text=text.replace(before,after)
    text+=TAIL.replace('frame-action_start>174','frame-action_start>147')+DMA.replace('frame-ready>188','frame-ready>147')+PALETTE
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace(f'audit_bounded_{fighter}_p{side}_jax_arms_body_pixels_runtime',f'audit_bounded_{fighter}_p{side}_jax_arm_prop_pixels_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,sources=sorted(sources),observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
