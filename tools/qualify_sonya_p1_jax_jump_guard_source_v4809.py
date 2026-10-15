"""Original physical policies/RAM pipeline plus declared Jax jump guard.

Requires actual previous native terminal and preserved whole-context failure.
Checks unchanged original action137/ground/21-damage instructions separately.
No source-only native jump, evasion, campaign, art/audio or port acceptance.
"""
import ast,hashlib,json,subprocess
from pathlib import Path
import qualify_sonya_p1_kitana_guard_source_v4795 as previous
import inspect_jax_137_ground_damage_source_v4805 as ground
import run_sonya_p1_jax_jump_guard_ram_v4808 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
LUA=capture.LUA
OUT=ROOT/'audit_v4810_sonya_p1_jax_jump_guard_source_checked'
TRANSITIVE_LUA=tuple(dict.fromkeys((LUA,*previous.TRANSITIVE_LUA)))
EXPECTED_SHA='843587F9ADA4EC895212C824D4FBABD85ED0150A9B842D1B48BD63113EBBA6AC'
BEFORE="    local reason\n    if jx_leg and frame-jx_leg<12 then"
AFTER="""    local reason
    if other.action==0x137 then jx_pound=frame+40 end
    if frame<jx_pound and height<=8 then
     jx_leg=nil
     if frame-jx_jump>=4 then jx_jump=frame end
     if frame-jx_jump<3 then reason='pound_jump_retry_edge';press('Up');press(human.x<other.x and'Left'or'Right')
     else reason='pound_jump_retry_release' end
    elseif jx_leg and frame-jx_leg<12 then"""

def reconstructed():
    original,mirror,kitana,adapted=previous.reconstructed()
    need(kitana.count('other.roster==4')==5 and kitana.count('other_now.roster~=4')==1,
         'All and only declared opponent predicates')
    jax=kitana.replace('kt_','jx_').replace('other.roster==4','other.roster==11').replace('other_now.roster~=4','other_now.roster~=11').replace('KITANA_','JAX_')
    changes=[('jx_upper=-1000;jx_guard=-1000 end','jx_upper=-1000;jx_guard=-1000;jx_pound=-1000;jx_jump=-1000 end'),
             (BEFORE,AFTER),
             ("log('JAX_DECISION','reason='..reason..' scope=physical_attempt_not_assumed_activation')",
              "log('JAX_DECISION',string.format('reason=%s pound_until=%d jump_start=%d scope=physical_attempt_not_assumed_activation',reason,jx_pound,jx_jump))")]
    for before,after in changes:
        need(jax.count(before)==1,'Exact independent original Jax physical adaptation')
        jax=jax.replace(before,after,1)
    variables=r'local kt_action_taps={}\nlocal rs_last'
    extended=r'local kt_action_taps={}\nlocal jx_last,jx_leg,jx_last_leg,jx_upper,jx_guard=nil,nil,-1000,-1000,-1000\nlocal jx_move=nil\nlocal jx_action_taps={}\nlocal jx_pound,jx_jump=-1000,-1000\nlocal rs_last'
    need(adapted.count(variables)==adapted.count('local replacement=[[\n')==1,'Unique fresh physical variable/branch placement')
    new=adapted.replace(variables,extended,1).replace('local replacement=[[\n','local replacement=[[\n'+jax,1)
    need(new.replace(extended,variables,1).replace('local replacement=[[\n'+jax,'local replacement=[[\n',1)==adapted,
         'Entire actual previous Kitana/mirror/range/boss/selection/continue/ending and RAM script restored outside new Jax branch')
    return jax,new

