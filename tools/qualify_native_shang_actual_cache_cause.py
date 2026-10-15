"""Qualify observed native cause, not a repair or a completed campaign.

Keep all4096 unique provenance records/4103 printed rows, every native
gameplay record and all146 global writes. Direct/ring duplicates are counted,
not silently dropped. Typed original program evidence binds the actual chain.
"""
import collections
import copy
import gzip
import hashlib
import json
import re
import struct
from pathlib import Path
import capture_native_sonya_shang_cache_cause as capture
import seal_native_sonya_shang_actual_cause as preserved

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_shang_actual_cache_cause_checked'
KINDS=['caller_input','victim_helper_enter','victim_index_input','index_start',
       'true_id_loaded','index_cell','index_result','caller_result',
       'victim_animation_enter','animation_token_consumed','cache_begin','first_global_write']
SITES=[0xff8cb010,0xff842ed0,0xff842f30,0xff83b7f0,0xff83b820,0xff83b840,
       0xff83b850,0xff8cb040,0xff842360,0xff83bb50,0xff838790,0x01060020]


def contract(chain,stock):
    need(len(chain)==12 and [q['kind'] for q in chain]==KINDS,'Entire twelve-event native caller-to-global-write chain')
    times=[float(q['seconds']) for q in chain]
    need(all(a<b for a,b in zip(times,times[1:])),'Actual strict native call/token/store chronology')
    ha,hm,ca,cm='01034020','0107A420','01034230','010757D0'
    for i,q in enumerate(chain):
        need(q['frame']=='480976' and q['human_actor']==ha and q['human_main']==hm and
             q['cpu_actor']==ca and q['cpu_main']==cm and q['human_id']==q['human_roster']=='18' and
             q['cpu_id']==q['cpu_roster']=='6' and q['health']=='0,56' and q['state']=='1,0' and
             q['mode']=='2' and q['stage']=='14' and q['winner']=='3' and
             q['writes']=='0' and q['assistance']=='none','Actual true18 victim/true6 performer, same physical slot and unassisted scene')
        actor=ha if i in (2,3,4,5,6,9,10,11) else ca
        main=hm if i in (2,3,4,5,6) else cm
        owner=ha if main==hm else ca
        need(q['actor']==actor and q['main']==main and q['main_owner']==owner and
             q['main_other']==(ca if main==hm else ha) and
             q['main_other_main']==(cm if main==hm else hm),
             'Exact actor/Main linkage; native renderer borrows victim A8 with performer Main, never a proxy')
        need(int(q['at'],16)==SITES[i] and int(q['pc'],16)==(0xff838860 if i==11 else SITES[i]+16),
             'Actual exact native instruction fetch/store location')
    off=lambda a:(a-0xff800000)//8
    word=lambda a:struct.unpack_from('<I',stock,off(a))[0]
    table=0xff9d7770;cell=table+18*32;result=word(cell);token=word(result)
    need(cell==0xff9d79b0 and result==0xff9d7b50 and token==0xffbf1840 and word(token)==0x007a003a,
         'Independent original table over-index selects composite, then raw58x122 bitmap descriptor rather than an animation/group')
    for i in (0,1,2,3):need(chain[i]['a0']==f'{table:08X}','Caller passes original victim roster table')
    need(chain[1]['stack0']=='FF8CB040' and chain[3]['stack0']=='FF842F60','Actual caller/lookup return addresses')
    need(chain[4]['a0']=='00000012' and chain[4]['a1']==f'{table:08X}' and
         chain[5]['a0']==f'{cell:08X}' and chain[5]['a1']==f'{table:08X}' and
         chain[5]['a0_rom']==f'{result:08X}' and chain[6]['a0']==f'{result:08X}' and
         chain[6]['a0_rom']==f'{token:08X}' and chain[7]['a0']==f'{result:08X}',
         'Actual true18 load,32-bit table cell and restored caller result')
    need(chain[8]['a11']==f'{result:08X}' and chain[8]['a0']=='00000006','Native six-field animation receives returned composite as stream')
    for i in (9,10):
        need(chain[i]['a0']==f'{token:08X}' and chain[i]['a9']==f'{result+32:08X}' and
             chain[i]['a11']==f'{result:08X}' and chain[i]['a9_prev_rom']==f'{token:08X}' and
             chain[i]['a0_rom']==f'{word(token):08X}',
             'Actual post-increment token reaches group renderer as raw bitmap descriptor')
    need(chain[11]['a0']=='FFBF1DC0' and chain[11]['a1']==chain[11]['at']=='01060020' and
         chain[11]['cache']=='0105ED30' and chain[11]['a9']=='FF9D7B70' and
         chain[11]['a9_prev_rom']=='FFBF1840','Actual unbounded descriptor walk overruns victim cache into game-global state')
    return dict(table=f'{table:08X}',trueVictimID=18,cell=f'{cell:08X}',returnedComposite=f'{result:08X}',
                consumedRawDescriptor=f'{token:08X}',postReadCursor=f'{result+32:08X}',firstGlobalAddress='01060020')


