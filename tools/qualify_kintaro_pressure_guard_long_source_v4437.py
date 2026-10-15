"""Same physical campaign; only the host observation window is extended."""
import json,re,subprocess
from pathlib import Path
import qualify_kintaro_pressure_guard_source_v4425 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
LUA='mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua'
OUT=ROOT/'audit_v4438_kintaro_pressure_guard_long_source_preflight'
TRANSITIVE_LUA=(LUA,'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua',
                'mk2ks_mileena_campaign_trace_v3848.lua')

def source_boundary():
    base=previous.source_boundary()
    old=(ROOT/previous.LUA).read_text()
    before="assert(limit==1500,'Finite host-only observation; no victory supplied')"
    after="assert(limit==5900,'Finite host-only observation; no victory supplied')"
    need(old.count(before)==1,'One explicit host deadline, no native game-clock change')
    need((ROOT/LUA).read_text()==old.replace(before,after,1),
         'Entire executed physical policy, native observers and six RAM sinks unchanged')
    # Both read-only runtime dependencies must be explicitly bound by the host.
    need(set(re.findall(r"(?:dofile|loadfile)\('([^']+)'",(ROOT/LUA).read_text()))==
         {'mk2ks_mileena_campaign_trace_v3848.lua'},'Exact read-only observer dependency')
    need("local path='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'" in old,
         'Exact original campaign controller dependency')
    for name in TRANSITIVE_LUA[1:]:
        text=(ROOT/name).read_text()
        need(not re.search(r'dofile\(|loadfile\(',text),
             'No omitted transitive Lua runtime source')
    original=(ROOT/'tools/run_kintaro_pressure_guard_campaign_v4427.py').read_text()
    changes=[('import qualify_kintaro_pressure_guard_source_v4425 as source',
              'import qualify_kintaro_pressure_guard_long_source_v4437 as source'),
             (previous.LUA,LUA),
             ('audit_v4429_kintaro_pressure_guard_campaign_observed',
              'audit_v4441_kintaro_pressure_guard_long_campaign_observed'),
             ('audit_v4426_kintaro_pressure_guard_source_preflight',OUT.name),
             ('audit_v4428_{fighter}_kintaro_pressure_guard_p2_campaign',
              'audit_v4440_{fighter}_kintaro_pressure_guard_long_p2_campaign'),
             ("MK2KS_CAMPAIGN_OBSERVER_LIMIT='1500'","MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'"),
             ("'-str','1600'","'-str','6000'"),
             ('seconds=1600,observer_limit_seconds=1500',
              'seconds=6000,observer_limit_seconds=5900'),
             ("    if fighter=='kano':files.add(ROOT/knife.policy.OBSERVER)\n",
              "    if fighter=='kano':files.add(ROOT/knife.policy.OBSERVER)\n"
              '    # Explicitly freeze every Lua source reached by this wrapper, including\n'
              '    # the loaded campaign controller and read-only Mileena observer.\n'
              '    files.update(ROOT/p for p in source.TRANSITIVE_LUA)\n')]
    for before,after in changes:
        need(original.count(before)==1,'Unique host-only collector adaptation')
        original=original.replace(before,after,1)
    need((ROOT/'tools/run_kintaro_pressure_guard_long_campaign_v4439.py').read_text()==original,
         'Whole original collector unchanged except host limit, fresh paths and explicit pins')
    return dict(passed=True,wrapperSHA256=sha(ROOT/LUA),
        expandedControllerSHA256=base['expandedControllerSHA256'],
        physicalInputsExactlyUnchanged=True,nativeStateUnchanged=True,
        allSixRAMFramesAndWholeGuestSinkRetained=True,hostDeadlineSeconds=5900,
        transitiveLuaSources=list(TRANSITIVE_LUA),fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh preflight before first boot')
    r=source_boundary()
    paths=[Path(__file__).resolve(),Path(previous.__file__).resolve(),ROOT/previous.LUA,
           ROOT/'tools/run_kintaro_pressure_guard_campaign_v4427.py',
           ROOT/'tools/run_kintaro_pressure_guard_long_campaign_v4439.py',
           ROOT/'audit_v4431_kintaro_pressure_guard_whole_campaign_checked/report.json']
    paths.extend(ROOT/p for p in TRANSITIVE_LUA)
    proof=json.loads(paths[5].read_text())
    need(proof['passed'] and proof['case']['passed'] and
         proof['case']['actualWholeCampaignGrammarRetained'],
         'Original bounded campaign fully qualified before extending observation')
    r['inputHashes']={str(p.resolve()):sha(p) for p in paths}
    OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
         'Compress before writes')
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='inputHashes'},indent=2),flush=True)
