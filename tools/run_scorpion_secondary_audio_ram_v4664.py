"""Fresh audio observation after4657 preboot lexical-guard failure.

Full original4658 pairing/native-state/PCM/channel/DCS gates remain intact.
Only unused leaves, qualified observer and exact source dependency pins change.
"""
import argparse,inspect,json,subprocess,traceback
from pathlib import Path
import run_scorpion_secondary_audio_ram_v4658 as old
ROOT,need,sha,state,previous=old.ROOT,old.need,old.sha,old.state,old.previous
NAME=old.NAME
LUA='mk2ks_scorpion_secondary_audio_ram_v4663.lua'
PREFLIGHT=ROOT/'audit_v4666_scorpion_secondary_audio_guard_source_checked/report.json'

def collector_source():
    text=old.collector_source()
    for before,after in(
      ('audit_v4661_scorpion_secondary_{fighter}_p{side}_audio_{suffix}','audit_v4667_scorpion_secondary_{fighter}_p{side}_audio_{suffix}'),
      ("ROOT/'tools/qualify_scorpion_secondary_audio_source_v4659.py'",
       "ROOT/'tools/qualify_scorpion_secondary_audio_guard_source_v4665.py',Path(old.__file__),ROOT/'tools/qualify_scorpion_secondary_audio_source_v4659.py',ROOT/'mk2ks_scorpion_secondary_audio_ram_v4657.lua'")):
        need(text.count(before)==1,'Exact fresh whole audio collector adaptation');text=text.replace(before,after)
    return text

def capture(fighter,side,enabled,guest):
    import qualify_scorpion_secondary_audio_guard_source_v4665 as source
    source.boundary();r=json.loads(PREFLIGHT.read_text())
    need(r['passed']and all(sha(p)==h for p,h in r['inputHashes'].items()),'Corrected exact source/observer preflight unchanged before boot')
    scope=dict(vars(previous),__file__=__file__,old=old,previous=previous,state=state,LUA=LUA,PREFLIGHT=PREFLIGHT)
    exec(compile(collector_source(),__file__+'::whole4658_corrected_source_capture','exec'),scope)
    return scope['capture'](fighter,side,enabled,guest)

scope=dict(vars(old),capture=capture,__file__=__file__)
exec(compile(inspect.getsource(old.pair),__file__+'::whole4658_native_PCM_state_pair','exec'),scope)
pair=scope['pair']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    out=ROOT/f'audit_v4668_scorpion_secondary_{args.fighter}_p{args.side}_audio_observed'
    need(not out.exists(),'Fresh immutable corrected audio observation')
    try:report=pair(args.fighter,args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualRoutes','actualQueues','actualDelivery','nativePackets')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
