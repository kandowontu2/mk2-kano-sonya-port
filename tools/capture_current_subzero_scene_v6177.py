"""Current earned Subzero continuous original CPU/DMA/shift/scanout replay.

Preserve whole4028/3625 renderer and controls, substitute only real native
freeze task/own groups/palette source and current independently rebuilt GFX.
No guest/register/state/health/RNG writes, raw media or source/build copies.
"""
import argparse,inspect,json,re,struct,traceback
from pathlib import Path
import numpy as np
import run_jax_clap_native_scene_v4028 as prior
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def palette_trace(line,guest):
 if line.startswith('MK2_SUBZERO_SCENE_PALETTE '):
  r=dict(re.findall(r'(\w+)=([^\s]+)',line));entry=int(r['entry'],16)
  need(entry==0xff841090 and int(r['pc'],16)==entry+16 and r['mask']=='FFFF'and
       int(r['value'],16)==struct.unpack_from('<H',guest,(entry-0xff800000)//8)[0]and
       r['actor']==r['owner']and int(r['id'])in(8,17,18)and r['slot']in('1','2')and
       r['writes']=='0'and r['assistance']=='none','Actual original palette primitive and true physical source actor')
  prior.PALETTE_ROUTES[int(r['actor'],16)]=int(r['pointer'],16)
 parsed=prior.model.parse(line)
 if parsed and parsed[0]=='FLOOR_QUEUE':
  q=parsed[1];prior.QUEUE_ROUTES[q['frame'],q['actor'],q['part']]=prior.PALETTE_ROUTES.get(q['actor'])

def native_palette(q,actual,guest,ids,side):
 need(q['slot']==side and q['id']==q['roster']and q['id']in(8,17,18),'True own freeze or actual stock Subzero palette owner')
 pointer=prior.QUEUE_ROUTES[q['frame'],q['actor'],q['part']]
 if pointer is None:
  if q['id']in(17,18):
   off=(0xf1500 if q['id']==17 else 0xf1600)if q['body']&64 else(0xfda00 if q['id']==17 else 0xfdb00)
   pointer=0xff800000+off*8
  else:
   table=0xff907b30 if q['body']&64 else 0xff907910
   pointer=struct.unpack_from('<I',guest,(table-0xff800000)//8+q['id']*4)[0]
 need(0xff800000<=pointer<0x100000000 and pointer%16==0,'Actual palette choice in whole independently qualified guest')
 off=(pointer-0xff800000)//8;count=struct.unpack_from('<H',guest,off)[0]
 need(2<=count<=256 and off+2+count*2<=len(guest),'Complete native palette bounds')
 colors=struct.unpack_from('<'+str(count)+'H',guest,off+2)
 expected=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<d for s,d in((10,16),(5,8),(0,0)))for c in colors],dtype=np.uint32)
 bank=q['bank']&0x7f00
 need(len(actual)==32768 and np.array_equal(actual[bank:bank+count],expected),'Every source-chosen native normal/alternate/ice palette pen, no forced recolour')
 prior.PALETTES.append(dict(id=q['id'],slot=side,count=count,bank=bank,pointer=pointer))
 return prior.PALETTES[-1]

def sources(payload,pins):
 image=bytearray(prior.sources(payload,pins))
 need(payload[0x1f6400:0x1f6404]==b'KSF1'and payload[0x1f6700:0x1f6704]==b'KSL1','Exact dedicated frozen whole-body and semantic-legs uploads')
 for offset,dest in ((0x1f6400,0x1fa0000),(0x1f6700,0x1fa4000)):
  first,count,second,last,mapped=struct.unpack_from('<5I',payload,offset+4)
  need(mapped==dest and first+count<=len(payload)and second+last<=len(payload)and dest+count+last<=len(image),
       'Entire independently source-qualified native frozen GFX upload extents')
  image[dest:dest+count]=payload[first:first+count];image[dest+count:dest+count+last]=payload[second:second+last]
 return bytes(image)

