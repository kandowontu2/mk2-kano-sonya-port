"""Actual frozen live-prefix command windows, not an inferred move activation.

Clean P2 native uppercut proof distinguishes gameplay capability from guard
controller failures. This observational analysis never qualifies a campaign.
"""
import collections,hashlib,json,re,subprocess
from pathlib import Path
import run_current_clean_uppercut_ram_v4155 as clean

ROOT,need,sha=clean.ROOT,clean.need,clean.sha
FOLDER=ROOT/'audit_v4146_sonya_guard_uppercut_ready_p2_campaign'
OUT=ROOT/'audit_v4159_guard_uppercut_actual_windows'

def main():
    need(not OUT.exists(),'Fresh immutable analysis')
    proof=json.loads((ROOT/'audit_v4157_current_sonya_p2_clean_uppercut_checked/report.json').read_text())
    need(proof['passed'] and proof['positive']['nativeContactDamage']==40 and not proof['fullPortAcceptance'],'Actual positive P2 gameplay proof')
    pins=dict(proof['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'Clean positive immutable witness')
    for p in (Path(__file__).resolve(),ROOT/'audit_v4157_current_sonya_p2_clean_uppercut_checked/report.json',ROOT/'mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua',ROOT/'tools/run_sonya_guard_uppercut_ready_campaign_v4145.py',FOLDER/'guest_memory_proof.json',FOLDER/'input_hashes_before.json'):
        pins[str(p.resolve())]=sha(p)
    length=(FOLDER/'run.log').stat().st_size
    with (FOLDER/'run.log').open('rb') as stream:raw=stream.read(length)
    need(len(raw)==length,'Frozen exact native prefix')
    end=raw.rfind(b'\n')+1;raw=raw[:end]
    fields={};decisions={};inputs=collections.defaultdict(list);actions=[]
    for line in raw.decode('utf-8').splitlines():
        if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
        r=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(r.get('frame','-1'))
        if line.startswith('MK2_NAT_CAMPAIGN_GUARD_FIELD '):fields[frame]=r
        elif line.startswith('MK2_NAT_CAMPAIGN_GUARD_DECISION '):decisions[frame]=r['reason']
        elif line.startswith('MK2_NAT_CAMPAIGN_INPUT '):inputs[frame].append(r)
        elif line.startswith('MK2_NAT_CAMPAIGN_GUARD_ACTION '):actions.append(r)
    attempts=[f for f,r in decisions.items() if r=='uppercut_attempt' and all(f+age in fields and f+age in decisions for age in range(12))]
    windows=[]
    for frame in attempts:
        timeline=[fields[frame+age] for age in range(12)]
        hp=[list(map(int,r['health'].split(','))) for r in timeline]
        windowActions=[r for r in actions if frame<=int(r['frame'])<frame+12]
        windows.append(dict(frame=frame,cpuRoster=int(timeline[0]['cpu_roster']),gap=abs(int(timeline[0]['h_x'])-int(timeline[0]['c_x'])),
          ownActions=[int(r['human_action']) for r in timeline],cpuActions=[int(r['cpu_action']) for r in timeline],
          ownFlags=[r['flags'] for r in timeline],ownBody=[r['body'] for r in timeline],health=hp,
          ownDamageDuringPreparation=hp[0][0]-hp[6][0],ownDamageDuringWholeCommand=hp[0][0]-hp[-1][0],
          actualOwnedActionStores=windowActions,actualLoggedInputs=[dict(age=age,records=inputs[frame+age]) for age in range(12)]))
    actual107=[r for r in actions if int(r['after'])==0x107]
    need(windows and not actual107,'Observed attempts without actual HUMAN107 stores; no invented activation')
    injuries=sum(w['ownDamageDuringWholeCommand']>0 for w in windows)
    native=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(native['sha256']==hashlib.sha256(clean.current.expected()).hexdigest().upper() and native['everyActualByteComparedInRAM'],'Same actual whole3836 guest as clean gameplay capability test')
    return dict(passed=True,observationalOnly=True,actualNativeLogPrefixBytes=end,actualNativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
      actualCompletedUppercutAttemptWindows=len(windows),actualHuman107Stores=len(actual107),windowsWithActualOwnDamage=injuries,
      actualWindows=windows,inputHashes=pins,cleanP2UppercutAccepted=True,campaignClearAccepted=False,fullPortAcceptance=False,
      interpretation='Native clean P2 uppercut works. Actual CPU windows show whether physical preparation survives; plans are not activation. CPU507 remains unclassified; CPU303 is not proof of ducking. Own110 is native LegGrab. No game, AI, health, position, RNG or input assignment changes.',scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before report writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('actualWindows','inputHashes')},indent=2),flush=True)
