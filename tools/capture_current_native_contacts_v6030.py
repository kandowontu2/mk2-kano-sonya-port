"""Whole native RAM transport, actual process identity and settled close controls."""
import argparse,inspect,json,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_special_shadow_v5133 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_native_close_spacing_v6029.lua'

def run(fighter,side):
 source=inspect.getsource(original.capture)
 replacements={
  'audit_v5134_special_repeat_{move}_p{side}_{victim}':'audit_v6031_contacts_{fighter}_p{side}',
  "for p in(LUA,Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):":
   "for p in(LUA,ROOT/'mk2ks_close_contacts_v6025.lua',ROOT/'mk2ks_special_shadow_v5131.lua',Path(original.__file__),Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):",
  "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM=victim)":
   "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM=victim,MK2KS_BASIC_ROOT=str(ROOT))",
  "  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\\n')":
  """  query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(process.pid)+"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
  actual=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
  identity=json.loads(actual.stdout)if actual.returncode==0 and actual.stdout.strip()else None
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,actualWindowsIdentity=identity),indent=2)+'\\n')""",
  "  native_exit=process.wait()":
   "  native_exit=process.wait()\n (folder/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=native_exit,actualWindowsIdentity=identity),indent=2)+'\\n')",
  "if re.search(r'_(SELECT|LIVE|READY|COMMAND|RECOVERED|REPEAT_READY|FINAL|FAILED|RESULT) ',line)":
   "if re.search(r'_(SELECT|LIVE|READY|STEP|RECOVERED|FINAL|FAILED|RESULT) ',line)",
  "if line.startswith('MK2_HSPECIAL_RESULT ')]":"if line.startswith('MK2_BASIC_RESULT ')]",
  "need(len(results)==1 and results[0]['completed']=='2'and results[0]['attempt']=='2','Both true physical move activations and complete recovery/follow-up')":
   "need(len(results)==1 and results[0]['completed']=='1'and results[0]['phases']=='7','Whole7 physical interactions and clean live final recovery')",
  "need(len(scenes)>=9 and all(any(s['attempt']==i and s['stage']==stage for s in scenes)for i in(1,2)for stage in('special_before','entry','special_recovered')),\n      'Actual own before/entry/recovery RGB captured for both cycles')":
   "need(len(scenes)>=36 and any(s['stage']=='contacts_final'for s in scenes),'Every interaction before/active/recovery and native final RGB transported')",
  "if f['attempt']=='1'and f['stage']=='phase_16': # One native full frame plus compact sheet.":
   "if f['stage']in('own_high_punch_block_phase32','own_low_kick_crouch_block_phase32','own_ground_throw_entry','own_ground_throw_phase48','stock_ground_throw_phase48','contacts_final'): # Bounded native previews.",
  "print('MK2_SPECIAL_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)":
   "(folder/'contacts_preview.png'if 'sheet'in locals()else folder/('native_'+f['stage']+'.png')).write_bytes(png.getvalue())",
  'bothPhysicalSpecialCyclesTransportPassed=True':'actualCloseControlsTransportPassed=True,fighter=fighter,actualWindowsIdentity=identity'}
 for before,after in replacements.items():
  need(source.count(before)==(2 if before.startswith("print('MK2_SPECIAL_PREVIEW_DATAURL")else 1),'Exact complete native transport adaptation '+before[:75])
  source=source.replace(before,after)
 source=source.replace('MK2_HSPECIAL_FAILED','MK2_BASIC_FAILED')
 scope=dict(original.capture.__globals__,native=current,LUA=LUA,__file__=__file__,original=original,fighter=fighter)
 exec(compile(source,__file__+'::whole_RAM_native_contact_transport','exec'),scope)
 report=scope['capture']('knife'if fighter=='kano'else'ring',side,'kitana')
 identity=report['actualWindowsIdentity']
 need(identity and identity['ProcessId']>0 and identity['Name']=='mkport_candidate.exe'and
      Path(identity['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
      'audit_v6031_contacts_'+fighter+'_p'+str(side)in identity['CommandLine']and str(LUA)in identity['CommandLine'],
      'Actual OS process creation/executable/complete command identity, after native terminal settled')
 report.update(actualCloseBlockThrowPhysicalProofPending=True,wholeCurrentBodyShadowProofPending=True,fullPortAcceptance=False)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v6032_contacts_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable current native-contact capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
