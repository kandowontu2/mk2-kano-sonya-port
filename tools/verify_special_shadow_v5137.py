"""Every owned native body/shadow field in two physical repeated specials.

Finite Prison/Kitana move/player-slot instances, no other arenas/CPU/KO/audio
or full artistic/port acceptance. Guest, ROM streams and raw scenes RAM-only.
"""
import argparse,copy,hashlib,json,re,struct,subprocess
from collections import defaultdict
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import verify_special_repeat_v5115 as human
from verify_move_phase_shadow_v5089 import native_group,reconstruct,short,subxy
ROOT,need,sha=native.ROOT,native.need,native.sha
HEX=human.HEX|set('graphic world b1 b2 b4 b7 a5 shadow_camera value color cache_row'.split())
def num(t,k):return int(t[k],16 if k in HEX else 10)
def load(move,side):
 folder=ROOT/f'audit_v5134_special_repeat_{move}_p{side}_kitana'
 report_path=ROOT/f'audit_v5135_special_repeat_{move}_p{side}_kitana_observed/report.json'
 report=json.loads(report_path.read_text());text=(folder/'run.log').read_text()
 need('hex='not in text,'No persisted raw buffers')
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_HSPECIAL_FAILED',text+(folder/'stderr.log').read_text(),re.I),'Actual native/observer success')
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text())
 return dict(move=move,side=side,folder=folder,report_path=report_path,report=report,rows=rows,streams=streams)
def check_body(b,guest,payload,frames,owners,ids):
 candidates=b['rows']['MK2_HPHASE_CANDIDATE'];queues=b['rows']['MK2_HPHASE_QUEUE']
 cm={(num(t,'frame'),num(t,'slot'),num(t,'part')):t for t in candidates};qm={(num(t,'frame'),num(t,'slot'),num(t,'part')):t for t in queues}
 need(len(cm)==len(candidates)and len(qm)==len(queues)and cm,'Unique actual complete native body candidates')
 compositions=defaultdict(list);visible=set();clipped=0
 for key,t in cm.items():
  f,s,part=key;need(f in frames and s in(1,2)and num(t,'pc')==0xff8042b0 and num(t,'row')==num(t,'cache')+part*112,'Every real candidate at original native opcode/cache row')
  need(num(t,'actor')==num(t,'owner')==owners[s][0]and num(t,'main')==owners[s][1]and num(t,'id')==num(t,'roster')==ids[s],'Entire body belongs to actual true owned actor')
  group=native_group(t,payload,guest);need(part in range(len(group)),'Part in complete terminated actual native pose');p=group[part]
  need((num(t,'source'),num(t,'size'),num(t,'command'))==(p['graphic'],p['width']|(p['height']<<16),(p['command']|0x8002)<<16),'Body source/size/command exactly matches independent pose descriptor')
  need(num(t,'clipLow')==0 and num(t,'clipHigh')==0x00fe0190,'Original whole native clip rectangle')
  x,y=short(num(t,'xy')),short(num(t,'xy')>>16);w,h=p['width'],p['height'];shown=x+w>0 and y+h>0 and x<400 and y<254
  need((key in qm)==shown,'Every actual complete body part published iff on screen')
  if shown:
   visible.add(key);q=qm[key]
   need(num(q,'pc')==0xff804420 and all(q[k]==t[k]for k in('actor','main','owner','id','roster','pose','facing','body','cache','part','row','source','size','command')),'Actual original candidate-to-FIFO provenance')
   dx,dy=short(num(t,'display')),short(num(t,'display')>>16);cmd=num(t,'command')>>16
   expected=((x+(w-1 if cmd&16 else 0)+dx)&65535)|(((y+(h-1 if cmd&32 else 0)+dy)&65535)<<16)
   need(num(q,'xy')==expected,'Original exact body flips/display-base publication')
  else:clipped+=1
  compositions[f,s].append(part)
 need(visible==set(qm)and set(compositions)=={(f,s)for f in frames for s in(1,2)},'Both entire actual native body composites observed at every ready field, including routine entries')
 for key,parts in compositions.items():need(parts==list(range(len(native_group(cm[key[0],key[1],0],payload,guest)))),'No missing or duplicate actual owned body component')
 return len(candidates),len(queues),clipped
