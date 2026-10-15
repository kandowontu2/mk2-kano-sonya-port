"""Whole original controller/guest/RAM boundaries plus readonly cache probe.

Only observer and host diagnostic stop differ. Retain actual global-state
corruption and parser failure; source checks cannot prove a native fix.
"""
import ast,hashlib,json,subprocess
from pathlib import Path
import qualify_sonya_p1_jax_jump_guard_source_v4809 as previous
import run_sonya_subzero_cache_trace_ram_v4820 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
LUA=capture.LUA
OUT=ROOT/'audit_v4822_sonya_subzero_cache_trace_source_checked'
TRANSITIVE_LUA=tuple(dict.fromkeys((LUA,*previous.TRANSITIVE_LUA)))
EXPECTED_SHA='3454546879C86D3469B79C451BA27EA9C4D4611379843E607FF5E6C493DC437E'

def source_boundary(wrapper=None):
    previous.source_boundary()
    wrapper=(ROOT/LUA).read_text() if wrapper is None else wrapper
    need(hashlib.sha256(wrapper.encode()).hexdigest().upper()==EXPECTED_SHA,
         'Exact reviewed readonly probe and diagnostic stop; no native memory/register/input replacement')
    for token in ("dofile('mk2ks_sonya_p1_jax_jump_guard_ram_v4807.lua')",'local ring,ring_size,flushed={},1200,false',
      "{0xff906050,'self_lookup'}","{0xff906090,'main_lookup'}","{0xff906110,'root_loaded'}",
      "{0xff906130,'lookup_cell'}","{0xff906140,'lookup_result'}","{0xff838790,'cache_begin'}",
      "{0xff8387f0,'group_next'}","{0xff838810,'descriptor'}","{0xff838a30,'cache_end'}",
      'cpu.PC.value==address+16','p:read_u32(0x01060220)==a','p:read_u16(a+0x1f0)==18',
      'cpu.PC.value~=0xff838860','bad_frame=frame','frame>=bad_frame+2','frame>=108270',
      'diagnostic_only=true','address>=0xfe800000 and address<=0xffffffc0'):
        need(token in wrapper,'Whole readonly actual-native source/role/cursor/host-stop boundary '+token)
    need('p:write_' not in wrapper and '.value=' not in wrapper and ':set_value(' not in wrapper,
         'No memory, register, health, AI, RNG, roster, palette, task or input mutations in observer')
    code=capture.collector_source();ast.parse(code)
    for token in ('audit_v4823_{fighter}_subzero_cache_trace_ram',"MK2KS_CAMPAIGN_SIDE='1'",'human_slot=1,cpu_slot=2',
      "MK2KS_TWO_PLAYER='0'",'raw==guest','rawRasterFilesWritten=0','raw_audio_files_written=0','Never persist encoded raster',
      "images[h['filename']]",'files.update(ROOT/p for p in source.TRANSITIVE_LUA)'):
        need(token in code,'Whole original cold/controller/source/RAM collector retained '+token)
    return dict(passed=True,diagnosticOnly=True,physicalSlot=1,identity=18,
        originalAllPhysicalPoliciesRetained=True,allSixRAMFramesAndWholeGuestSinkRetained=True,
        observerReadOnly=True,hostDiagnosticStopAfterActualBadWrite=True,
        sourceOnlyNativeRootCauseOrFixAccepted=False,actualNaturalTowerClearAccepted=False,
        newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable probe source result')
    prior_path=previous.OUT/'report.json';prior=json.loads(prior_path.read_text())
    checkpoint_path=ROOT/'audit_v4816_jax_evasion_and_subzero_overrun_progress/progress.json'
    checkpoint=json.loads(checkpoint_path.read_text())
    terminal_path=ROOT/'audit_v4812_sonya_p1_jax_jump_guard_observed/report.json';terminal=json.loads(terminal_path.read_text())
    failure_path=ROOT/'audit_v4818_sonya_p1_jax_jump_guard_whole_campaign_checked/report.json';failure=json.loads(failure_path.read_text())
    need(prior['passed'] and prior['originalSourceFaultsRetained']==20 and len(prior['actualSourceFaultsRejected'])==7,
         'All27old physical/readonly/native source faults retained')
    need(terminal['passed'] and terminal['nativeExit']==0 and terminal['actualStages']==list(range(8))
         and not failure['passed'] and "KeyError('frame')" in failure['error'],
         'Actual previous native terminal and frame-less-reentry parser counterexample preserved')
    need(checkpoint['nativeDefect']['firstFrame']==108255 and checkpoint['nativeDefect']['stableAllContextsContradicted']
         and not checkpoint['fullPortAcceptance'],'Actual native state corruption is required evidence, not an invented reproduction')
    positive=source_boundary();wrapper=(ROOT/LUA).read_text();faults=[]
    for label,bad in (
      ('wrong_original_controller',wrapper.replace('v4807.lua','v4793.lua',1)),
      ('wrong_cache_instruction',wrapper.replace('0xff838860','0xff838850',1)),
      ('proxy_actor_scope',wrapper.replace('==18','==1',1)),
      ('native_state_restore',wrapper+"p:write_u16(0x010601F0,1)\n"),
      ('native_register_repair',wrapper+"cpu.A0.value=0\n")):
        need(bad!=wrapper,'Real observer source mutation')
        try:source_boundary(bad)
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Native probe fault admitted '+label)
        need(source_boundary()==positive,'Entire exact readonly probe positive restored')
    pins=dict(prior['inputHashes'])
    for p,h in terminal['inputHashes'].items():
        need(p not in pins or pins[p]==h,'Consistent actual native/controller pins');pins[p]=h
    for p in [prior_path,checkpoint_path,terminal_path,failure_path,Path(__file__).resolve(),Path(capture.__file__).resolve(),
      ROOT/'tools/run_current_p1_campaign_ram_v4772.py',*(ROOT/p for p in TRANSITIVE_LUA)]:pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every old actual/native/public/source evidence and fresh observer byte unchanged')
    report=dict(positive,inputHashes=pins,originalSourceFaultsRetained=27,actualSourceFaultsRejected=faults)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
