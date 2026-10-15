"""Terminal-first current CPU transport plus original RAM-only shadow streams.

One replay adds previously missing drawing evidence. Input/RNG/state trajectory
must exactly match6303. No raw GFX/RGB/guest files, builds, ZIPs or source copies.
"""
import gzip,hashlib,inspect,json,re
from pathlib import Path
import capture_current_kano_cpu_extended_v6292 as prior
import capture_current_cpu_knife_v6285 as terminal
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FOLDER=ROOT/'audit_v6314_current_cpu_blade_knife_shadow_ram'
LUA=ROOT/'mk2ks_current_cpu_blade_knife_shadow_v6312.lua'


def stream(line,streams):
 fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
 need(len(raw)==int(fields['bytes']),'Full actual unique shadow stream')
 graphic,mapped,command=(int(fields[k],16)for k in('graphic','mapped','command'))
 width,height=(int(fields[k])for k in('width','height'))
 need(mapped==graphic-(0x0a000000 if 0x10000000<=graphic<0x1a000000 else 0)and(command>>12)&7==6,
      'Original six-bit native stream mapping')
 need(not 0x10000000<=graphic<0x1a000000 or command&128,'Imported body stream remains compressed')
 bit=mapped%8;origin=bit;starts=[];headers=[]
 if command&128:
  for y in range(height):
   starts.append(graphic+bit-origin);need(bit+8<=len(raw)*8,'Complete original packed-row header')
   header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255;bit+=8
   pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
   need(pre+post<=width and bit+(width-pre-post)*6<=len(raw)*8,'Complete original packed-row pixels')
   headers.append(dict(row=y,pre=pre,post=post,pixels=width-pre-post));bit+=(width-pre-post)*6
 proof=dict(**fields,sha256=hashlib.sha256(raw).hexdigest().upper(),actualRowStarts=starts,
            actualRowHeaders=headers,usedBits=bit-origin,streamFormat='compressed6'if command&128 else'stockRaw6',
            compressedRowStreamVerified=bool(command&128),rawGFXFilesWritten=0)
 need(not any(p['stream']==proof['stream']for p in streams),'Each actual static stream observed once')
 streams.append(proof)
 return 'MK2_HPHASE_PART_DIGEST '+' '.join(k+'='+str(v)for k,v in fields.items())+' sha256='+proof['sha256']+'\n'


def capture():
 qualified=json.loads((ROOT/'audit_v6311_current_kano_cpu_blade_knife_checked/report.json').read_text())
 need(qualified['passed']and all(sha(p)==h for p,h in qualified['inputHashes'].items()),'Actual previous complete native phase proof unchanged')
 baseline=json.loads((ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json').read_text())
 original=ROOT/'mk2ks_special_shadow_v5131.lua'
 need(sha(original)==baseline['inputHashes'][str(original)],'Entire original qualified body/shadow observer unchanged')
 source=inspect.getsource(terminal.capture)
 namespace=dict(terminal.capture.__globals__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,stream=stream)
 changes={
  "prior=json.loads(prior_path.read_text())":"prior=json.loads(prior_path.read_text());prior['inputHashes']={str(Path(k).resolve()):v for k,v in prior['inputHashes'].items()}",
  "MK2KS_TEST_BOOT_FRAME='960'":"MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_CONTINUATION_POLICY='retreat'",
  "MK2KS_CPU_PAIR_CONFIRM_AGE='264'":"MK2KS_CPU_PAIR_CONFIRM_AGE='265'",
  'errors=[];proof=None;scenes=[];':'errors=[];proof=None;scenes=[];streams=[];',
  'if line.startswith((\'MK2_KNIFE_RAM_RGB \',\'MK2_KNIFE_RAM_GUEST \')):':
   "if line.startswith('MK2_HPHASE_PART '):\n      log.write(stream(line,streams))\n     elif line.startswith(('MK2_KNIFE_RAM_RGB ','MK2_KNIFE_RAM_GUEST ')):",
  'report=dict(passed=False,':'(FOLDER/\'shadow_stream_memory_proofs.json\').write_text(json.dumps(streams,indent=2)+\'\\n\')\n report=dict(passed=False,',
  "report['independentSemantics']=original.verify(text,guest)":
   "report['independentSemantics']=phase_gate(text,guest)\n  with gzip.open(previous/'run.log.gz','rt',encoding='utf-8')as file:old_text=file.read()\n  prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_')\n  need([s for s in text.splitlines()if s.startswith(prefixes)]==[s for s in old_text.splitlines()if s.startswith(prefixes)],'Every original native physical/RNG/state/health record unchanged under drawing observer')\n  report['originalWholePhysicalTrajectoryUnchanged']=True\n  report['actualUniqueShadowStreams']=len(streams)",
  'for p in (LUA,Path(__file__).resolve(),':
   "for p in (ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua',ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua',ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',ROOT/'tools/capture_current_cpu_knife_v6285.py',ROOT/'tools/verify_current_kano_cpu_blade_knife_v6304.py',ROOT/'tools/current_kano_cpu_extended_contract_v6291.py',ROOT/'tools/verify_current_kano_cpu_blade_knife_v6310.py',ROOT/'audit_v6311_current_kano_cpu_blade_knife_checked/report.json',LUA,Path(__file__).resolve(),",
 }
 # Reconstruct the exact executed6310 gate without running its existing main
 # or creating another qualification folder.
 import ast
 import verify_current_kano_cpu_blade_knife_v6304 as phase
 tree=ast.parse(Path(phase.__file__).read_text())
 node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='knife'for t in n.targets))
 adaptations=ast.literal_eval(node.value.args[1]);adaptations["native['mode']==(2 if serial==1 else 7)"]="native['mode']==(7)"
 adaptations["allfields=rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in allfields}"]="allfields=[r for r in rows(log,'FIELD')if actions[0]['frame']<r['frame']<=max(actions[0]['frame']+50,max(q['frame']for q in overlap.rows(log,'RETIRE')))];by={(r['frame'],r['slot']):r for r in allfields}"
 scope=dict(phase.gate.__globals__,knife=phase.model.bind(phase.model.knife.knives,adaptations))
 gate_source=inspect.getsource(phase.gate)
 before='shots=knife(text,guest)'
 need(gate_source.count(before)==1,'Retain6310 complete knife mode2 callback requirement')
 gate_source=gate_source.replace(before,"shots=knife(text,guest)\n need(all(r['mode']==2 for r in model.knife.R.rows(text,'FIELD')if 2443<=r['frame']<=2495),'Complete actual knife callbacks mode2 after observed mode7 handoff')",1)
 exec(compile(gate_source,__file__+'::entire_qualified_blade_knife_gate','exec'),scope)
 namespace.update(phase_gate=scope['gate'],previous=ROOT/'audit_v6303_current_kano_cpu_confirm265_ram')
 for before,after in changes.items():
  need(source.count(before)==1,'Single exact terminal transport adaptation '+before[:65]);source=source.replace(before,after,1)
 exec(compile(source,__file__+'::whole_robust_terminal_collector_plus_streams','exec'),namespace)
 return namespace['capture']()


if __name__=='__main__':capture()
