"""Actual remaining KanoP2/SonyaP1 native arm packet return-PC witnesses.

All controls, full initialized guest and PCM capture from4212 retained. Only
read-only return-PC observer4223 changes the original stream. No proxy, writes,
stock-reference relabelling, raw ROM/audio/raster copies or full-port claim.
"""
import hashlib,inspect,json,subprocess,traceback
from pathlib import Path
import run_jax_arms_native_audio_routes_v4212 as original
import run_jax_arms_direct_packet_callers_v4224 as caller
import verify_jax_arms_complete_audio_v4232 as complete
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v4236_remaining_arm_packet_callers_observed'
CASES=[]

def capture_function():
    source=inspect.getsource(caller.capture_function)
    before='audit_v4225_jax_arms_callers_';after='audit_v4235_jax_arms_callers_'
    need(source.count(before)==1,'Only fresh remaining-capture labels changed');source=source.replace(before,after)
    ns=dict(vars(caller));ns.update(__file__=__file__)
    exec(compile(source,__file__+'::complete4224_return_pc_capture','exec'),ns)
    return ns['capture_function']()

def run():
    need(not OUT.exists(),'Fresh immutable remaining caller matrix')
    caller.source_boundary();guest=original.expected();original.state.scene_state.source_contract(guest)
    existing=complete.direct_sources(guest)
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(caller.__file__).resolve()):sha(caller.__file__),str(Path(complete.__file__).resolve()):sha(complete.__file__)}
    capture,expanded=capture_function()
    for fighter,side in(('kano',2),('sonya',1)):
        folder,headers,pcm=capture(fighter,side,True,guest)
        text=(folder/'run.log').read_text();m=json.loads((folder/'result.json').read_text())
        physical=original.state.gate(text,fighter,side,guest,folder.name)
        prior=ROOT/f'audit_v4213_jax_arms_{fighter}_p{side}_audio_queue_samples'
        before=(prior/'run.log').read_text();old=json.loads((prior/'result.json').read_text())
        need(m['mixedPCMBytesVerifiedInRAM']==old['mixedPCMBytesVerifiedInRAM']and m['mixedPCMSHA256']==old['mixedPCMSHA256'],'Entire native PCM unchanged by actual return-PC observation')
        for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','CHANNEL','RESULT'):
            projected=[{k:v for k,v in r.items()if k!='return_pc'or tag=='ROUTE'}for r in original.rows(text,tag)]
            need(projected==original.rows(before,tag),'Every actual native event unchanged except added return-PC '+tag)
        physical_lines=lambda s:[l for l in s.splitlines()if l.startswith('MK2_STOCK_HEAD_V921_')]
        need(physical_lines(text)==physical_lines(before),'Entire original physical/state/health/command grammar unchanged')
        rows=[r for r in original.rows(text,'PACKET')if r['return_pc']!='FFA12B90']
        need([(r['return_pc'],int(r['a3'],16))for r in rows]==[('FFA13070',0),('FF8CDC10',0x34),('FF8CDD90',0x35),('FF82CB70',0x38)]and rows[2]['a1']=='00000002','Actual four direct original clear/fatal/mode2 completion/continuation callers and packets')
        need(len(original.rows(text,'PACKET'))==59 and len([r for r in original.rows(text,'ROUTE')if r['entry']in('FFA12530','FFA12430')])==55,'All55queued selectors and4direct native packets observed')
        for p,h in m['input_hashes'].items():need(p not in pins or pins[p]==h,'Same exact executed remaining native inputs');pins[p]=h
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        for p in(prior/'run.log',prior/'result.json'):pins[str(p)]=sha(p)
        CASES.append(dict(context=f'{fighter}P{side}',actualEarnedState=physical,actualDirectPackets=rows,allNativeEventsAndEntirePCMUnchangedByObserver=True,wholeOriginalCallerCodeBound=True))
        print(f'{fighter}P{side}: all4actual direct caller return-PCs observed, all native events/wholePCM unchanged',flush=True)
    for name in('audit_v4226_jax_arms_direct_packet_callers_observed','audit_v4230_sonya_p2_arm_audio_reject_observed'):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());pins[str(p)]=sha(p)
        for p,h in r['inputHashes'].items():need(p not in pins or pins[p]==h,'Exact earlier native caller witness');pins[p]=h
    for p,h in pins.items():need(sha(p)==h,'All source/native comparator bytes unchanged')
    return dict(passed=True,actualContexts=4,actualDirectCallerPackets=16,cases=existing+CASES,inputHashes=pins,
      expandedOriginalCaptureSHA256=expanded,actualAllFourDirectCallerOriginsObservedAndSourceBound=True,
      allNativeEventsAndEntirePCMUnchangedByObserver=True,fullNativePCMOnOffProofPending='audit_v4233_jax_arms_complete_audio_checked/report.json',
      allArenasAccepted=False,alternateCostumesAccepted=False,allFinisherAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=CASES,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable remaining caller report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','completed','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
