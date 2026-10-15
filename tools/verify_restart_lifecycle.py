"""Full post-ending fresh match -> real join -> complete KO/move lifecycle."""
import argparse
import json
import re
from pathlib import Path
from verify_current_lifecycle import verify as verify_cycles, rows as cycle_rows

IDS={'kano':17,'sonya':18}
COORDS={17:(0,0),1:(1,0),0:(2,0),2:(3,0),9:(4,0),18:(5,0),8:(1,1),6:(2,1),4:(3,1),11:(4,1),5:(1,2),3:(2,2),10:(3,2),7:(4,2)}
HEX={'actor','main','pc','a8','a13'}
TEXT={'target','victim','move','route','button','pass'}


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_JOIN_LIFE_'+tag+' '):continue
        row={}
        for key,value in re.findall(r'(\w+)=([^\s]+)',line):
            if key in TEXT and not (key=='target' and tag in ('CSS','HIGHLIGHT')):row[key]=value
            elif key in ('p1','p2'):row[key]=tuple(map(int,value.split(',')))
            else:row[key]=int(value,16 if key in HEX else 10)
        if tag=='CSS':row.setdefault('route','')
        result.append(row)
    return result


def _verify(log,target,side,require_restart,mobility=False,projectile=False,impact=False,projectile_contact_verifier=None):
    errors=[]
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    short=mobility or projectile
    move=('knife' if target=='kano' else 'ring') if projectile else ('ball' if target=='kano' else 'square') if mobility else ('blade' if target=='kano' else 'bicycle')
    victim='sonya' if target=='kano' else 'kano'
    ids={side:IDS[target],3-side:IDS[victim]}
    begin,css,attach,highlight,match,complete,result=[rows(log,t) for t in ('BEGIN','CSS','ATTACH','HIGHLIGHT','MATCH','COMPLETE','RESULT')]
    check(len(begin)==len(attach)==len(result)==1 and len(css)==len(highlight)==len(match)==len(complete)==2,'Actual complete challenger transition anchors')
    if not (len(begin)==len(attach)==len(result)==1 and len(css)==len(highlight)==len(match)==len(complete)==2):
        return {'passed':False,'errors':errors,'target':target,'side':side}
    b,a,r=begin[0],attach[0],result[0];bf=b['frame'];cf=css[0]['frame'];mf=match[0]['frame'];df=complete[0]['frame']
    check(b['target']==target and b['side']==side and b['joining']==3-side and b['victim']==victim and b['move']==move and b['mode']==2 and
          b[f'p{side}']==(1,IDS[target]) and b[f'p{3-side}'][0]==0 and b['writes']==0,'Fresh human/CPU roles before actual join')
    if require_restart:
        fresh=re.findall(r'^MK2_RESTART_COMPLETE frame=(\d+)[^\r\n]* live=601 errors=0 restart_writes=0',log,re.M)
        fresh_match=re.findall(r'^MK2_RESTART_MATCH frame=(\d+) target='+target+r' id='+str(IDS[target])+r' ',log,re.M)
        check(len(fresh)==len(fresh_match)==1 and int(fresh[0])==bf and bf-int(fresh_match[0])==600,'Actual prior 601-field post-ending match anchors')
    check(60<cf-bf<350 and a=={'frame':cf+156,'move':move,'side':side,'target':target,'victim':victim,'writes':0} and cf+184<mf<cf+900 and (df==mf+600 if short else df>mf+1500),'Native attach/highlight/confirmation/match chronology')
    controls=rows(log,'CONTROL');expected=[]
    for key,first in (('coin',10),('coin',30),('start',60)):
        expected += [(bf+age,3-side,key) for age in range(first,first+5)]
    for c in css:
        slot=c['slot'];desired=ids[slot];x,y=COORDS[c['initial']];tx,ty=COORDS[desired]
        route=['up']*y+[('left' if tx<x else 'right')]*abs(tx-x)+['down']*ty
        check(c['frame']==cf and c['target']==desired and c['state']==3 and c['route']==','.join(route) and c['writes']==0,'Actual canonical joined CSS routes/controllers')
        for i,key in enumerate(route):expected += [(cf+56+i*12+j,slot,key) for j in range(5)]
        expected += [(cf+176+j,slot,'hp') for j in range(8)]
    check(sorted((c['frame'],c['slot'],c['button']) for c in controls)==sorted(expected) and all(c['value']==1 and c['writes']==0 for c in controls),'All real coin/start/navigation/confirmation pulses')
    check({c['slot'] for c in css}=={1,2} and {h['slot'] for h in highlight}=={1,2} and
          all(h['frame']==cf+156 and h['age']==156 and h['target']==h['roster']==ids[h['slot']] and h['state']==3 and h['writes']==0 for h in highlight),'Both actual native highlights before confirmation')
    fields=rows(log,'FIELD');by_frame={(f['frame'],f['slot']):f for f in fields}
    check(len(fields)==len(by_frame)==2*(df-mf+1) and set(by_frame)=={(f,s) for f in range(mf,df+1) for s in (1,2)},'Every joined field through KO/next-round completion')
    null_frames=set()
    for f in fields:
        slot=f['slot']
        check(f['age']==f['frame']-mf and f['roster']==ids[slot] and f['state']==1 and 0x01000000<=f['main']<0x01100000 and f['writes']==0 and f['mode'] in (2,5,6,7),'Actual joined epoch/roster/controller/native modes')
        if f['actor']==0:
            null_frames.add(f['frame']);check(f['mode']==6 and f['id']==65535,'Only native round construction may retire actors')
        else:check(0x01000000<=f['actor']<0x01100000 and f['id']==ids[slot],'Actual owned live actors outside round construction')
    check(len(null_frames)==(0 if short else 1),'Expected actual native round-construction fields')
    if len(null_frames)==1:
        nf=next(iter(null_frames));check(all(by_frame[nf,s]['actor']==0 and by_frame[nf-1,s]['actor']!=0 and by_frame[nf+1,s]['actor']!=0 for s in (1,2)),'Both round actors retire/reconstruct within one native field')
    for tag,anchors,at in (('MATCH',match,mf),('COMPLETE',complete,df)):
        check({s['slot'] for s in anchors}=={1,2} and all(s==by_frame.get((at,s['slot'])) and s['mode']==2 and s['id']==ids[s['slot']] for s in anchors),'Actual '+tag+' matches same-frame owners')
    check(all(m['hp']==161 for m in match),'Native join resets both health bars')
    if projectile:
        from verify_projectile_contact import verify as verify_contact, rows as contact_rows
        life=(projectile_contact_verifier(log,target,side) if projectile_contact_verifier is not None else
              verify_contact(log,target,side,impact=impact))
        traced=contact_rows(log,'FIELD');typed=contact_rows(log,'HEALTH')
        check(df-mf==600,'Full 601-field joined projectile contact')
    elif mobility:
        from verify_mobility_contact import verify as verify_contact, rows as contact_rows
        life=verify_contact(log,target,side)
        traced=contact_rows(log,'FIELD');typed=contact_rows(log,'HEALTH')
        check(df-mf==600,'Full 601-field joined mobility contact and subsequent controls')
    else:
        life=verify_cycles(log,move,side,victim,require_base=False)
        traced=cycle_rows(log,'FIELD');typed=cycle_rows(log,'HEALTH')
    errors.extend('Lifecycle: '+e for e in life['errors'])
    for f in traced:
        actual=by_frame.get((f['frame'],f['slot']))
        check(actual is not None and all(actual[k]==f[k] for k in ('actor','main','id','roster','state','hp')),'Full-cycle fields bind to actual joined match, not another run')
    native=rows(log,'HEALTH')
    damage=[h for h in native if h['pc']==0xFF836700]
    check(len(damage)==len(typed) and [{k:h[k] for k in ('frame','slot','before','after','pc','a8','a13')} for h in damage]==
          [{k:h[k] for k in ('frame','slot','before','after','pc','a8','a13')} for h in typed],'Whole joined health stores exactly match native move damage')
    resets=[h for h in native if h['pc']!=0xFF836700]
    if short:check(not resets,'No joined health resets or nonnative damage substitutions')
    check(all(h['pc'] in (0xFF825930,0xFF825960,0xFF9DECE0,0xFF9DED10,0xFF9DEF40,0xFF9DEF70) for h in resets),'Only original native round/HUD reset writes outside damage')
    for slot in (() if short else (1,2)):
        h=[x for x in resets if x['slot']==slot]
        if slot==3-side:
            reset_pc=0xFF825930 if slot==1 else 0xFF825960
            check(bool(h) and (h[0]['pc'],h[0]['before'],h[0]['after'])==(reset_pc,0,161),'Actual KO victim native round reset')
            h=h[1:]
        sentinel=0xFF9DECE0 if slot==1 else 0xFF9DED10
        fill=0xFF9DEF40 if slot==1 else 0xFF9DEF70
        expected_fill=[4,*range(6,161,2),161]
        check(len(h)==81 and h[0]['pc']==sentinel and h[0]['before']==161 and h[0]['after']==65535 and
              [x['after'] for x in h[1:]]==expected_fill and all(x['pc']==fill for x in h[1:]),'Exact original next-round HUD sentinel/fill, slot '+str(slot))
    for slot in (1,2):
        value=161;writes=[h for h in native if h['slot']==slot];index=0
        for frame in range(mf,df+1):
            while index<len(writes) and writes[index]['frame']<frame:
                h=writes[index];check(h['before']==value,'Original complete joined health-write chain');value=h['after'];index+=1
            check(by_frame.get((frame,slot),{}).get('hp')==value,'Every actual joined health field matches native stores')
    check(r=={'pass':'true','target':target,'side':side,'victim':victim,'move':move,'begin':bf,'css':cf,'attached':a['frame'],'match':mf,'complete':df,'fields':df-mf+1,'errors':0,'writes':0},'Actual completed native joined lifecycle result')
    check('MK2_JOIN_LIFE_ERROR' not in log,'No actual joined observer errors')
    return {'passed':not errors,'errors':errors,'target':target,'side':side,'move':move,'joined_fields':df-mf+1,
            'full_post_ending_match_required':require_restart,'scope':('actual_join_projectile_geometry_contact_not_full_impact_choreography_CPU_or_audio' if projectile else 'actual_join_full_lifecycle_not_unassisted_source_tower_or_CPU')}


