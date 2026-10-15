"""Actual earned split and original mirrored actor grammar in six contexts.

Two explicitly labelled stock references qualify held WIN-page semantics.
Own IDs17/18 remain real identities. No game, health, AI or pixel writes.
Continuous pixel replay is a prerequisite, not a substitute for state proof.
This does not qualify all finisher audio, arenas or the complete port.
"""
import copy,json,re,struct,subprocess,traceback
from pathlib import Path
import run_kung_lao_split_native_scene_v3970 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v3975_kung_lao_split_earned_grammar_checked'
IDS={'kano':17,'sonya':18,'liu_kang':1,'kitana':4}
HEX={'at','pc','actor','other','a0','a9','a11','main','sp','st','flags','other_flags'}

def rows(text):
    found=[]
    for line in text.splitlines():
        m=re.match(r'MK2_STOCK_HEAD_V921_(\w+) ',line)
        if m:
            header=re.match(r'MK2_STOCK_HEAD_V921_\w+ frame=\d+ victim=(\w+) side=[12] killer=kung_lao writes=0 assistance=none ',line)
            found.append(dict(tag=m[1],header_victim=header[1]if header else'invalid',**dict(re.findall(r'(\w+)=([^\s]+)',line))))
        elif line.startswith('MK2_SPLIT_V1098_STATE '):
            r=dict(tag='SPLIT',**dict(re.findall(r'(\w+)=([^\s]+)',line)))
            for k in HEX:r[k]=int(r[k],16)
            for k in ('frame','age','id','other_id','writes'):r[k]=int(r[k])
            found.append(r)
    return found

