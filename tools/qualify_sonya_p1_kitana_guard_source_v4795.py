"""Exact new physical Kitana branch with all old native/RAM/source boundaries.

Duplicates the original mirror guard into a separate CPU4 context. Original
CPU18 mirror, CPU5/10 ranged and boss policies stay byte-for-byte intact.
Source qualification is not a native move, campaign or port acceptance.
"""
import ast,hashlib,json,subprocess
from pathlib import Path
import qualify_current_p1_campaign_source_v4783 as previous
import run_sonya_p1_kitana_guard_ram_v4794 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
LUA=capture.LUA
OUT=ROOT/'audit_v4796_sonya_p1_kitana_guard_source_checked'
TRANSITIVE_LUA=tuple(dict.fromkeys((LUA,*previous.TRANSITIVE_LUA)))
EXPECTED_SHA='3ACF4B698FF44AE5FEA15140D1A2EB8597959FB78ECDCB9F94F0A96BEDAE6E0B'

def reconstructed():
    original=(ROOT/'mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua').read_text()
    first=original.index("   elseif strategy=='guard_punish' and other.roster==18 then")
    last=original.index("   elseif strategy=='zoning' or strategy=='guard_punish' then",first+1)
    mirror=original[first:last]
    need(mirror.count('other.roster==18')==5,'All five CPU-context/threshold predicates declared')
    kitana=mirror.replace('gp_','kt_').replace('other.roster==18','other.roster==4')
    allowed='(other_now.roster~=5 and other_now.roster~=10 and other_now.roster~=18)'
    need(kitana.count(allowed)==1,'Original observer target guard remains mandatory')
    kitana=kitana.replace(allowed,'(other_now.roster~=4)',1).replace('GUARD_','KITANA_')
    variables=r'local gp_action_taps={}\nlocal rs_last'
    extended=r'local gp_action_taps={}\nlocal kt_last,kt_leg,kt_last_leg,kt_upper,kt_guard=nil,nil,-1000,-1000,-1000\nlocal kt_move=nil\nlocal kt_action_taps={}\nlocal rs_last'
    before="assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')"
    after=before.replace("=='2'","=='1'")
    need(original.count(before)==original.count(variables)==original.count('local replacement=[[\n')==1,
         'Exactly declared original physical source boundaries')
    adapted=original.replace(before,after,1).replace(variables,extended,1).replace('local replacement=[[\n','local replacement=[[\n'+kitana,1)
    restored=adapted.replace(after,before,1).replace(extended,variables,1).replace('local replacement=[[\n'+kitana,'local replacement=[[\n',1)
    need(restored==original,'Every original mirror/range/boss/observer/RAM byte restored outside three declared physical changes')
    return original,mirror,kitana,adapted

