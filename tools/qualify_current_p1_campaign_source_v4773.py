"""Full original campaign controls with one physical-slot precondition adapter.

Proves source boundaries before genuine player-one selection/combat. Does not
claim a player-one campaign clear, ending fidelity or release readiness.
"""
import ast,json,re,subprocess
from pathlib import Path
import run_current_p1_campaign_ram_v4772 as capture
import qualify_kano_current_p2_campaign_source_v4482 as kano
import qualify_kintaro_pressure_guard_long_source_v4437 as sonya
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
LUA=capture.LUA
OUT=ROOT/'audit_v4774_current_p1_campaign_source_checked'
TRANSITIVE_LUA=tuple(dict.fromkeys((LUA,*kano.TRANSITIVE_LUA,*sonya.TRANSITIVE_LUA)))
EXPECTED="""-- Same native cold controllers, with only the physical-slot precondition changed.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(fighter=='kano' or fighter=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path,before,after
if fighter=='kano' then
 path='mk2ks_kano_current_p2_campaign_ram_v4472.lua'
 before="assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"
 after="assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')"
else
 path='mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua'
 before="assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"
 after="assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')"
end
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local first,last=assert(source:find(before,1,true),'Exact original physical-slot precondition')
assert(not source:find(before,last+1,true),'Only one physical-slot precondition changes')
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@'..path..'::player_one_precondition_only_4771','t',_ENV))()
"""

def source_boundary(wrapper=None,driver_override=None):
    kano.source_boundary();sonya.source_boundary()
    wrapper=(ROOT/LUA).read_text()if wrapper is None else wrapper
    need(wrapper==EXPECTED,'Exact role routing and one slot-precondition-only wrapper; no extra calls, state writes or input changes')
    adapted=[]
    for fighter,source,original,driver in(
      ('kano',kano,"assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')",'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua'),
      ('sonya',sonya,"assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')",'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua')):
        text=(ROOT/source.LUA).read_text();replacement=original.replace("=='2'","=='1'")
        need(text.count(original)==1,'Actual unique original wrapper physical-slot precondition')
        text=text.replace(original,replacement,1)
        need(text.count(replacement)==1 and text.count('count==6')==1 and 'assert(#raw==1048576)'in text and
             "dofile('mk2ks_mileena_campaign_trace_v3848.lua')"in text,
             'Whole original controls, six RAM image sinks, initialized guest and read-only victim observer retained')
        body=(ROOT/driver).read_text()if driver_override is None else driver_override
        need(body==(ROOT/driver).read_text(),'Every original slot-polymorphic controller source byte unchanged')
        for token in("assert(side==1 or side==2)","local opponent=3-side",
          "buttons[key]=high['P'..side..' '..key]","buttons.Coin=system['Coin '..side]",
          "buttons.Start=system[side==1 and '1 Player Start' or '2 Players Start']",
          "slots[side].state","slots[opponent].state","route(p:read_u16(slots[side].roster))",
          "p:read_u16(slots[side].roster)~=identity","frame-ending_completed>=300"):
            need(token in body,'Original player-one button/state/selection/ending routing '+token)
        need('actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0'in body and
             'actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0'in body,
             'Both exact native physical player-slot address layouts retained, not proxy identities')
        adapted.append(dict(fighter=fighter,physicalSlot=1,trueIdentity=17 if fighter=='kano'else 18,
          originalWrapper=source.LUA,originalDriver=driver,onlyPhysicalSlotPreconditionChanged=True))
    text=capture.collector_source();ast.parse(text)
    for token in("MK2KS_CAMPAIGN_SIDE='1'",'human_slot=1,cpu_slot=2',"MK2KS_TWO_PLAYER='0'",
                  'rawRasterFilesWritten=0','raw_audio_files_written=0','Never persist encoded raster',
                  'raw==guest','images[h[\'filename\']]','files.update(ROOT/p for p in source.TRANSITIVE_LUA)'):
        need(token in text,'Whole original true solo/RAM-only/transitive-source collector '+token)
    return dict(passed=True,contexts=adapted,physicalSlot=1,allOriginalPhysicalPoliciesRetained=True,
      allSixRAMFramesAndWholeGuestSinkRetained=True,hostDeadlineSeconds=5900,transitiveLuaSources=list(TRANSITIVE_LUA),
      rawMediaFilesWritten=0,newBuilds=0,actualPlayerOneNativeCampaignClearAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable preboot source result')
    positive=source_boundary();faults=[];w=(ROOT/LUA).read_text()
    for label,wrong in(
      ('wrong_slot',w.replace("assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')","assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')")),
      ('wrong_kano_controller',w.replace(kano.LUA,sonya.LUA)),
      ('wrong_sonya_controller',w.replace(sonya.LUA,kano.LUA)),
      ('proxy_fighter',w.replace("fighter=='kano' or fighter=='sonya'","fighter=='liu_kang' or fighter=='sonya'")),
      ('native_write',w+"p:write_u16(0x01060280,1)\n")):
        need(wrong!=w,'Actual non-vacuous slot/controller/source fault')
        try:source_boundary(wrong)
        except (ValueError,AssertionError,SyntaxError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual player-one source fault admitted '+label)
        need(source_boundary()==positive,'Whole original source and slot adapter restored')
    driver=(ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua').read_text()
    for label,bad in(('wrong_input_slot',driver.replace("high['P'..side..' '..key]","high['P2 '..key]")),
                      ('wrong_actor_layout',driver.replace('actor=0x01060220','actor=0x01060df0')),
                      ('shortened_attract',driver.replace('frame-ending_completed>=300','frame-ending_completed>=3'))):
        need(bad!=driver,'Actual original controller mutation')
        try:source_boundary(driver_override=bad)
        except (ValueError,AssertionError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Original slot-routing fault admitted '+label)
        need(source_boundary()==positive,'Exact complete original controllers restored')
    pins={}
    for leaf in('audit_v4483_kano_current_p2_campaign_source_preflight/report.json',
                 'audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json',
                 'audit_v4758_kano_complete_native_ending_pixels_and_hardware_checked/report.json',
                 'audit_v4758_sonya_complete_native_ending_pixels_and_hardware_checked/report.json'):
        path=ROOT/leaf;report=json.loads(path.read_text());need(report['passed'],'Actual original source or complete current player-two native evidence passed')
        for p,h in report['inputHashes'].items():need(p not in pins or pins[p]==h,'Consistent original compiled/native inputs');pins[p]=h
        pins[str(path.resolve())]=sha(path)
    for p in[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(capture.previous.__file__).resolve(),
             Path(kano.__file__).resolve(),Path(sonya.__file__).resolve(),*(ROOT/p for p in TRANSITIVE_LUA)]:pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every executed original controller/source/native evidence byte unchanged')
    report=dict(positive,actualSourceFaultsRejected=faults,inputHashes=pins)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