def check(b,guest,payload,gfx):
 rows=b['rows'];side=b['side'];identity=human.SPECS[b['move']][0]
 # The older physical/ownership/health checker receives its exact finite view.
 # All unfiltered body records, including entry frames, are checked independently below.
 sample_frames={s['frame']for s in b['report']['actualScenes']}
 entry=human.SPECS[b['move']][1]
 entry_frames={num(t,'frame')for t in rows['MK2_HSPECIAL_EVENT']if num(t,'entry')==entry}
 finite=dict(b);finite['rows']=dict(rows)
 for tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):finite['rows'][tag]=[t for t in rows[tag]if num(t,'frame')in sample_frames-entry_frames]
 state=human.check(finite,guest,payload)
 fields=rows['MK2_HPHASE_POST_FIELD'];by={(num(t,'frame'),num(t,'slot')):t for t in fields};frames={f for f,s in by}
 first=min(frames);owners={s:(num(by[first,s],'actor'),num(by[first,s],'main'))for s in(1,2)};ids={side:identity,3-side:4};floors={s:num(by[first,s],'floor')for s in(1,2)}
 body_parts,published,clipped=check_body(b,guest,payload,frames,owners,ids)
 begins=rows['MK2_HPHASE_SHADOW_BEGIN'];begin_by={(num(t,'frame'),num(t,'slot')):t for t in begins}
 need(len(begin_by)==len(begins)==len(by)and set(begin_by)==set(by),'Exactly one actual original shadow eligibility call per real owned actor/field')
 for key,t in begin_by.items():
  s=key[1];need(num(t,'actor')==num(t,'owner')==owners[s][0]and num(t,'main')==owners[s][1]and num(t,'id')==ids[s]and num(t,'pc')==0xff801080 and num(t,'value')==0xb500 and num(t,'mask')==65535,'Original shadow eligibility instruction and actual owner')
 streams={t['stream']:t for t in b['streams']};need(len(streams)==len(b['streams'])and streams,'Unique actual static GFXROM shadow streams')
 decoded={}
 for key,t in streams.items():
  graphic,mapped,w,h,c=num(t,'graphic'),int(t['mapped'],16),num(t,'width'),num(t,'height'),num(t,'command')
  need(key==f'{graphic:08X}_{w}_{h}_{c:04X}'and mapped==graphic-(0x0a000000 if 0x10000000<=graphic<0x1a000000 else 0),'Exact unique actual native ROM descriptor/mapping')
  size=num(t,'bytes');need(size==(w*h*6+h*8+15)//8+4,'Complete source-derived native stream capture bound')
  raw=bytes(gfx[mapped//8:mapped//8+size]);need(len(raw)==size and hashlib.sha256(raw).hexdigest().upper()==t['sha256'],'Every actual unique sprite byte equals independently interleaved compiled ROM graphics')
  need(c&128 and (c>>12)&7==6 and t['compressedRowStreamVerified']and t['streamFormat']=='compressed6','Every current owned shadow stream strictly compressed six-bit; no raw stepping acceptance')
  bit=mapped%8;origin=bit;starts=[];headers=[]
  for row in range(h):
   starts.append(graphic+bit-origin);need(bit+8<=len(raw)*8,'Complete independent actual row header')
   header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255;bit+=8
   pre=(header&15)<<((c>>8)&3);post=(header>>4)<<((c>>10)&3)
   need(pre+post<=w and bit+(w-pre-post)*6<=len(raw)*8,'Complete source-derived packed row pixels')
   headers.append(dict(row=row,pre=pre,post=post,pixels=w-pre-post));bit+=(w-pre-post)*6
  need(t['actualRowStarts']==starts and t['actualRowHeaders']==headers and t['usedBits']==bit-origin,'Every actual packed ROM row independently decoded')
  decoded[key]=starts
 projections=rows['MK2_HPHASE_PROJECTION'];pm=defaultdict(list);dma=defaultdict(list)
 for t in rows['MK2_HPHASE_SHADOW_DMA']:dma[num(t,'frame'),num(t,'cache_row')].append(t)
 own_copies=total_copies=0;matched_dma=set();used_streams=set()
 for t in projections:
  f,s=num(t,'frame'),num(t,'slot');need((f,s)in begin_by,'Actual projection belongs to native shadow call')
  begin=begin_by[f,s];cache=num(t,'cache');part=num(t,'component');group=native_group(t,payload,guest)
  need(part in range(len(group))and num(t,'row')==cache+part*112 and cache==num(begin,'cache'),'Actual projected terminated source component and owned cache')
  need(all(t[k]==begin[k]for k in('actor','main','owner','id','pose','cache','body','facing'))and num(t,'body')&16 and num(t,'floor')==floors[s],'Original eligible owned body and exact unchanged own floor')
  p=group[part];need(all(num(t,k)==v for k,v in p.items()),'Every native projected cache word matches complete original pose descriptor and flips')
  need(num(t,'pc')==0xff8012c0 and num(t,'value')==0x4e90 and num(t,'mask')==65535,'Actual original direct native shadow projection opcode')
  key=f'{p["graphic"]:08X}_{p["width"]}_{p["height"]}_{p["command"]:04X}';need(key in decoded,'Actual projection has full independently bound static ROM stream proof');used_streams.add(key)
  camera=num(t,'shadow_camera');b2=num(t,'b2');b4=num(t,'b4');a5=num(t,'a5')
  need(camera==(num(t,'b1')|short(camera)&65535)and b4==subxy(num(t,'world'),camera)and b2==((num(t,'stageY')-short(camera>>16)+num(t,'b7'))&65535)<<16,'Exact original world/camera/native-floor shadow projection registers')
  gap=(short(b2>>16)-(short(b4>>16)-p['dy']))&65535
  x=(short(b4)-p['dx']+(p['width']-1 if p['command']&16 else 0)+short(a5))&1023
  y=(short(b2>>16)-gap//4+short(a5>>16))&511
  dkey=(f,num(t,'row'));need(dkey not in matched_dma,'Unique actual projection row per native field');matched_dma.add(dkey)
  copies=dma[dkey];height=p['height'];need(len(copies)==height//4+1 and len(copies)>1,'Entire original quarter-height shadow copy cadence')
  for i,d in enumerate(copies):
   need((num(d,'x'),num(d,'y'),num(d,'width'),num(d,'height'),num(d,'command'),num(d,'palette'),num(d,'color'),num(d,'mask'),num(d,'pc'))==(x,(y+i)&511,p['width'],1,p['command']|0x8008,0,0x0f0f,65535,0xff801610 if i==len(copies)-1 else 0xff8015a0),'Every actual native floor-shadow copy has exact projected geometry, original pen and instruction cadence')
  indices=list(range(0,4*(height//4),4));indices.append(indices[-1])
  need([num(d,'source')for d in copies]==[decoded[key][i]for i in indices],'Every actual native projected shadow source row and duplicated final row are exact')
  pm[f,s].append(part);total_copies+=len(copies)
  if ids[s]in(17,18):own_copies+=len(copies)
 need(used_streams==set(streams),'Every unique observed stream belongs to actual owned projections')
 # Other effect-object native shadows may share the observer, but cannot be attributed to a fighter.
 other_dma=sum(len(v)for k,v in dma.items()if k not in matched_dma)
 for key,t in begin_by.items():
  expected=list(range(len(native_group(t,payload,guest))))if num(t,'body')&16 else[]
  need(pm[key]==expected,'Every source-defined eligible owned shadow component observed; ineligible bodies produce none')
 return dict(move=b['move'],side=side,state=state,actualContiguousActorFields=len(fields),actualRoutineEntryFrames=sorted(entry_frames),entryBodyPublicationProven=True,everyReadyBodyComponentSourceBound=True,actualNativeBodyCandidates=body_parts,actualPublishedBodyParts=published,actualClippedBodyParts=clipped,actualShadowEligibilityCalls=len(begins),actualOwnedShadowComponents=len(projections),actualUniqueROMStreams=len(streams),actualSourceBoundShadowCopies=total_copies,actualAddedFighterShadowCopies=own_copies,unattributedOtherObjectShadowCopies=other_dma,fullPortAcceptance=False,fullArtAcceptance=False,nativeFloorShadowCoverageAccepted=False,fullAudioAcceptance=False)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=tuple(human.SPECS),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 out=ROOT/f'audit_v5138_special_shadow_{args.move}_p{args.side}_checked';need(not out.exists(),'Fresh independent actual shadow proof')
 guest=native.expected();payload=(ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();pins={str(Path(__file__).resolve()):sha(__file__)};gfx=reconstruct(pins)
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in[(0xff801070,0xff8017b0),(0xff804160,0xff804430)]:need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],'Entire original native body/shadow kernel unchanged')
 b=load(args.move,args.side);case=check(b,guest,payload,gfx)
 for p,h in b['report']['inputHashes'].items():need(sha(p)==h,'Every executed current source/compiled input unchanged');pins[p]=h
 for p in(b['report_path'],ROOT/'tools/verify_special_repeat_v5115.py',ROOT/'tools/verify_move_phase_shadow_v5089.py',*(p for p in b['folder'].rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
 # Genuine mutations of actual records; one copy at a time, no no-op/KeyError counting.
 faults=[]
 mutations=[('missing_entry_body','MK2_HPHASE_CANDIDATE','source','00000000'),('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),('shadow_ineligible','MK2_HPHASE_SHADOW_BEGIN','body','0002'),('projection_shift','MK2_HPHASE_PROJECTION','dx','999'),('wrong_native_camera','MK2_HPHASE_PROJECTION','b4','00000000'),('wrong_native_floor','MK2_HPHASE_PROJECTION','floor','999'),('wrong_shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),('wrong_shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),('wrong_shadow_source','MK2_HPHASE_SHADOW_DMA','source','00000001')]
 for label,tag,key,value in mutations:
  changed=copy.deepcopy(b);index=next(i for i,t in enumerate(changed['rows'][tag])if num(t,'frame')in case['actualRoutineEntryFrames'])if label=='missing_entry_body'else 0
  need(changed['rows'][tag][index][key]!=value,'Actual fault is a real change, never no-op');changed['rows'][tag][index][key]=value
  try:check(changed,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual semantic fault accepted: '+label)
 for label in('actual_rom_stream_wrong','packed_row_start_wrong'):
  changed=copy.deepcopy(b)
  if label=='actual_rom_stream_wrong':changed['streams'][0]['sha256']='0'*64
  else:changed['streams'][0]['actualRowStarts'][1]+=1
  try:check(changed,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual source-stream fault accepted: '+label)
 need(all(sha(p)==h for p,h in pins.items()),'Every final source/evidence/native input stable')
 report=dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,payloadSHA256=native.PAYLOAD_SHA,case=case,actualSemanticFaultsRejected=faults,inputHashes=pins,scope=__doc__,rawGuestGFXRGBPCMOrWAVFilesWritten=0,fullPortAcceptance=False,fullArtAcceptance=False,nativeFloorShadowCoverageAccepted=False,fullAudioAcceptance=False)
 out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compress compact proof')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected')},indent=2))
if __name__=='__main__':main()
