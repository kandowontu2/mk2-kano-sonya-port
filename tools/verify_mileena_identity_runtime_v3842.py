"""Accept actual native swallowing stream/cleanup state in four earned contexts.

Not raster artwork, floor shadows/audio, all finishers or campaign acceptance.
"""
import copy,json,re,struct,subprocess
from pathlib import Path
import verify_native_mileena_victim_data_v3819 as data
import verify_mileena_cache_cause_v3793 as cause
ROOT=data.ROOT;OUT=ROOT/'audit_v3843_mileena_identity_runtime_checked'
def parse(text):
    return cause.parse(text.replace('MK2_CACHE_V3823_','MK2_CACHE_V3780_'))
def gate(rows,fighter,side):
    errors=[]
    def need(c,s):
        if not c:errors.append(s)
    identity=17 if fighter=='kano'else 18;count=7 if identity==17 else 8
    actions=[r for r in rows if r['tag']=='ACTION'];eats=[r for r in rows if r['tag']=='EATEN_TASK'];reads=[r for r in rows if r['tag']=='ROW']
    need(len(actions)==len(eats)==1 and len(reads)==2,'Actual native fatality/victim/lookup chain')
    if not(actions and eats and len(reads)==2):return dict(passed=False,errors=errors)
    action,eat,lo,hi=actions[0],eats[0],reads[0],reads[1]
    actor,main=action['victim_actor'],action['victim_main'];stream=(0xffd61400,0xffd61500)[identity-17]
    need(action['victim']==fighter and action['side']==side and action['damage']==322 and action['gap']<=69,'Real context and two full earned rounds')
    release=[r for r in rows if r['tag']=='HK_RELEASE']
    need(len(release)==1 and release[0]['held_fields']==135 and release[0]['frame']<action['frame'],'Real original held-HK release')
    health=[r for r in rows if r['tag']=='HEALTH'];damage=[r for r in health if r['pc']==0xff836700 and r['after']<r['before']<=161]
    need(sum(r['before']-r['after']for r in damage)==322 and sum(r['after']==0 for r in damage)==2,'Original collision damage earns two KOs')
    # Original FF9DEC90 initializes BOTH lifebar globals to FFFF, then
    # FF9DEEB0 restores them from A10=4 in the same field before match2.
    # This is a source-proven original UI initialization pair, not collision
    # health. The whole original routine is byte-identical in expected guest;
    # actual health rows also match the unmodified capture through ACTION.
    sentinel_pairs=set()
    for i,r in enumerate(health[:-1]):
        following=health[i+1]
        if r['frame']<action['frame'] and r['before']<=161 and r['after']==65535 and r['pc']==(0xff9dece0 if side==1 else 0xff9ded10) and following['frame']==r['frame'] and following['before']==65535 and following['after']==4 and following['pc']==(0xff9def40 if side==1 else 0xff9def70) and following['a13']==r['a13']:
            sentinel_pairs.update((i,i+1))
    need(all((i in sentinel_pairs or 0<=r['before']<=161 and 0<=r['after']<=161)and r['pc']!=0xff838860 for i,r in enumerate(health)),'No cache-driven/invalid health except exact original paired pre-action lifebar init')
    need(eat['id']==identity and eat['a8']==actor and eat['a13']==main and eat['pc']==0xff9e7d80,'Original native task owns actual true-ID victim')
    for i,r in enumerate((lo,hi)):
        need(r['pc']==0xff83b850 and r['at']==0xffd61800+identity*32+i*16 and r['mask']==0xffff and r['row']==r['id']==identity and r['a1']==0xffd61800 and r['a8']==actor and r['a13']==main,'Actual correct extended-table halfword read and physical ownership')
    need(lo['data']|(hi['data']<<16)==stream,'Lookup returns owned STREAM, not frame group or proxy')
    groups=[r for r in rows if r['tag']=='GROUP'and 0xffd61000<=r['a0']<0xffd613c0]
    need(len(groups)==count,'Every native pose is consumed exactly once')
    for phase,r in enumerate(groups):
        index=phase+(7 if identity==18 else 0)
        need(r['a0']==0xffd61000+index*64 and r['a9']==stream+(phase+1)*32 and r['frame']==lo['frame']+phase*4 and r['pc']==0xff8387a0 and r['a8']==actor and r['a13']==main,'Owned sequential group, physical actor and exact original four-field cadence')
        need(r['group'].split(',')[:2]==[f'{0xffd60000+index*160:08X}','00000000'],'Owned descriptor and immediate group terminator')
    disappeared=[r for r in rows if r['tag']=='DISAPPEAR'and r['frame']>=lo['frame']]
    need(len(disappeared)==1,'Actual native disappearance after animation')
    if disappeared:
        r=disappeared[0];need(r['pc']==0xff838f70 and r['frame']==lo['frame']+count*4 and r['a0']==r['a8']==actor and r['a13']==main and r['id']==identity and r['a9']==stream+(count+1)*32,'Original disappearance sees consumed native stream terminator')
        retired=[x for x in rows if x['tag']=='RETIRE'and x['frame']==r['frame']and x['a0']==actor]
        need(len(retired)==1 and retired[0]['pc']==0xff841ed0 and retired[0]['a8']==actor and retired[0]['a13']==main,'Actual native victim task retires')
    need(not any(r['tag']in ('OLD_ROW','OVERRUN')for r in rows),'No stale short-table reads or global cache overruns')
    terminal=[r for r in rows if r['tag']=='RESULT'and r['kind']=='CACHE_V3780'];exits=[r for r in rows if r['tag']=='HOST_EXIT'and r['kind']=='MILEENA_V3784']
    need(len(terminal)==len(exits)==1 and terminal[0]['bad_frame']==-1 and terminal[0]['frame']==action['frame']+601 and terminal[0]['records']>=count and exits[0]['frame']==action['frame']+601,'All retained observers live through full post-finisher host window; no bad-trigger exit')
    wins=[r for r in rows if r['tag']=='WIN'];need(len(wins)==2 and all(r['pc']==0xff8296b0 for r in wins),'Native two-round winner dispatch')
    states=[r for r in rows if r['tag']=='STATE'];need(any(r.get('mode')=='5'and r['frame']>lo['frame']+count*4 for r in states),'Game reaches normal post-match mode, not the original watchdog reset')
    for r in states:
        need(r['ids']==f'5,{identity}' and all(0<=int(h)<=161 for h in r['hp'].split(',')),'Native physical IDs/health retained throughout sampled state')
    return dict(passed=not errors,errors=errors,actionFrame=action['frame'],lookupFrame=lo['frame'],poseCount=len(groups),disappearanceFrame=disappeared[0]['frame']if disappeared else None,originalDamage=sum(r['before']-r['after']for r in damage),physicalActor=f'{actor:08X}',physicalMain=f'{main:08X}',scope=__doc__)
