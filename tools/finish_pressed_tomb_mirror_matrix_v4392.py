"""Finish actual4role native pressed-drop matrix; preserve both failed attempts.

Reuse successfully qualified P1 PCM pairs; never replay their frozen captures.
P2 slots use the source/writer-qualified arrival instead of a fixed P1 offset.
All original complete native earned/input/audio/mix/cleanup gates remain intact.
"""
import hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import run_pressed_tomb_mirror_audio_ram_v4395 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v4393_both_characters_both_slots_pressed_mirror_drop_checked'
COMPLETED=[]

def actual_branch_faults(text,fighter,side,guest):
    def change(prefix,key,value):
        lines=text.splitlines();i=next(i for i,s in enumerate(lines)if s.startswith(prefix)and key+'='in s)
        lines[i]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,lines[i],count=1)
        return '\n'.join(lines)+'\n'
    variants={
      'branchPC':change('MK2_STAGE_PROVENANCE_BRANCH ','pc','00000000'),
      'branchIO':change('MK2_STAGE_PROVENANCE_BRANCH ','io0','FFFFFFFF'),
      'branchActor':change('MK2_STAGE_PROVENANCE_BRANCH ','a8','00000000'),
      'branchMain':change('MK2_STAGE_PROVENANCE_BRANCH ','a13','00000000'),
    }
    lines=text.splitlines();i=next(i for i,s in enumerate(lines)if s.startswith('MK2_STAGE_INPUT ')and
      'button=Down'in s and int(re.search(r'frame=(\d+)',s).group(1))==int(runtime.state.native.legacy.rows(text,'FIELD')[0]['frame'])+32)
    variants['missingActualDownField']='\n'.join(lines[:i]+lines[i+1:])+'\n'
    ceiling=next(i for i,s in enumerate(lines)if s.startswith('MK2_STAGE_PROVENANCE_MOTION ')and 'pc=FF83CD20'in s)
    for key,value in (('pc','00000000'),('value','00000000'),('mask','00000000'),('a8','00000000'),('a13','00000000')):
        altered=list(lines);altered[ceiling]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,altered[ceiling],count=1)
        variants['ceilingWriter:'+key]='\n'.join(altered)+'\n'
    rejected={}
    for key,altered in variants.items():
        try:runtime.state.check_log(altered,fighter,side,1,guest=guest)
        except Exception as error:rejected[key]=str(error)
        else:raise ValueError('Actual source/input/ceiling writer fault accepted: '+key)
    need(len(rejected)==10 and runtime.state.check_log(text,fighter,side,1,guest=guest)['passed'],'All actual10branch/writer/input faults rejected; original restored')
    return rejected

def main():
    need(not OUT.exists(),'Fresh immutable fully qualified native pressed mirror matrix')
    partialpath=ROOT/'audit_v4386_both_characters_both_slots_pressed_tomb_mirror_audio/report.json'
    partial=json.loads(partialpath.read_text());need(not partial['passed']and
      'Complete actual original direct-drop dispatch/phase chronology'in partial['error'],'Original failed fixed-arrival P2 qualification retained')
    need({(c['fighter'],c['side'])for c in partial['completed']}=={('kano',1),('sonya',1)},'Only two actually completed P1 PCM comparisons reused')
    p2path=ROOT/'audit_v4397_pressed_kano_p2_native_role_audio_checked/report.json'
    p2=json.loads(p2path.read_text());need(p2['passed']and (p2['case']['fighter'],p2['case']['side'])==('kano',2),'Actual fresh completed native KanoP2 PCM/phase/source checks')
    capture,proof=runtime.preflight();guest=runtime.runtime.old.expected()
    COMPLETED.extend(partial['completed']);COMPLETED.append(p2['case'])
    pins=dict(p2['inputHashes']);pins[str(p2path)]=sha(p2path);pins[str(partialpath)]=sha(partialpath)
    pins[str(Path(__file__).resolve())]=sha(__file__);pins[str(Path(runtime.__file__))]=sha(runtime.__file__)
    case=runtime.pair('sonya',2,guest,capture)
    need(case['lateOwnedMirrorVictimScreams']==1,'Actual native SonyaP2 female late victim scream')
    COMPLETED.append(case)
    for c in COMPLETED:
        native=[]
        for name in(c['capture'],c['baseline']):
            leaf=ROOT/name;meta=json.loads((leaf/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'All consistent actual original/fresh inputs');pins[p]=h
            for p in leaf.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
            text=(leaf/'run.log').read_text()
            native.append(runtime.state.qualify_pressed_drop(text,c['fighter'],c['side'],1,'positive',guest))
            need(runtime.state.check_log(text,c['fighter'],c['side'],1,guest=guest)['passed'],'Both actual full1731/native drop/cleanup contracts independently qualified')
        need(native[0]==native[1],'Actual source-qualified pressed branch/task/phase identical samples on/off')
        text=(ROOT/c['capture']/'run.log').read_text();c['nativePressedBranch']=native[0]
        c['actualNativePhaseFaultsRejected']=runtime.state.pressed_phase_faults(text,c['fighter'],c['side'],guest)
        c['actualSourceWriterInputFaultsRejected']=actual_branch_faults(text,c['fighter'],c['side'],guest)
        c['actualFaultsRejected']=runtime.state.actual_faults(text,c['fighter'],c['side'],guest)
        scream=next(r for r in runtime.runtime.old.rows(text,'ROUTE') if r['entry']=='FFA11FD0')
        c['nativeRoleVoice']=runtime.voice.qualify_scream(text,c['fighter'],c['side'],guest,scream)
        c['actualVoiceFaultsRejected']=runtime.voice.faults(text,c['fighter'],c['side'],guest)
        print(json.dumps(dict(qualified=c['fighter'],side=c['side'],arrivalOffset=native[0]['actualNativeCeilingArrivalOffset'],
          nativeLandingField=native[0]['phase']['nativeLandingField'],fullPortAcceptance=False)),flush=True)
    need({(c['fighter'],c['side'],c['victim'])for c in COMPLETED}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)},'Actual all4true mirror roles, no relabelled victim/slot')
    need(all(sha(p)==h for p,h in pins.items()),'All original/new source and native evidence bytes unchanged')
    return dict(passed=True,candidate=runtime.runtime.old.NAME,cases=COMPLETED,inputHashes=pins,sourcePreflight=proof,
      nativePressedQualifierSHA256=hashlib.sha256(inspect.getsource(runtime.state.qualify_pressed_drop).encode()).hexdigest().upper(),
      actualNativeBothDownMirrorDropContexts=4,actualPairedCaptures=8,actualWriterAndInputFaultsRejected=40,
      current3836BothCharactersBothSlotsNativePressedMirrorTombDropPhaseCleanupLateVictimRouteDCSDeliveryWinnerMixAccepted=True,
      successfullyQualifiedP1PCMContextsReusedNotRerun=True,originalFailedP2FixedArrivalReportPreserved=str(partialpath),
      originalFailedP2VoiceRangeReportPreserved=str(ROOT/'audit_v4391_pressed_kano_p2_tomb_mirror_audio_checked/report.json'),
      fullTombRasterAndFloorShadowAccepted=False,unpressedRandomMirrorDropContextsAccepted=False,
      nativeDCSStageVictimFullWaveformAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite actual native matrix outcomes');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Matrix compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
