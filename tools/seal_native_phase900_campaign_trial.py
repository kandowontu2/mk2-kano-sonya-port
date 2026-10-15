"""Retain genuine six-stage continued play; full ending/join still failed."""
import gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_ai_response_full_context as native
import native_process_census_v6647 as census
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=native.ROOT,native.need,native.sha

def seal(capture):
    folder=ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice_phase900'
    out=folder/'bounded_controller_result.json'
    need(not out.exists() and not census.census(),'Actual native terminal, original bounded failure not overwritten')
    r=capture['result'];text=capture['text']
    need(r['passed'] and r['nativeExit']==0 and r['actualStages']==list(range(6)) and
         r['executableSHA256']==native.EXE_SHA and r['guestSHA256']==native.GUEST_SHA and
         hashlib.sha256(capture['guest']).hexdigest().upper()==native.GUEST_SHA and not r['nativeCacheOverrunObserved'],
         'Same actual current guest, six real stages, normal native exit and no cache/global corruption')
    need(all(sha(p)==h for p,h in r['inputHashes'].items()),'All actually executed files intact before preserving trial')
    def rows(tag):return [dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    losses,ends,stops,live=rows('LOSS'),rows('RESULT'),rows('CONTROLLER_STOP'),rows('LIVE')
    need(len(losses)==8 and len(ends)==len(stops)==1 and ends[0]['losses']=='8' and
         ends[0]['ending']==ends[0]['ending_completed']=='-1' and not rows('CPU_ICE') and
         'MK2_POSTENDING_BEGIN ' not in text and 'MK2_POSTENDING_COMPLETE ' not in text,
         'Real paid-continue limit and no earned ending, join or fabricated CPU ice coverage')
    need(live and all(x['human']=='17:17' and x['writes']=='0' and x['assistance']=='none' for x in live),
         'Every sampled actual live actor remains true Kano17, never Liu proxy')
    boot=rows('BOOT');need(len(boot)==1 and boot[0]['boot']=='900','Only ordinary physical coin/start delay changed')
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I) and
         not (folder/'stderr.log').read_text(),'No native error mistaken for test-player losses')
    stages={}
    for x in live:
        stages.setdefault(x['stage'],set()).add(x['cpu'])
    storage=[]
    for p in folder.rglob('*'):
        if not p.is_file():continue
        need(p.resolve().is_relative_to(ROOT.resolve()) and not p.is_symlink(),'Exact original trial evidence file')
        digest=sha(p)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,check=True)
        need(sha(p)==digest,'Original evidence bytes conserved')
        storage.append(dict(path=str(p),sha256=digest,allocatedBytes=allocated(p)))
    report=dict(passed=False,transportPassed=True,nativeExit=0,failedCampaignPreserved=True,
                actualPaidContinueLosses=8,actualStages=list(range(6)),actualOpponentIDsByStage={k:sorted(v) for k,v in stages.items()},
                actualObservedTrueKanoFields=len(live),ordinaryCoinStartBootField=900,endingAccepted=False,postEndingJoinAccepted=False,
                realCPUFreezeLaunchesObserved=0,CPUFreezeCoverageClaim=False,
                reason='Current genuine Kano run advanced through five opponents but the zoning test player repeatedly lost to Kitana4 at stage5.',
                softlockClaim=False,gameBugClaim=False,fullArtAcceptance=False,fullAudioAcceptance=False,
                fullPortAcceptance=False,goalStatus='active',inputHashes=r['inputHashes'],sourceAndEvidenceFiles=storage,
                allocatedEvidenceBytes=sum(x['allocatedBytes'] for x in storage),newBuilds=0,newROMCopies=0,newZIPs=0,
                nextAction='Use already qualified character-specific ordinary campaign tactics rather than treating automated-player losses as an engine defect. Preserve the original earned ending and fresh join requirement.')
    out.write_text(json.dumps(report,indent=2)+'\n')
    return dict(campaignPassed=False,nativeExit=0,stages=list(range(6)),sampledTrueKanoFields=len(live),
                paidLosses=8,allocatedEvidenceBytes=report['allocatedEvidenceBytes'])
