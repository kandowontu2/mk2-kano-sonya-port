"""Exact read-only Shao descriptor observer; every physical input remains unchanged."""
import argparse,json,re
from pathlib import Path
import verify_current_boss_shao_guard_walk_v2542 as native
ROOT=native.ROOT;launch=native.current_launch
BLOCK="-- BEGIN v2565 read-only scheduled-Shao collision descriptor provenance.\nlocal shao_lookup_serial,shao_lookup_pending,shao_lookup_latest=0,nil,nil\nlocal function shao_cpu_context()\n if not first_live or p:read_u16(0x01061b30)~=16 or p:read_u16(0x010601d0)~=2 or\n    p:read_u16(slots[side].state)~=1 or p:read_u16(slots[side].hp)==0 or\n    p:read_u16(slots[opponent].hp)==0 then return end\n local own,other=sample(side),sample(opponent)\n if not own or not other or own.id~=identity or own.roster~=identity or own.owner~=own.actor or\n    other.id~=13 or other.roster~=13 or other.owner~=other.actor then return end\n return own,other\nend\nlocal function shao_stack()\n local sp=cpu.SP.value\n if not valid(sp)or sp+6*32>0x01100000 then return sp,0,'unavailable' end\n local words={}\n for index=0,5 do words[#words+1]=string.format('%08X',p:read_u32(sp+index*32))end\n return sp,1,table.concat(words,',')\nend\ntaps[#taps+1]=p:install_read_tap(0xff8eb9e0,0xff8eb9ef,'actual Shao collision selector',function(at)\n if at~=0xff8eb9e0 then return end\n local own,other=shao_cpu_context()\n if not own or cpu.A8.value~=other.actor or cpu.A13.value~=other.main then return end\n shao_lookup_serial=shao_lookup_serial+1\n shao_lookup_pending={serial=shao_lookup_serial,frame=frame,actor=other.actor,main=other.main,selector=cpu.A0.value}\n local sp,stack_valid,stack=shao_stack()\n log('CPU_COLLISION_ENTRY',string.format('serial=%d stage=16 entry=%08X pc=%08X actor=%08X main=%08X owner=%08X a8=%08X a13=%08X id=13 roster=13 selector=%d reaction=%d sp=%08X stack_valid=%d stack=%s health=%d,%d',\n  shao_lookup_serial,at,cpu.PC.value,other.actor,other.main,other.owner,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A11.value,sp,stack_valid,stack,own.hp,other.hp))\nend)\ntaps[#taps+1]=p:install_read_tap(0xff8eba80,0xff8eba8f,'actual Shao collision descriptor return',function(at)\n if at~=0xff8eba80 then return end\n local own,other=shao_cpu_context()\n if not own or cpu.A8.value~=other.actor or cpu.A13.value~=other.main then return end\n local pending=shao_lookup_pending\n assert(pending and pending.frame==frame and pending.actor==other.actor and pending.main==other.main,'Coherent actual native Shao lookup')\n local descriptor=cpu.A0.value\n assert(descriptor>=0xff800000 and descriptor+144<=0x100000000,'Actual ROM attack descriptor')\n shao_lookup_latest={serial=pending.serial,frame=frame,actor=other.actor,main=other.main,selector=pending.selector,descriptor=descriptor}\n local sp,stack_valid,stack=shao_stack()\n log('CPU_COLLISION_RETURN',string.format('serial=%d stage=16 entry=%08X pc=%08X actor=%08X main=%08X owner=%08X a8=%08X a13=%08X id=13 roster=13 selector=%d descriptor=%08X damage_word=%04X reaction=%d sp=%08X stack_valid=%d stack=%s health=%d,%d',\n  pending.serial,at,cpu.PC.value,other.actor,other.main,other.owner,cpu.A8.value,cpu.A13.value,pending.selector,descriptor,p:read_u16(descriptor+5*16),cpu.A11.value,sp,stack_valid,stack,own.hp,other.hp))\n shao_lookup_pending=nil\nend)\ntaps[#taps+1]=p:install_write_tap(slots[side].hp,slots[side].hp+15,'actual scheduled-Shao damage context',function(at,data,mask)\n if mask~=0xffff or cpu.PC.value~=0xff836700 or(data&0xffff)>=p:read_u16(at)then return end\n local own,other=shao_cpu_context()\n if not own then return end\n local scheduled=cpu.A8.value==other.actor and cpu.A13.value==other.main\n local recent=shao_lookup_latest\n local same=recent and recent.frame==frame and recent.actor==cpu.A8.value and recent.main==cpu.A13.value\n local sp,stack_valid,stack=shao_stack()\n log('CPU_DAMAGE_CONTEXT',string.format('stage=16 at=%08X pc=%08X slot=%d before=%d after=%d mask=%04X actor=%08X main=%08X owner=%08X a8=%08X a13=%08X id=13 roster=13 scheduled_writer=%d serial=%d selector=%d descriptor=%08X a10=%08X reaction=%d sp=%08X stack_valid=%d stack=%s',\n  at,cpu.PC.value,side,p:read_u16(at),data&0xffff,mask,other.actor,other.main,other.owner,cpu.A8.value,cpu.A13.value,scheduled and 1 or 0,same and recent.serial or 0,same and recent.selector or -1,same and recent.descriptor or 0,cpu.A10.value,cpu.A11.value,sp,stack_valid,stack))\nend)\n-- END v2565 read-only scheduled-Shao collision descriptor provenance.\n"

