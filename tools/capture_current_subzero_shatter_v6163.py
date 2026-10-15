"""Current earned freeze/shatter/next-match, retaining the whole physical driver.

The original18976-byte own GFX and whole guest are compared in RAM. Preserve
all original native branches and four event-bound RGB observations. Record
actual Windows identity and terminal before assertions, drain on observation
faults, and save only one bounded native contact sheet (no source/build copy).
This is not continuous scene, full audio, normal-health freeze or full-port QA.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import run_native_subzero_legs_nextmatch_v5001 as prior
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def run(fighter,side):
 source=inspect.getsource(prior.capture)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'Exact immutable current transport anchor')
  source=source.replace(before,after,1)
 replace('audit_v5002_subzero_','audit_v6164_current_subzero_')
 replace('guestproof=gfxproof=None;scenes=[]','guestproof=gfxproof=None;scenes=[];native_panels=[];transport_errors=[]')
 replace('[*controllers,Path(__file__),Path(native.__file__)',
         '[*controllers,Path(prior.__file__),Path(__file__),Path(native.__file__)')
 replace("  print(f'{fighter} P{side} actual shatter lifecycle started pid={process.pid}',flush=True)",
         "  query=\"Get-CimInstance Win32_Process -Filter 'ProcessId=\"+str(process.pid)+\"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress\"\n  census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)\n  wi=json.loads(census.stdout)if census.returncode==0 and census.stdout.strip()else None\n  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,actualWindowsIdentity=wi),indent=2)+'\\n')\n  print(f'{fighter} P{side} current freeze/shatter native PID={process.pid}',flush=True)")
 replace("      png=io.BytesIO();Image.frombytes('RGB',(400,254),raw,'raw','BGRX').save(png,format='PNG')\n      print('MK2_NATIVE_SUBZERO_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)",
         "      native_panels.append(Image.frombytes('RGB',(400,254),raw,'raw','BGRX'))\n      scene['actualRGBSHA256']=hashlib.sha256(native_panels[-1].tobytes()).hexdigest().upper()")
 # Observation errors must not wait in Popen.__exit__ with a full native pipe.
 start=source.index('   for line in process.stdout:\n')+len('   for line in process.stdout:\n')
 stop=source.index('  code=process.wait()\n',start)
 body=source[start:stop]
 source=source[:start]+'    try:\n'+''.join(' '+line if line.strip()else line for line in body.splitlines(True))+"    except Exception as error:\n     transport_errors.append(repr(error));log.write('CURRENT_TRANSPORT_ERROR '+repr(error)+'\\n');log.flush()\n"+source[stop:]
 replace('  code=process.wait()\n',
         "  code=process.wait()\n  (folder/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=wi),indent=2)+'\\n')\n  need(wi and wi['ProcessId']==process.pid and wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(ROOT/LUA)in wi['CommandLine'],'Actual native creation/executable/full command confirmed')\n  need(not transport_errors,'Every actual observed transport record accepted after native exit')\n  need(len(native_panels)==4,'Four complete native event-bound review panels')\n  from PIL import ImageDraw\n  sheet=Image.new('RGB',(800,556),(22,22,22));draw=ImageDraw.Draw(sheet)\n  for index,(label,panel,scene)in enumerate(zip(('frozen body','shattered legs','native victory','subsequent CPU match'),native_panels,scenes)):\n   x,y=index%2*400,index//2*278\n   draw.text((x+5,y+5),fighter+' P'+str(side)+' '+label+' field '+str(scene['frame']),fill=(255,255,255))\n   sheet.paste(panel,(x,y+24))\n  sheet.save(folder/'native_review.png')\n")
 replace('actualScenes=scenes,inputHashes=pins,fullPortAcceptance=False',
         "actualScenes=scenes,inputHashes=pins,actualWindowsTerminal=json.loads((folder/'native_terminal.json').read_text()),nativeReview=str(folder/'native_review.png'),newSourceDirectoryCopies=0,newBuildCopies=0,fullPortAcceptance=False")
 scope=dict(prior.capture.__globals__,native=current,prior=prior,__file__=__file__)
 exec(compile(source,__file__+'::complete_current_physical_shatter','exec'),scope)
 return scope['capture'](fighter,side)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6165_current_subzero_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh current terminal report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actionRows')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
