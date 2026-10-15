"""Entire native campaign/boss/ending grammar on fresh current5219 Kano P2.

Retain5199 whole semantic verifier and18 effective native/guest-proof faults.
Only physical-slot metadata, current provenance and RAM/gzip carrier adapt.
No assumption of chronology equality with older builds or player one.
"""
import inspect,json,re,sys,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_current_kano_p2_campaign_v5621 as capture
import verify_current_kano_p1_whole_campaign_v5199 as original

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5624_current_kano_p2_campaign_checked'

def matched(folder,pins):
 need(folder==capture.OUT,'Exact fresh executed current P2 capture')
 meta=json.loads((folder/'result.json').read_text())
 before=json.loads((folder/'input_hashes_before.json').read_text())
 need(meta['passed']and meta['nativeExit']==0 and meta['fighter']=='kano'and meta['physicalSlot']==2 and
  meta['identity']==17 and before==meta['inputHashes']and meta['candidate']==current.NAME and
  meta['executableSHA256']==current.EXE_SHA and meta['guestSHA256']==current.GUEST_SHA and
  meta['rawMediaGuestAudioFilesWritten']==meta['newBuilds']==0,'Actual terminal current Kano P2 provenance')
 need(all(sha(p)==h for p,h in before.items()),'All executed compiled/controller inputs unchanged')
 build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(all(before.get(p)==h for p,h in build['input_hashes'].items()),'All actual compiled sources retained')
 boundary=capture.boundary.source_boundary()
 need(boundary['passed']and boundary['physicalInputsExactlyUnchanged']and boundary['physicalSlot']==2,
  'Whole previously qualified Kano P2 physical policy, no guest/AI/health/RNG assistance')
 source=capture.capture_source()
 need("MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='2'"in source and
  "MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'"in source,
  'Exact actual P2 native button policy')
 for name in capture.CONTROLLERS:
  p=ROOT/name
  need(before[str(p.resolve())]==sha(p)and not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',p.read_text()),
   'All actual transitive controller/observer source pinned, no state writes')
 process=json.loads((folder/'process.json').read_text())
 command=process['command']
 need(command[0]==str(ROOT/current.NAME/'mkport_candidate.exe')and command[-1]==str(ROOT/capture.LUA)and
  '-nocheat'in command and command[command.index('-frameskip')+1]=='0'and
  command[command.index('-str')+1]=='6000','Actual current executable and complete native P2 command')
 proof=json.loads((folder/'guest_memory_proof.json').read_text())
 need(capture.qualify_payload_metadata_warning((folder/'stderr.log').read_text(),proof)==
  meta['qualifiedTestCandidateMetadataWarning'],'Actual source/full-guest metadata and empty stderr; no warning waiver')
 need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
  'No raw guest/audio/RGB dumps or automatic timed-boot PNG')
 pins.update(before)

def whole_run():
 scope=dict(vars(original),__file__=__file__,current=current,capture=capture,OUT=OUT,matched=matched)
 for function in [original.campaign_meta,original.ram_guest,original.ram_guest_checked,
                  original.make_native,original.run]:
  source=inspect.getsource(function)
  changes=[]
  if function is original.campaign_meta:
   changes=[('human_slot=1,cpu_slot=2','human_slot=2,cpu_slot=1')]
  if function is original.run:
   changes=[("parse(text,1,'kano')","parse(text,2,'kano')"),
    ("'roster','17,1'","'roster','1,17'"),
    ('actualNaturalCurrentKanoP1BossesOwnEndingAttractAccepted','actualNaturalCurrentKanoP2BossesOwnEndingAttractAccepted')]
  for before,after in changes:
   need(source.count(before)==1,'One exact whole native slot adaptation '+before)
   source=source.replace(before,after,1)
  exec(compile(source,__file__+'::entire_'+function.__name__,'exec'),scope)
 return scope['run']()

if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal result, never restart on observation timeout')
 need(not OUT.exists(),'Fresh immutable full campaign verdict')
 try:report=whole_run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:
  print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
