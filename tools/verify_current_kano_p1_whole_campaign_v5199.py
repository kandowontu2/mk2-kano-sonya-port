"""Whole current4992 Kano P1 native campaign and original boss-input gate.

Only source-bound capture provenance, gzip transport and RAM guest proof adapt.
The original selection/schedule/morph/health/winner/continue/boss/ending grammar
is retained. A natural clear does not imply full ending art or audio fidelity.
"""
import gzip,hashlib,inspect,json,re,sys,traceback
from pathlib import Path
import native_subzero_legs_context_v4993 as current
import run_current_kano_p1_campaign_v5195 as capture
import verify_kano_current_p2_whole_campaign_v4487 as original
import verify_sonya_zoning700_campaign_v4015 as ram

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5200_current_kano_p1_whole_campaign_checked'

def read_log(folder):
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8-sig')as reader:return reader.read()

def campaign_meta(folder):
 meta=json.loads((folder/'result.json').read_text())
 return dict(meta,player='kano',human_slot=1,cpu_slot=2,strategy='zoning',boot_frame=600,
  exit_code=meta['nativeExit'],assistance='none',input_hashes=meta['inputHashes'],boss_policy='shao_knife_retreat')

def matched(folder,pins):
 meta=json.loads((folder/'result.json').read_text());before=json.loads((folder/'input_hashes_before.json').read_text())
 need(folder==capture.OUT and meta['passed']and meta['nativeExit']==0 and meta['fighter']=='kano'and
  meta['physicalSlot']==1 and meta['identity']==17 and before==meta['inputHashes']and
  meta['candidate']==current.NAME and meta['executableSHA256']==current.EXE_SHA and
  meta['guestSHA256']==current.GUEST_SHA and meta['rawMediaGuestAudioFilesWritten']==meta['newBuilds']==0,
  'Actual source-bound terminal current Kano P1 capture')
 need(all(sha(p)==h for p,h in before.items()),'Every executed input unchanged')
 build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(all(before.get(p)==h for p,h in build['input_hashes'].items()),'Every compiled input preserved')
 pins.update(before)
 text='\n'.join((ROOT/p).read_text()for p in capture.CONTROLLERS)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',text),'No guest/health/AI/RNG assistance')
 source=Path(capture.__file__).read_text()
 need("'-nocheat'"in source and "'-noautoframeskip','-frameskip','0'"in source and
  "MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'"in source and
  "MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'"in source,
  'Exact ordinary native button-only Kano P1 controls')
 proof=json.loads((folder/'guest_memory_proof.json').read_text())
 need(capture.qualify_payload_metadata_warning((folder/'stderr.log').read_text(),proof)==meta['qualifiedTestCandidateMetadataWarning'],
  'Only exact source/payload/whole-guest qualified metadata warning')
 need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
  'No guest/raster/audio file dumps')
 original.original.knife.source_boundary()

def ram_guest(folder,pins,wanted,text,proof_override=None):
 p=folder/'guest_memory_proof.json'
 proof=json.loads(p.read_text())if proof_override is None else proof_override
 digest=hashlib.sha256(wanted).hexdigest().upper()
 need(len(wanted)==1048576 and digest==current.GUEST_SHA,'Independent full current initialized guest')
 need(proof==dict(frame=1,bytes=1048576,sha256=digest,everyActualByteComparedInRAM=True,
  executableSHA256=current.EXE_SHA,payloadSHA256=current.PAYLOAD_SHA,captureSourceSHA256=sha(capture.__file__),
  transportSourceSHA256=sha(ROOT/capture.LUA),guestDumpFilesWritten=0),
  'Actual entire RAM guest, executable/payload/host/Lua provenance')
 lines=text.splitlines();header=f'MK2_CAMPAIGN_GUEST_RAM_DIGEST frame=1 bytes=1048576 sha256={digest}'
 need([line for line in lines if line.startswith('MK2_CAMPAIGN_GUEST_RAM')]==[header]and
  not any('hex='in line for line in lines),'Exactly one actual digest, no raw guest/RGB persisted')
 at=lines.index(header)
 need(any(s.startswith('MK2_NAT_CAMPAIGN_BOOT frame=1 ')for s in lines[:at])and
  any(s.startswith('MK2_NAT_CAMPAIGN_MORPH_ROM frame=1 ')for s in lines[at+1:]),
  'Actual first-frame guest between BOOT and MORPH_ROM')
 pins[str(p.resolve())]=sha(p);return wanted

def ram_guest_checked(folder,pins,wanted,text,errors):
 try:return ram_guest(folder,pins,wanted,text)
 except ValueError as error:errors.append(str(error));return wanted

def adapt_transport(source):
 source=ram.adapt_guest_transport(source)
 changes=[
  ("result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))","result=campaign_meta(folder)"),
  ("harnesses=[folder/'input_sources/tree'/DRIVER]","harnesses=[ROOT/DRIVER]")]
 for before,after in changes:
  need(source.count(before)==1,'One exact source-bound transport adaptation '+before)
  source=source.replace(before,after,1)
 before="(folder/'run.log').read_text(encoding='utf-8-sig')"
 need(source.count(before)==2,'Actual and disabled obsolete chronology reads only')
 return source.replace(before,'read_log(folder)')

def make_native():
 factory=inspect.getsource(original.original.knife.make_verifier)
 before='    namespace=dict(vars(old));namespace.update'
 need(factory.count(before)==1,'Full original Knife native factory and physical-input replay')
 factory=factory.replace(before,'    source=adapt_transport(source)\n'+before,1)
 scope=dict(vars(original.original.knife),adapt_transport=adapt_transport)
 exec(compile(factory,__file__+'::entire_factory_current_RAM_gzip','exec'),scope)
 verifier=scope['make_verifier']((current.expected(),None,None,None,None))
 verifier.__globals__.update(NAME=current.NAME,matched=matched,ram_guest_checked=ram_guest_checked,
  campaign_meta=campaign_meta,read_log=read_log)
 return verifier

