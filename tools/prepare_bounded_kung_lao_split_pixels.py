"""Full-source/native-clip/presented split pixels through full follow-through."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_effect_census import TAIL
from prepare_bounded_jax_clap_effect_pixels import DMA
from prepare_bounded_kung_lao_split_followthrough_palette import TAIL as PALETTE

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arms_body_pixels_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_kung_lao_split_descriptors_checked/report.json').read_text());assert proof['passed']
    sources={r['source'] for rows in proof['descriptors'].values() for r in rows};assert len(sources)==12
    table=','.join('[0x'+s+']=true' for s in sorted(sources))
    text=(old/'prepared_observer.lua').read_text()
    before='frame-ready>=1 and frame-ready<=147';assert text.count(before)==2
    text=text.replace(before,'frame-ready>=1 and frame-ready<=299')
    changes=[('local idle_owned={}','local clap_effect_sources={'+table+'}\nlocal idle_owned={}'),
        ('if a and a.actor==regs.A0.value then','if slot==1 and a and regs.A0.value>=0x01000000 and regs.A0.value<0x01100000 and p:read_u16(regs.A0.value+0x1f0)==identity and clap_effect_sources[regs.A11.value] then'),
        ('assert(not idle_owned[key]);idle_owned[key]={slot=slot,id=a.id,pose=a.pose}','local prior=idle_owned[key];if prior then prior.count=prior.count+1 else idle_owned[key]={slot=slot,id=a.id,pose=a.pose,count=1}end'),
        ('idle_owned[key]=nil','own.count=own.count-1;if own.count==0 then idle_owned[key]=nil end')]
    for before,after in changes:assert text.count(before)==1;text=text.replace(before,after)
    text+=TAIL.replace('frame-action_start>174','frame-action_start>299')+DMA.replace('frame-ready>188','frame-ready>299')+PALETTE.replace('SOURCES',table)
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            for before,after in [("$env:MK2KS_STOCK_KILLER='jax'","$env:MK2KS_STOCK_KILLER='kung_lao'"),("$env:MK2KS_STOCK_COMMAND='bbbb_lp'","$env:MK2KS_STOCK_COMMAND='fff_lk'"),("$env:MK2KS_STOCK_GAP='96'","$env:MK2KS_STOCK_GAP='112'")]:
                assert runner.count(before)==1;runner=runner.replace(before,after)
            runner=runner.replace('jax_arms_body_pixels_runtime','kung_lao_split_pixels_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,sources=sorted(sources),observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
