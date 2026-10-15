"""Actual rare unpressed mirror drop: complete original native contract/faults.

Earned full-health KOs, paid arena advance, true IDs, native input/parser/gates,
801 cleanup fields and original source/PC/IO/RNG/task/269 motion callbacks are
required together. Does not accept phase art, shadows, waveform or full port.
"""
import argparse,copy,ctypes,hashlib,json,re,subprocess
from pathlib import Path
import find_tomb_mirror_native_random_drop_v4455 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4459_tomb_mirror_random_drop_checked'

def change(log,prefix,frame,key,value):
    lines=log.splitlines();pattern=rf'\b{key}=[^\s]+'
    hits=[i for i,s in enumerate(lines) if s.startswith(prefix+f' frame={frame} ') and re.search(pattern,s)]
    need(len(hits)==1,'Exactly one actual motion callback field')
    i=hits[0];old=lines[i];lines[i]=re.sub(pattern,key+'='+str(value),old,count=1)
    need(lines[i]!=old,'Non-vacuous actual callback corruption')
    return '\n'.join(lines)+'\n'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('search',type=Path);parser.add_argument('--delay',type=int)
    args=parser.parse_args();report_path=args.search.resolve()
    need(report_path.is_relative_to(capture.OUT) and report_path.is_file(),'Actual terminal immutable search report')
    prior=json.loads(report_path.read_text())
    need(prior['passed'] and prior['allStartedRunsActuallyTerminal'] and prior['nativeDropsFound'],
         'A genuinely observed unpressed native drop, never a held result or an input plan')
    selected=next((r for r in prior['nativeDropsFound'] if args.delay is None or r['physicalDelay']==args.delay),None)
    need(selected is not None,'Actual selected native drop exists')
    fighter,side,delay=selected['fighter'],selected['side'],selected['physicalDelay']
    output=OUT/f'{fighter}_p{side}_delay{delay:02d}';need(not output.exists(),'Fresh immutable actual drop proof')
    folder=Path(selected['capture']).resolve();need(folder.is_relative_to(capture.OUT),'Exact search capture target')
    meta=json.loads((folder/'result.json').read_text());frozen=json.loads((folder/'source_snapshot_paths.json').read_text())
    need(meta['exit_code']==0 and meta['candidate']==capture.NAME and meta['fighter']==fighter and meta['side']==side and
         meta['physicalCommandDelay']==delay and meta['assistance']=='none' and meta['guest_writes']==0 and
         not meta['cheats_enabled'] and meta['rawRasterAudioROMBuildCopiesWritten']==0,
         'Actual terminal normal3836 capture and complete source bindings')
    pins={}
    def pin(p,wanted=None):
        key=str(Path(p).resolve());h=sha(p)
        need(wanted is None or h==wanted,'Exact actually executed input byte unchanged')
        need(key not in pins or pins[key]==h,'Consistent shared original bytes');pins[key]=h
    for p,h in meta['input_hashes'].items():
        pin(p,h)
        if Path(p).suffix in ('.lua','.py','.ps1','.json'):
            dest=Path(frozen[p]).resolve();need(dest.is_relative_to(folder),'Frozen source stays in actual leaf');pin(dest,h)
    guest=capture.native.runtime.old.expected();log=(folder/'run.log').read_text()
    need(meta['guestSHA256']==hashlib.sha256(guest).hexdigest().upper() and
         [s for s in log.splitlines() if s.startswith('MK2_TOMB_TIMING_GUEST_DIGEST ')]==
         ['MK2_TOMB_TIMING_GUEST_DIGEST frame=1 bytes=1048576 sha256='+meta['guestSHA256']],
         'Actual entire guest RAM byte comparison, exact one first-frame digest')
    positive=capture.native.branch(log,guest,fighter,side)
    need(positive==selected['nativeBranch'] and positive['nativeDrop'] and
         0<=positive['actualNativeRandomValue']<50,'Exactly the actual original unpressed rare branch')
    earned=capture.native.runtime.state.actual_faults(log,fighter,side,guest)
    branch_faults=capture.native.faults(log,guest,fighter,side)
    phase=positive['nativeMotion']['phase'];begin=phase['branchFrame']
    rows={int(r['frame']):r for r in capture.native.runtime.state.native.records(log,'FIELD')}
    phase_faults=[]
    for label,age,key in (('ceiling hold',2,'y'),('slow descent',130,'vy'),
                          ('fall gravity',242,'gravity'),('native floor landing',269,'y')):
        frame=begin+age;base=16 if key in ('vy','gravity') else 10
        value=int(rows[frame][key],base)+1;value=f'{value:08X}' if base==16 else str(value)
        bad=change(log,'MK2_STAGE_PROVENANCE_FIELD',frame,key,value)
        try:capture.native.branch(bad,guest,fighter,side)
        except ValueError as error:phase_faults.append(dict(label=label,frame=frame,key=key,rejectedBy=str(error)))
        else:raise ValueError('Altered actual native drop callback accepted')
        need(capture.native.branch(log,guest,fighter,side)==positive,'Exact full positive restored after every callback fault')
    for p in folder.rglob('*'):
        if p.is_file():pin(p)
    for p in (report_path,Path(__file__).resolve(),Path(capture.__file__).resolve()):pin(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual native source/evidence unchanged')
    report=dict(passed=True,fighter=fighter,side=side,physicalCommandDelay=delay,capture=str(folder),
       nativeBranch=positive,actualOriginalFullEarnedFaultsRejected=earned,
       actualOriginalBranchPCActorMainIOFaultsRejected=branch_faults,actual269PhaseFaultsRejected=phase_faults,
       nativeRNGInputsHealthIdentityPositionsNotWritten=True,
       nativeRandomDropStateAndOriginal801CleanupAccepted=True,
       fullMoveArtFloorShadowsAudioAndAllMirrorContextsAccepted=False,fullPortAcceptance=False,
       scope=__doc__,inputHashes=pins)
    output.mkdir(parents=True)
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(output)],capture_output=True).returncode==0,
         'Proof compressed before writes')
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualOriginalFullEarnedFaultsRejected')},indent=2),flush=True)

if __name__=='__main__':main()