def gate(rs,fighter,side,guest,payload):
    identity=IDS[fighter];items=lambda t:[r for r in rs if r['tag']==t]
    state_rows=[r for r in rs if r['tag']!='SPLIT']
    need(state_rows and all(r['header_victim']==fighter and r['side']==str(side)and r['killer']=='kung_lao'and r['writes']=='0'and r['assistance']=='none'for r in state_rows),'Every original physical event actual context and zero assistance')
    action,wrap,live,terminal=(items(t)for t in ('ACTION','WRAP','FIRST_LIVE','RESULT'))
    need(len(action)==len(wrap)==len(live)==len(terminal)==1,'One earned split action, completion, first live and terminal')
    action,wrap,live,terminal=action[0],wrap[0],live[0],terminal[0];origin=int(action['frame'])
    need(action['address']=='FF8C6040'and action['variant']=='1'and action['damage']=='322'and action['mode']=='2'and live['ids']==f'0,{identity}'and
         live['own']==action['actor']and live['victim']==action['victim_actor']and action['actor']!=action['victim_actor']and action['main']!=action['victim_main'],'True original Kung Lao and actual victim, two full rounds, no proxy')
    health=items('HEALTH');damage=[r for r in health if r['pc']=='FF836700'and int(r['frame'])<=origin]
    writers={'FF836700','FF825930'if side==1 else'FF825960','FF9DECE0'if side==1 else'FF9DED10','FF9DEF40'if side==1 else'FF9DEF70'}
    need(all(r['pc']in writers for r in health)and all(0<=int(r['after'])<=int(r['before'])<=161 for r in damage)and
         sum(int(r['before'])-int(r['after'])for r in damage)==322 and sum(r['after']=='0'for r in damage)==2,'Original health writers, bounded real collisions and two native KOs')
    need([r['count']for r in items('WIN')]==['1','2']and not items('CACHE_OVERWRITE'),'Two original round-win reads and no global body cache overwrite')
    need(not any(r['mode']=='0'and int(r['frame'])>600 for r in items('MODE')),'No watchdog or attract reset during active gameplay')
    approach=items('APPROACH');need(len(approach)==1,'One original physical approach');first=int(approach[0]['frame'])
    need(108<=int(approach[0]['gap'])<=116 and origin==first+36,'Original gap112 tolerance and actual command cadence')
    inputs={(int(r['frame']),int(r['slot']),r['button'])for r in items('INPUT')};winner=3-side;forward='Left'if side==1 else'Right'
    need(all((first+age,winner,forward)in inputs for age in (10,18,26))and all((first+age,winner,'Low_Kick')in inputs for age in (34,35,36))and
         all((first+age,winner,'Block')in inputs for age in range(10,34)),'Actual Forward Forward Forward plus low kick, original held block')
    comparisons=[r for r in items('COMPARE')if int(r['frame'])==origin and r['table']in ('FF878BF0','FF878C00','FF878C10')]
    need(len(comparisons)==3 and all(r['actual']==r['wanted']and r['pc']=='FF8777A0'for r in comparisons),'Original input-history comparisons accept all three directions')
    def read(address,fmt):
        if address>=0xff800000:raw=guest;lo=(address-0xff800000)//8
        else:need(0xfe800000<=address<0xff800000,'Native guest or mapped payload pointer');raw=payload;lo=(address-0xfe800000)//8
        size=struct.calcsize(fmt);need(address%16==0 and 0<=lo and lo+size<=len(raw),'Whole source-bound native read extent')
        return struct.unpack_from(fmt,raw,lo)[0]
    read32=lambda a:read(a,'<I');read16=lambda a:read(a,'<H')
    table=read32(0xff8cea70);stream=read32(table+identity*32);words=[read32(stream+n*32)for n in range(12)]
    need(words[3]==words[11]==0 and all(words[n]>=0xff800000 for n in (*range(3),*range(4,11))),'Actual three/zero/seven/zero source grammar')
    returns=[r for r in items('TABLE_RETURN')if int(r['table'],16)==table]
    need(len(returns)==1 and returns[0]['id']==str(identity)and int(returns[0]['value'],16)==stream and returns[0]['actor']==action['victim_actor']and returns[0]['main']==action['victim_main']and returns[0]['age']=='76','Actual true-ID split table consumer and original physical owner')
    states=[r for r in items('SPLIT')if r['id']==identity]
    need(states and all(r['pc']==r['at']+16 and r['writes']==0 and r['assistance']=='none'for r in states),'Every original split instruction fetch read-only')
    addresses=(0xff8cecb0,0xff8cece0,0xff8cede0,0xff8cef00,0xff8cefb0,0xff8cf030,0xff842630,0xff842650,0xff842690,0xff8426b0)
    at={a:[r for r in states if r['at']==a]for a in addresses}
    need(all(len(at[a])==1 for a in addresses[:6]),'Exactly one actual native split constructor')
    entry,lookup,seed=(at[a][0]for a in addresses[:3])
    stance=read32(read32(0xff906150+identity*32));selected=stance;selectors=[]
    while read32(selected)==8:
        wanted,target=read16(selected+32),read32(selected+48);selectors.append((wanted,target))
        need(len(selectors)<=19,'Bounded original MAIN0 selector walk');selected+=48
        if wanted==identity:selected=target;break
        selected+=32
    need(entry['a9']==0 and lookup['a9']==stance and seed['a9']==selected,'MAIN0 only seeds the second actor; no cut-body MAIN0 substitution')
    restored=at[0xff8cf030][0];physical,other,main=restored['actor'],restored['other'],restored['main'];half=stream+128
    need(physical==int(action['victim_actor'],16)and main==int(action['victim_main'],16)and physical!=other and restored['other_id']==identity and restored['a9']==restored['a11']==half,'Two genuine victim actors share original physical MAIN and SAME half stream')
    before,after=at[0xff8cef00][0],at[0xff8cefb0][0]
    need(before['other']==other and after['actor']==other and(before['other_flags']^after['flags'])==0x10,'Native second actor constructor toggles only X mirror')
    steps=[at[a]for a in addresses[6:]];need([len(r)for r in steps]==[8,8,8,8],'All seven paired half poses plus zero sentinel')
    first_age=steps[0][0]['age'];need(first_age in(166,167),'Original first half age')
    for n,rs4 in enumerate(zip(*steps)):
        a,b,c,d=rs4;cursor=half+n*32
        need(a['actor']==physical and a['other']==other and c['actor']==d['actor']==other and all(r['main']==main and r['id']==identity for r in rs4),'Actual primary/secondary identities and shared owner MAIN')
        need(a['a9']==a['a11']==cursor and b['a9']==cursor+32 and b['a11']==cursor and c['a9']==cursor and d['a9']==cursor+32 and d['a11']==cursor,'Same original stream with independent cursor advance')
        need(a['age']==first_age+6*n and all(r['frame']==a['frame']for r in rs4),'Original six-field paired animation cadence')
        need((a['flags']^a['other_flags'])&0x10==0x10 and a['words9']==a['words11']and a['words9'].split(',')[0]==f'{words[n+4]:08X}','Actual opposite X flip and same source group through final zero')
        need(d['sp']==a['sp']-64 and d['st']==b['st'],'Original saved-register stack and second status')
    palettes=items('PALETTE');need(len(palettes)==2 and {int(r['actor'],16)for r in palettes}=={physical,other},'Both actual actor palette fetches')
    for r in palettes:
        headless=read32(0xff90c840);pointer=read32(headless+identity*64+(32 if int(r['flags'],16)&64 else 0))
        need(int(r['pointer'],16)==pointer and r['id']==str(identity)and r['physical_actor']==action['victim_actor']and r['physical_main']==action['victim_main']and int(r['owner'],16)==physical and r['pc']=='FF90C8E0','Source-bound native death palette for both true victim actors')
    need(int(wrap['frame'])==origin+179 and wrap['age']=='179'and wrap['pc']=='FF8CDC50'and wrap['actor']==action['actor']and wrap['main']==action['main'],'Original native winner continuation owner and timing')
    need(terminal['damage']=='322'and terminal['wins']=='2'and int(terminal['action'])==origin and int(terminal['wrap'])==origin+179 and int(terminal['frame'])==origin+750,'Actual native result and full host observation window')
    need(any(r['mode']=='3'and origin+179<int(r['frame'])<origin+750 for r in items('MODE'))and [int(r['age'])for r in items('DISPLAY')]==list(range(0,601,10)),'Original continue mode and complete diagnostic chronology retained')
    return dict(origin=origin,identity=identity,side=side,nativeDamage=322,nativeKOs=2,firstHalfAge=first_age,pairedHalfSteps=8,physicalActor=physical,secondaryActor=other,sharedMain=main,stanceSeed=stance,selectedSeed=selected,selectors=selectors,splitStream=stream,nativeWrapAge=179,hostTerminal=origin+750)

