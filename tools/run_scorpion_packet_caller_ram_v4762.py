"""Full original secondary-finisher audio pairing plus actual caller stack.

No native state, physical controller, PCM scope or existing record changes.
Only read-only packet caller observations and fresh immutable leaves added.
"""
import argparse,inspect,json,subprocess,traceback
from pathlib import Path
import run_scorpion_secondary_audio_ram_v4664 as old
ROOT,need,sha,state,previous=old.ROOT,old.need,old.sha,old.state,old.previous
NAME=old.NAME
LUA='mk2ks_scorpion_secondary_packet_caller_ram_v4761.lua'
PREFLIGHT=ROOT/'audit_v4764_scorpion_packet_caller_source_checked/report.json'

def collector_source():
    text=old.collector_source()
    for before,after in(
      ('audit_v4667_scorpion_secondary_{fighter}_p{side}_audio_{suffix}',
       'audit_v4765_scorpion_secondary_{fighter}_p{side}_packet_caller_{suffix}'),
      ("ROOT/'tools/qualify_scorpion_secondary_audio_guard_source_v4665.py'",
       "ROOT/'tools/qualify_scorpion_packet_caller_source_v4763.py',ROOT/'tools/run_scorpion_secondary_audio_ram_v4664.py',ROOT/'tools/qualify_scorpion_secondary_audio_guard_source_v4665.py',ROOT/'mk2ks_scorpion_secondary_audio_ram_v4663.lua'")):
        need(text.count(before)==1,'Unique complete original audio collector addition');text=text.replace(before,after)
    return text

def capture(fighter,side,enabled,guest):
    import qualify_scorpion_packet_caller_source_v4763 as source
    source.boundary();report=json.loads(PREFLIGHT.read_text())
    need(report['passed']and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Complete original observer and new read-only caller source qualified unchanged before boot')
    scope=dict(vars(previous),__file__=__file__,old=old.old,previous=previous,state=state,LUA=LUA,PREFLIGHT=PREFLIGHT)
    exec(compile(collector_source(),__file__+'::whole4664_audio_capture_plus_caller','exec'),scope)
    return scope['capture'](fighter,side,enabled,guest)

def caller_inventory(text,baseline):
    rows=lambda t,tag:previous.rows(t,tag)
    calls=rows(text,'PACKET_CALLER');packets=rows(text,'PACKET')
    need(len(calls)==len(packets)==28 and calls==rows(baseline,'PACKET_CALLER'),
         'Every actual packet has one identical samples-on/off caller witness')
    keys=('frame','seconds','writes','assistance','entry','a1','a3','a4','a8','a13')
    for packet,call in zip(packets,calls):
        need(all(call[k]==packet[k]for k in keys)and call['entry']=='FFA13BA0'and
             0x01000000<=int(call['sp'],16)<0x01100000,
             'Actual stack record bound to exact owned native dispatcher time/registers')
    return calls

pair_source=inspect.getsource(old.old.pair)
before="    pins={str(Path(__file__).resolve()):sha(__file__)}"
need(pair_source.count(before)==1,'Whole original paired PCM/state/queue/channel/DCS gate retained')
pair_source=pair_source.replace(before,"    callers=caller_inventory(t,bt)\n"+before,1)
before='sourceQualifiedVoiceEffectCallerFidelity=False,'
need(pair_source.count(before)==1,'Observation does not infer source-qualified callers from stack alone')
pair_source=pair_source.replace(before,'actualPacketCallerWitnesses=callers,everyNativePacketCallerObserved=True,\n                '+before,1)
scope=dict(vars(old.old),capture=capture,caller_inventory=caller_inventory,__file__=__file__)
exec(compile(pair_source,__file__+'::whole4658_PCM_state_pair_plus_actual_caller','exec'),scope)
pair=scope['pair']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    out=ROOT/f'audit_v4766_scorpion_secondary_{args.fighter}_p{args.side}_packet_caller_observed'
    need(not out.exists(),'Fresh immutable actual paired caller observation')
    try:report=pair(args.fighter,args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualRoutes','actualQueues','actualDelivery','nativePackets','actualPacketCallerWitnesses')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
