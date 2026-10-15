"""Real Kano wins against Shang, who morphs before the last genuine KO."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_own_finishers_dispatch_preparation'
out=sync.ROOT/'audit_bounded_morphed_victim_finishers_preparation';assert not out.exists()
source=(old/'finishers.lua').read_text()
def once(before,after):
    global source
    assert source.count(before)==1,before
    source=source.replace(before,after)
once('local join_at=nil','local join_at=nil\nlocal victim_morph_due=nil')
once('n==side and identity or killer_id)', 'n==side and 6 or killer_id)')
once('n==side and identity or killer_id,table.concat','n==side and 6 or killer_id,table.concat')
once('own.id~=killer_id or victim.id~=identity or own.owner~=own.actor',
     'own.id~=killer_id or(victim.id~=6 and victim.id~=identity)or victim.roster~=6 or own.owner~=own.actor')
once("assert(#taps==20,'Retain both original action variants and native table lookup observers')",
     "assert(#taps==(first_live and 21 or 20),'Original finisher observers plus real victim ID tap')")
before="  if not first_live then first_live=frame;log('FIRST_LIVE',string.format('own=%08X victim=%08X ids=%d,%d',own.actor,victim.actor,own.id,victim.id))end"
once(before,'''  if not first_live then
   first_live=frame
   taps[#taps+1]=p:install_write_tap(victim.actor+0x1f0,victim.actor+0x1ff,'actual victim native ID',function(at,data,mask)
    local current=sample(side)
    if not current or at~=current.actor+0x1f0 or mask&0xffff~=0xffff then return end
    log('VICTIM_MORPH_STORE',string.format('old=%d id=%d roster=%d actor=%08X main=%08X pc=%08X a9=%08X a0=%08X',
     current.id,data&0xffff,current.roster,current.actor,current.main,cpu.PC.value,cpu.A9.value,cpu.A0.value))
   end)
   log('FIRST_LIVE',string.format('own=%08X victim=%08X ids=%d,%d',own.actor,victim.actor,own.id,victim.id))
  end''')
once('   if gap>80 then press(winner_side,forward)', '''   if wins==1 and victim.hp<=41 and victim.id==6 and not victim_morph_due then
    victim_morph_due=frame+80;log('VICTIM_MORPH_PLAN','due='..victim_morph_due..' victim_hp='..victim.hp)
   end
   if victim_morph_due and frame-victim_morph_due<40 then
    local age=frame-victim_morph_due
    if name=='kano' then
     if age>=0 and(age<2 or(age>=8 and age<10))then press(side,forward)end
     if age>=4 and age<6 then press(side,'Down')end
     if age>=8 and age<10 then press(side,'Low Kick')end
    elseif name=='sonya'and age>=0 and age<8 then
     press(side,'Down');press(side,'Low Punch');press(side,'Block')
    end
   elseif gap>80 then press(winner_side,forward)''')
assert all(t not in source for t in(':write_',':snapshot(',':pixels(','io.open(','read_range('))
out.mkdir();lua=out/'finishers.lua';lua.write_text(source)
for target in('kano','sonya'):
    for side in(1,2):
        runner=(old/f'run_kano_p{3-side}.ps1').read_text()
        runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
        runner=runner.replace("MK2KS_TEST_FIGHTER='kitana'",f"MK2KS_TEST_FIGHTER='{target}'")
        runner=runner.replace(f'audit_bounded_own_finisher_dispatch_kano_p{3-side}_runtime',f'audit_bounded_morphed_victim_finisher_{target}_p{side}_runtime')
        runner=runner.replace("'-str','100'","'-str','120'")
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared four genuine Kano primary fatalities against actual Shang added-form victims')