def main():
    need(not OUT.exists(),'Fresh immutable proof')
    observation=ROOT/'audit_v3972_kung_lao_split_native_scene_observed/report.json';seen=json.loads(observation.read_text())
    need(seen['passed']and len(seen['cases'])==6,'Six actual native split captures including two true stock controls')
    base,_,prior,_,_=capture.data.old.expected_current();payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    guest,_=capture.data.check(prior,stock,payload,base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    off=lambda a:(a-0xff800000)//8
    original=bytearray(stock[off(0xff8ce9f0):off(0xff8cf110)]);struct.pack_into('<I',original,off(0xff8cea70)-off(0xff8ce9f0),0xff800000+0xfbf40*8)
    need(guest[off(0xff8ce9f0):off(0xff8cf110)]==original and guest[off(0xff842590):off(0xff842710)]==stock[off(0xff842590):off(0xff842710)],'Entire original victim task and paired animation, only declared victim table operand')
    need(guest[0xfbf40:0xfbf40+17*4]==stock[off(0xff8cf110):off(0xff8cf110)+17*4],'All seventeen original victim rows preserved')
    for at,wanted in ((0xff8ceca0,0x5729),(0xff8cefd0,0x4d2b),(0xff842680,0x4d69),(0xff8426c0,0x4d2b)):
        need(struct.unpack_from('<H',stock,off(at))[0]==wanted,'Original seed/restore/cursor instruction')
    need(struct.unpack_from('<I',stock,off(0xff8cecc0))[0]==0xff906090,'Original MAIN0 seed lookup call')
    lo,hi=off(0xff9dec90),off(0xff9def70);need(guest[lo:hi]==stock[lo:hi],'Original continue health sentinel/restoration code retained')
    pins={str(observation):sha(observation),str(Path(__file__).resolve()):sha(__file__)};cases=[];semantics=[]
    for c in seen['cases']:
        fighter,side=c['fighter'],c['side'];folder=ROOT/f'audit_v3971_kung_lao_{fighter}_p{side}_native_scene_ram'
        meta=json.loads((folder/'result.json').read_text());need(meta['exit_code']==0 and not meta['modelErrors']and meta['ramGuestSHA256']==capture.model.digest(guest),'Actual terminal whole guest/native renderer exact')
        for p,h in meta['input_hashes'].items():need(sha(p)==h,'All executed inputs unchanged');pins[p]=h
        rs=rows((folder/'run.log').read_text());positive=gate(rs,fighter,side,guest,payload);faults=[]
        trials=[('proxy_id','FIRST_LIVE','ids','0,8'),('foreign_action','ACTION','actor','01000000'),('wrong_health_writer','HEALTH','pc','FF838860'),('wrong_parser','COMPARE','actual','999'),('wrong_row','TABLE_RETURN','value','00000000'),('wrong_palette','PALETTE','pointer','00000000'),('wrong_wrap_owner','WRAP','main','01000000'),('wrong_terminal','RESULT','wins','3')]
        for label,tag,key,value in trials:
            changed=copy.deepcopy(rs);candidates=[r for r in changed if r['tag']==tag]
            target=next(r for r in candidates if (tag!='COMPARE'or r['table']=='FF878BF0')and(tag!='TABLE_RETURN'or r['table']=='FFFDFA00'))
            need(target[key]!=value,'Actual non-vacuous state fault');target[key]=value
            try:gate(changed,fighter,side,guest,payload)
            except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual state fault accepted '+label)
            need(gate(rs,fighter,side,guest,payload)==positive,'Actual positive restored after every fault')
        for label,at,key,value in (('main0_replaced',0xff8cece0,'a9',positive['splitStream']),('secondary_proxy',0xff8cf030,'other_id',8),('wrong_mirror',0xff8cefb0,'flags',0),('wrong_half_cursor',0xff842690,'a9',0),('wrong_cadence',0xff842630,'age',0),('wrong_saved_stack',0xff8426b0,'sp',0)):
            changed=copy.deepcopy(rs);target=next(r for r in changed if r['tag']=='SPLIT'and r['id']==IDS[fighter]and r['at']==at)
            need(target[key]!=value,'Actual non-vacuous constructor fault');target[key]=value
            try:gate(changed,fighter,side,guest,payload)
            except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual constructor fault accepted '+label)
            need(gate(rs,fighter,side,guest,payload)==positive,'Exact constructor positive restored')
        records=json.loads((folder/'continuous_scene_records.json').read_text());retired=c['nativeBothPointerTeardown'];later=[r for r in records if r['frame']>=retired+3]
        need(c['actualNativeHeldWinnerPageAfterPointersClear']and c['postRetirementNewVictimFIFO']==0 and c['postRetirementNewRender']is False and later and all(not r['modeledFlip']and r['rgbSHA256']==records[retired-positive['origin']-1]['rgbSHA256']for r in later),'Native last winner page held exactly without new victim rendering after pointer teardown')
        need(later[-1]['body'][str(side)]['pixels']>0 and later[-1]['nativeSecondarySplitPixels']>0,'Actual held native page contains both split halves, separately from live actors')
        semantics.append(dict(fighter=fighter,side=side,stockReferenceOnly=IDS[fighter]in(1,4),pointerTeardownAge=retired-positive['origin'],postRetirementFields=len(later),newFlips=0,newVictimFIFO=0,heldVictimPixels=later[-1]['body'][str(side)]['pixels'],heldSecondaryPixels=later[-1]['nativeSecondarySplitPixels']))
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        cases.append(dict(fighter=fighter,side=side,state=positive,actualRecordFaultsRejected=faults))
    need({s['fighter']for s in semantics if s['stockReferenceOnly']}=={'kitana','liu_kang'}and len({(s['pointerTeardownAge'],s['postRetirementFields'])for s in semantics})==1,'Both genuine stock reference semantics match all four own contexts, not a guessed cleanup exemption')
    return dict(passed=True,cases=cases,actualContexts=6,ownContexts=4,stockContexts=2,actualRecordFaultsRejected=sum(len(c['actualRecordFaultsRejected'])for c in cases),stockHeldWinnerPageSemanticsAccepted=True,heldPageComparisons=semantics,inputHashes=pins,allFinisherAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited report compression')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
