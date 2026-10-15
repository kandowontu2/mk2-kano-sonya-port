"""Focused genuine stock4 corner/held-page control, not universal art approval."""
import copy,hashlib,json,re,struct,subprocess,traceback
from pathlib import Path
import numpy as np
from PIL import Image
import run_jax_arms_stock_corner_v4091 as capture
import verify_jax_arms_earned_v4078 as grammar
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4095_jax_arms_stock_corner_checked'

def gate(text,frames,image,guest,side):
    old=grammar.old.prior
    stock=old.rows(text,'MK2_STOCK_HEAD_V921');items=lambda tag:[r for t,r in stock if t==tag]
    actions,wraps,stops=items('ACTION'),items('WRAP'),items('RESULT')
    need(len(actions)==len(wraps)==len(stops)==1,'One actual original stock action/completion/terminal')
    action=actions[0];origin=int(action['frame'])
    need(action['address']=='FF8BE240'and action['variant']=='2'and action['damage']=='322'and action['mode']=='2','Actual original earned native Jax secondary action')
    live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']=='11,4'and live[0]['own']==action['actor']and live[0]['victim']==action['victim_actor'],'Genuine native Kitana4 victim, not relabelled Kano/Sonya')
    damage=[r for r in items('HEALTH')if r['pc']=='FF836700'and int(r['frame'])<=origin];health=161;closed=0
    for r in damage:
        before,after=int(r['before']),int(r['after']);need(before==health and 0<=after<before<=161,'Whole actual stock collision health chain')
        health=after
        if after==0:closed+=1;health=161
    need(closed==2 and sum(int(r['before'])-int(r['after'])for r in damage)==322 and len(items('WIN'))==2,'Two real161HP collision KOs')
    writers={'FF836700','FF825930'if side==1 else'FF825960','FF9DECE0'if side==1 else'FF9DED10','FF9DEF40'if side==1 else'FF9DEF70'}
    need(all(r['pc']in writers for r in items('HEALTH')),'Only original stock collision/reset health writes')
    approach=items('APPROACH');need(len(approach)==1,'One genuine native spacing')
    start=int(approach[0]['frame']);inputs={(int(r['frame']),r['button'])for r in items('INPUT')if r['slot']==str(3-side)}
    need(92<=int(approach[0]['gap'])<=100 and origin==start+44 and all((start+a,'Block')in inputs for a in(10,18,26,34))and(start+42,'Low_Punch')in inputs,'Actual four Block edges and LP, not state-assisted finisher')
    need(wraps[0]['age']=='147'and wraps[0]['pc']=='FF8CDC50'and int(wraps[0]['frame'])==origin+147 and
         int(stops[0]['frame'])==origin+750 and stops[0]['wins']=='2'and stops[0]['damage']=='322'and not items('CACHE_OVERWRITE'),'Original native timing and safe earned stock continuation')
    position=[r for r in items('TABLE_RETURN')if r['table']=='FFFDD280']
    need(len(position)==1 and position[0]['value']=='000AFF88'and position[0]['id']=='4'and position[0]['age']=='40'and position[0]['actor']==action['victim_actor'],'Actual original Kitana position row consumed by true stock victim')
    states=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_ARM_STOCK_STATE ')]
    ages=[41,89,170,176,182,608]
    need([int(r['age'])for r in states]==ages and [int(r['age'])for r in frames]==ages and all(int(r['frame'])==origin+age for r,age in zip(states,ages)),'Six actual source-bound presentation epochs, not whole-scene equivalence')
    need(all(r['writes']=='0'and r['assistance']=='none'and r['roster']=='4'for r in states)and all(r['id']=='4'and r['actor']==action['victim_actor']for r in states[:-1])and
         states[-1]['id']=='-1'and states[-1]['actor']=='00000000','True stock victim throughout six observations and actual pointer zero on final native WIN page')
    guest_rows=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_ARM_STOCK_GUEST_DIGEST ')]
    need(len(guest_rows)==1 and guest_rows[0]['sha256']==hashlib.sha256(guest).hexdigest().upper(),'Actual whole initialized guest compared in RAM')
    pixels=np.asarray(Image.open(image).convert('RGB'));need(pixels.shape==(834,800,3),'Exactly six essential native panels')
    for index,r in enumerate(frames):
        x,y=(index%2)*400,(index//2)*278
        need(hashlib.sha256(pixels[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()==r['rgbSHA256']and int(r['frame'])==origin+ages[index],'Every actual stock contact panel fullRGB exact, no composite/reposition/art substitution')
    return dict(identity=4,side=side,origin=origin,nativeWrapAge=147,realCollisionDamage=322,positionRow='000AFF88',firstNativeVictimX=int(states[0]['x']),
        allSixNativePanelsBound=True,actualPointerZeroOnFinalNativeWINPage=True,actualStockNativeVictimStandsArmlessOnHeldPage=True,wholeStockSceneReplayAccepted=False)

def run():
    need(not OUT.exists(),'Fresh immutable focused stock proof')
    observation=capture.OUT/'report.json';value=json.loads(observation.read_text());need(value['passed']and value['actualStockContexts']==2 and value['actualAddedCharacterContexts']==0,'Actual two original stock controls, never own-character evidence')
    guest=capture.current.expected();grammar.source_contract(guest);pins={str(observation):sha(observation),str(Path(__file__).resolve()):sha(__file__),str(Path(grammar.__file__)):sha(grammar.__file__)}
    cases=[]
    for case in value['cases']:
        side=case['side'];folder=Path(case['capture']);text=(folder/'run.log').read_text();image=Path(case['essentialNativeReview']);frames=case['frames']
        for p,h in case['inputHashes'].items():need(sha(p)==h,'Actual executed stock/control bytes unchanged');pins[p]=h
        positive=gate(text,frames,image,guest,side);faults=[]
        for tag,key,new,prefix in(('FIRST_LIVE','ids','11,17','MK2_STOCK_HEAD_V921_'),('ACTION','variant','1','MK2_STOCK_HEAD_V921_'),
                                 ('WRAP','age','146','MK2_STOCK_HEAD_V921_'),('TABLE_RETURN','value','00000000','MK2_STOCK_HEAD_V921_'),
                                 ('STATE','id','17','MK2_ARM_STOCK_'),('STATE','roster','17','MK2_ARM_STOCK_')):
            line=next(s for s in text.splitlines()if s.startswith(prefix+tag+' '))
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(n==1 and changed!=line,'Actual non-vacuous stock row fault')
            damaged=text.replace(line,changed,1)
            try:gate(damaged,frames,image,guest,side)
            except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
            else:raise ValueError('Actual stock control fault accepted '+key)
            need(gate(text,frames,image,guest,side)==positive,'Actual original stock positive restored')
        changed=copy.deepcopy(frames);changed[0]['rgbSHA256']='0'*64
        try:gate(text,changed,image,guest,side)
        except ValueError as error:faults.append(dict(tag='actual_native_panel',rejectedBy=str(error)))
        else:raise ValueError('Changed actual stock native panel digest accepted')
        need(gate(text,frames,image,guest,side)==positive,'Original actual stock panel restored')
        cases.append(dict(stock=positive,actualRowCounterexamplesRejected=faults))
    return dict(passed=True,actualStockContexts=2,actualAddedCharacterContexts=0,actualRowFaultsRejected=14,actualNativePanels=12,actualNativePanelPixels=1219200,cases=cases,inputHashes=pins,
        actualStockArmlessStandingVictimHeldWINBehaviorObserved=True,ownCornerArtPositionAccepted=False,fullStockSceneReplayAccepted=False,allStockFinisherFidelityAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable focused stock report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Stock proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
