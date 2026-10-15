"""Actual corrected executable whole campaign, same full native semantic gate.

Require byte-identical complete actual chronology to the independently
fault-qualified previous campaign. Re-run the entire native/boss gate on the
new capture, plus real current-row faults. Never use an early prefix as clear.
"""
import argparse,gzip,hashlib,inspect,json,re,sys,traceback
from pathlib import Path
from types import SimpleNamespace
import current_payload_metadata_context_v5229 as current
import run_corrected_p1_campaigns_v5230 as host
import verify_current_kano_p1_whole_campaign_v5199 as kano
import verify_extended_sonya_p1_whole_campaign_v5213 as sonya
ROOT,need,sha=current.ROOT,current.need,current.sha

def run(fighter):
 module=kano if fighter=='kano'else sonya
 ref=host.kano if fighter=='kano'else host.sonya
 folder=ROOT/f'audit_v5231_{fighter}_corrected_p1_campaign'
 carrier=SimpleNamespace(OUT=folder,LUA=ref.LUA,CONTROLLERS=ref.CONTROLLERS,__file__=host.__file__)
 prior_path=(ROOT/'audit_v5200_current_kano_p1_whole_campaign_checked/report.json'if fighter=='kano'else
  ROOT/'audit_v5214_extended_sonya_p1_whole_campaign_checked/report.json')
 prior=json.loads(prior_path.read_text())
 accepted_key='actualNaturalCurrent'+('Kano'if fighter=='kano'else'Sonya')+'P1BossesOwnEndingAttractAccepted'
 need(prior['passed']and prior[accepted_key]and prior['case']['unassisted_clear_proven']and
  len(prior['actualNativeAndRAMProofFaultsRejected'])==18 and
  all(sha(p)==h for p,h in prior['inputHashes'].items()),'Complete prior true-ID/native/boss/ending/attract/18fault campaign proof')
 actual=json.loads((folder/'result.json').read_text())
 with gzip.open(folder/'run.log.gz','rb')as reader:raw=reader.read()
 with gzip.open(ref.OUT/'run.log.gz','rb')as reader:previous_raw=reader.read()
 old_lines=previous_raw.splitlines(keepends=True);actual_lines=raw.splitlines(keepends=True)
 old_speed=re.fullmatch(rb'Average speed: ([0-9]+\.[0-9]+)% \(([0-9]+) seconds\)\r?\n',old_lines[-1])
 actual_speed=re.fullmatch(rb'Average speed: ([0-9]+\.[0-9]+)% \(([0-9]+) seconds\)\r?\n',actual_lines[-1])
 need(old_speed and actual_speed and old_speed[2]==actual_speed[2]and
  sum(line.startswith(b'Average speed: ')for line in old_lines)==
  sum(line.startswith(b'Average speed: ')for line in actual_lines)==1,
  'Exactly one final non-game host performance trailer with identical emulated duration')
 need(actual_lines[:-1]==old_lines[:-1],'Every actual native/RGB/selection/input/winner/boss/ending byte identical; only final host speed percentage may differ')
 actual_native_raw=b''.join(actual_lines[:-1])
 text=raw.decode().replace('\r\n','\n')
 def matched(capture,pins):
  need(capture==folder,'Exact actually executed fresh capture')
  meta=json.loads((folder/'result.json').read_text())
  before=json.loads((folder/'input_hashes_before.json').read_text())
  need(meta['passed']and meta['nativeExit']==0 and meta['fighter']==fighter and meta['physicalSlot']==1 and
   meta['identity']==(17 if fighter=='kano'else 18)and meta['candidate']==current.NAME and
   meta['executableSHA256']==current.EXE_SHA and meta['guestSHA256']==current.GUEST_SHA and
   meta['inputHashes']==before and meta['rawMediaGuestAudioFilesWritten']==meta['newBuilds']==0,
   'Actual terminal corrected-build native/physical scope')
  need(all(sha(p)==h for p,h in before.items()),'All actual executed compiled/control sources intact')
  build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
  need(all(before.get(p)==h for p,h in build['input_hashes'].items()),'Every actual compiled input preserved')
  proof=json.loads((folder/'guest_memory_proof.json').read_text())
  need(host.metadata_clean((folder/'stderr.log').read_text(),proof)==meta['qualifiedTestCandidateMetadataWarning'],
   'Correct actual compiled declaration/payload/full initialized guest with no warning waiver')
  need(inspect.getsource(ref.capture)==inspect.getsource(host.kano.capture if fighter=='kano'else host.sonya.capture),
   'Entire actual physical/RAM/gzip capture function unchanged')
  for name in ref.CONTROLLERS:
   p=ROOT/name
   need(before[str(p.resolve())]==sha(p)and not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',p.read_text()),
    'Actual every transitive controller source pinned and no game-state assistance')
  p=json.loads((folder/'process.json').read_text())
  need(p['command'][0]==str(ROOT/current.NAME/'mkport_candidate.exe')and
   p['command'][-1]==str(ROOT/ref.LUA)and '-nocheat'in p['command']and '-nothrottle'in p['command'],
   'Actual new executable/native physical driver command')
  need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),'No raw guest/raster/audio files')
  pins.update(before)
 scope=dict(vars(module),current=current,capture=carrier,matched=matched)
 # Adapt only the exact current guest-proof provenance, not native semantics.
 guest_source=inspect.getsource(module.ram_guest)
 exec(compile(guest_source,__file__+'::same_whole_RAM_guest_contract','exec'),scope)
 checked_source=inspect.getsource(module.ram_guest_checked)
 exec(compile(checked_source,__file__+'::same_accumulating_RAM_guest_contract','exec'),scope)
 exec(compile(inspect.getsource(module.make_native),__file__+'::same_entire_native_factory','exec'),scope)
 verifier=scope['make_native']();positive=verifier(folder)
 need(positive['passed']and positive['unassisted_clear_proven']and
  positive['stages_reached']==list(range(13))+[14,15,16],'Actual corrected executable full native/boss/own-ending/300attract gate')
 rows=kano.original.original.knife.old.parse(text,1,fighter);faults=[]
 for tag,key,value,label in [('LIVE','human','1:1','True live human ID'),('ENDING_COMPLETED','pictures','0,0','Both own native picture/story pages')]:
  r=next(r for r in rows if r['tag']==tag)
  damaged=kano.original.original.change(text,tag,r['frame'],key,value)
  rejected=verifier(folder,text_override=damaged)
  need(not rejected['passed']and any(label in error for error in rejected['errors']),'Same full actual current semantic gate rejects '+tag)
  faults.append(dict(tag=tag,key=key,rejectedBy=label))
 need(verifier(folder)==positive,'Full actual current positive restored after real current-row faults')
 pins=dict(positive['inputHashes'])
 for p,h in prior['inputHashes'].items():
  need(p not in pins or pins[p]==h,'Consistent unchanged old/current semantic evidence');pins[p]=h
 for p in[Path(__file__),Path(host.__file__),Path(current.__file__),prior_path,*folder.rglob('*')]:
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every actual old/new source/evidence byte retained')
 return dict(passed=True,fighter=fighter,physicalSlot=1,candidate=current.NAME,executableSHA256=current.EXE_SHA,
  case=positive,actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted=True,
  completeNativeLogBytes=len(raw),completeNativeLogSHA256=hashlib.sha256(raw).hexdigest().upper(),
  entirePriorFaultQualifiedNativeChronologyByteIdentical=True,
  completeNativeChronologyBytes=len(actual_native_raw),completeNativeChronologySHA256=hashlib.sha256(actual_native_raw).hexdigest().upper(),
  onlyExcludedHostTrailer=dict(previousSpeedPercent=old_speed[1].decode(),actualSpeedPercent=actual_speed[1].decode(),emulatedSeconds=int(actual_speed[2])),
  priorWholeCampaignAnd18NativeRAMFaultProof=str(prior_path),actualCurrentRowFaultsRejected=faults,inputHashes=pins,
  completeEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
 out=ROOT/f'audit_v5235_{args.fighter}_corrected_p1_campaign_checked'
 need(not out.exists(),'Fresh immutable whole corrected campaign')
 need((ROOT/f'audit_v5231_{args.fighter}_corrected_p1_campaign/result.json').exists(),'Await actual terminal, never synthesize a result on observation timeout')
 try:report=run(args.fighter)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