def run(fighter,side):
 prior.NAME=current.NAME
 prior.OUT=ROOT/f'audit_v6179_current_subzero_{fighter}_p{side}_scene_observed'
 prior.REVIEW=ROOT/f'audit_v6178_current_subzero_{fighter}_p{side}_native_scene_ram/review'
 prior.OBSERVER=ROOT/'mk2ks_current_subzero_scene_v6176.lua'
 prior.graphics.NAME='diagnostic_v1836_ball_register_boundary'
 from verify_finish_display_v798 import check_owned_body_palette
 prior.model.check_owned_body_palette=check_owned_body_palette
 source=inspect.getsource(prior.run)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'Exact complete native renderer current Subzero binding')
  source=source.replace(before,after,1)
 replace('audit_v4029_jax_clap_{fighter}_p{side}_native_scene_ram','audit_v6178_current_subzero_{fighter}_p{side}_native_scene_ram')
 replace('    count=7','    count=2')
 replace("    base_guest,_,base_payload,_,_=data.old.expected_current()\n    candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()\n    guest,_=data.check(base_payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))",
         "    guest=current.expected()\n    candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()")
 first=source.index("    original_rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()")
 last=source.index("    pins=dict(positive['inputHashes']);image=sources(payload,pins)",first)
 source=source[:first]+"    phase_targets={0xffd62400,0xffd63400}if identity==17 else{0xffd62480,0xffd63460}\n    need(len(phase_targets)==count,'Both source-qualified own frozen whole and semantic legs groups')\n"+source[last:]
 replace("'36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'",'(current.EXE_SHA)')
 replace("    for p in files:\n        if p.is_file()and p.suffix in('.lua','.py','.ps1'):\n            target=CASE/'input_sources'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);need(sha(target)==sha(p),'Exact hierarchy source snapshot')",
         "    REVIEW.mkdir() # Preserve every input hash; no redundant source tree.")
 replace("MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='fff_lp_release',MK2KS_STOCK_GAP='64'",
         "MK2KS_STOCK_KILLER='subzero',MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168'")
 replace("        print(f'Actual3836 native Jax head-clap {fighter}P{side} RAM scene pid='+str(process.pid),flush=True)",
         "        query=\"Get-CimInstance Win32_Process -Filter 'ProcessId=\"+str(process.pid)+\"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress\"\n        observed=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)\n        wi=json.loads(observed.stdout)if observed.returncode==0 and observed.stdout.strip()else None\n        (CASE/'process.json').write_text(json.dumps(dict(pid=process.pid,command=cmd,actualWindowsIdentity=wi),indent=2)+'\\n')\n        print(f'Current native Subzero whole scene {fighter}P{side} PID='+str(process.pid),flush=True)")
 replace("    terminal=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,assistance='none',guest_writes=0,ramGuestSHA256=ram_guest,",
         "    (CASE/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=wi),indent=2)+'\\n')\n    need(wi and wi['ProcessId']==process.pid and wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve()and str(OBSERVER)in wi['CommandLine'],'Actual Windows creation/executable/full command native terminal')\n    terminal=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,assistance='none',guest_writes=0,ramGuestSHA256=ram_guest,")
 replace("begin['id']==11 and begin['human_slot']==side and begin['entry']==0xff8c7820 and\n        begin['actor']==state[f'p{winner}']and begin['main']==state[f'main{winner}']",
         "begin['id']==identity and begin['human_slot']==side and begin['entry']==0xff8c2320 and\n        begin['actor']==state[f'p{side}']and begin['main']==state[f'main{side}']")
 replace('sourceFIFOProjectionShadowQualificationPending=True,','sourceFIFOProjectionShadowQualificationPending=True,actualWindowsTerminal=json.loads((CASE/\'native_terminal.json\').read_text()),nativeReview=str(REVIEW/f\'{fighter}-p{side}-native-clap-review.png\'),newBuildCopies=0,newSourceDirectoryCopies=0,')
 namespace=dict(prior.run.__globals__,current=current,__file__=__file__,sources=sources,palette_trace=palette_trace,native_palette=native_palette)
 exec(compile(source,__file__+'::whole_current_Subzero_native_CPU_DMA_scanout','exec'),namespace)
 return namespace['run'](fighter,side)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6179_current_subzero_{a.fighter}_p{a.side}_scene_observed';need(not out.exists(),'Fresh actual continuous native report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','retainedOriginalPositiveControl')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
