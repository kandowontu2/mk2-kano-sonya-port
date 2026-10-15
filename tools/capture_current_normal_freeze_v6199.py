"""Current normal ice/thaw/control capture with every live native shadow row.

Preserve whole5045 stream decoder and physical5043/1021 controls. Current
source-qualified EXE/guest, actual Windows identity and terminal, exception
draining, one bounded four-stage native review, no source/build/raw copies.
Write the complete accumulated part inventory only once after native terminal.
"""
from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
import current_payload_metadata_context_v5229 as native
prior_source=Path(__file__).with_name('run_normal_subzero_freeze_projection_v5045.py')
source=prior_source.read_text()
def replace(before,after,count=1):
 global source
 assert source.count(before)==count,'Exact whole original capture adaptation: '+before
 source=source.replace(before,after)
replace('import native_subzero_legs_context_v4993 as native','import current_payload_metadata_context_v5229 as native')
replace("LUA='mk2ks_normal_subzero_freeze_projection_v5043.lua'","LUA='mk2ks_current_normal_freeze_shadow_v6198.lua'")
replace('audit_v5046_normal_subzero_','audit_v6200_current_normal_subzero_')
replace('audit_v5047_normal_subzero_','audit_v6201_current_normal_subzero_')
replace("controllers=[ROOT/LUA,ROOT/'mk2ks_stock_fatality_v1021.lua']","controllers=[ROOT/LUA,ROOT/'mk2ks_normal_subzero_freeze_projection_v5043.lua',ROOT/'mk2ks_stock_fatality_v1021.lua']")
replace('for p in[*controllers,Path(__file__),Path(native.__file__),', 'for p in[*controllers,prior_source,Path(__file__),Path(native.__file__),')
replace(' proof_guest=proof_gfx=None;scenes=[];parts=[]',' proof_guest=proof_gfx=None;scenes=[];parts=[];native_images=[];errors=[]')
replace("  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\\n')",
"  query=\"Get-CimInstance Win32_Process -Filter 'ProcessId=\"+str(process.pid)+\"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress\"\n  actual=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)\n  wi=json.loads(actual.stdout)if actual.returncode==0 and actual.stdout.strip()else None\n  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,actualWindowsIdentity=wi),indent=2)+'\\n')")
replace("     (folder/'packed_part_memory_proofs.json').write_text(json.dumps(parts,indent=2)+'\\n')",'     # Complete inventory remains in RAM until actual native terminal.')
replace("      png=io.BytesIO();Image.frombytes('RGB',(400,254),raw,'raw','BGRX').save(png,format='PNG')\n      print('MK2_NORMAL_FREEZE_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)",
"      image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')\n      scenes[-1]['actualRGBSHA256']=hashlib.sha256(image.tobytes()).hexdigest().upper()\n      native_images.append(image)")
# Drain precisely the same process even after a host decoding assertion. Do
# not restart, print raw bytes, synthesize missing rows or accept partial proof.
start=source.index('   for line in process.stdout:\n')
end=source.index('  native_exit=process.wait()',start)
body=source[start+len('   for line in process.stdout:\n'):end]
source=source[:start]+"   for line in process.stdout:\n    if errors:\n     if 'hex='not in line:log.write(line)\n     continue\n    try:\n"+''.join(' '+line if line.strip()else line for line in body.splitlines(keepends=True))+"    except Exception as error:\n     errors.append(dict(error=repr(error),traceback=traceback.format_exc(),actualTag=line.split()[0]if line.split()else None))\n     print('Actual current normal-freeze observer failure; draining same native process to terminal: '+repr(error),flush=True)\n"+source[end:]
replace('  native_exit=process.wait()',"  native_exit=process.wait()\n (folder/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=native_exit,actualWindowsIdentity=wi),indent=2)+'\\n')\n (folder/'packed_part_memory_proofs.json').write_text(json.dumps(parts,indent=2)+'\\n')")
replace('actualScenes=scenes,actualShadowParts=parts,inputHashes=pins,',"actualScenes=scenes,actualShadowParts=parts,inputHashes=pins,actualWindowsTerminal=json.loads((folder/'native_terminal.json').read_text()),modelErrors=errors,")
replace(" need(native_exit==0 and proof_guest and proof_gfx and all(sha(p)==h for p,h in pins.items()),'Actual terminal transport and immutable inputs')",
" need(wi and wi['ProcessId']==process.pid and wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(ROOT/LUA)in wi['CommandLine'],'Actual native Windows creation/executable/full command')\n need(native_exit==0 and not errors and proof_guest and proof_gfx and all(sha(p)==h for p,h in pins.items()),'Actual terminal transport and immutable inputs')")
replace(' return meta'," review=folder/'review';review.mkdir()\n atlas=Image.new('RGB',(800,556));draw=ImageDraw.Draw(atlas)\n need(len(native_images)==4,'Four complete actual native stage images, not model/borrowed pixels')\n for i,(scene,image)in enumerate(zip(scenes,native_images)):\n  x,y=i%2*400,i//2*278;atlas.paste(image,(x,y+24));draw.text((x+4,y+5),scene['stage']+' native screen bitmap '+str(scene['frame']),fill='white')\n path=review/f'{fighter}-p{side}-native-freeze-review.png';atlas.save(path)\n meta.update(nativeReview=str(path),actualNativeReviewPanels=4,all701LiveShadowFieldsObserved=True,newBuildCopies=0,newSourceDirectoryCopies=0)\n return meta")
exec(compile(source,__file__+'::whole_current_ordinary_native_stream_capture','exec'),globals())