def main():
    data.need(not OUT.exists(),'Fresh runtime proof')
    old_guest,_,base,_,_=data.old.expected_current();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();payload=(data.ASSET/'roms/mk2ks/mk2ks.mdata').read_bytes()
    expected,_=data.check(base,stock,payload,old_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    build_path=ROOT/'diagnostic_v3836_native_mileena_rom_identity/build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));cases=[];pins={str(build_path):cause.sha(build_path),str(Path(__file__).resolve()):cause.sha(__file__)}
    data.need(build['executable_sha256']=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and build['expected_guest_sha256']==data.sha(expected),'Actual newly compiled build bound to independent full guest')
    prior_leaves={('kano',1):'audit_v3788_mileena_kano_p1_earned_cache',('kano',2):'audit_v3788_mileena_kano_p2_earned_cache',('sonya',1):'audit_v3788_mileena_sonya_p1_earned_cache',('sonya',2):'audit_v3786_mileena_earned_cache'}
    for fighter,side in prior_leaves:
        leaf=ROOT/f'audit_v3838_mileena_{fighter}_p{side}_rom_identity';meta=json.loads((leaf/'result.json').read_text());text=(leaf/'run.log').read_text()
        data.need(meta['terminalExitCode']==0 and meta['candidate']==build['name'],'Actual terminal candidate case')
        for p,h in meta['input_hashes'].items():data.need(cause.sha(p)==h,'Executed input unchanged');pins[p]=h
        data.need((leaf/'guest_maincpu.bin').read_bytes()==expected,'Every initialized guest byte agrees with independent reconstruction')
        data.need(not re.search(r'LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS',text+(leaf/'stderr.log').read_text(),re.I),'No instrumentation or initialization failure')
        data.need(not list(leaf.rglob('*.png'))and not list(leaf.rglob('*.wav')),'No raw raster or PCM copies')
        rows=parse(text);positive=gate(rows,fighter,side);data.need(positive['passed'],repr(positive))
        prior=ROOT/prior_leaves[(fighter,side)]/'run.log';oldtext=prior.read_text()
        def inputs(t):return [line for line in t.splitlines()if line.startswith('MK2_MILEENA_V3784_INPUT')and int(re.search(r'frame=(\d+)',line)[1])<=positive['actionFrame']]
        data.need(inputs(text)==inputs(oldtext),'All physical commands unchanged through original failing action')
        def health_prefix(t):return [line for line in t.splitlines()if line.startswith('MK2_MILEENA_V3784_HEALTH')and int(re.search(r'frame=(\d+)',line)[1])<=positive['actionFrame']]
        data.need(health_prefix(text)==health_prefix(oldtext),'Every actual pre-action health write including exact original UI sentinel pair unchanged')
        begin=(0xff9dec90-0xff800000)//8;end=(0xff9def70-0xff800000)//8
        data.need(expected[begin:end]==old_guest[begin:end]==stock[begin:end],'Entire original UI sentinel/restoration routine unchanged, no custom health exception code')
        rejected=[]
        for name,tag,key,value in [('proxy_id','EATEN_TASK','id',1),('wrong_owner','EATEN_TASK','a8',0x01032130),('old_lookup','ROW','a1',0xff9e9140),('wrong_pointer','ROW','data',0),('wrong_lookup_pc','ROW','pc',0xff906130),('missing_damage','ACTION','damage',161),('wrong_cadence','GROUP','frame',0),('wrong_group','GROUP','a0',0xff9e9520),('wrong_descriptor','GROUP','group','FFBFE0C0,00000000'),('missing_disappearance','DISAPPEAR','pc',0),('wrong_disappearance_owner','DISAPPEAR','a0',0),('bad_cache_exit','RESULT','bad_frame',223502),('wrong_health','HEALTH','after',32383)]:
            mutated=copy.deepcopy(rows);target=next(r for r in mutated if r['tag']==tag and(tag!='GROUP'or 0xffd61000<=r['a0']<0xffd613c0)and(tag!='RESULT'or r['kind']=='CACHE_V3780'));target[key]=value
            data.need(not gate(mutated,fighter,side)['passed'],'Reject actual-row counterexample '+name);rejected.append(name)
        data.need(gate(rows,fighter,side)['passed'],'Restored actual positive')
        for p in leaf.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=cause.sha(p)
        pins[str(prior)]=cause.sha(prior);cases.append(dict(fighter=fighter,side=side,actualNativeState=positive,actualRowFaultsRejected=rejected))
    OUT.mkdir();data.need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed evidence')
    value=dict(passed=True,candidate=build['name'],cases=cases,inputHashes=pins,actualContexts=4,actualRowFaultsRejected=52,wholeGuestAccepted=True,nativeVictimStreamsAndCleanupAccepted=True,artPixelsShadowsOrAudioAccepted=False,fullCampaignStabilityAccepted=False,fullPortAcceptance=False,scope=__doc__)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:v for k,v in value.items()if k not in ('inputHashes','cases')}))
if __name__=='__main__':main()
