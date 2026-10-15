"""Cold native ordinary movement/attacks/blocking, whole original RAM transport.

Reuse all existing full guest/GFX/source-stream/body/shadow observations; alter
only physical controller program and admission labels. Four small preview PNG
artifacts are declared, no raw VRAM/RGB/audio/ROM buffers persisted.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_special_shadow_v5133 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_basic_ground_shadow_v5993.lua'

def run(fighter,side):
 source=inspect.getsource(original.capture)
 replacements={
  "audit_v5134_special_repeat_{move}_p{side}_{victim}":"audit_v5995_basic_{fighter}_p{side}",
  "for p in(LUA,Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):":
   "for p in(LUA,ROOT/'mk2ks_special_shadow_v5131.lua',Path(original.__file__),Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):",
  "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM=victim)":
   "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM=victim,MK2KS_BASIC_ROOT=str(ROOT))",
  "if re.search(r'_(SELECT|LIVE|READY|COMMAND|RECOVERED|REPEAT_READY|FINAL|FAILED|RESULT) ',line)":
   "if re.search(r'_(SELECT|LIVE|READY|STEP|FINAL|FAILED|RESULT) ',line)",
  "if line.startswith('MK2_HSPECIAL_RESULT ')]":"if line.startswith('MK2_BASIC_RESULT ')]",
  "need(len(results)==1 and results[0]['completed']=='2'and results[0]['attempt']=='2','Both true physical move activations and complete recovery/follow-up')":
   "need(len(results)==1 and results[0]['completed']=='1'and results[0]['phases']=='25'and results[0]['terminalAge']=='1540','All ordinary physical phases and clean live final recovery')",
  "need(len(scenes)>=9 and all(any(s['attempt']==i and s['stage']==stage for s in scenes)for i in(1,2)for stage in('special_before','entry','special_recovered')),\n      'Actual own before/entry/recovery RGB captured for both cycles')":
   "need(len(scenes)>=75 and any(s['stage']=='ordinary_final'for s in scenes),'Every ordinary phase start/mid/end and final RGB transported')",
  "print('MK2_SPECIAL_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)":
   "(folder/'ordinary_preview.png').write_bytes(png.getvalue())",
  "bothPhysicalSpecialCyclesTransportPassed=True":"ordinaryPhysicalControlsTransportPassed=True,fighter=fighter,previewPNGArtifactsWritten=1"}
 for before,after in replacements.items():
  count=source.count(before);need(count== (2 if before.startswith("print('MK2_SPECIAL_PREVIEW_DATAURL")else 1),'Exact complete original transport adaptation '+before[:70])
  source=source.replace(before,after)
 source=source.replace('MK2_HSPECIAL_FAILED','MK2_BASIC_FAILED')
 namespace=dict(original.capture.__globals__,native=current,LUA=LUA,__file__=__file__,original=original,fighter=fighter)
 exec(compile(source,__file__+'::whole_RAM_transport_ordinary_controls','exec'),namespace)
 report=namespace['capture']('knife'if fighter=='kano'else'ring',side,'kitana')
 report['inputHashes'][str(Path(__file__).resolve())]=sha(__file__)
 report.update(fullOrdinaryStateBodyShadowProofPending=True,fullPortAcceptance=False)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v5996_basic_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable ordinary capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
