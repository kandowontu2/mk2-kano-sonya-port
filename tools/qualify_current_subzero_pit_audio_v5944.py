"""Pre-native whole controller/observer/collector/mixer qualification, no acceptance.

Only stock opponent8, Pit metadata ownership fields, fresh leaves/namespaces
change. Full original ordinary controls and native source audio algorithms
remain byte-exact otherwise; current compiled/public/user-dirty bytes guarded.
"""
import ast,hashlib,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5946_current_subzero_pit_audio_source_checked'

def once(s,a,b):need(s.count(a)==1,'One explicit complete source substitution '+a);return s.replace(a,b,1)
def literals(wrapper):
 pairs=[]
 for statement in re.findall(r'replace\((.*?)\)\n',wrapper,re.S):
  strings=re.findall(r'([\'"])(.*?)\1',statement,re.S)
  if len(strings)==2:pairs.append(tuple(value for quote,value in strings))
 return pairs

def run():
 import run_current_subzero_pit_audio_v5945 as host
 current.expected();parentpath=ROOT/'audit_v5938_current_pit_stock_shadow_progress/progress.json'
 parent=json.loads(parentpath.read_text());need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Prior whole finite Pit scenes and original five goal groups remain intact')
 proofpath=host.original.source.OUT/'report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Entire prior cold RAM observer/state/mixer qualification unchanged')
 observer=(ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua').read_text()
 pairs=literals((ROOT/host.OBSERVER).read_text())
 need(len(pairs)==6,'Exactly two original Pit origin changes plus four passive ownership-format/arguments extensions')
 for before,after in pairs:observer=once(observer,before,after)
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(',observer),
      'Whole15tap native DAC/ROM/PCM/precise14channel algorithm remains passive')
 driver=(ROOT/'mk2ks_current_cross_tomb_driver_v5833.lua').read_text()
 before="assert(source:find('local victim_id=id==17 and 18 or 17',1,true))"
 need(driver.count(before)==1 and "replace('local victim_id=id==17 and 18 or 17','local victim_id=8')"in(ROOT/'mk2ks_current_subzero_pit_driver_v5940.lua').read_text(),
      'One explicit actual selected stock8 opponent; no own performer identity or physical control change')
 before='victim = 18 if own == 17 else 17'
 expected=once(host.state.original.contract_source,before,"victim = 8\n    need(arena==6 and case=='positive','Explicit physically selected original Sub-Zero8 Pit context only')")
 need(host.state.contract_source==expected and host.state.fault_source==host.state.original.fault_source and
      host.state.actual_faults.__globals__['check_log']is host.state.check_log,'Entire original1731/3643 true own ID/physical health/input/action/801retirement contract plus all12 actual faults')
 fn,digest=host.collector();old,_=host.original.collector();expected=old.source
 for before,after in (('audit_v5897_current_cross_pit_winner_mix_','audit_v5947_current_subzero_pit_mix_'),
                      ("lua='"+host.original.LUA+"'","lua='"+host.LUA+"'"),('    files.update(ROOT/p for p in '+repr(host.original.EXTRA_INPUTS)+')',
                                               '    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')')):
  expected=once(expected,before,after)
 need(fn.source==expected and fn.__globals__['NAME']==current.NAME and fn.__globals__['state']is host.state and
      fn.__globals__['source']is host.source and fn.__globals__['model']is host.model and
      host.run.source==host.original.run.source and host.run.__globals__['runtime'].state is host.state,
      'Whole RAM-only native collector and full raw/source-fault mixer use exact intended original/current namespaces')
 pins=dict(proof['inputHashes']);pins[str(proofpath)]=sha(proofpath);pins[str(parentpath)]=sha(parentpath)
 for leaf in host.EXTRA_INPUTS+(host.LUA,host.OBSERVER):
  path=ROOT/leaf
  if path.suffix=='.py':ast.parse(path.read_text())
  pins[str(path)]=sha(path)
 pins[str(Path(__file__))]=sha(__file__)
 need(all(sha(p)==h for p,h in pins.items()),'All current/compiled/prior/new source inputs unchanged before real boot')
 return dict(passed=True,sourceOnly=True,parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],inputHashes=pins,
  transportSourceSHA256=digest,executedFullAudioObserverSHA256=hashlib.sha256(observer.encode()).hexdigest().upper(),
  wholeOwnPerformerStockOpponentStateSHA256=host.state.CONTRACT_SHA256,wholeActual12StateFaultSHA256=host.state.FAULT_SHA256,
  actualOriginalVictimID=8,addedCharacterProxy=False,actualNativeAudioAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable stock-victim audio source preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','remaining')},indent=2),flush=True)
