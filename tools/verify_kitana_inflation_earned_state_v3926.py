"""Current true-ID earned inflation command/tables/complete continuation.

Original921 physical controls are retained; only its PNG sink and the host
exit are adapted. Native scene/FIFO/pixels are separate prerequisites, never
replaced by a name or table-only compatibility test. No all-finisher claim.
"""
import copy,json,re,struct,subprocess,traceback
from pathlib import Path
import run_kitana_inflation_native_scene_v3920 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v3927_kitana_inflation_earned_state_checked'

def rows(text):
    result=[]
    for line in text.splitlines():
        match=re.match(r'MK2_STOCK_HEAD_V921_(\w+) ',line)
        if match:
            result.append(dict(tag=match[1],**dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return result

def gate(rs,fighter,side,guest):
    identity=17 if fighter=='kano'else 18
    items=lambda tag:[r for r in rs if r['tag']==tag]
    need(rs and all(r['victim']==fighter and r['side']==str(side)and r['killer']=='kitana'and r['writes']=='0'and r['assistance']=='none'for r in rs),'Every actual original state event true context/read-only')
    action,wrap,live,terminal=items('ACTION'),items('WRAP'),items('FIRST_LIVE'),items('RESULT')
    need(len(action)==len(wrap)==len(live)==len(terminal)==1,'One real native action, completion, first live and terminal')
    action,wrap,live,terminal=action[0],wrap[0],live[0],terminal[0];origin=int(action['frame'])
    need(action['damage']=='322'and action['mode']=='2'and action['actor']!=action['victim_actor']and action['main']!=action['victim_main']and
         live['ids']==f'4,{identity}'and live['own']==action['actor']and live['victim']==action['victim_actor'],'Native true Kitana/own victim and two earned rounds, no proxy')
    health=items('HEALTH');damage=[r for r in health if r['pc']=='FF836700'and int(r['frame'])<=origin]
    writers={'FF836700','FF825930'if side==1 else'FF825960','FF9DECE0'if side==1 else'FF9DED10','FF9DEF40'if side==1 else'FF9DEF70'}
    need(all(r['pc']in writers for r in health)and all(0<=int(r['after'])<=int(r['before'])<=161 for r in damage)and
         sum(int(r['before'])-int(r['after'])for r in damage)==322 and sum(r['after']=='0'for r in damage)==2,'All native physical health writers/collision bounds earn exactly two full KOs')
    wins=items('WIN');need([r['count']for r in wins]==['1','2']and not items('CACHE_OVERWRITE'),'Two native winner-table reads, no body-cache global overwrite')
    need(not any(r['mode']=='0'and int(r['frame'])>600 for r in items('MODE')),'No native watchdog/attract reset during gameplay')
    approach=items('APPROACH');need(len(approach)==1,'One actual physical approach')
    first=int(approach[0]['frame']);need(60<=int(approach[0]['gap'])<=68 and origin==first+44,'Original native command gap and entry cadence')
    inputs={(int(r['frame']),int(r['slot']),r['button'])for r in items('INPUT')}
    winner=3-side;forward='Left'if side==1 else'Right'
    need(all((first+age,winner,button)in inputs for age,button in((10,forward),(18,forward),(26,'Down'),(34,forward))),'Genuine original Forward Forward Down Forward physical command')
    need(all((f,winner,'Low_Kick')in inputs for f in range(first-60,first+42))and
         all((f,winner,'Low_Kick')not in inputs for f in range(first+42,origin+1)),'Actual held low kick then original release, not an injected action')
    compares=[r for r in items('COMPARE')if int(r['frame'])==origin]
    need(len(compares)==4 and all(r['actual']==r['wanted']for r in compares),'Actual original history parser accepts all four direction entries')
    parameters=items('PARAMETER');need(len(parameters)==2,'Both native timing/position word reads')
    for operand,dest,wanted in((0xff8cc790,0xfd680,0x40),(0xff8ccc80,0xfd6c0,0xffb7)):
        table=0xff800000+dest*8;at=table+identity*16
        matches=[r for r in parameters if int(r['operand'],16)==operand];need(len(matches)==1,'One actual parameter consumer')
        r=matches[0];need(struct.unpack_from('<I',guest,(operand-0xff800000)//8)[0]==table and struct.unpack_from('<H',guest,dest+identity*2)[0]==wanted and
             int(r['table'],16)==table and int(r['at'],16)==at and int(r['value'],16)==wanted and r['row']==str(identity)and
             r['actor']==action['victim_actor']and r['main']==action['victim_main']and r['pc']=='FF82EE10','Actual correctly typed own timing/position row, original consumer and physical victim owner')
    gore=items('GORE_ROW');need(len(gore)==6,'Three whole native stream/palette pointers read as six actual bus halves')
    for operand,dest in((0xff9ec840,0xfac40),(0xff9ec8b0,0xfac90),(0xff9ecbd0,0xface0)):
        table=0xff800000+dest*8;pointer=struct.unpack_from('<I',guest,dest+identity*4)[0]
        need(struct.unpack_from('<I',guest,(operand-0xff800000)//8)[0]==table,'Independent current native table operand')
        reads=sorted([r for r in gore if int(r['operand'],16)==operand],key=lambda r:int(r['half']))
        need(len(reads)==2 and [r['half']for r in reads]==['0','1']and all(int(r['table'],16)==table and
             int(r['at'],16)==table+identity*32+i*16 and int(r['value'],16)==pointer>>(i*16)&65535 and int(r['mask'],16)==65535 and
             r['row']==str(identity)and r['actor']==action['victim_actor']and r['main']==action['victim_main']and r['pc']=='FF83B850'for i,r in enumerate(reads)),'Genuine source-bound native whole pointer row and true physical owner')
    need(int(wrap['frame'])==origin+276 and wrap['age']=='276'and wrap['pc']=='FF8CDC50'and wrap['actor']==action['actor']and wrap['main']==action['main'],'Exact original native winner completion')
    need(terminal['damage']=='322'and terminal['wins']=='2'and int(terminal['action'])==origin and int(terminal['wrap'])==origin+276 and int(terminal['frame'])==origin+750,'Actual complete host window, original state and native continuation retained')
    need(any(r['mode']=='3'and origin+276<int(r['frame'])<origin+750 for r in items('MODE')),'Actual native continue screen reached before host exit')
    need([int(r['age'])for r in items('DISPLAY')]==list(range(0,601,10)),'All original diagnostic chronology retained despite RAM-only image sinks')
    return dict(origin=origin,identity=identity,side=side,actualNativeDamage=322,nativeKOs=2,nativeCompletionAge=276,wholeNativeTableReads=8,hostTerminal=origin+750,realContinueScreen=True)

def main():
    need(not OUT.exists(),'Fresh immutable earned-state proof')
    observation=ROOT/'audit_v3922_kitana_inflation_native_scene_observed/report.json';observed=json.loads(observation.read_text());need(observed['passed']and len(observed['cases'])==4,'Four actual current whole native scene captures')
    base,_,prior,_,_=capture.data.old.expected_current();payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    guest,_=capture.data.check(prior,stock,payload,base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    for source,dest,stride in((0xff8cd3b0,0xfd680,2),(0xff8cd2f0,0xfd6c0,2),(0xff9ed0f0,0xfac40,4),(0xff9eca40,0xfac90,4),(0xff9ecc30,0xface0,4)):
        lo=(source-0xff800000)//8;need(guest[dest:dest+17*stride]==stock[lo:lo+17*stride],'Every original stock table row preserved exactly')
    # Exact original UI health sentinel/restoration code, not a custom health
    # writer exemption. Physical collision checks remain strict above.
    lo,hi=(0xff9dec90-0xff800000)//8,(0xff9def70-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi],'Whole original UI sentinel/restoration routine unchanged')
    pins={str(observation):sha(observation),str(Path(__file__).resolve()):sha(__file__)};cases=[]
    for c in observed['cases']:
        fighter,side=c['fighter'],c['side'];folder=ROOT/f'audit_v3921_kitana_{fighter}_p{side}_native_scene_ram'
        meta=json.loads((folder/'result.json').read_text());text=(folder/'run.log').read_text()
        need(meta['exit_code']==0 and meta['candidate']==capture.NAME and meta['ramGuestSHA256']==capture.model.digest(guest)and not meta['modelErrors'],'Actual terminal current whole guest/native pixels, no verifier-only proxy')
        for p,h in meta['input_hashes'].items():need(sha(p)==h,'Executed inputs unchanged');pins[p]=h
        rs=rows(text);positive=gate(rs,fighter,side,guest);faults=[]
        trials=[('proxy_first_live','FIRST_LIVE','ids','4,1'),('foreign_actor','ACTION','actor','01000000'),('fabricated_damage','ACTION','damage','161'),
                ('wrong_health_writer','HEALTH','pc','FF838860'),('wrong_parameter_owner','PARAMETER','actor','01000000'),('wrong_native_pointer_half','GORE_ROW','value','FFFF'),
                ('wrong_command_parser','COMPARE','actual','999'),('wrong_completion_owner','WRAP','main','01000000'),('fabricated_terminal','RESULT','wins','3')]
        for label,tag,key,value in trials:
            changed=copy.deepcopy(rs);target=next(r for r in changed if r['tag']==tag and(tag!='COMPARE'or int(r['frame'])==positive['origin']))
            need(target[key]!=value,'Non-vacuous actual native state fault');target[key]=value
            try:gate(changed,fighter,side,guest)
            except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual state fault accepted '+label)
            need(gate(rs,fighter,side,guest)==positive,'Exact actual positive restored after each fault')
        changed=copy.deepcopy(rs);victim=3-side;first=next(r for r in changed if r['tag']=='APPROACH');f=int(first['frame'])+10
        changed=[r for r in changed if not(r['tag']=='INPUT'and r['frame']==str(f)and r['slot']==str(victim)and r['button']==('Left'if side==1 else'Right'))]
        need(len(changed)<len(rs),'Actual direction input removed')
        try:gate(changed,fighter,side,guest)
        except ValueError as error:faults.append(dict(kind='missing_actual_physical_direction',rejectedBy=str(error)))
        else:raise ValueError('Missing real input accepted')
        need(gate(rs,fighter,side,guest)==positive,'Final exact positive restored')
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        cases.append(dict(fighter=fighter,side=side,actualEarnedNativeState=positive,actualRecordFaultsRejected=faults))
    return dict(passed=True,actualContexts=4,actualRecordFaultsRejected=40,cases=cases,inputHashes=pins,currentNativeEarnedInflationStateAccepted=True,
        fullFinisherAudioAccepted=False,allFinishersAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited report compression')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
