"""Read-only actual return-PC trace for extra arm-rip native sound packets.

Single real KanoP1 earned context, not four-context fidelity acceptance. Whole
guest and PCM remain in RAM. Original4212 capture/3958 controls are preserved.
"""
import hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import run_jax_arms_native_audio_routes_v4212 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v4226_jax_arms_direct_packet_callers_observed'

def capture_function():
    source=inspect.getsource(original.capture)
    changes={
      'audit_v4213_jax_arms_':'audit_v4225_jax_arms_callers_',
      'mk2ks_jax_arms_audio_routes_ram_v4210.lua':'mk2ks_jax_arms_audio_callers_ram_v4223.lua',
      'Path(__file__).resolve(),ROOT/lua':'Path(__file__).resolve(),Path(original.__file__).resolve(),ROOT/\'mk2ks_jax_arms_audio_routes_ram_v4210.lua\',ROOT/lua',
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Unique original RAM capture/label/pin adaptation');source=source.replace(before,after)
    ns=dict(vars(original));ns.update(__file__=__file__,original=original)
    exec(compile(source,__file__+'::complete_original4212_capture','exec'),ns)
    return ns['capture'],hashlib.sha256(source.encode()).hexdigest().upper()

def source_boundary():
    previous=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    wrapper=(ROOT/'mk2ks_jax_arms_audio_callers_ram_v4223.lua').read_text()
    before="'entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X',\n   entry,cpu.A1.value,cpu.A3.value,cpu.A4.value,a,m))"
    after="'entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X return_pc=%08X',\n   entry,cpu.A1.value,cpu.A3.value,cpu.A4.value,a,m,p:read_u32(cpu.SP.value)))"
    need(previous.count(before)==1 and wrapper==previous.replace(before,after),'Only actual read-only queue/packet return-PC logging added, no state or control change')
    original.state.source_boundary()

def run():
    need(not OUT.exists(),'Fresh immutable direct caller observation');source_boundary()
    guest=original.expected();original.state.scene_state.source_contract(guest)
    capture,expanded_sha=capture_function();folder,headers,a=capture('kano',1,True,guest)
    text=(folder/'run.log').read_text();meta=json.loads((folder/'result.json').read_text())
    physical=original.state.gate(text,'kano',1,guest,folder.name)
    previous=ROOT/'audit_v4213_jax_arms_kano_p1_audio_queue_samples'
    prior_text=(previous/'run.log').read_text();prior_meta=json.loads((previous/'result.json').read_text())
    need(meta['mixedPCMBytesVerifiedInRAM']==prior_meta['mixedPCMBytesVerifiedInRAM']and meta['mixedPCMSHA256']==prior_meta['mixedPCMSHA256'],'Entire genuine native waveform unchanged by read-only return-PC observation')
    for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','CHANNEL','RESULT'):
        projected=[{k:v for k,v in r.items()if k!='return_pc' or tag=='ROUTE'}for r in original.rows(text,tag)]
        need(projected==original.rows(prior_text,tag),'Every native event unchanged except added return-PC field '+tag)
    need([s for s in text.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_')]==[s for s in prior_text.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_')],'Entire original earned physical input and native health/state unchanged')
    packets=original.rows(text,'PACKET');need(packets and all(re.fullmatch('[0-9A-F]{8}',p['return_pc'])for p in packets),'Every actual packet caller observed from native stack')
    selectors=[r for r in original.rows(text,'ROUTE')if r['entry']in('FFA12530','FFA12430')]
    direct=[p for p in packets if p['return_pc']!='FFA12B90']
    need(len(packets)==59 and len(selectors)==55 and len(direct)==4,'Actual55queued selectors and4additional direct packet calls')
    need(int((a!=0).sum())>0,'Non-silent real PCM, not disabled audio engine')
    pins=dict(meta['input_hashes']);pins.update({str(Path(__file__).resolve()):sha(__file__),str(previous/'run.log'):sha(previous/'run.log'),str(previous/'result.json'):sha(previous/'result.json')})
    for p in folder.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
    for p,h in pins.items():need(sha(p)==h,'All executed and comparator bytes unchanged')
    return dict(passed=True,actualContext='kanoP1',actualEarnedState=physical,allNativeEventsAndEntirePCMUnchangedByObserver=True,
      expandedOriginalCaptureSHA256=expanded_sha,nativePackets=59,queuedSelectorPackets=55,additionalDirectNativePackets=direct,
      inputHashes=pins,sourceQualifiedAdditionalDirectPacketCallerOriginsAccepted=False,allFourArmContextsAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable caller report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