def run():
    need(not OUT.exists() and not capture.core.base.census.census(),'Fresh actual-cause receipt after original native terminal')
    paths=[capture.SOURCE/'report.json',preserved.OUT/'report.json',
           ROOT/'audit_native_shang_cause_preceding_campaign_checked/report.json']
    source,saved,prefix=[json.loads(p.read_text()) for p in paths]
    need(source['passed'] and saved['preservationPassed'] and not saved['passed'] and
         saved['actualGlobalStores']==146 and saved['earlierThirteenExactConservationAccepted'] and
         prefix['passed'] and prefix['accepted']['completeOriginalRows']==1009959 and
         prefix['accepted']['completedOpponents']==13 and len(prefix['allObservedCategoryFaultsRejected'])==56 and
         saved['actualNativeIdentity']==prefix['actualLiveNativeIdentity'],'Whole real failure and all thirteen earned fights retained')
    pins={}
    for proof in (source,saved,prefix):
        need(not proof['fullPortAcceptance'],'Finite proof does not complete the port')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'Every frozen input unchanged: '+p);pins[p]=h
    log=capture.OUT/'run.log.gz'
    with gzip.open(log,'rt') as f:lines=list(f)
    cause_lines=[q for q in lines if q.startswith('MK2_SONYA_SHANG_CACHE_CAUSE ')]
    parse=lambda line:dict(re.findall(r'(\w+)=([^\s]+)',line))
    records=[parse(q) for q in cause_lines]
    unique=list({json.dumps(q,sort_keys=True):q for q in records}.values())
    stop=[parse(q) for q in lines if q.startswith('MK2_SONYA_SHANG_CACHE_CAUSE_RESULT ')]
    need(len(records)==4103 and len(unique)==4096 and len(stop)==1 and
         stop[0]==dict(frame='480977',first_bad='480976',records='193832',retained='4096',writes='0',assistance='none'),
         'All4103 printed/4096 unique retained records and193832 observed native events accounted, including seven direct/ring duplicates')
    relevant=[q for q in unique if q['frame']=='480976' and q['kind'] in KINDS]
    chain=sorted(relevant,key=lambda q:float(q['seconds']))
    stock_path=ROOT/'mk2/mk2-maincpu.bin';stock=stock_path.read_bytes()
    need(sha(stock_path)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Exact independent original program')
    accepted=contract(chain,stock)
    faults=[]
    for i,q in enumerate(chain):
        changed=copy.deepcopy(chain);changed[i]['actor']='01000000'
        for name,bad in (('changed actor role',changed),('omitted native handoff',chain[:i]+chain[i+1:])):
            try:contract(bad,stock)
            except ValueError as error:faults.append(dict(kind=q['kind'],fault=name,rejectedBy=str(error)))
            else:raise ValueError('Altered native cause accepted')
    for i,key,value in ((4,'a0','00000001'),(5,'a0','FF9D79D0'),(6,'a0','FF9D7970'),
                        (8,'a11','FF9D7970'),(9,'a9','FF9D7B50'),(9,'a9_prev_rom','00000000'),
                        (10,'a0','FF9D7B50'),(11,'a1','0105ED30'),(9,'main_owner','01034020')):
        changed=copy.deepcopy(chain);changed[i][key]=value
        try:contract(changed,stock)
        except ValueError as error:faults.append(dict(kind=chain[i]['kind'],fault=key+'='+value,rejectedBy=str(error)))
        else:raise ValueError('Altered native type/ownership/overrun accepted')
    need(len(faults)==33 and contract(chain,stock)==accepted,'All33 actual role/type/omission faults reject; whole positive survives')
    all_native=[q for q in lines if q.startswith('MK2_NAT_CAMPAIGN_')]
    with gzip.open(capture.previous.OUT/'run.log.gz','rt') as f:previous_native=[q for q in f if q.startswith('MK2_NAT_CAMPAIGN_')]
    need(all_native==previous_native,'Entire old gameplay/health/input/failure chronology unchanged, not just the successful prefix')
    caches=[parse(q) for q in lines if q.startswith('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ')]
    overruns=[parse(q) for q in lines if q.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')]
    need(len(caches)==len(overruns)==146 and all(q['frame']=='480976' and q['pc']=='FF838860' and
         q['a8']=='01034020' and q['a13']=='010757D0' and q['a9']=='FF9D7B70' for q in overruns) and
         any('frame=480977 ' in q and 'stage=65535 ' in q and 'schedule=FFFFFFFF ' in q
             for q in lines if q.startswith('MK2_NAT_CAMPAIGN_STATE ')),
         'All146 native global stores and actual following destroyed scene retained')
    borrowed=[q for q in unique if q['kind']=='animation_token_consumed' and q['a0']=='FF9D7CB0']
    metadata_path=ROOT/capture.core.NAME/'build-info.json'
    metadata=json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    payload_path=Path(metadata['payload_hardlink_to_immutable_prior']);payload=payload_path.read_bytes()
    offset=lambda a:(a-0xfe800000)//8
    own56=struct.unpack_from('<I',payload,offset(0xff020000)+56*4)[0]
    need(sha(payload_path)==metadata['payload_sha256'] and own56==0xff02b070 and len(borrowed)==4 and
         [q['frame'] for q in borrowed]==['480932','480938','480944','480950'] and
         [q['a9'] for q in borrowed]==['FF02B150','FF02B1B0','FF02B210','FF02B270'] and
         all(q['actor']=='01034020' and q['human_id']=='18' and q['cpu_id']=='6' and
             struct.unpack_from('<I',payload,offset(int(q['a9'],16)-32))[0]==0xff9d7cb0 for q in borrowed),
         'Four actual inherited Liu victim composites in Sonya own main56, not a guessed visual defect')
    for p in (*paths,Path(__file__).resolve(),Path(capture.__file__),Path(preserved.__file__),
              stock_path,metadata_path,payload_path,log):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every frozen source/log/outcome intact after actual-cause qualification')
    report=dict(passed=True,nativeCauseAccepted=True,runtimeRootCauseResolved=True,nativeRepairAccepted=False,
        actualNativeIdentity=saved['actualNativeIdentity'],accepted=accepted,completeActualChain=chain,
        semanticFaultsRejected=faults,completePrintedProvenanceRows=4103,uniqueRetainedProvenanceRows=4096,
        completeObservedNativeProvenanceEvents=193832,explicitDirectRingDuplicateRows=7,
        completeProvenanceSHA256=hashlib.sha256(''.join(cause_lines).encode()).hexdigest().upper(),
        allPrintedKindCounts=dict(collections.Counter(q['kind'] for q in records)),
        entireGameplayChronologyExactlyConserved=True,completeNativeGameplayRows=len(all_native),
        completeNativeGameplaySHA256=hashlib.sha256(''.join(all_native).encode()).hexdigest().upper(),
        actualGlobalStores=146,actualCorruptingNativeFrame=480976,actualCorruptedSceneFrame=480977,
        entireFailedCampaignRemainsFailed=True,earlierThirteenEarnedFightsAccepted=True,
        actualBorrowedLiuVictimPoseBeforeLookup=True,actualBorrowedPoseRecords=borrowed,
        secondaryPaletteLookupAlsoRequiresRosterExtension=True,secondaryPaletteLookupRuntimeAcceptance=False,
        requiredRepair='Replace the missing true17/18 victim animation/palette rows with typed, character-owned native data. Repaint the four inherited Liu groups in BOTH owned main56 scripts. Preserve original native commands, alignment, palette ownership, timing, scheduler and every stock roster row. No proxy, renderer cap, fatality bypass or tactic-only avoidance.',
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(nativeCauseAccepted=True,nativeRepairAccepted=False,actualGlobalStores=146,
                         semanticFaultsRejected=33,completeNativeGameplayRows=len(all_native),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':run()
