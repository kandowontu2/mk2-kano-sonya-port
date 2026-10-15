"""True-ID stock Reptile victims in both slots; art remains explicitly wrong."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
import verify_death_palette_v882 as palette

ROOT=Path(__file__).resolve().parents[1]
CASES=('audit_v887_sonya_p2_stock_reptile_victim','audit_v888_kano_p1_stock_reptile_victim',
       'audit_v888_kano_p2_stock_reptile_victim','audit_v888_sonya_p1_stock_reptile_victim')
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
  need(result['executable_sha256']==palette.EXE and result['payload_sha256']==palette.PAYLOAD,case+': exact current build')
  if check_files:
   for filename,wanted in result['input_hashes'].items():
    path=Path(filename);need(path.is_file()and digest(path)==wanted,'Frozen input changed: '+filename);pins[filename]=wanted
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),case+': no runtime errors')
  rows=records(text)
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
  values=(0xff3b,0,16,32)if identity==17 else(0xff3f,0xfffb,16,0)
  pcs=(0xff8c8aa0,0xff8c8ab0,0xff8c8af0,0xff8c8b30)
  need(len(row_reads)==4 and [int(r['field'])for r in row_reads]==list(range(4))and
       all(int(r['row'])==identity and int(r['data'],16)==values[i]and int(r['mask'],16)==0xffff and
           int(r['at'],16)==0xfffd4000+identity*64+i*16 and int(r['pc'],16)==pcs[i]and
           int(r['frame'])==start+97 for i,r in enumerate(row_reads)),case+': exact original four-field victim-table consumer')
  head=heads[0];wrap=wraps[0]
  need(head['descriptor']=='FFB4A4B0'and head['stream']==stream and int(head['age'])==129 and
       int(head['frame'])==start+129,case+': expose actual remaining Liu head, do not conceal art gap')
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
   if check_files and path.is_file():pins[str(path)]=digest(path)
  terminal=items('RESULT')
  need(len(terminal)==1 and terminal[0]['damage']=='322'and terminal[0]['wins']=='2'and
       int(terminal[0]['action'])==start and int(terminal[0]['wrap'])==start+187 and
       int(terminal[0]['frame'])>start+1500,case+': terminal continuation after native wrap')
  summaries[case]={'victim':name,'slot':side,'nativeDamage':damage,'originalAction':start,
                   'nativeWrapAge':187,'rowReadAge':97,'bodyPalette':f'{pointer:08X}',
                   'snapshots':len(display),'remainingHeadIsLiu':True,'bodyArtAccepted':False}
  if check_files:
   for file in('run.log','result.json'):pins[str(directory/file)]=digest(directory/file)
 need(len(summaries)==4 and {(v['victim'],v['slot'])for v in summaries.values()}==
      {(n,s)for n in('kano','sonya')for s in(1,2)},'Both true victims in both physical slots')
 return {'passed':not errors,'errors':sorted(set(errors)),'nativeVictimTableAndNormalPaletteRuntimeAcceptance':not errors,
         'fullNativeDeathArtAcceptance':False,'fullPortAcceptance':False,'alternatePaletteRuntimeAcceptance':False,
         'cases':summaries,'inputHashes':pins}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 if args.output.exists():raise ValueError('Preserve evidence')
 report=verify();args.output.mkdir();(args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
 raise SystemExit(0 if report['passed']else 1)
if __name__=='__main__':main()
