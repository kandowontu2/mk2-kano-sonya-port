"""Exact terminal native campaign, live unchanged whole qualifier, full goal retained."""
import json,subprocess
from pathlib import Path
import run_current_clean_uppercut_ram_v4155 as clean

ROOT,need,sha=clean.ROOT,clean.need,clean.sha
PARENT=ROOT/'audit_v4163_uppercut_diagnosis_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4165_ready_campaign_terminal_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'All inherited evidence unchanged')
    def pin(p):p=Path(p).resolve();pins[str(p)]=sha(p)
    pin(PARENT);pin(__file__)
    folder=ROOT/'audit_v4146_sonya_guard_uppercut_ready_p2_campaign'
    meta=json.loads((folder/'result.json').read_text())
    observed=ROOT/'audit_v4147_sonya_guard_uppercut_ready_campaign_observed/report.json'
    report=json.loads(observed.read_text())
    need(meta['exit_code']==0 and meta['actualNativeFrameCallbacks']==423 and report['passed'] and report['observations'][0]['terminal0'] and not report['independentCampaignAcceptance'] and not report['fullPortAcceptance'],'Actual native terminal observation only')
    need(report['observations'][0]['endingStarts']==report['observations'][0]['endingCompletions']==0,'Own ending still not reached')
    for p in folder.rglob('*'):
        if p.is_file():pin(p)
    pin(observed)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=102752 OR ProcessId=51464 OR ProcessId=135860" | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Actual live whole qualifier process')
    processes=json.loads(q.stdout)
    if isinstance(processes,dict):processes=[processes]
    need(len(processes)==1 and processes[0]['ProcessId']==102752 and processes[0]['Name']=='python.exe' and 'verify_guard_uppercut_ready_whole_campaign_v4160.py' in processes[0]['CommandLine'],'Native/collector terminal, exact full qualifier live now')
    need(not (ROOT/'audit_v4161_guard_uppercut_ready_whole_campaign_checked/report.json').exists(),'Whole qualification still pending, not implicitly passed')
    pending=state['pendingSonyaP2GuardCampaign']
    pending.update(status='native and collector terminal0; exec23118 consumed; whole original grammar qualifier running confirmed by CIM',nativePIDMissing=True,collectorPIDMissing=True,
      campaignTerminalExitCode=0,actualNativeFrameCallbacks=423,observationReport=str(observed),wholeQualifierExecuted=True,
      wholeQualifierExecSession=1580,wholeQualifierPID=102752,wholeQualifierLiveProcesses=processes,fullIndependentCampaignAccepted=False)
    state.update(inputHashes=pins,previousCheckpoint=str(PARENT),inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Preserve all inherited evidence, complete original scope and exclusions.'),
      thisGoalTurnClassification=state['thisGoalTurnClassification']+' Native4146 then completed terminal0 at322771fields with102paidlosses/103selections,423actualRAMonlyframes,stages0..9/noending. Consumed exact23118; started unused4160 full original campaign/state/input/fault qualifier exec1580/PID102752 confirmed live. It remains pending, not a towerclear.',
      pendingSonyaP2GuardCampaign=pending,nextImplementationAction='Poll exact1580/PID102752 full qualifier, confirmed live. No restart on timeout. On real terminal consume handle and inspect4161; preserve any failed qualification with fresh source/leaf repair, never narrow original campaign/health/schedule/paidcontinue/ending/boss algorithm. Controller is losing CPU attack preparation: clean SonyaP2 native107 works,23actual command windows all took own damage. Diagnose real native whiff/recovery and physical input timing rather than game proxy or injected state. Keep all original remaining five groups, public1836/ZIP and installed dirty sources untouched until combined acceptance. No full tower or own ending/attract claim from102losses. Use dependency-aware cleanup, no broad rejected deletion retry or raw native dump copies.',goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Full original goal unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed checkpoint before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),wholeQualifierExecSession=1580,wholeQualifierPID=102752,pins=len(pins),goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
