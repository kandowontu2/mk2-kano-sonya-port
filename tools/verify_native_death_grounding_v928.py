"""Actual native owned death art, with grounding/roll acceptance still separate."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from PIL import Image
import build_native_death_art_v900 as assets
import verify_native_gore_victim_tables_v924 as gore

ROOT=Path(__file__).resolve().parents[1]
CASES=tuple(f'audit_v927_{name}_p{side}_native_death_grounding'for name in('kano','sonya')for side in(1,2))
EXE='B36C121BDDDBD30EE977098329BEF48FAFEF4F3164F8CA126D5D81DD42A7F8CE'
PAYLOAD='CC4F29043DE71AEEB0820D15E5A449A14073CDFBFA3F58B756751C92073964DF'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def records(text):
 parsed=[]
 for m in re.finditer(r'^MK2_REPTILE_V879_(\w+) (.*)$',text,re.M):
  row=dict(re.findall(r'(\w+)=([^\s]+)',m[2]))
  header=re.match(r'frame=\d+ victim=(kano|sonya) side=[12] writes=0 assistance=none ',m[2])
  row['header_victim']=header[1]if header else 'invalid'
  parsed.append((m[1],row))
 return parsed
def verify(texts=None,check_files=True):
 texts={case:(ROOT/case/'run.log').read_text(encoding='utf-8-sig')for case in CASES}if texts is None else texts
 errors=[];pins={};summaries={}
 def need(ok,label):
  if not ok:errors.append(label)
 for case,text in texts.items():
  directory=ROOT/case;result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
  name=result['player'];side=result['victim_slot'];identity=17 if name=='kano'else 18
  pointer=0xfffed000 if identity==17 else 0xfffed800
  stream='FF00B910'if identity==17 else'FF02B910'
  need(result['exit_code']==0 and result['winner_slot']==3-side and result['seconds']==95 and
       result['assistance']=='none'and result['cheats_enabled']is False,case+': cold physical-only completion')
  need(result['executable_sha256']==EXE and result['payload_sha256']==PAYLOAD,case+': exact current build')
  if check_files:
   for filename,wanted in result['input_hashes'].items():
    path=Path(filename);need(path.is_file()and digest(path)==wanted,'Frozen input changed: '+filename);pins[filename]=wanted
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),case+': no runtime errors')
  rows=records(text)
  original_case=case.replace('audit_v927_','audit_v904_',1)
  previous_text=(ROOT/original_case/'run.log').read_text(encoding='utf-8-sig')
  need(rows==records(previous_text),case+': unchanged genuine input/state/fatality replay after read-only camera instrumentation')
  need(all(r['writes']=='0'and r['assistance']=='none'and r['header_victim']==name and int(r['side'])==side for tag,r in rows),case+': consistent physical identity')
  need(not any(tag=='CACHE_OVERWRITE'for tag,r in rows),case+': no body-cache overrun')
  def items(tag):return [r for t,r in rows if t==tag]
  actions=items('ACTION');row_reads=items('ROW');heads=items('HEAD');wraps=items('WRAP');selected=items('PALETTE')
  need(len(actions)==len(heads)==len(wraps)==1,case+': one complete original fatality')
  if len(actions)!=1 or len(heads)!=1 or len(wraps)!=1:continue
  action=actions[0];start=int(action['frame'])
  need(action['damage']=='322'and action['mode']=='2'and action['actor']!=action['victim_actor']and
       action['main']!=action['victim_main'],case+': genuine two-round KO and distinct physical owners')
  live=items('FIRST_LIVE')
  need(len(live)==1 and live[0]['ids']==f'9,{identity}'and live[0]['own']==action['actor']and
       live[0]['victim']==action['victim_actor'],case+': actual Reptile and true victim, no proxy')
  health=items('HEALTH');damage=0;collisions=[]
  writers={0xff836700,0xff825930 if side==1 else 0xff825960,
           0xff9dece0 if side==1 else 0xff9ded10,0xff9def40 if side==1 else 0xff9def70}
  for r in health:
   before,after,pc=int(r['before']),int(r['after']),int(r['pc'],16)
   need(pc in writers,case+': original physical health writers only')
   if pc==0xff836700:
    need(0<=after<=before<=161,case+': original collision damage bounds')
    if int(r['frame'])<=start:damage+=before-after;collisions.append(r)
  need(damage==322 and len(collisions)==10 and sum(r['after']=='0'for r in collisions)==2,case+': observed 322 damage, two native KOs')
  need(len(items('WIN'))==2,case+': both original round wins observed')
  # Bind actual physical input sequence, not a claimed action name.
  inputs=items('INPUT');commands=[r for r in inputs if start-45<=int(r['frame'])<=start]
  lp=[r for r in commands if r['button']=='Low_Punch'and int(r['slot'])==3-side]
  need(len(lp)>=2 and int(lp[0]['frame'])==start-2 and
       any(r['button']=='Down'and int(r['slot'])==3-side for r in commands)and
       len([r for r in commands if r['button']in('Left','Right')and int(r['slot'])==3-side])>=8,
       case+': real Back Back Down LP input before stock action')
  values=(0xff3b,0xfffd,16,32)if identity==17 else(0xff3f,0xfffc,16,0)
  pcs=(0xff8c8aa0,0xff8c8ab0,0xff8c8af0,0xff8c8b30)
  need(len(row_reads)==4 and [int(r['field'])for r in row_reads]==list(range(4))and
       all(int(r['row'])==identity and int(r['data'],16)==values[i]and int(r['mask'],16)==0xffff and
           int(r['at'],16)==0xfffd4000+identity*64+i*16 and int(r['pc'],16)==pcs[i]and
           int(r['frame'])==start+97 for i,r in enumerate(row_reads)),case+': exact original four-field victim-table consumer')
  head=heads[0];wrap=wraps[0]
  expected_head='FFFD5460'if name=='kano'else'FFFD5D20'
  need(head['descriptor']==expected_head and head['stream']==stream and int(head['age'])==129 and
       int(head['frame'])==start+129,case+': own native head descriptor, no Liu fallback')
  need(int(wrap['age'])==187 and int(wrap['frame'])==start+187 and wrap['pc']=='FF8C9690',case+': native completion 90 fields after row read')
  need(len(selected)==2 and all(int(r['pointer'],16)==pointer and r['id']==str(identity)and
       r['pc']=='FF90C8E0'and r['physical_actor']==action['victim_actor']and
       r['physical_main']==action['victim_main']and r['owner']==action['victim_actor']and
       int(r['frame']) in(start+129,start+130)for r in selected),case+': real independent normal palette selection')
  need(any(r['actor']==r['physical_actor']and r['main']==r['physical_main']for r in selected),case+': physical body palette, not just detached effect')
  display=items('DISPLAY')
  need([int(r['age'])for r in display]==list(range(0,301,10))and
       all(int(r['frame'])==start+int(r['age'])for r in display),case+': actual full finisher snapshot chronology')
  pictures=directory/'snap'
  for age in range(0,301,10):
   path=pictures/f'reptile_victim_{start}_{age:03d}.png'
   need(path.is_file()and Image.open(path).size==(400,254),case+': actual picture '+str(age))
   previous=ROOT/original_case/'snap'/path.name
   need(previous.is_file()and path.read_bytes()==previous.read_bytes(),case+': unchanged actual rendered snapshot after read-only camera instrumentation')
   if check_files and path.is_file():pins[str(path)]=digest(path)
  terminal=items('RESULT')
  need(len(terminal)==1 and terminal[0]['damage']=='322'and terminal[0]['wins']=='2'and
       int(terminal[0]['action'])==start and int(terminal[0]['wrap'])==start+187 and
       int(terminal[0]['frame'])>start+1500,case+': terminal continuation after native wrap')
  summaries[case]={'victim':name,'slot':side,'nativeDamage':damage,'originalAction':start,
                   'nativeWrapAge':187,'rowReadAge':97,'bodyPalette':f'{pointer:08X}',
                   'snapshots':len(display),'remainingHeadIsLiu':False,'bodyArtAccepted':False}
  # Independently bind the installed guest descriptors and graphics to the
  # selected assets; do not treat a builder's green report as runtime proof.
  payload=(ROOT/'diagnostic_v918_native_gore_victim_tables/roms/mk2ks/mk2ks.mdata').read_bytes()
  guest=(directory/'guest_maincpu.bin').read_bytes()
  wanted_guest=gore.expected_guest()
  need(guest==wanted_guest,case+': entire current guest differs only by the five native victim table extensions')
  gfx=(directory/'native_death_gfx.bin').read_bytes()
  need(gfx==payload[assets.PIXELS:assets.PIXELS+49228],case+': actual initialized graphics exact packed assets')
  encoding=json.loads((ROOT/'audit_v900_native_death_grounding_encoding/report.json').read_text())
  frames=encoding['fighters'][name]['frames']
  by_source={int(r['graphics'],16):r for r in frames}
  art=[]
  for match in re.finditer(r'^MK2_DEATH_ART_V897_(\w+) (.*)$',text,re.M):
   art.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',match[2]))))
  need(all(r['writes']=='0'and r['assistance']=='none'for t,r in art),case+': read-only art observers')
  queued=[r for t,r in art if t=='QUEUE'];dmas=[r for t,r in art if t=='DMA']
  seen=set();owned_body=owned_head=0;ground_rows=set()
  fifo={(r['frame'],r['cursor'],r['source']):r for r in queued}
  for r in queued:
   source=int(r['source'],16);asset=by_source.get(source)
   need(asset is not None,case+': every native queue uses this victim artwork')
   if asset is None:continue
   need(r['physical']==action['victim_actor']and r['main']==action['victim_main']and
        r['owner']==r['physical']and r['id']==str(identity),case+': physical true-ID art owner')
   if asset['kind']=='body':
    need(r['actor']==r['physical']and int(r['pose'],16)==assets.GROUPS[name][asset['pose']],case+': actual owned main60 body pose')
    need(r['y']==r['floor'],case+': headless physical actor retains its own native floor')
    need(int(r['floor'])==int(r['stageY'])-(134 if name=='kano'else 135),case+': original stage-relative owned floor anchor')
    owned_body+=1;seen.add(asset['pose'])
   else:
    need(r['actor']!=r['physical']and r['cache']==asset['descriptor'],case+': independent native detached-head descriptor')
    owned_head+=1
  for r in dmas:
   asset=by_source.get(int(r['source'],16))
   need(asset is not None and r['queue_match']=='1'and r['fifo_physical']==action['victim_actor']and
        r['fifo_main']==action['victim_main'],case+': actual DMA bound to original native FIFO')
   if asset is not None:
    need([int(r['width']),int(r['height'])]==asset['size'],case+': actual native dimensions match encoded sprite')
    if asset['kind']=='body':
     q=fifo.get((r['frame'],r['cursor'],r['source']))
     need(q is not None,case+': exact current-frame ground projection queue')
     if q is not None:
      # Native win presentation changes display Y; the floor moves with it.
      # Use measured scene state, not a fixed screen row or art-specific offset.
      page=int(q['displayY'])&256
      ground=int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-page
      need((int(r['y'])&255)+int(r['height'])-1==ground,case+': every collapse pose contacts the native raster ground row')
      ground_rows.add(ground)
  need(ground_rows=={228,233,238},case+': measured ordinary and native win camera phases')
  need(seen==set(range(7))and owned_body>100 and owned_head>0 and len(dmas)==len(queued),case+': all seven body poses and separate head rendered')
  art_terminal=[r for t,r in art if t=='RESULT']
  need(len(art_terminal)==1 and int(art_terminal[0]['native_dma'])==len(dmas)and
       int(art_terminal[0]['last'])<int(terminal[0]['frame'])-1000,case+': native art retires well before terminal continuation')
  summaries[case].update(nativeBodyQueues=owned_body,nativeHeadQueues=owned_head,nativeArtDMAs=len(dmas),
                        headDescriptor=expected_head,ownedBodyPoses=sorted(seen),
                        floorGroundingAccepted=not any(e.startswith(case+':')for e in errors),
                        groundRasterRows=sorted(ground_rows))
  if check_files:
   for file in('guest_maincpu.bin','native_death_gfx.bin'):pins[str(directory/file)]=digest(directory/file)
  if check_files:
   for file in('run.log','result.json'):pins[str(directory/file)]=digest(directory/file)
 need(len(summaries)==4 and {(v['victim'],v['slot'])for v in summaries.values()}==
      {(n,s)for n in('kano','sonya')for s in(1,2)},'Both true victims in both physical slots')
 return {'passed':not errors,'errors':sorted(set(errors)),'nativeVictimTableAndNormalPaletteRuntimeAcceptance':not errors,
         'ownedHeadAndHeadlessBodyNativeRuntimeAcceptance':not errors,
         'reptileVictimDeadPoolGroundingAcceptance':not errors,'allFinisherAllArenaGroundingAcceptance':False,
         'fullNativeDeathArtAcceptance':False,'fullPortAcceptance':False,'alternatePaletteRuntimeAcceptance':False,
         'cases':summaries,'inputHashes':pins}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 if args.output.exists():raise ValueError('Preserve evidence')
 report=verify();args.output.mkdir();(args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
 raise SystemExit(0 if report['passed']else 1)
if __name__=='__main__':main()
