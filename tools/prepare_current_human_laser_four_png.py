"""Prepare only: bounded physical earned laser; never import historic collectors."""
import hashlib
import json
from pathlib import Path
import verify_native_source_sync as sync

sync.verify()
root = sync.ROOT
out = root / 'audit_current_human_laser_four_png_preparation'
assert not out.exists()
s = (root / 'mk2ks_native_kano_laser_action.lua').read_text()
s = s.replace("local side=assert(tonumber(os.getenv('MK2KS_LASER_SIDE')));assert(side==1 or side==2)", 'local side=1')
s = s.replace('local css,plans,taps,epochs={},{},{},{}', 'local css,plans,taps={},{},{}\nlocal captures,pending={},{}')
s = s.replace('local serial,bones,particles,emitters=0,0,0,0', 'local bones,particles,emitters=0,0,0')
start = s.index('local function membership(')
end = s.index("tap(address(0xb0b00)", start)
s = s[:start] + s[end:]
start = s.index("tap(address(0xafe00)")
end = s.index('for _,at in ipairs({0xff840450', start)
s = s[:start] + s[end:]
start = s.index('local function rgb(age)')
end = s.index('emu.register_frame(function()', start)
s = s[:start] + s[end:]
start = s.index(' if not sent then')
end = s.index(' if frame>=300', start)
s = s[:start] + " if frame>=8000 then log('BOUND','maximum_fields=8000');manager.machine:exit();return end\n" + s[end:]
start = s.index('  for job,e in pairs(epochs)do')
end = s.index('  if age>=750 then', start)
s = s[:start] + """  if age==450 then pending[frame]='unobscured_followthrough' end
  local label=pending[frame]
  if label and not captures[label]then
   local count=0;for _ in pairs(captures)do count=count+1 end;assert(count<4)
   captures[label]=true;log('CAPTURE','label='..label..' mode='..p:read_u16(0x010601d0))
   screen:snapshot(assert(os.getenv('MK2KS_LASER_PNG_DIR'))..'/'..label..'.png')
  end
""" + s[end:]
s = s.replace('if age>=750 then', 'if age>=450 then')
insert = """
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'independent fullword laser phases',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff or data<0x6b40 or data>0x6b44 then return end
 local own,victim=sample(side),sample(other)
 log('PHASE_RAW',string.format('cue=%04X pc=%08X actor=%08X main=%08X',data,cpu.PC.value,cpu.A8.value,cpu.A13.value))
 if not started or not own or not victim then return end
 assert(own.id==17 and own.roster==17 and own.state==1 and own.owner==own.actor and own.hp>0)
 assert(victim.id==18 and victim.roster==18 and victim.state==1 and victim.owner==victim.actor and victim.hp==0)
 assert(cpu.A8.value==own.actor and cpu.A13.value==own.main)
 local label=({[0x6b40]='charge',[0x6b41]='beam',[0x6b43]='burst'})[data]
 log('PHASE_OWNED',string.format('cue=%04X actor=%08X main=%08X victim=%08X victim_main=%08X',data,own.actor,own.main,victim.actor,victim.main))
 if label and not captures[label]then pending[frame+4]=label end
end)
"""
s = s.replace('emu.register_frame_done(function()', insert + '\nemu.register_frame_done(function()', 1)
assert ':pixels(' not in s and 'MK2_LASER_GUEST' not in s and 'read_block' not in s
assert ':write_' not in s and s.count('screen:snapshot(') == 1
out.mkdir()
lua = out / 'campaign.lua'
lua.write_text(s)
sha = hashlib.sha256(lua.read_bytes()).hexdigest().upper()
runner = (root/'audit_current_cpu_laser_four_png_preparation/run.ps1').read_text()
runner = runner.replace('audit_current_cpu_laser_four_png_runtime', 'audit_current_human_laser_four_png_runtime')
runner = runner.replace('audit_current_cpu_laser_four_png_preparation/campaign.lua', out.name+'/campaign.lua')
runner = runner.replace('A90120BAFA98D1277D8970D6E02FB6841912D705D70C110F25AD8D7FC0E9BBA1', sha)
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True, LuaSHA256=sha,
    physicalFixture='mk2ks_native_kano_laser_action.lua; accepted audit_native_kano_laser_action_p1',
    controls='Both paid human slots; P1 Kano17/P2 Sonya18. Physical repeated Down+HP earns two rounds. Finish flag3 and actual victimHP0; walk to146..154 then LP/Block/Block/HK at10/18/26/34, three fields each, Block released beforeHK.',
    media='Only4 PNG: owned phaseword charge/beam/burst+4 fields and age450 unobscured followthrough; total256KiB. Last image requires actual mode/hiddenbody/child inspection, not universal pool retirement.',
    observations='Native HP writes, button history, true17/18 actor/Main owner, actualFFD85800 action, victim contact/hide/park/ownedcache cleanup, actualnativewinner, bothbody scalarfields0..450. No RAM/GFX/PCM dumps, no emulator launch.',
    limits='8000fields/180sec/320MiB/10MiB; runtimefresh', fullPortAccepted=False), indent=2))
print(out, sha)
