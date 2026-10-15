"""Current-build earned Kitana inflation with the complete native scene replay.

Preserve original physical controller and every CPU/DMA/shift/palette/VRAM/RGB
comparison. Use current reconstructed guest and payload, record real Windows
process identity/terminal, and omit redundant source-directory copies. Raw
media stays in RAM; save one bounded native review sheet per physical context.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import run_kitana_inflation_native_scene_v3920 as prior
import verify_kitana_inflation_earned_state_v3933 as earned
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def run(fighter,side):
 prior.NAME=current.NAME
 prior.OUT=ROOT/f'audit_v6115_current_kitana_{fighter}_p{side}_scene_observed'
 prior.REVIEW=ROOT/f'audit_v6114_current_kitana_{fighter}_p{side}_native_scene_ram/review'
 prior.graphics.NAME='diagnostic_v1836_ball_register_boundary'
 # Original positive control must retain its original palette contract.
 from verify_finish_display_v798 import check_owned_body_palette
 prior.model.check_owned_body_palette=check_owned_body_palette
 source=inspect.getsource(prior.run)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'One exact full-scene current identity/transport adaptation')
  source=source.replace(before,after,1)
 replace('audit_v3921_kitana_{fighter}_p{side}_native_scene_ram','audit_v6114_current_kitana_{fighter}_p{side}_native_scene_ram')
 replace("    base_guest,_,base_payload,_,_=data.old.expected_current()\n    candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()\n    guest,_=data.check(base_payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))",
         "    guest=current.expected()\n    candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()")
 replace("'36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'",'(current.EXE_SHA)')
 replace("    for p in files:\n        if p.is_file()and p.suffix in('.lua','.py','.ps1'):\n            target=CASE/'input_sources'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);need(sha(target)==sha(p),'Exact hierarchy source snapshot')",
         "    REVIEW.mkdir() # No duplicate source tree; all original files hash-bound.")
 replace("        print(f'Actual3836 native Kitana inflation {fighter}P{side} RAM scene pid='+str(process.pid),flush=True)",
         "        query=\"Get-CimInstance Win32_Process -Filter 'ProcessId=\"+str(process.pid)+\"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress\"\n        observation=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)\n        identity=json.loads(observation.stdout)if observation.returncode==0 and observation.stdout.strip()else None\n        (CASE/'process.json').write_text(json.dumps(dict(pid=process.pid,command=cmd,actualWindowsIdentity=identity),indent=2)+'\\n')\n        print(f'Current native Kitana inflation {fighter}P{side} PID='+str(process.pid),flush=True)")
 replace("    terminal=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,assistance='none',guest_writes=0,ramGuestSHA256=ram_guest,",
         "    (CASE/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=identity),indent=2)+'\\n')\n    need(identity and identity['ProcessId']==process.pid and identity['Name']=='mkport_candidate.exe'and Path(identity['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve()and str(OBSERVER)in identity['CommandLine'],'Actual creation/executable/full-command identity at native terminal')\n    terminal=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,assistance='none',guest_writes=0,ramGuestSHA256=ram_guest,")
 scope=dict(prior.run.__globals__,current=current,__file__=__file__)
 exec(compile(source,__file__+'::whole_current_native_scene_replay','exec'),scope)
 report=scope['run'](fighter,side)
 folder=ROOT/f'audit_v6114_current_kitana_{fighter}_p{side}_native_scene_ram'
 report['actualEarnedNativeState']=earned.gate(earned.rows((folder/'run.log').read_text()),fighter,side,current.expected())
 report['actualWindowsTerminal']=json.loads((folder/'native_terminal.json').read_text())
 report['newSourceDirectoryCopies']=0
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6115_current_kitana_{a.fighter}_p{a.side}_scene_observed';need(not out.exists(),'Fresh exact current full-scene report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','retainedOriginalPositiveControl')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
