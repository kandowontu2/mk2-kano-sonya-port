"""Unchanged accepted Kano physical policy, current guest/raster sinks RAM-only."""
import hashlib,json,re,subprocess
from pathlib import Path
import verify_sonya_zoning700_campaign_v4015 as original
import verify_current_campaign_shao_knife_observer_v3526 as knife
ROOT,need,sha=original.ROOT,original.need,original.sha
LUA='mk2ks_kano_current_p2_campaign_ram_v4472.lua'
OUT=ROOT/'audit_v4474_kano_current_p2_campaign_source_preflight'
TRANSITIVE_LUA=(LUA,knife.DRIVER,knife.policy.OBSERVER,'mk2ks_mileena_campaign_trace_v3848.lua')

def source_boundary():
    original.transport_boundary()
    source=(ROOT/'mk2ks_guarded_campaign_guest_ram_v4006.lua').read_text()
    changes=[("assert(fighter=='sonya','Actual unfinished Sonya player-two campaign only')",
              "assert(fighter=='kano','Actual unfinished current Kano player-two campaign only')\nassert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"),
             ("local path='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'",f"local path='{knife.DRIVER}'")]
    for before,after in changes:
        need(source.count(before)==1,'Only declared fighter routing and physical-slot precondition')
        source=source.replace(before,after,1)
    source+=original.DEADLINE+"dofile('mk2ks_mileena_campaign_trace_v3848.lua')\n"
    need((ROOT/LUA).read_text()==source,'Entire existing RAM wrapper, only actual Kano routing/host deadline/read-only observer')
    driver=knife.source_boundary()
    historical=json.loads((ROOT/'audit_v3748_guarded_p2_campaign_state_checked/report.json').read_text())
    case=next(r for r in historical['cases'] if r['player']=='kano')
    need(historical['passed'] and case['passed'] and case['unassisted_clear_proven'],
         'Actually completed original Kano P2 controller, not a Sonya/proxy control policy')
    for name in (knife.DRIVER,knife.BASELINE,knife.policy.OBSERVER,knife.RUNNER):
        p=ROOT/name;need(sha(p)==case['inputHashes'][str(p)],'Exact physically qualified Kano policy bytes')
    guest_sink="local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
    need(driver.count(guest_sink)==1 and driver.count('screen:snapshot(')==6,'Every original host media sink accounted for')
    expanded=driver.replace(guest_sink,'_campaign_guest(raw)',1).replace('screen:snapshot(','_campaign_emit(')
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|return\s+data',expanded),
         'Original controls/read observers only; no guest/AI/health/ID/RNG writes')
    need(set(re.findall(r"dofile\('([^']+)'",expanded))=={knife.policy.OBSERVER},'Exact original frozen read-only Knife observer')
    for name in TRANSITIVE_LUA[2:]:
        text=(ROOT/name).read_text()
        need(not re.search(r'dofile\(|loadfile\(|:write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value',text),
             'No omitted transitive observer or game/controller writes')
    return dict(passed=True,wrapperSHA256=sha(ROOT/LUA),
                expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper(),
                physicalInputsExactlyUnchanged=True,trueIdentity=17,physicalSlot=2,
                allSixRAMFramesAndWholeGuestSinkRetained=True,hostDeadlineSeconds=5900,
                transitiveLuaSources=list(TRANSITIVE_LUA),naturalCurrentTowerClearAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable source preflight before first boot')
    report=source_boundary()
    paths=[Path(__file__).resolve(),Path(original.__file__).resolve(),Path(knife.__file__).resolve(),
           ROOT/'mk2ks_guarded_campaign_guest_ram_v4006.lua',ROOT/'mk2ks_guarded_campaign_ram_v3743.lua',
           ROOT/'audit_v3748_guarded_p2_campaign_state_checked/report.json',
           ROOT/'tools/run_kano_current_p2_campaign_ram_v4475.py']+[ROOT/p for p in TRANSITIVE_LUA]
    report['inputHashes']={str(p.resolve()):sha(p) for p in paths}
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Source proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
