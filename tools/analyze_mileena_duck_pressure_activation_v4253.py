"""Actual terminal physical attempts versus native activation and interruption.

Observations only: no CPU action category is assigned a safe-state meaning,
no health change is attributed to an attack without its collision provenance,
and neither ordinary move activation nor an earned round is a tower clear.
"""
import collections,json,subprocess
from pathlib import Path
import verify_mileena_duck_pressure_prefix_v4249 as physical

ROOT,need,sha=physical.ROOT,physical.need,physical.sha
FOLDER=physical.FOLDER
OUT=ROOT/'audit_v4254_mileena_duck_pressure_activation_observed'

def main():
    need(not OUT.exists(),'Fresh immutable observational report')
    meta=json.loads((FOLDER/'result.json').read_text())
    need(meta['exit_code']==0 and meta['assistance']=='none' and not meta['cheats_enabled'],
         'Actual terminal input-only capture')
    text=(FOLDER/'run.log').read_text()
    replay=physical.replay(text)
    rows=physical.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='DUCK_FIELD'}
    decisions={r['frame']:r for r in rows if r['tag']=='DUCK_DECISION'}
    stores=[r for r in rows if r['tag']=='DUCK_ACTION' and int(r['after'])==0x107]
    handlers=[r for r in rows if r['tag']=='DUCK_HANDLER']
    attempts=[]
    for frame,d in decisions.items():
        if d['reason']!='uppercut_edge' or (frame-1 in decisions and
            decisions[frame-1]['reason']=='uppercut_edge'):continue
        f=fields[frame]
        later=[fields[n] for n in range(frame,frame+31) if n in fields and
               fields[n]['human_actor']==f['human_actor'] and fields[n]['human_main']==f['human_main']]
        need(later,'Actual edge has real native field')
        last=later[-1]
        before=fields.get(frame-6)
        if before and (before['human_actor']!=f['human_actor'] or
                       before['human_main']!=f['human_main']):before=None
        attempts.append(dict(frame=frame,downStart=int(d['down_start']),
          gap=abs(int(f['h_x'])-int(f['c_x'])),
          humanAction=int(f['human_action']),humanFlags=int(f['flags'],16),humanBody=int(f['body'],16),
          cpuAction=int(f['cpu_action']),cpuFlags=int(f['cpu_flags'],16),cpuBody=int(f['cpu_body'],16),
          hpAtEdge=[int(n) for n in f['health'].split(',')],
          hpAtLastObservedField=[int(n) for n in last['health'].split(',')],
          lastObservedFrame=last['frame'],
          ownHealthLostDuringPreparation=(int(before['health'].split(',')[0])-int(f['health'].split(',')[0])) if before else None,
          nativeHuman107StoreFrames=[r['frame'] for r in stores if frame<=r['frame']<frame+30 and r['actor']==f['human_actor']],
          nativeUppercutHandlerFrames=[r['frame'] for r in handlers if frame<=r['frame']<frame+30 and r['actor']==f['human_actor']]))
    need(attempts and stores and handlers,'Non-vacuous physical edges and actual original HUMAN107/routine')
    transitions=[]
    for r in handlers:
        window=[f for n,f in fields.items() if r['frame']-3<=n<=r['frame']+15 and
                f['human_actor']==r['actor'] and f['human_main']==r['main']]
        transitions.append(dict(actualHandler=r,actualNativeFields=window,
          matchingNativeHuman107Stores=[s for s in stores if r['frame']<=s['frame']<=r['frame']+15 and
            s['actor']==r['actor'] and s['main']==r['main']]))
    pins=dict(meta['input_hashes'])
    for p in (Path(__file__),Path(physical.__file__),FOLDER/'run.log',FOLDER/'result.json',FOLDER/'guest_memory_proof.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual executed/evidence byte remains unchanged')
    return dict(passed=True,observationalOnly=True,actualReplay=replay,
      actualHPButtonRisingEdges=len(attempts),actualNativeHuman107Stores=len(stores),
      actualNativeUppercutRoutineFetches=len(handlers),
      hpEdgesWithNativeHuman107Within30Fields=sum(bool(a['nativeHuman107StoreFrames']) for a in attempts),
      hpEdgesWithHumanFlag10=sum(bool(a['humanFlags']&0x10) for a in attempts),
      hpEdgesWithHumanBody04=sum(bool(a['humanBody']&4) for a in attempts),
      hpEdgesAfterObservedPreparationInjury=sum((a['ownHealthLostDuringPreparation'] or 0)>0 for a in attempts),
      cpuActionCategoriesAtHPEdge={f'{k:04X}':v for k,v in sorted(collections.Counter(a['cpuAction'] for a in attempts).items())},
      cpu507Classification='unclassified',actualEdgeWindows=attempts,actualNativeActivationTimelines=transitions,
      inputHashes=pins,damageAttributedToUppercut=False,naturalTowerClearAccepted=False,
      fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress report before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualEdgeWindows','actualNativeActivationTimelines')},indent=2),flush=True)
