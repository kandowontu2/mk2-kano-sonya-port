"""All FIFO through179+120, actual custom-sprite palette delivery, no media."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local split_sources={SOURCES}
local split_palette=p:install_write_tap(0x01a80010,0x01a8001f,'actual split palette delivery',function(at)
 if not action_start or frame-action_start<1 or frame-action_start>299 or at~=0x01a80010 then return end
 local source=p:read_u16(0x01a80020)|(p:read_u16(0x01a80030)<<16)
 if not split_sources[source]then return end
 local victim=sample(side)
 print(string.format('MK2_SPLIT_PALETTE frame=%d age=%d source=%08X dma_bank=%04X victim_bank=%04X victim_id=%d victim_actor=%08X writes=0 assistance=none',frame,frame-action_start,source,p:read_u16(0x01a80080)&0x7f00,victim.bank&0x7f00,victim.id,victim.actor))
end)
emu.register_stop(function()assert(split_palette)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_draw_census_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_followthrough_palette_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_kung_lao_split_descriptors_checked/report.json').read_text());assert proof['passed']
    sources={r['source'] for rows in proof['descriptors'].values() for r in rows};assert len(sources)==12
    text=(old/'prepared_observer.lua').read_text();before='frame-action_start>179';assert text.count(before)==1
    text=text.replace(before,'frame-action_start>299')+TAIL.replace('SOURCES',','.join('[0x'+s+']=true' for s in sorted(sources)))
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace('kung_lao_split_draw_census_runtime','kung_lao_split_followthrough_palette_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,sources=sorted(sources),observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