def verify(log,target,side,require_restart=True):
    try:return _verify(log,target,side,require_restart)
    except (KeyError,ValueError,TypeError,IndexError) as error:
        return {'passed':False,'errors':['Malformed/incomplete joined trace: '+str(error)],'target':target,'side':side}


def verify_mobility_join(log,target,side,require_restart=True):
    try:return _verify(log,target,side,require_restart,True)
    except (KeyError,ValueError,TypeError,IndexError) as error:
        return {'passed':False,'errors':['Malformed/incomplete joined mobility trace: '+str(error)],'target':target,'side':side}


def verify_projectile_join(log,target,side,require_restart=True,impact=False,contact_verifier=None):
    try:return _verify(log,target,side,require_restart,projectile=True,impact=impact,projectile_contact_verifier=contact_verifier)
    except (KeyError,ValueError,TypeError,IndexError) as error:
        return {'passed':False,'errors':['Malformed/incomplete joined projectile trace: '+str(error)],'target':target,'side':side}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path)
    parser.add_argument('--target',choices=IDS,required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
    parser.add_argument('--mobility-contact',action='store_true');parser.add_argument('--cold',action='store_true')
    args=parser.parse_args()
    verifier=verify_mobility_join if args.mobility_contact else verify
    result=verifier(args.log.read_text(encoding='utf-8-sig'),args.target,args.side,require_restart=not args.cold)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
