"""Native terminal CPU lock-state evidence; observations, never campaign acceptance."""
import collections,json,re,subprocess
from pathlib import Path
import run_current_clean_uppercut_ram_v4155 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v4146_sonya_guard_uppercut_ready_p2_campaign'
OUT=ROOT/'audit_v4167_cpu_busy_attack_windows'

def main():
    need(not OUT.exists(),'Fresh immutable analysis')
    meta=json.loads((FOLDER/'result.json').read_text())
    need(meta['exit_code']==0 and meta['candidate']==current.current.NAME,'Actual completed current3836 campaign')
    fields={};decisions={}
    with (FOLDER/'run.log').open() as stream:
        for line in stream:
            if line.startswith(('MK2_NAT_CAMPAIGN_GUARD_FIELD ','MK2_NAT_CAMPAIGN_GUARD_DECISION ')):
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(r['frame'])
                if '_GUARD_FIELD ' in line:fields[frame]=r
                else:decisions[frame]=r['reason']
    windows=[]
    for frame,reason in decisions.items():
        if reason!='uppercut_attempt' or not all(frame+i in fields for i in range(12)):continue
        timeline=[fields[frame+i] for i in range(12)];initial=timeline[0]
        need(initial['human_id']==initial['human_roster']=='18' and initial['human_owner']==initial['human_actor'],'Actual own identity/ownership')
        hp=[int(r['health'].split(',')[0]) for r in timeline]
        windows.append(dict(frame=frame,stage=int(initial['stage']),cpuRoster=int(initial['cpu_roster']),
          cpuAction=int(initial['cpu_action']),cpuFlags=int(initial['cpu_flags'],16),cpuBody=int(initial['cpu_body'],16),
          humanAction=int(initial['human_action']),humanFlags=int(initial['flags'],16),humanBody=int(initial['body'],16),
          ownDamageBeforeHP=hp[0]-hp[6],ownDamageThroughCommand=hp[0]-hp[-1],
          cpuFlagsDuringPreparation=[r['cpu_flags'] for r in timeline[:7]],cpuBodyDuringPreparation=[r['cpu_body'] for r in timeline[:7]]))
    need(windows,'Non-vacuous actual CPU attack windows')
    cleanClose=[]
    for frame,f in fields.items():
        if f['cpu_roster']!='5':continue
        gap=abs(int(f['h_x'])-int(f['c_x']))
        if gap<63 and int(f['h_floor'])-int(f['h_y'])<=8 and int(f['c_floor'])-int(f['c_y'])<=8 and not int(f['flags'],16)&0x1c and not int(f['body'],16)&0x0c and not int(f['cpu_flags'],16)&0x1c and not int(f['cpu_body'],16)&0x0c:
            cleanClose.append(frame)
    pins={str(p.resolve()):sha(p) for p in (Path(__file__),FOLDER/'result.json',FOLDER/'run.log',ROOT/'tools/current_sonya_cpu_ring_contract_v2017.py',ROOT/'tools/cpu_followup_contract_v545.py',ROOT/'audit_v4157_current_sonya_p2_clean_uppercut_checked/report.json')}
    return dict(passed=True,observationalOnly=True,actualCompletedUppercutWindows=len(windows),
      windowsBeginningWithCpuBusyFlag=sum(bool(w['cpuFlags']&0x10) for w in windows),
      windowsBeginningWithCpuBodyAttackLock=sum(bool(w['cpuBody']&4) for w in windows),
      windowsWithOwnDamageBeforeHP=sum(w['ownDamageBeforeHP']>0 for w in windows),
      windowsWithOwnDamageThroughCommand=sum(w['ownDamageThroughCommand']>0 for w in windows),
      actualWindows=windows,actualBothUnlockedCloseMileenaFields=len(cleanClose),firstBothUnlockedCloseMileenaFields=cleanClose[:20],
      inputHashes=pins,campaignClearAccepted=False,fullPortAcceptance=False,
      inference='Action category303 alone did not establish safe CPU stance. Native action lock flag10/body4 are independently checked in existing original setup/cleanup contracts; this report observes actual current CPU values, not the exact native setter instruction for Mileena. Require genuine CPU lock release before choosing attack; keep physical input and original difficulty. No gameplay mutation.')

if __name__=='__main__':
    report=main();OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compression before report writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('actualWindows','inputHashes')},indent=2),flush=True)
