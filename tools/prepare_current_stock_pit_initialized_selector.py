"""Plan from initialized age56 selector publication, not stale age0 roster."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_stock_pit_other_sides_preparation'
out=sync.ROOT/'audit_current_stock_pit_initialized_selector_preparation'
assert not out.exists();out.mkdir()
for case in ('sonya_p1_kitana','kano_p2_subzero'):
    source=(base/(case+'.lua')).read_text()
    old="    plans[n]=route(p:read_u16(slots[n].roster),target)\n    log('SELECT','slot='..n..' target='..target..' route='..table.concat(plans[n],','))"
    assert source.count(old)==1
    source=source.replace(old,"    plans[n]=nil\n    log('SELECT_PENDING','slot='..n..' target='..target)")
    old='   local age=frame-css[n]\n   for index,key in ipairs(plans[n])do'
    assert source.count(old)==1
    new="""   local age=frame-css[n]
   if age==56 then
    local target=n==side and id or victim_id
    plans[n]=route(p:read_u16(slots[n].roster),target)
    log('SELECT','slot='..n..' target='..target..' route='..table.concat(plans[n],','))
   end
   for index,key in ipairs(plans[n] or {})do"""
    source=source.replace(old,new)
    assert ':write_' not in source and ':snapshot(' not in source
    lua=out/(case+'.lua');lua.write_text(source)
    runner=(base/(case+'.ps1')).read_text().replace(base.name+'/'+case+'.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/(case+'.lua')),sync.sha(lua)).replace('audit_current_stock_pit_'+case+'_runtime','audit_current_stock_pit_initialized_selector_'+case+'_runtime')
    (out/(case+'.ps1')).write_text(runner)
print('Prepared initialized-selector successors, run serially,90sec/320MiB/no media')
