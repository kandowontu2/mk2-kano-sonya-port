"""Prepare only; repair phase ownership and use an actual paid next scene."""
import hashlib
import json
import verify_native_source_sync as sync

sync.verify()
root=sync.ROOT
base=root/'audit_current_human_laser_four_png_preparation'
out=root/'audit_current_human_laser_four_png_v2_preparation'
assert not out.exists()
s=(base/'campaign.lua').read_text()
s=s.replace('local captures,pending={},{}','local captures,pending={},{}\nlocal continue_frame,next_css=nil,nil')
old='assert(cpu.A8.value==own.actor and cpu.A13.value==own.main)'
new="""if data==0x6b40 or data==0x6b41 then
  assert(cpu.A8.value==own.actor and cpu.A13.value==own.main)
 elseif data==0x6b42 then
  assert(cpu.A8.value==victim.actor and cpu.A13.value==victim.main)
 else
  assert(cpu.A8.value==victim.actor and cpu.A13.value==own.main)
 end"""
assert s.count(old)==1
s=s.replace(old,new)
needle=" local mode=p:read_u16(0x010601d0)\n"
insert=""" local mode=p:read_u16(0x010601d0)
 if started and completed and mode==3 then
  continue_frame=continue_frame or frame
  local age=frame-continue_frame
  if age>=20 and age<24 then input(2,'Coin')end
  if age>=50 and age<54 then input(2,'Coin')end
  if age>=80 and age<84 then input(2,'Start')end
 end
 if started and completed and mode==4 then next_css=next_css or frame end
"""
assert s.count(needle)==1
s=s.replace(needle,insert)
s=s.replace("  if age==450 then pending[frame]='unobscured_followthrough' end", "  if next_css and frame-next_css==100 then pending[frame]='next_paid_selection' end")
s=s.replace("if age>=450 then log('STOP'", "if captures.next_paid_selection then log('STOP'")
s=s.replace('if age<=450 then','if age<=1000 then')
assert ':pixels(' not in s and ':write_' not in s and s.count('screen:snapshot(')==1
out.mkdir()
lua=out/'campaign.lua';lua.write_text(s)
sha=hashlib.sha256(lua.read_bytes()).hexdigest().upper()
runner=(base/'run.ps1').read_text().replace('audit_current_human_laser_four_png_runtime','audit_current_human_laser_four_png_v2_runtime').replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace('5413B0D5C812745CFC23001C56B4C1F76CE78EFC2F46F701638CCCB51AD34FD6',sha)
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sha,
  physicalPrefixUnchangedUntilActualContinue=True,
  correctedSemantics='6B40/41 performerA8+performerMain;6B42 victimA8+victimMain;6B43/44 victimA8+performerMain. Bound to both true17/18 roster/owner/state/HP and native actual entry. Source temporaryvictim A8 is intentional, not proxy.',
  nextScene='After actualnativewinner then actualmode3, physicalP2Coin20..23/Coin50..53/Start80..83. FourthPNG actualnativeCSSmode4+100fields. Existing physicalCSSroute retained. No state writes/forcedtransition; targetunobserved if no actualCSS.',
  debrisLifetime='Actual source emitters intentionally survive winner/fatality lettering; original reference mass-deletes atscenechange (exampleage517), not atwinner196. Do not demand emptywinner450 or claim everyallocation retired. Newimage only demonstrates nextscene visiblecomposition afterpaidcontinue; native typedcleanup/source and existing lifetimeproof retained.',
  limits='8000fields180sec320MiB10MiB; only4PNGtotal256KiB; no rawpayloads',fullPortAccepted=False),indent=2))
print(out,sha)