def run():
 need(not OUT.exists(),'Fresh immutable current whole native campaign')
 text=read_log(capture.OUT);native=make_native();positive=native(capture.OUT)
 need(positive['passed'],'Entire original native/boss-input grammar: '+repr(positive['errors']))
 need(positive['unassisted_clear_proven']and positive['stages_reached']==list(range(13))+[14,15,16],
  'Actual all native opponents, both own bosses and own ending/return')
 rows=original.original.knife.old.parse(text,1,'kano');change=original.original.change
 faults=[]
 def reject(label,damaged,error):
  need(damaged!=text,'Actual nonvacuous captured-row fault '+label)
  result=native(capture.OUT,text_override=damaged)
  need(not result['passed']and any(error in e for e in result['errors']),'Specific original gate rejects '+label)
  faults.append(dict(kind=label,rejectedBy=error))
 first=lambda tag:next(r for r in rows if r['tag']==tag)
 r=first('LIVE');reject('proxy_live_id',change(text,'LIVE',r['frame'],'human','1:1'),'True live human ID')
 r=first('SELECT_ID');reject('foreign_confirm_roster',change(text,'SELECT_ID',r['frame'],'roster',1),'selection check retains own true ID')
 r=next(r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before'])
 reject('foreign_damage_writer',change(text,'HEALTH',r['frame'],'pc','FFF00000'),'exact original writer')
 reject('negative_damage_health',change(text,'HEALTH',r['frame'],'after',-1),'collision never heals')
 r=first('WIN');reject('foreign_win_instruction',change(text,'WIN',r['frame'],'pc','FFF00000'),'winner-table call')
 reject('fabricated_zero_win_health',change(text,'WIN',r['frame'],'health','0,0'),'Native winning health')
 r=first('ROM');reject('changed_native_schedule',change(text,'ROM',r['frame'],'ids',r['ids'].replace('18','1',1)),'Original-derived true-ID schedule')
 r=first('SPECIAL');reject('foreign_special_actor',change(text,'SPECIAL',r['frame'],'a8','01000000'),'special instruction fetch')
 r=first('ENDING_COMPLETED')
 reject('missing_ending_pages',change(text,'ENDING_COMPLETED',r['frame'],'pictures','0,0'),'Both own native picture/story pages')
 reject('retained_ending_roster',change(text,'ENDING_COMPLETED',r['frame'],'roster','17,1'),'return to attract roster')
 fields={r['frame']for r in rows if r['tag']=='BOSS_FIELD'}
 attack=next(r for r in rows if r['tag']=='INPUT'and r['frame']in fields and r['button']=='High_Punch')
 line=next(s for s in text.splitlines()if s.startswith(f"MK2_NAT_CAMPAIGN_INPUT frame={attack['frame']} ")and 'button=High_Punch 'in s)
 reject('missing_actual_boss_attack',text.replace(line+'\n','',1),'independently replayed native state')
 guest=current.expected();proof=json.loads((capture.OUT/'guest_memory_proof.json').read_text())
 for key,value in [('sha256','0'*64),('bytes',1048575),('everyActualByteComparedInRAM',False),
  ('captureSourceSHA256','0'*64),('transportSourceSHA256','0'*64),('guestDumpFilesWritten',1)]:
  bad=dict(proof);bad[key]=value
  try:ram_guest(capture.OUT,{},guest,text,bad)
  except ValueError as error:faults.append(dict(kind='actual_guest_'+key,rejectedBy=str(error)))
  else:raise ValueError('Actual full guest proof fault admitted '+key)
 header=next(s for s in text.splitlines()if s.startswith('MK2_CAMPAIGN_GUEST_RAM_DIGEST '))
 reject('missing_actual_guest_digest',text.replace(header+'\n','',1),'Exactly one actual digest')
 need(native(capture.OUT)==positive,'Entire original positive restored after all actual faults')
 completed=[r for r in rows if r['tag']=='ENDING_COMPLETED'];finals=[r for r in rows if r['tag']=='RESULT']
 need(len(completed)==len(finals)==1 and finals[0]['frame']==completed[0]['frame']+300,
  'All300ordinary native return-to-attract fields, not host deadline')
 need('MK2_CAMPAIGN_HOST_DEADLINE 'not in text,'Natural completion, no deadline credited')
 cache=[s for s in text.splitlines()if s.startswith('MK2_MILEENA_CAMPAIGN_RESULT ')]
 need(len(cache)==1 and 'global_cache_stores=0'in cache[0]and 'MK2_MILEENA_CAMPAIGN_OVERRUN 'not in text,
  'No original cache global stores through actual terminal')
 pins=dict(positive['inputHashes'])
 for p in[Path(__file__).resolve(),*capture.OUT.rglob('*')]:
  if p.is_file():pins[str(p.resolve())]=sha(p)
 for module in tuple(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p and Path(p).suffix=='.py'and Path(p).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(p).resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All current source and actual native evidence retained')
 raw=gzip.open(capture.OUT/'run.log.gz','rb').read()
 return dict(passed=True,case=positive,inputHashes=pins,actualNativeAndRAMProofFaultsRejected=faults,
  actualNaturalCurrentKanoP1BossesOwnEndingAttractAccepted=True,actualAttractFollowThroughFields=300,
  completeUncompressedLogBytes=len(raw),completeUncompressedLogSHA256=hashlib.sha256(raw).hexdigest().upper(),
  actualNativeCacheGlobalStores=0,fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable terminal result');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)