def need(ok,label):
 if not ok:raise ValueError(label)

def restore(text):
 baseline=ROOT/'mk2ks_natural_campaign_boss_shao_guard_walk_v2540.lua'
 need(launch.sha(baseline)=='EE9BD536A3E5413C1847861D8ADFC145C1012A3BB20216BCFBA5DF47F583615A','Immutable original physical controller')
 need(text.count(BLOCK)==1,'One exact bounded read-only CPU descriptor observer')
 original=text.replace(BLOCK,'',1)
 need(original==baseline.read_text().rstrip()+'\n','Every selection, button, health/win/ending observer and native physical policy byte-exact')
 return native.restore_shao_guard_walk_policy(original)

def verify():
 path=ROOT/'mk2ks_natural_campaign_boss_shao_descriptor_observed_v2565.lua';text=path.read_text().rstrip()+'\n'
 restore(text);need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',text),'No guest/register/state writes')
 runner=ROOT/'tools/run_current_boss_shao_descriptor_observed_v2566.ps1'
 old=ROOT/'tools/run_current_boss_shao_guard_walk_v2541.ps1'
 restored=runner.read_text().replace('mk2ks_natural_campaign_boss_shao_descriptor_observed_v2565','mk2ks_natural_campaign_boss_shao_guard_walk_v2540')
 need(restored.rstrip()+'\n'==old.read_text().rstrip()+'\n','Entire existing physical launcher differs only in read-only observer file')
 mutations={
  'wrong_lookup_address':text.replace('p:install_read_tap(0xff8eb9e0,0xff8eb9ef','p:install_read_tap(0xff8eb9f0,0xff8eb9ff',1),
  'removed_actual_cpu_main_filter':text.replace(' or cpu.A13.value~=other.main','',1),
  'changed_existing_HP_timing':text.replace('frame-boss_walk_last_x>=12 and opening','frame-boss_walk_last_x>=10 and opening',1),
  'changed_own_identity':text.replace('kano=17,sonya=18','kano=1,sonya=18',1),
  'added_guest_write':text+"p:write_u16(0x010602f0,161)\n",
 }
 rejected=[]
 for name,changed in mutations.items():
  need(changed!=text,'Non-vacuous source counterexample '+name)
  try:restore(changed)
  except ValueError:rejected.append(name)
  else:raise ValueError('Changed read-only/physical boundary accepted '+name)
 restore(text)
 pins=launch.source_pins()
 recovery_path=ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json'
 recovery=json.loads(recovery_path.read_text());need(recovery['passed']and recovery['wholeCurrentGuestAndPayloadReconstructed'],'Exact dynamic dependencies recovered')
 for file,wanted in recovery['inputHashes'].items():need(launch.sha(file)==wanted,'Exact current and historical source dependency');pins[file]=wanted
 for p in(path,runner,old,recovery_path,Path(__file__).resolve()):pins[str(p)]=launch.sha(p)
 launch.module_pins(pins)
 return dict(passed=True,fullReadOnlyObserverInverse=True,wholeLauncherInverse=True,rejectedSpecificSourceCounterexamples=rejected,
  physicalInputsUnchanged=True,gameChanged=False,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable read-only observer proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
