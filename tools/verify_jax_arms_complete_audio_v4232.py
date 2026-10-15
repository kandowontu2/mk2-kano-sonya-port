"""Verify all eight immutable arm audio captures, with real priority decline.

Never rerun successful native captures or alter immutable failed reports.
Actual direct caller witnesses cover KanoP1/SonyaP2 only; the other two contexts
still need equivalent return-PC qualification. Full port remains unaccepted.
"""
import copy,json,subprocess,traceback
from pathlib import Path
import verify_jax_arms_native_audio_routes_v4231 as verify
ROOT,need,sha=verify.ROOT,verify.need,verify.sha
OUT=ROOT/'audit_v4233_jax_arms_complete_audio_checked'
CASES=[]

def direct_sources(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for first,last in((0xffa13020,0xffa130c0),(0xff8cdb70,0xff8cdda0),(0xff82cb20,0xff82cb90)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==stock[lo:hi],'Whole native clear/fatal completion/continuation packet code unchanged')
    records=[]
    for name in('audit_v4226_jax_arms_direct_packet_callers_observed','audit_v4230_sonya_p2_arm_audio_reject_observed'):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed']and r['allNativeEventsAndEntirePCMUnchangedByObserver'],'Actual return-PC observer proven non-invasive')
        expected=[('FFA13070',0),('FF8CDC10',0x34),('FF8CDD90',0x35),('FF82CB70',0x38)]
        rows=r['additionalDirectNativePackets']
        need([(x['return_pc'],int(x['a3'],16))for x in rows]==expected and rows[2]['a1']=='00000002','Actual clear0/fatal begin34/native mode2 completion35/continue38 caller and packet inventory')
        records.append(dict(context=r['actualContext'],actualDirectPackets=rows,wholeOriginalCallerCodeBound=True))
    return records

def run():
    need(not OUT.exists(),'Fresh immutable complete PCM/state proof')
    old=ROOT/'audit_v4220_jax_arms_native_audio_routes_checked/report.json'
    failed=json.loads(old.read_text());need(not failed['passed']and len(failed['completed'])==3,'Original invalid every-selector-admitted assumption preserved with3completed contexts')
    guest=verify.capture.expected();verify.source_contract(guest);direct=direct_sources(guest)
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(verify.__file__).resolve()):sha(verify.__file__),str(Path(verify.previous.__file__).resolve()):sha(verify.previous.__file__),str(Path(verify.clap.__file__).resolve()):sha(verify.clap.__file__),str(old):sha(old)}
    for name in('audit_v4226_jax_arms_direct_packet_callers_observed','audit_v4230_sonya_p2_arm_audio_reject_observed'):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());pins[str(p)]=sha(p)
        for path,h in r['inputHashes'].items():need(path not in pins or pins[path]==h,'Same frozen direct/decline witnesses');pins[path]=h
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        case=verify.qualify(fighter,side,guest);CASES.append(case)
        for enabled in(True,False):
            folder=verify.folder(fighter,side,enabled);m=json.loads((folder/'result.json').read_text())
            for p,h in m['input_hashes'].items():need(p not in pins or pins[p]==h,'Same actual executed inputs');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
        print(f'{fighter}P{side}: {len(case["nativeAudio"]["actualCommands"])} admitted selectors, {len(case["nativeAudio"]["actualNativePriorityDeclines"])} genuine native declines;26faults rejected',flush=True)
    actual=CASES[-1]['nativeAudio']['actualNativePriorityDeclines'][0];negative=[]
    for key,new in(('pc','FFF00000'),('a8','01000000'),('a1','00000015'),('a3','00000000'),('priority0','21'),('priority1','22'),('priority2','0')):
        changed=dict(actual['actualNativeDecline']);need(changed[key]!=new,'Non-vacuous real native reject fault');changed[key]=new
        try:verify.decline_gate(actual['call'],changed,guest)
        except ValueError as error:negative.append(dict(field=key,rejectedBy=str(error)))
        else:raise ValueError('Native decline counterexample accepted '+key)
        verify.decline_gate(actual['call'],actual['actualNativeDecline'],guest)
    for p,h in pins.items():need(sha(p)==h,'All native capture/proof/source logical bytes unchanged')
    return dict(passed=True,candidate=verify.capture.NAME,actualContexts=4,actualPairedCaptures=8,cases=CASES,inputHashes=pins,
      originalCompleteEarnedArmStatePaletteTableAlgorithmRetained=True,completeGenericPCMChannelsPacketsADSPAlgorithmRetained=True,actual50HzSoundDeadlineBound=True,
      actualNativeAdmittedSelectors=sum(len(c['nativeAudio']['actualCommands'])for c in CASES),actualNativePriorityDeclines=1,actualNativeDeclineFaultsRejected=negative,
      actualStateAudioPaletteFaultsRejected=sum(len(c['actualRowCounterexamplesRejected'])for c in CASES),actualNativeDCSBytesDelivered=sum(c['nativeAudio']['nativePacketBytesDelivered']for c in CASES),
      fullNativePCMExactlyUnaffectedBySamples=True,allObservedSelectorsAdmissionOrDeclineSourceBound=True,actualTrueVictimGenderAndNativePacketsAccepted=True,
      sourceBoundDirectCallerWitnesses=direct,allFourDirectPacketCallerOriginsAccepted=False,stockReferenceWholeWaveformFidelityAccepted=False,
      allVictimFinisherAudioAccepted=False,alternateCostumesAccepted=False,allArenasAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=CASES,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable complete proof');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','completed','inputHashes','sourceBoundDirectCallerWitnesses')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
