"""Whole4773 slot/controller/transport/source gates plus exact Lua correction.

Both real preboot failures are retained. A first argument function call drops
extra returns when assert also receives a message; assign find results first.
"""
import inspect,json,re,subprocess
from pathlib import Path
import qualify_current_p1_campaign_source_v4773 as previous
import run_current_p1_campaign_ram_v4782 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
LUA=capture.LUA
OUT=ROOT/'audit_v4784_current_p1_campaign_source_checked'
TRANSITIVE_LUA=(LUA,*previous.TRANSITIVE_LUA)
BEFORE="local first,last=assert(source:find(before,1,true),'Exact original physical-slot precondition')"
AFTER="local first,last=source:find(before,1,true)\nassert(first,'Exact original physical-slot precondition')"
need(previous.EXPECTED.count(BEFORE)==1,'Exact original actual failed assignment')
EXPECTED=previous.EXPECTED.replace(BEFORE,AFTER,1)
boundary_source=inspect.getsource(previous.source_boundary)
scope=dict(vars(previous),__file__=__file__,capture=capture,LUA=LUA,OUT=OUT,TRANSITIVE_LUA=TRANSITIVE_LUA,EXPECTED=EXPECTED)
exec(compile(boundary_source,__file__+'::whole4773_only_actual_Lua_find_assignment_corrected','exec'),scope)
whole_boundary=scope['source_boundary']

def source_boundary(wrapper=None,driver_override=None):
    result=whole_boundary(wrapper,driver_override)
    old=(ROOT/previous.LUA).read_text();new=(ROOT/LUA).read_text()
    need(old.count(BEFORE)==1 and old.replace(BEFORE,AFTER,1)==new,
         'Byte-exact single Lua assignment correction; no native controls, observer or transport changes')
    for fighter in('kano','sonya'):
        folder=ROOT/f'audit_v4775_{fighter}_current_p1_campaign_ram'
        actual=json.loads((folder/'result.json').read_text());error=(folder/'stderr.log').read_text()
        report=json.loads((ROOT/f'audit_v4776_{fighter}_current_p1_campaign_observed/report.json').read_text())
        need(actual['exit_code']==3 and actual['ramGuestSHA256']is None and actual['actualNativeFrameCallbacks']==0 and
             not report['passed']and 'attempt to perform arithmetic on a string value (local \'last\')'in error,
             'Both actual preboot Lua failures and zero native guest/gameplay acceptance retained')
    generated=capture.collector_source()
    for token in('audit_v4785_{fighter}_current_p1_campaign_ram',"MK2KS_CAMPAIGN_SIDE='1'",'human_slot=1,cpu_slot=2'):
        need(token in generated,'Same whole physical P1 collector in unused corrected leaves '+token)
    return dict(result,bothActualPrebootFailuresRetained=True,onlyOneLuaReturnAssignmentCorrected=True)

def main():
    need(not OUT.exists(),'Fresh immutable corrected-source preflight')
    prior=ROOT/'audit_v4774_current_p1_campaign_source_checked/report.json';proof=json.loads(prior.read_text())
    need(proof['passed']and len(proof['actualSourceFaultsRejected'])==8 and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),'All original slot/controller/transport source gates and eight faults retained')
    positive=source_boundary();w=(ROOT/LUA).read_text();faults=[]
    for label,bad in(('original_failed_Lua_assignment',w.replace(AFTER,BEFORE,1)),
                      ('wrong_slot',w.replace("assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')","assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')",1)),
                      ('wrong_kano_controller',w.replace(previous.kano.LUA,previous.sonya.LUA)),
                      ('proxy_character',w.replace("fighter=='kano' or fighter=='sonya'","fighter=='liu_kang' or fighter=='sonya'")),
                      ('native_write',w+"p:write_u16(0x01060280,1)\n")):
        need(bad!=w,'Actual source counterexample')
        try:source_boundary(bad)
        except (ValueError,AssertionError,SyntaxError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual corrected wrapper source fault admitted '+label)
        need(source_boundary()==positive,'Entire corrected positive restored after every source fault')
    pins=dict(proof['inputHashes'])
    for p in[prior,Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(previous.__file__).resolve(),
             ROOT/'tools/run_current_p1_campaign_ram_v4772.py',*(ROOT/p for p in TRANSITIVE_LUA)]:pins[str(p.resolve())]=sha(p)
    for fighter in('kano','sonya'):
        folder=ROOT/f'audit_v4775_{fighter}_current_p1_campaign_ram'
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
        p=ROOT/f'audit_v4776_{fighter}_current_p1_campaign_observed/report.json';pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every original source/actual failure and corrected immutable byte unchanged')
    report=dict(positive,originalSourceFaultsRetained=8,actualSourceFaultsRejected=faults,inputHashes=pins)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
