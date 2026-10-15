"""Observer slot/Main key repair against actual native reuse; no gameplay delta.

This is source and predicate-model proof only. Existing captures are immutable
and retain their missing-event exclusions. A native run of the repaired Lua is
still required; modelled observer admission never creates native event evidence.
"""
import collections,json,subprocess
from pathlib import Path
import verify_mileena_ring_spacing_prefix_v4269 as physical
ROOT,need,sha=physical.ROOT,physical.need,physical.sha
OUT=ROOT/'audit_v4277_mileena_observer_slot_reuse_source_checked'
OLD=ROOT/'mk2ks_mileena_ring_spacing_campaign_ram_v4259.lua'
NEW=ROOT/'mk2ks_mileena_ring_spacing_campaign_ram_v4275.lua'

def source_check(actual):
    expected=OLD.read_text()
    replacements={
      '     if not rs_taps[observed_main] then':
      "     -- Main task memory may be reused by the opposite slot next round.\n     -- Keep an observer for each actual slot/Main pair, never a frozen role\n     -- associated only with the address. All existing native guards remain.\n     local observed_key=tostring(n)..':'..tostring(observed_main)\n     if not rs_taps[observed_key] then",
      '      rs_taps[observed_main]=p:install_write_tap':
      '      rs_taps[observed_key]=p:install_write_tap',
      '      taps[#taps+1]=rs_taps[observed_main]':
      '      taps[#taps+1]=rs_taps[observed_key]',
    }
    for a,b in replacements.items():
        need(expected.count(a)==1,'Exact unique observer-key repair');expected=expected.replace(a,b,1)
    need(actual==expected,'Whole physical inputs/native read guards/selection/boss/endings/RAM sinks unchanged; only observer slot/Main key changes')

def model(fields,include_slot):
    bindings={};counts=collections.Counter();misses=[]
    for f in fields:
        need(f['human_main']!=f['cpu_main'],'Actual native distinct Main tasks')
        for who,n in (('human',2),('cpu',1)):
            main=f[who+'_main'];key=(n,main) if include_slot else main
            bindings.setdefault(key,n)
            accepted=bindings[key]==n
            counts[who+'_admitted_predicates' if accepted else who+'_rejected_wrong_frozen_side']+=1
            if not accepted:misses.append((f['frame'],who,main,bindings[key],n))
    return dict(counts=dict(counts),actualFieldPredicateChecks=len(fields)*2,
                wrongFrozenSidePredicateChecks=len(misses),firstActualReuseCases=misses[:12])

def main():
    need(not OUT.exists(),'Fresh immutable source repair proof')
    physical.capture.source.source_boundary();source_check(NEW.read_text())
    report_path=ROOT/'audit_v4274_mileena_ring_spacing_throw_windows_observed/report.json'
    observed=json.loads(report_path.read_text())
    need(observed['passed'] and not observed['completeNativeThrowInventoryAccepted'] and
         observed['actualMissingHumanCapturePairsExplainedByMainAddressSideReuse']==7,
         'Actual retained missing native pairs established, not theoretical fixture')
    text=(physical.FOLDER/'run.log').read_text();replay=physical.replay(text)
    fields=[r for r in physical.parse(text) if r['tag']=='RANGE_FIELD']
    old,new=model(fields,False),model(fields,True)
    need(old['counts'].get('cpu_rejected_wrong_frozen_side',0)==9030 and
         old['counts'].get('human_rejected_wrong_frozen_side',0)==5027,
         'Same actual capture reproduces original frozen-side predicate gaps')
    need(new['wrongFrozenSidePredicateChecks']==0 and new['actualFieldPredicateChecks']==len(fields)*2,
         'Slot/Main key admits every actual correct-side predicate, not fabricated event execution')
    faults=[];actual=NEW.read_text()
    for label,a,b in (
      ('collapse_slot_key',"tostring(n)..':'..tostring(observed_main)","tostring(observed_main)"),
      ('key_always_human_slot',"tostring(n)..':'", "tostring(side)..':'"),
      ('lose_native_slot_guard','p:read_u32(slots[observed_side].main)~=observed_main','false'),
      ('change_physical_range','elseif gap<150 then','elseif gap<80 then')):
        need(actual.count(a)==1,'Actual non-vacuous source repair fault')
        try:source_check(actual.replace(a,b,1))
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Unexpected source delta accepted '+label)
        source_check(actual);need(model(fields,True)==new,'Exact actual predicate positive restored')
    need(model(fields,False)['wrongFrozenSidePredicateChecks']>0,'Old key is an actual failing model control')
    pins=dict(observed['inputHashes'])
    for p in (Path(__file__),OLD,NEW,Path(physical.__file__),report_path):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All original captures and repaired source unchanged')
    return dict(passed=True,actualNativeFieldReplay=replay,actualPredicateChecks=new['actualFieldPredicateChecks'],
      originalObserverPredicateModel=old,repairedObserverPredicateModel=new,actualSourceFaultsRejected=faults,
      physicalControllerAndGameUnchanged=True,nativeRepairedObserverRuntimeProven=False,
      missingOldEventsNotFabricated=True,oldCapturesRemainIncomplete=True,
      inputHashes=pins,naturalTowerClearAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress source repair proof before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualNativeFieldReplay')},indent=2),flush=True)
