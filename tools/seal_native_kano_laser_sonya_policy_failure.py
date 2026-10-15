"""Preserve actual failed controller trial and release its exact RAM host.

A passing preservation receipt never accepts a campaign, ending or game fix.
All original failed reports/inputs remain immutable; no new native replay.
"""
import gzip
import hashlib
import json
import os
import re
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_sonya_postending as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_kano_laser_sonya_policy_failure_preserved'
RETIRED=ROOT/'audit_native_kano_laser_sonya_policy_failure_retirement'
PARENT,GAME,PORT=168996,191216,55236


def prepare(ram,carrier,server):
    need(not OUT.exists() and os.getpid()==PARENT and server.server_port==PORT,
         'Exact actual original failed trial RAM parent/server')
    folder=original.OUT; result=json.loads((folder/'result.json').read_text())
    stopped=json.loads((folder/'explicit_unsuccessful_physical_policy_stop.json').read_text())
    terminal=json.loads((folder/'native_terminal.json').read_text())
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    need(not result['passed'] and not stopped['passed'] and stopped['testIntentionallyStopped'] and
         stopped['observedPaidContinueLosses']>=26 and stopped['actualHumanRoundWinReads']==0 and
         result['nativeExit']==terminal['nativeExit']==stopped['nativeExit']==0xffffffff and
         terminal['identity']['ProcessId']==GAME and terminal['identity']['ParentProcessId']==PARENT and
         not stopped['endingReached'] and not stopped['postEndingJoinAccepted'],
         'Actual failed ordinary-policy outcome, never relabeled success/softlock/ending')
    need(proof['everyActualByteComparedInRAM'] and
         hashlib.sha256(ram['guest']).hexdigest().upper()==proof['sha256']==result['guestSHA256'] and
         proof['executableSHA256']==result['executableSHA256'] and
         not (folder/'stderr.log').read_text().strip() and not result['nativeCacheOverrunObserved'],
         'Whole actual current guest matched, empty error stream; finite observed no-overrun scope only')
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream: text=stream.read()
    rows=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    losses,wins,live,selected=map(rows,('LOSS','WIN','LIVE','SELECT_ID'))
    need(len(losses)>=stopped['observedPaidContinueLosses'] and all(q['slot']=='2' for q in wins) and
         all(q['human']=='18:18' and q['cpu']=='17:17' and q['stage']=='0' and q['writes']=='0' and q['assistance']=='none' for q in live) and
         all(q['roster']=='18' and q['state']=='3' for q in selected) and
         not re.search(r'MK2_MILEENA_CAMPAIGN_OVERRUN |MK2_CURRENT_CAMPAIGN_CACHE_FAILURE |MK2_NAT_CAMPAIGN_ENDING_COMPLETED |MK2_POSTENDING_COMPLETE |LUA ERROR|stack traceback|fatal error',text),
         'Complete lossless observed prefix shows real selections/combat/losses, no current ending/join or observed cache corruption')
    raw=ram['scope']['RAM_RAW']; images=ram['scope']['RAM_IMAGES']
    need(len(raw)==len(images)==len(carrier['rgbFrames'])==1 and
         carrier['rgbFrames'][0]['pixels'] is next(iter(raw.values())),
         'One original retained raw raster, one PIL rendering, preview aliases no extra raw copy')
    view=carrier['rgbFrames'][0]
    need(hashlib.sha256(view['pixels']).hexdigest().upper()==view['header']['sha256'] and
         any(q=={k:v for k,v in view['header'].items()} for q in result['actualScenes']),
         'Individually inspected original native selection raster exactly matches captured digest')
    pins=result['inputHashes']; need(all(sha(p)==h for p,h in pins.items()),'Every original compiled/executed input remains frozen')
    scope,host=original.functions(ram['scope']['native'])
    need(scope['capture'].__code__.co_code==ram['scope']['capture'].__code__.co_code,
         'Reconstructed entire executed host function bytecode, no capture invocation/replay')
    OUT.mkdir()
    with gzip.open(OUT/'original_executed_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=host,files={p:dict(sha256=h,text=Path(p).read_text())
            for p,h in pins.items() if Path(p).suffix in ('.py','.lua')}),stream)
    bound=dict(pins)
    for p in [Path(__file__),*folder.rglob('*'),OUT/'original_executed_sources.json.gz']:
        if p.is_file(): bound[str(p.resolve())]=sha(p)
    report=dict(passed=True,failedPhysicalControllerOutcomePreserved=True,gameplayAccepted=False,
        candidate=original.NAME,actualNativeGame=GAME,actualRAMParent=PARENT,port=PORT,
        actualPaidLosses=len(losses),actualCPURoundWinReads=len(wins),actualHumanRoundWinReads=0,
        actualTrueOwnedIdentityFields=len(live),latestObservedNativeFrame=int(live[-1]['frame']),
        selectedIdentity=18,nativeCPUIdentity=17,observedCacheOverruns=0,
        cacheScope='Complete received native prefix only; forced diagnostic stop is not whole-lifetime/ending acceptance',
        actualNativeRGBCallbacks=result['actualNativeRGBFrameCallbacks'],rawNativeBuffersToRelease=1,pilRenderingBuffersToRelease=1,
        nativeSelectionRasterIndividuallyViewed=view['header'],earlierFailuresUntouched=True,
        endingReached=False,postEndingJoinAccepted=False,fullPortAcceptance=False,goalStatus='active',inputHashes=bound,
        nextAction='Fresh current campaign with normal guard/leg input policy for actual CPU Kano; original remaining tower/endings/join requirements unchanged.',
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(preserved=True,actualPaidLosses=len(losses),rawBuffersToRelease=1,campaignAccepted=False)),flush=True)


def retire():
    need(not RETIRED.exists(),'Fresh exact failed-trial RAM release receipt')
    report=json.loads((OUT/'report.json').read_text())
    need(report['passed'] and report['failedPhysicalControllerOutcomePreserved'] and
         not report['gameplayAccepted'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'All actual unsuccessful outcome and executed sources preserved')
    query=f'Get-CimInstance Win32_Process -Filter "ProcessId={PARENT} OR ProcessId={GAME}" | Select-Object ProcessId | ConvertTo-Json -Compress'
    answer=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(answer.returncode==0 and not answer.stdout.strip() and not answer.stderr.strip(),'Both exact original native/RAM processes absent')
    with socket.socket() as connection:
        connection.settimeout(1); need(connection.connect_ex(('127.0.0.1',PORT))!=0,'Exact original native RAM preview server closed')
    dirs=[original.OUT,original.INIT,original.SOURCE,OUT]
    files=[p for d in dirs for p in d.rglob('*') if p.is_file()]
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),
         'No raw disk media, ROM copies, build or archive in this actual failed batch')
    RETIRED.mkdir()
    (RETIRED/'report.json').write_text(json.dumps(dict(passed=True,exactRAMParentRetired=PARENT,
        exactNativeGameRetired=GAME,exactReviewPortClosed=PORT,rawNativeBuffersReleased=1,pilRenderingBuffersReleased=1,
        failedPhysicalControllerOutcomePreserved=True,batchEvidenceLogicalBytes=sum(p.stat().st_size for p in files),
        inputHashes={str(p.resolve()):sha(p) for p in [Path(__file__),*files]},
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(retired=True,failedCampaignPreserved=True,newRawMedia=0)),flush=True)


if __name__=='__main__': retire()
