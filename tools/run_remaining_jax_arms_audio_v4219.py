"""Preserve terminal4212 failed deadline assumption; qualify real captured data.

Do not rerun its completed KanoP1 pair. Remaining fresh contexts use the exact
same frozen4212 capture function, original controller and4210 read-only taps.
"""
import json,subprocess,traceback
from pathlib import Path
import run_jax_arms_native_audio_routes_v4212 as capture
import verify_jax_arms_native_audio_routes_v4218 as verify
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4220_jax_arms_native_audio_routes_checked'
CASES=[]

def run():
    need(not OUT.exists(),'Fresh immutable full paired proof')
    failed=ROOT/'audit_v4214_jax_arms_native_audio_routes_observed/report.json'
    prior=json.loads(failed.read_text());need(not prior['passed']and 'through749 sound fields'in prior['error'],'Original false video/audio tick assumption preserved')
    first_gate=ROOT/'audit_v4217_jax_arms_native_audio_routes_checked/report.json'
    need(not json.loads(first_gate.read_text())['passed'],'Original too-wide selector-to-packet time window failure preserved')
    guest=capture.expected();verify.source_contract(guest)
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(verify.__file__).resolve()):sha(verify.__file__),str(Path(verify.previous.__file__).resolve()):sha(verify.previous.__file__),str(Path(verify.clap.__file__).resolve()):sha(verify.clap.__file__),str(failed):sha(failed)}
    pins[str(first_gate)]=sha(first_gate)
    for fighter,side in (('kano',1),('kano',2),('sonya',1),('sonya',2)):
        if (fighter,side)!=('kano',1):
            for enabled in (True,False):capture.capture(fighter,side,enabled,guest)
        case=verify.qualify(fighter,side,guest);CASES.append(case)
        for enabled in (True,False):
            folder=verify.folder(fighter,side,enabled);meta=json.loads((folder/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Same exact executed matrix input');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
        print(f'{fighter}P{side}: full earned147-field state;55 independently decoded native selectors; {len(case["actualRowCounterexamplesRejected"])} actual faults rejected',flush=True)
    for p,h in pins.items():need(sha(p)==h,'All sources/native inputs/capture metadata unchanged')
    return dict(passed=True,candidate=capture.NAME,actualContexts=4,actualPairedCaptures=8,cases=CASES,inputHashes=pins,
      actualRowCounterexamplesRejected=sum(len(c['actualRowCounterexamplesRejected'])for c in CASES),actualNativeSelectorCommands=sum(len(c['nativeAudio']['actualCommands'])for c in CASES),actualNativeDCSBytesDelivered=sum(c['nativeAudio']['nativePacketBytesDelivered']for c in CASES),
      actual50HzNativeSoundDeadlineBound=True,originalCompleteEarnedArmStateAndPaletteAlgorithmRetained=True,completeGenericNativePCMPacketADSPAlgorithmRetained=True,
      fullNativePCMExactlyUnaffectedBySamples=True,actualNativeArmVoiceGenderAndPacketAccepted=True,allObservedSelectorCommandsSourceBound=True,
      additionalDirectPacketCallerOriginsAccepted=False,
      stockReferenceWholeWaveformFidelityAccepted=False,allVictimFinisherAudioAccepted=False,allArenasAccepted=False,alternateCostumesAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=CASES,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable full proof');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','completed','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
