"""Keep the actual bounded unsuccessful campaign and real CPU guard evidence."""
import gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_ai_response_full_context as native
import native_process_census_v6647 as census
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=native.ROOT,native.need,native.sha

def seal(capture):
    folder=ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice'
    out=folder/'bounded_controller_result.json'
    need(not out.exists() and not census.census(),'Actual original native terminal before immutable failure preservation')
    result=capture['result'];text=capture['text']
    need(result['passed'] and result['nativeExit']==0 and result['actualStages']==[0,1] and
         not result['nativeCacheOverrunObserved'],'Actual native transport succeeded; campaign did not clear')
    need(hashlib.sha256(capture['guest']).hexdigest().upper()==native.GUEST_SHA==result['guestSHA256'] and
         result['executableSHA256']==native.EXE_SHA,'Whole same actual current native guest')
    need(all(sha(p)==h for p,h in result['inputHashes'].items()),'Every actually executed input still unchanged')
    def rows(tag):return [dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    losses,stops,ends,ice=rows('LOSS'),rows('CONTROLLER_STOP'),rows('RESULT'),rows('CPU_ICE')
    need(len(losses)==8 and len(stops)==len(ends)==1 and ends[0]['losses']=='8' and
         ends[0]['ending']==ends[0]['ending_completed']=='-1' and len(ice)==2 and
         'MK2_POSTENDING_BEGIN ' not in text and 'MK2_POSTENDING_COMPLETE ' not in text,
         'Eight actual paid-continue losses, original bounded failure, never earned ending/join')
    for r in ice:
        need(r['entry']=='FF8A5900' and r['pc']=='FF8A5910' and r['value']=='24A0' and r['mask']=='FFFF' and
             r['id']=='8' and r['projectile']=='13' and r['human_id']=='17' and r['writes']=='0' and r['assistance']=='none',
             'Real source-bound CPU Subzero ice and true Kano owner, no assistance')
        frame=int(r['frame'])
        next_inputs=[x['button'] for x in rows('INPUT') if int(x['frame'])==frame+1]
        need(next_inputs==['Down','Block'],'Only ordinary Down/Block reacts on next native field')
    need('LUA ERROR' not in text and not (folder/'stderr.log').read_text(),'No native script/runtime error disguised as controller loss')
    driver=ROOT/'tools/capture_native_postending_join_cpu_ice.py'
    with gzip.open(folder/'executed_cpu_ice_driver.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(path=str(driver),sha256=sha(driver),text=driver.read_text()),stream)
    storage=[]
    for p in folder.rglob('*'):
        if not p.is_file():continue
        need(p.resolve().is_relative_to(ROOT.resolve()) and not p.is_symlink(),'Exact bounded evidence file')
        digest=sha(p)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,check=True)
        need(sha(p)==digest,'Original bounded trial bytes preserved')
        storage.append(dict(path=str(p),sha256=digest,allocatedBytes=allocated(p)))
    report=dict(passed=False,transportPassed=True,nativeExit=0,failedCampaignPreserved=True,
                actualPaidContinueLosses=8,actualStages=[0,1],endingAccepted=False,postEndingJoinAccepted=False,
                realCPUFreezeLaunchesObserved=2,ordinaryNextFieldReactiveGuardObserved=True,
                blockingContactSuccessClaim=False,reason='Automated physical guarded approach still loses to native Subzero; this is not evidence of a softlock or balance defect.',
                softlockClaim=False,gameBugClaim=False,fullPortAcceptance=False,goalStatus='active',
                sourceAndEvidenceFiles=storage,inputHashes=result['inputHashes'],driverSHA256=sha(driver),
                allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage),newBuilds=0,newROMCopies=0,newZIPs=0,
                nextAction='Fresh ordinary cold boot/coin-start timing may select another genuine native tower order. Keep original full ending and fresh Sonya join requirement; no guest RNG/state/AI/HP assistance.')
    out.write_text(json.dumps(report,indent=2)+'\n')
    return dict(campaignPassed=False,nativeExit=0,paidLosses=8,realCPUFreezeLaunches=2,
                allocatedEvidenceBytes=report['allocatedEvidenceBytes'])
