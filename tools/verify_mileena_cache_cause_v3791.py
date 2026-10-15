"""Prove actual unmodified-build Mileena victim-table corruption, not a fix.

Four real two-human contexts, original collision damage and native fatality
entry, actual ID-indexed reads followed by cache stores into player globals.
Counterexamples mutate executed rows. Art, game stability and port completion
are explicitly NOT accepted by this diagnostic.
"""
import copy,hashlib,json,re,struct,traceback
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
import verify_current_cpu_square_v3280 as guest_model
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3792_mileena_cache_cause_checked'
CONTEXTS=(('kano',1,'audit_v3788_mileena_kano_p1_earned_cache'),
 ('kano',2,'audit_v3788_mileena_kano_p2_earned_cache'),
 ('sonya',1,'audit_v3788_mileena_sonya_p1_earned_cache'),
 ('sonya',2,'audit_v3786_mileena_earned_cache'))
HEX={'pc','a0','a1','a5','a6','a7','a8','a9','a13','at','data','mask','actor','main','victim_actor','victim_main','own','victim'}
def parse(text):
    rows=[]
    for line in text.splitlines():
        match=re.match(r'^MK2_(CACHE_V3780|MILEENA_V3784)_(\w+) ',line)
        if not match:continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line));row['tag']=match[2];row['kind']=match[1]
        for k,v in list(row.items()):
            if k in HEX and re.fullmatch(r'[0-9A-F]{4,8}',v):row[k]=int(v,16)
            elif k in ('frame','row','id','side','damage','gap','before','after','held_fields','bad_frame','records')and re.fullmatch(r'-?\d+',v):row[k]=int(v)
        rows.append(row)
    return rows
