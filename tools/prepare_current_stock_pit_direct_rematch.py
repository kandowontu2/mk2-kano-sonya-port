"""Recognize full-health direct native rematches, keep earned admission gates."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_stock_pit_other_sides_preparation'
out=sync.ROOT/'audit_current_stock_pit_direct_rematch_preparation'
assert not out.exists();out.mkdir()
for case in ('sonya_p1_kitana','kano_p2_subzero'):
    source=(base/(case+'.lua')).read_text()
    old=' if mode==2 and pending and h and v and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then'
    assert source.count(old)==1
    new=''' local direct_rematch=not pending and window and arena==match and h and v and h.hp==161 and v.hp==161
 if mode==2 and (pending or direct_rematch) and h and v and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then'''
    source=source.replace(old,new)
    marker='  match=match+1;pending=false;kos=0;damage=0;window=nil;command=nil;rematch_at=nil'
    assert source.count(marker)==1
    source=source.replace(marker,"  if direct_rematch then log('DIRECT_REMATCH','arena='..arena..' health='..h.hp..','..v.hp..' ids='..h.id..','..v.id)end\n"+marker)
    assert ':write_' not in source and ':snapshot(' not in source
    lua=out/(case+'.lua');lua.write_text(source)
    runner=(base/(case+'.ps1')).read_text().replace(base.name+'/'+case+'.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/(case+'.lua')),sync.sha(lua)).replace('audit_current_stock_pit_'+case+'_runtime','audit_current_stock_pit_direct_rematch_'+case+'_runtime')
    (out/(case+'.ps1')).write_text(runner)
print('Prepared full-health direct-rematch controller successors; run serially')