def source_boundary(wrapper=None,kitana_override=None):
    previous.source_boundary()
    wrapper=(ROOT/LUA).read_text() if wrapper is None else wrapper
    need(hashlib.sha256(wrapper.encode()).hexdigest().upper()==EXPECTED_SHA,
         'Exact reviewed physical wrapper: no extra identity/AI/RNG/health/task/register write or undeclared input policy')
    original,mirror,kitana,adapted=reconstructed()
    if kitana_override is not None:need(kitana_override==kitana,'Exact independently reconstructed physical guard branch')
    for token in ('own.id~=18 or own.roster~=18','own.owner~=own.actor','cpu.A8.value~=own.actor or cpu.A13.value~=own.main',
                  'cpu_height>15 and gap<100','ready and gap<78 and frame-kt_upper>=26',
                  "if age>=3 and age<7 then press('Low Punch');press('Block')end",
                  "reason='active_guard';press('Down');press('Block')",'p:install_write_tap',"'KITANA_FIELD'","'KITANA_DECISION'",
                  '(other_now.roster~=4)'):
        need(token in kitana,'Complete independent physical policy and readonly native ownership observer '+token)
    need('p:write_' not in kitana and ':set_value(' not in kitana and '.value=' not in kitana,
         'Only ordinary press(button) calls; taps observe stores and return no replacement value')
    body=capture.collector_source();ast.parse(body)
    for token in ('audit_v4797_{fighter}_p1_kitana_guard_ram',"MK2KS_CAMPAIGN_SIDE='1'",'human_slot=1,cpu_slot=2',
                  "MK2KS_TWO_PLAYER='0'",'raw==guest','rawRasterFilesWritten=0','raw_audio_files_written=0',
                  'Never persist encoded raster',"images[h['filename']]",'files.update(ROOT/p for p in source.TRANSITIVE_LUA)'):
        need(token in body,'Whole original cold solo/source/RAM collector retained '+token)
    need('assert(count==6' in adapted and 'assert(#raw==1048576)' in adapted
         and "dofile('mk2ks_mileena_campaign_trace_v3848.lua')" in adapted,
         'All original six image sinks, initialized guest sink and native Mileena cache observer retained')
    return dict(passed=True,physicalSlot=1,identity=18,newPhysicalCpuContext=4,
        allOriginalOtherPhysicalPoliciesRetained=True,allSixRAMFramesAndWholeGuestSinkRetained=True,
        separatePerFieldKitanaStateAndDecisionObserver=True,actualPlayerOneNativeCampaignClearAccepted=False,
        newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable preboot source proof')
    prior_path=previous.OUT/'report.json';prior=json.loads(prior_path.read_text())
    diagnosis_path=ROOT/'audit_v4792_sonya_p1_bounded_kitana_diagnosis/report.json'
    diagnosis=json.loads(diagnosis_path.read_text())
    need(prior['passed'] and prior['originalSourceFaultsRetained']==8 and len(prior['actualSourceFaultsRejected'])==5
         and diagnosis['passed'] and not diagnosis['actualNaturalP1TowerClearAccepted'],
         'All original source faults and actual incomplete native Kitana campaign retained')
    need(all(sha(p)==h for p,h in prior['inputHashes'].items()),'Every old compiled/native/control/RAM source byte unchanged')
    positive=source_boundary();wrapper=(ROOT/LUA).read_text();kitana=reconstructed()[2];faults=[]
    for label,bad in (
        ('wrong_physical_slot',wrapper.replace("MK2KS_CAMPAIGN_SIDE')=='1'","MK2KS_CAMPAIGN_SIDE')=='2'",1)),
        ('wrong_target_context',wrapper.replace("'other.roster==4'","'other.roster==1'",1)),
        ('native_health_write',wrapper+"p:write_u16(0x010602F0,161)\n"),
        ('proxy_identity',wrapper+"p:write_u16(0x01060280,1)\n")):
        need(bad!=wrapper,'Real source mutation, not fixture')
        try:source_boundary(wrapper=bad)
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Physical wrapper fault admitted '+label)
        need(source_boundary()==positive,'Actual positive restored')
    for label,bad in (
        ('missing_anti_air',kitana.replace('cpu_height>15 and gap<100','false',1)),
        ('foreign_special_owner',kitana.replace('own.id~=18 or own.roster~=18','own.id~=1 or own.roster~=1',1)),
        ('wrong_physical_leg_edge',kitana.replace("press('Low Punch');press('Block')","press('High Kick')",1))):
        need(bad!=kitana,'Actual reconstructed policy mutation')
        try:source_boundary(kitana_override=bad)
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Independent physical policy fault admitted '+label)
        need(source_boundary()==positive,'Full physical positive restored')
    pins=dict(prior['inputHashes'])
    for p in [prior_path,diagnosis_path,Path(__file__).resolve(),Path(capture.__file__).resolve(),
              ROOT/'tools/run_current_p1_campaign_ram_v4772.py',*(ROOT/p for p in TRANSITIVE_LUA)]:pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All immutable prior and fresh source bytes unchanged')
    report=dict(positive,inputHashes=pins,originalSourceFaultsRetained=13,actualSourceFaultsRejected=faults,
                reconstructedKitanaBranchSHA256=hashlib.sha256(kitana.encode()).hexdigest().upper())
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
