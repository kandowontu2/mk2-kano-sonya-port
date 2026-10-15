"""Actual native CPU throw setter/capture windows versus physical controller state."""
import collections,json,subprocess
from pathlib import Path
import verify_mileena_ring_spacing_prefix_v4269 as physical
ROOT,need,sha=physical.ROOT,physical.need,physical.sha
FOLDER=physical.FOLDER
OUT=ROOT/'audit_v4272_mileena_ring_spacing_throw_windows_observed'

def main():
    need(not OUT.exists(),'Fresh immutable actual window observation')
    meta=json.loads((FOLDER/'result.json').read_text())
    need(meta['exit_code']==0 and meta['assistance']=='none' and not meta['cheats_enabled'],
         'Actual completed unassisted capture')
    text=(FOLDER/'run.log').read_text();replay=physical.replay(text);rows=physical.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='RANGE_FIELD'}
    decisions={r['frame']:r for r in rows if r['tag']=='RANGE_DECISION'}
    captures=[r for r in rows if r['tag']=='RANGE_ACTION' and r['pc']=='FF8428A0']
    throws=[r for r in rows if r['tag']=='RANGE_CPU_ACTION' and int(r['after'])==0x507]
    windows=[]
    for r in throws:
        frame=r['frame'];f=fields.get(frame);d=decisions.get(frame)
        paired=[c for c in captures if c['frame']==frame and f and c['actor']==f['human_actor'] and c['main']==f['human_main']]
        need(r['pc']=='FF8B6FA0' and int(r['a0'],16)&0xffff==0x507,'Actual original native CPU throw writer')
        if f:
            need(r['actor']==f['cpu_actor'] and r['main']==f['cpu_main'] and len(paired)==1,
                 'Actual same-field CPU throw writer and original victim capture pair')
        after=[fields[n] for n in range(frame+1,frame+13) if n in fields and f and
               fields[n]['human_actor']==f['human_actor'] and fields[n]['cpu_actor']==f['cpu_actor']]
        windows.append(dict(actualNativeCpuThrowStore=r,actualNativeVictimCapture=paired,
          actualField=f,actualPhysicalDecision=d,physicalRingAge=(frame-int(d['ring_start'])) if d and int(d['ring_start'])>=0 else None,
          physicalJumpAge=(frame-int(d['jump_start'])) if d else None,actualFollowingFields=after))
    need(windows,'Non-vacuous original native throw activations')
    counts=collections.Counter(w['actualPhysicalDecision']['reason'] if w['actualPhysicalDecision'] else 'outside_observed_field' for w in windows)
    need(sum(counts.values())==replay['actualNativeCpuGroundThrowStores'],'Every actual native CPU throw inventoried')
    pinpaths=(Path(__file__),Path(physical.__file__),FOLDER/'run.log',FOLDER/'result.json',FOLDER/'guest_memory_proof.json')
    pins=dict(meta['input_hashes']);pins.update({str(p.resolve()):sha(p) for p in pinpaths})
    need(all(sha(p)==h for p,h in pins.items()),'All executed and observational bytes unchanged')
    return dict(passed=True,observationalOnly=True,actualReplay=replay,actualOriginalCpuThrowStores=len(throws),
      actualSameFieldOwnedVictimCapturePairs=sum(bool(w['actualNativeVictimCapture']) for w in windows),
      physicalDecisionCategoriesAtActualCpuThrow=dict(counts),
      actualNativeThrowWindows=windows,inputHashes=pins,
      everyObserved507FieldProvenAsActualEntry=False,controllerAttemptsNeverAssumedActivation=True,
      naturalTowerClearAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress report before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualNativeThrowWindows')},indent=2),flush=True)