def source_boundary(wrapper=None,jax_override=None):
    previous.source_boundary()
    wrapper=(ROOT/LUA).read_text() if wrapper is None else wrapper
    need(hashlib.sha256(wrapper.encode()).hexdigest().upper()==EXPECTED_SHA,
         'Exact reviewed physical Jax wrapper and four readonly native taps; no undeclared native writes')
    jax,adapted=reconstructed()
    if jax_override is not None:need(jax_override==jax,'Exact independently reconstructed source-bound ordinary Jax controls')
    for token in ('other.action==0x137','jx_pound=frame+40','frame<jx_pound and height<=8',
                  "reason='pound_jump_retry_edge';press('Up')","reason='pound_jump_retry_release'",'frame-jx_jump>=4',
                  'own.id~=18 or own.roster~=18','(other_now.roster~=11)',"'JAX_FIELD'","'JAX_DECISION'",'p:install_write_tap'):
        need(token in jax,'Complete physical evasion/guard and true owner observation '+token)
    need('p:write_' not in jax and ':set_value(' not in jax and '.value=' not in jax,
         'Only ordinary press(button); observer callbacks return no replacement values')
    for token in ("{0xff86dd90,'ground_entry'}","{0xff86e020,'ground_result'}",
                  "{0xff86e070,'ground_damage'}","{0xff831360,'human_jump'}",'cpu.PC.value~=address+16',
                  'p:read_u16(h+0x1f0)~=18','p:read_u16(c+0x1f0)~=11','p:read_u32(hm+0xc0)~=h',
                  'p:read_u32(cm+0xc0)~=c','cpu.A8.value~=owner or cpu.A13.value~=main','(cpu.ST.value>>30)&1'):
        need(token in wrapper,'Readonly actual native callback context/source/ownership boundary '+token)
    code=capture.collector_source();ast.parse(code)
    for token in ('audit_v4811_{fighter}_p1_jax_jump_guard_ram',"MK2KS_CAMPAIGN_SIDE='1'",'human_slot=1,cpu_slot=2',
                  "MK2KS_TWO_PLAYER='0'",'raw==guest','rawRasterFilesWritten=0','raw_audio_files_written=0',
                  'Never persist encoded raster',"images[h['filename']]",'files.update(ROOT/p for p in source.TRANSITIVE_LUA)'):
        need(token in code,'Every whole cold/current3836/source/RAM-only collector boundary '+token)
    need('assert(count==6' in adapted and 'assert(#raw==1048576)' in adapted
         and "dofile('mk2ks_mileena_campaign_trace_v3848.lua')" in adapted,
         'All original six RAM image sinks, initialized guest and readonly cache observer retained')
    return dict(passed=True,physicalSlot=1,identity=18,newPhysicalCpuContext=11,originalKitanaAndAllOtherPoliciesRetained=True,
        allSixRAMFramesAndWholeGuestSinkRetained=True,separatePerFieldJaxStateAndDecisionObserver=True,
        separateFourReadOnlyNativeGroundAndJumpCallbacks=True,
        actualNativeJumpOrGroundDamageEvasionAccepted=False,actualPlayerOneCampaignClearAccepted=False,
        newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable source result')
    prior_path=previous.OUT/'report.json';prior=json.loads(prior_path.read_text())
    terminal_path=ROOT/'audit_v4798_sonya_p1_kitana_guard_observed/report.json'
    failure_path=ROOT/'audit_v4804_sonya_p1_kitana_guard_whole_campaign_checked/report.json'
    terminal=json.loads(terminal_path.read_text());failure=json.loads(failure_path.read_text())
    ground_path=ground.OUT/'report.json';ground_proof=json.loads(ground_path.read_text())
    need(prior['passed'] and prior['originalSourceFaultsRetained']==13 and len(prior['actualSourceFaultsRejected'])==7,
         'All20old source faults retained')
    need(terminal['passed'] and terminal['nativeExit']==0 and terminal['actualStages']==[0,1,2,3,4]
         and terminal['endingStarts']==terminal['endingCompletions']==0 and not failure['passed']
         and 'One complete native field and physical decision per observed field' in failure['error'],
         'Actual native terminal and mandatory-context failure retained before fresh Jax controls; never a restarted live run')
    need(ground_proof['passed'] and len(ground_proof['actualInstructionFaultsRejected'])==9
         and ground_proof['sourceInstructionBoundaryOnly'] and not ground_proof['actualNativeJumpEvadedDamageAccepted'],
         'Original ground/velocity/21damage code separately qualified, no source-only runtime claim')
    guest=capture.previous.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(ground.qualify(guest,stock)==ground_proof['sourceGate'],'All exact original native instructions unchanged')
    need(all(sha(p)==h for p,h in prior['inputHashes'].items()),'Every original compiled/native/control source unchanged')
    positive=source_boundary();wrapper=(ROOT/LUA).read_text();jax=reconstructed()[0];faults=[]
    for label,bad in (
        ('wrong_slot',wrapper.replace("MK2KS_CAMPAIGN_SIDE')=='1'","MK2KS_CAMPAIGN_SIDE')=='2'",1)),
        ('wrong_jax_context',wrapper.replace("'other.roster==11'","'other.roster==1'",1)),
        ('wrong_jump_entry',wrapper.replace('0xff831360','0xff831000',1)),
        ('fabricated_native_carry',wrapper+"cpu.ST.value=0\n"),
        ('native_health_write',wrapper+"p:write_u16(0x010602F0,161)\n")):
        need(bad!=wrapper,'Actual nonvacuous source mutation')
        try:source_boundary(wrapper=bad)
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual physical/native wrapper fault admitted '+label)
        need(source_boundary()==positive,'Actual entire source positive restored')
    for label,bad in (
        ('missing_pound_jump',jax.replace("press('Up')","press('Down')",1)),
        ('missing_jump_release_edge',jax.replace('frame-jx_jump<3','frame-jx_jump<4',1))):
        need(bad!=jax,'Actual reconstructed physical mutation')
        try:source_boundary(jax_override=bad)
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Physical Jax policy fault admitted '+label)
        need(source_boundary()==positive,'Every original native/control/source positive restored')
    pins=dict(prior['inputHashes'])
    for report in (terminal,ground_proof):
        for p,h in report['inputHashes'].items():
            need(p not in pins or pins[p]==h,'Consistent actual native/source input pins');pins[p]=h
    for p in [prior_path,terminal_path,failure_path,ground_path,Path(__file__).resolve(),Path(capture.__file__).resolve(),
              Path(ground.__file__).resolve(),*(ROOT/p for p in TRANSITIVE_LUA)]:pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All executed prior evidence/failures and fresh source bytes unchanged')
    report=dict(positive,inputHashes=pins,originalSourceFaultsRetained=20,actualSourceFaultsRejected=faults,
                originalGroundInstructionFaultsRetained=9,reconstructedJaxBranchSHA256=hashlib.sha256(jax.encode()).hexdigest().upper())
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
