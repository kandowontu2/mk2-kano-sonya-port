"""UNEXECUTED Kitana9-only ring spacing; actual writer context, no guessed move labels."""
import json,re
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p2_jax_standing_guard_preparation'
out=root/'audit_current_sonya_p2_kitana_ring_spacing_preparation';assert not out.exists()
original=(base/'campaign.lua').read_text()
ring=(root/'audit_current_sonya_p2_jax_ring_spacing_preparation/campaign.lua').read_text()
start=ring.index("   elseif fighter=='sonya' and side==2 and other.roster==11 and stage==8 then")
end=ring.index("   elseif fighter=='sonya' and side==2 and other.roster==17 and stage==7 then",start+1)
branch=ring[start:end].replace('other.roster==11 and stage==8','other.roster==4 and stage==9').replace('jrs_','krs_').replace('SONYA_JAX_','SONYA_KITANA_')
marker="   elseif fighter=='sonya' and side==2 and other.roster==11 and stage==8 then"
assert original.count(marker)==1
globals="local krs_last,krs_ring,krs_dir,krs_jumpdir=nil,nil,nil,nil\nlocal krs_jump=-1000\n"
source=globals+original.replace(marker,branch+marker)
observer='''
local kitana_cpu_action_taps={}
emu.register_frame(function()
 if p:read_u16(0x01061b30)~=9 then return end
 local h,c=sample(2),sample(1)
 if not h or not c or h.id~=18 or h.roster~=18 or c.id~=4 or c.roster~=4 or h.owner~=h.actor or c.owner~=c.actor then return end
 local main=c.main
 if kitana_cpu_action_taps[main]then return end
 kitana_cpu_action_taps[main]=true
 taps[#taps+1]=p:install_write_tap(main+0x1f0,main+0x1ff,'passive true CPU Kitana action setter',function(at,data,mask)
  if at~=main+0x1f0 or mask~=0xffff or p:read_u16(0x01061b30)~=9 or p:read_u16(0x010601d0)~=2 then return end
  local own,target=sample(2),sample(1)
  if not own or not target or own.id~=18 or own.roster~=18 or target.id~=4 or target.roster~=4 or target.main~=main or own.owner~=own.actor or target.owner~=target.actor then return end
  log('SONYA_KITANA_CPU_ACTION',string.format('stage=9 actor=%08X main=%08X owner=%08X id=4 roster=4 before=%d after=%d pc=%08X a8=%08X a13=%08X flags=%04X body=%04X gap=%d height=%d',target.actor,main,target.owner,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value,target.flags,target.body,math.abs(own.x-target.x),target.floor-target.y))
 end)
end)
for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(observed_hp,observed_hp+15,'passive actual Sonya Kitana damage writer',function(at,data,mask)
  if at~=observed_hp or mask~=0xffff or p:read_u16(0x01061b30)~=9 or p:read_u16(0x010601d0)~=2 then return end
  local before,after=p:read_u16(at),data&0xffff
  if after>=before or before>161 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=18 or h.roster~=18 or c.id~=4 or c.roster~=4 or h.owner~=h.actor or c.owner~=c.actor then return end
  local writer=cpu.A13.value;local owner=valid(writer)and p:read_u32(writer+0xc0)or 0;local creator=valid(writer)and p:read_u32(writer+0x230)or 0
  log('SONYA_KITANA_DAMAGE',string.format('stage=9 victim_slot=%d before=%d after=%d pc=%08X ids=4,18 human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X writer_actor=%08X writer_main=%08X writer_owner=%08X writer230=%08X human_action=%d cpu_action=%d gap=%d height=%d cpu_height=%d',observed_slot,before,after,cpu.PC.value,h.actor,h.main,c.actor,c.main,cpu.A8.value,writer,owner,creator,h.action,c.action,math.abs(h.x-c.x),h.floor-h.y,c.floor-c.y))
 end)
end
'''
source+=observer
def conservation(candidate):
    assert candidate.startswith(globals) and candidate.endswith(observer)
    body=candidate[len(globals):-len(observer)]
    assert body.count(branch)==1 and body.replace(branch,'',1)==original
    assert ':write_' not in candidate and ':snapshot(' not in candidate
conservation(source);faults=[]
for label,bad in [('changed earlier Jax jump40',source.replace('jgl_until=frame+40','jgl_until=frame+41',1)),('wrong new Kitana stage',source.replace(branch,branch.replace('stage==9','stage==8',1),1)),('lost passive true CPU ID',source.replace(observer,observer.replace('c.id~=4','c.id~=3',1),1))]:
    try:conservation(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Source fault admitted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_jax_standing_guard_runtime','audit_current_sonya_p2_kitana_ring_spacing_runtime')
(out/'run.ps1').write_text(runner)
log=root/'audit_current_sonya_p2_jax_standing_guard_runtime/run.log'
lines=log.read_text().splitlines();rows=[(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in lines if s.startswith('MK2_NAT_CAMPAIGN_')]
fight=next(r for t,r in rows if t=='FIGHT' and r['stage']=='9');live=next(r for t,r in rows if t=='LIVE' and r['frame']=='104520');damage=next(r for t,r in rows if t=='HEALTH' and r['frame']=='104541' and r['slot']=='2')
assert fight['cpu']=='4:4' and fight['human']=='18:18' and live['cpu_actor']!=damage['a8'] and live['cpu_main']!=damage['a13']
assert int(damage['before'])-int(damage['after'])==32
hist=root/'audit_v5640_sonya_p2_kitana_ring_probe_checked/report.json';accepted=json.loads(hist.read_text())
assert accepted['passed'] and accepted['native']['actualOwnKitanaRoundWins']==2
report=dict(prepared=True,emulatorLaunched=False,runtimeAcceptance=False,fullPortAcceptance=False,proposedConservedPrefix=104518,
            currentFirstKitanaFight=fight,currentFirstCPUActionSample=live,currentFirst32HPIndependentWriter=damage,
            oldFinitePhysicalRingSpacingReference=str(hist),historicalProofNotCurrentAcceptance=True,
            attributionLimit='Action8 plus32HP effect writer differs from actual CPU actor/Main; without actual setter/native caller/creator context do not name fanlift/thrownfan/upper. Added passive setter/HPwriter records will enable source-bound classification.',
            soleControlChange='Stage9 trueKitana4 only: historical ring D2..5/F7..10/LP8..12 atgap150+, guarded64fieldcadence; backjump3on1off below150, HK3on3off onlyactuallyairborne. Earlier Baraka/Kano/Jax controllers unchanged.',
            effectiveSourceFaultsRejected=faults,luaSHA256=sync.sha(lua),inputHashes={str(p):sync.sha(p) for p in (hist,log)},
            limits=dict(wallSeconds=180,memoryMiB=320,textMiB=10,media=False,guestWrites=False))
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(prepared=True,emulatorLaunched=False,luaSHA256=sync.sha(lua),faults=len(faults))))
