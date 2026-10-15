"""Existing punch-free babality fixture, genuine second-round Shang morph."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_current_babalities_preparation'
out=sync.ROOT/'audit_bounded_morphed_babalities_preparation';assert not out.exists()
source=(old/'babalities.lua').read_text()
def once(before,after):
    global source
    assert source.count(before)==1,before
    source=source.replace(before,after)
once('local wanted={[side]=winner_id,[3-side]=victim_id}', 'local wanted={[side]=6,[3-side]=victim_id}\nlocal morph_due,id_observer=nil,nil')
once('h.id~=winner_id or v.id~=victim_id','(h.id~=6 and h.id~=winner_id)or v.id~=victim_id')
once(' if at~=0xfffef800+winner_id*32 or p:read_u16(slots[side].hp)==0 or p:read_u16(slots[3-side].hp)~=0 then return end',
''' local own=sample(side)
 if not own or at~=0xfffef800+own.id*32 or own.roster~=6 or p:read_u16(slots[side].hp)==0 or p:read_u16(slots[3-side].hp)~=0 then return end''')
once("  assert(h.id==winner_id and v.id==victim_id and h.owner==h.actor and v.owner==v.actor,'Actual human and victim ownership')",'''  assert((h.id==6 or h.id==winner_id)and h.roster==6 and v.id==victim_id and h.owner==h.actor and v.owner==v.actor,'Actual Shang roster/current form and native victim')
  if not id_observer then
   id_observer=p:install_write_tap(h.actor+0x1f0,h.actor+0x1ff,'actual native morph ID',function(at,data,mask)
    local current=sample(side)
    if not current or at~=current.actor+0x1f0 or mask&0xffff~=0xffff then return end
    log('MORPH_STORE',string.format('old=%d id=%d roster=%d actor=%08X main=%08X pc=%08X a9=%08X a0=%08X',
     current.id,data&0xffff,current.roster,current.actor,current.main,cpu.PC.value,cpu.A9.value,cpu.A0.value))
   end)
   taps[#taps+1]=id_observer
  end''')
once("   if math.abs(h.x-v.x)>62 then press(side,h.x<v.x and'Right'or'Left')",'''   if native_kos==1 and v.hp<=32 and h.id==6 and not morph_due then
    morph_due=frame+80;log('MORPH_PLAN','due='..morph_due..' victim_hp='..v.hp)
   end
   if morph_due and frame-morph_due<40 then
    local age=frame-morph_due
    local back=h.x<v.x and'Left'or'Right'
    if winner_name=='kano' then
     if age>=0 and(age<2 or(age>=8 and age<10))then press(side,back)end
     if age>=4 and age<6 then press(side,'Down')end
     if age>=8 and age<10 then press(side,'Low Kick')end
    elseif age>=0 and age<8 then
     press(side,'Down');press(side,'Low Punch');press(side,'Block')
    end
   elseif math.abs(h.x-v.x)>62 then press(side,h.x<v.x and'Right'or'Left')''')
assert all(t not in source for t in(':write_',':snapshot(',':pixels(','io.open(','read_range('))
out.mkdir();lua=out/'babalities.lua';lua.write_text(source)
for target in('kano','sonya'):
    for side in(1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/babalities.lua',out.name+'/babalities.lua').replace(sync.sha(old/'babalities.lua'),sync.sha(lua))
        runner=runner.replace('audit_bounded_current_babality_','audit_bounded_morphed_babality_')
        runner=runner.replace("'-str','100'","'-str','120'")
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared genuine Shang morph babality cases; native punch eligibility unchanged')