def cause_gate(rows,fighter,side):
    errors=[]
    def require(value,message):
        if not value:errors.append(message)
    identity=17 if fighter=='kano'else18
    action=[r for r in rows if r['tag']=='ACTION'];eaten=[r for r in rows if r['tag']=='EATEN_TASK']
    reads=[r for r in rows if r['tag']=='ROW'];bad=[r for r in rows if r['tag']=='OVERRUN'];exits=[r for r in rows if r['kind']=='CACHE_V3780'and r['tag']=='HOST_EXIT']
    if not(action and eaten and len(reads)==2 and bad and exits):return dict(passed=False,errors=['Complete executed action/victim/table/cache/exit chain'])
    a,e,lo,hi,b,x=action[0],eaten[0],reads[0],reads[1],bad[0],exits[0]
    require(len(action)==1 and a['victim']==fighter and a['side']==side and a['damage']==322 and a['gap']<=69,'True context, two full original-health rounds and stock release distance')
    release=[r for r in rows if r['tag']=='HK_RELEASE']
    require(len(release)==1 and release[0]['held_fields']==135 and release[0]['frame']<a['frame'],'Actual physically held button release precedes native fatality')
    health=[r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before']<=161]
    require(sum(r['before']-r['after']for r in health)==322 and sum(r['after']==0 for r in health)==2,'Every earned decrement attributed to original native collision writer')
    require(e['id']==identity and e['a8']==a['victim_actor']and e['a13']==a['victim_main']and e['pc']==0xff9e7d80,'Actual native eaten task owns the true physical victim')
    for index,r in enumerate((lo,hi)):
        require(r['pc']==0xff83b850 and r['mask']==0xffff and r['row']==identity and r['id']==identity and
          r['at']==0xff9e9140+identity*32+index*16 and r['a1']==0xff9e9140 and r['a8']==e['a8']and r['a13']==e['a13'],
          'Both actual native ID-indexed halfword reads, physical ownership and exact writer')
    pointer=lo['data']|(hi['data']<<16)
    require(pointer==(0xff9e9520 if fighter=='kano'else0),'Actual short-table result is wrong-grammar Kano group or Sonya NULL')
    require(b['pc']==0xff838860 and 0x01060000<=b['at']<=0x01061fff and b['mask']==0xffff and
      b['a8']==e['a8']and b['a13']==e['a13']and a['frame']<e['frame']<=lo['frame']<=b['frame'],
      'Original cache copy overruns globals after the invalid true-ID lookup')
    require(x['bad_frame']==b['frame']and x['frame']==b['frame']+40,'Finite host exit after observed overrun; not a game victory or reset workaround')
    return dict(passed=not errors,errors=errors,pointer=pointer,actionFrame=a['frame'],lookupFrame=lo['frame'],overrunFrame=b['frame'],physicalVictim=f'{e["a8"]:08X}',physicalMain=f'{e["a13"]:08X}',observedGlobalStores=len(bad))
def run():
    need(not OUT.exists(),'Fresh immutable cause proof')
    expected=guest_model.expected_current()[0]
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    rd=lambda data,addr:struct.unpack_from('<I',data,(addr-0xff800000)//8)[0]
    need(rd(expected,0xff9e7ea0)==rd(original,0xff9e7ea0)==0xff9e9140,'Actual compiled model leaves the missing consumer unchanged')
    need(rd(expected,0xff9e9140+17*32)==0xff9e9520 and rd(expected,0xff9e9140+18*32)==0,'Independent whole initialized guest predicts both actual bad rows')
    pins={str(Path(__file__).resolve()):sha(__file__)};cases=[]
    for fighter,side,leaf in CONTEXTS:
        folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
        need(meta['terminalExitCode']==0 and meta['candidate']==current.NAME and not meta['fullPortAcceptance'],'Stopped actual3680 diagnostic only')
        for p,h in meta['input_hashes'].items():need(sha(p)==h,'Actual immutable executed input '+p);pins[p]=h
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav')),'No raster or PCM files')
        if (folder/'guest_maincpu.bin').exists():need((folder/'guest_maincpu.bin').read_bytes()==expected,'Whole guest independently reconstructed, no masked bytes')
        text=(folder/'run.log').read_text();need(not re.search(r'LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS',text+(folder/'stderr.log').read_text(),re.I),'Observer execution valid, guest corruption is still a real defect')
        rows=parse(text);positive=cause_gate(rows,fighter,side);need(positive['passed'],repr(positive))
        faults=(('proxy_victim','EATEN_TASK','id',1),('wrong_victim_owner','EATEN_TASK','a8',0x01032130),
          ('wrong_lookup_pc','ROW','pc',0xff906130),('wrong_row','ROW','row',1),('wrong_halfword_mask','ROW','mask',0xff),
          ('safe_pointer_substitution','ROW','data',0x1234),('unrelated_health_writer','OVERRUN','pc',0xff836700),
          ('cache_within_actor_not_globals','OVERRUN','at',0x0105f230),('unearned_two_rounds','ACTION','damage',161),
          ('missing_original_release','HK_RELEASE','held_fields',0),('wrong_bad_frame','HOST_EXIT','bad_frame',0))
        rejected=[]
        for label,tag,key,value in faults:
            mutated=copy.deepcopy(rows);target=next(r for r in mutated if r['tag']==tag and(tag!='HOST_EXIT'or r['kind']=='CACHE_V3780'));target[key]=value
            result=cause_gate(mutated,fighter,side);need(not result['passed'],'Reject actual-row fault '+label);need(cause_gate(rows,fighter,side)['passed'],'Restore complete actual positive')
            rejected.append(dict(name=label,errors=result['errors']))
        cases.append(dict(fighter=fighter,victimSlot=side,capture=leaf,cause=positive,actualRowFaultsRejected=rejected,
          wholeGuestDumpAvailable=(folder/'guest_maincpu.bin').exists(),fullPortAcceptance=False))
    # The long cold replay retains the same original physical/controller rows
    # through the first actual corrupting store. Its unretained diagnostic taps
    # were collected: preserve that failure and do not claim its provenance.
    old=ROOT/'audit_v3768_guarded_sonya_extended_p2_campaign/run.log';cold=ROOT/'audit_v3778_campaign_cache_provenance/run.log'
    def prefix(path):
        result=[]
        for line in path.read_text().splitlines():
            if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
            match=re.search(r' frame=(\d+) ',line)
            if match and int(match[1])<=223502:result.append(line)
        return result
    need(prefix(old)==prefix(cold),'Exact original cold controller/combat prefix through same corrupting frame')
    need('records=0'in cold.read_text()and 'bad_frame=-1'in cold.read_text(),'Original unretained tap diagnostic failure honestly preserved')
    for p in(old,cold,ROOT/'audit_v3775_guarded_sonya_p2_extended_state_checked/report.json',ROOT/'mame-mkp/src/frontend/mame/luaengine_mem.cpp'):pins[str(p)]=sha(p)
    return dict(passed=True,candidate=current.NAME,cases=cases,inputHashes=pins,actualColdCorruptionFrame=223502,
      stockCpuIdentityCorrected='Mileena ID5; Reptile is ID9',coldControllerPrefixByteMatched=True,
      unretainedTapDiagnosticAccepted=False,gameSourceOrPlayableBytesChanged=False,newBuildsOrPayloads=0,
      fullPortAcceptance=False,stabilityFixAccepted=False,scope=__doc__)
if __name__=='__main__':
    try:report=run()
    except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else1)
