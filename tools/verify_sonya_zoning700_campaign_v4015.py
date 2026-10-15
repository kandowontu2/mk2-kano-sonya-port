"""Qualify actual3836 zoning Start700 P2 with the whole campaign verifier.

Only compiled-build provenance and six PNG/one initialized guest sink adapt.
All actual native schedule/ID/morph/health/KO/paid-continue/ending checks and
independent boss physical-input replay remain. A loss or time limit cannot
prove a campaign clear. Raster digests do not prove ending-art fidelity.
"""
import argparse,hashlib,inspect,json,re,sys,subprocess,traceback
from pathlib import Path
import run_sonya_zoning700_campaign_v4008 as capture
import verify_native_mileena_victim_data_v3819 as data
import verify_current_campaign_shao_knife_observer_v3526 as knife
import verify_current_campaign_shao_ring_retreat_v3491 as ring

ROOT,need,sha,NAME=capture.ROOT,capture.need,capture.sha,capture.NAME
OUT=ROOT/'audit_v4016_sonya_zoning700_campaign_checked'

DEADLINE="""-- Only the host observation deadline changes. Exit before MAME's -str
-- fallback, which otherwise writes an automatic PNG (video.cpp). This does
-- not supply inputs, alter the game clock, health, roster, AI or a victory.
local limit=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_OBSERVER_LIMIT')))
assert(limit==5900,'Declared finite observation window only')
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=limit then
  print(string.format('MK2_CAMPAIGN_HOST_DEADLINE seconds=%.9f limit=%d assistance=none writes=0',
   manager.machine.time:as_double(),limit))
  manager.machine:exit()
 end
end)
"""

def transport_boundary():
    original=(ROOT/'mk2ks_guarded_campaign_ram_v3743.lua').read_text()
    before="""-- Original input-only campaign; change only the six PNG output sinks.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local path=assert(({kano='mk2ks_natural_campaign_shao_knife_retreat_v3510.lua',
 sonya='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'})[fighter])"""
    after="""-- Original physical campaign: change only six PNG sinks and one guest-file sink.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(fighter=='sonya','Actual unfinished Sonya player-two campaign only')
local path='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'"""
    need(original.count(before)==1,'Unique original fighter routing, no physical controller changes')
    expected=original.replace(before,after)
    added="""local guest_sink="local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
local start=assert(source:find(guest_sink,1,true))
assert(not source:find(guest_sink,start+#guest_sink,true),'Exactly one original initialized guest sink')
source=source:sub(1,start-1)..'_campaign_guest(raw)'..source:sub(start+#guest_sink)
"""
    expected=expected.replace("local adapted,count=source:gsub",added+"local adapted,count=source:gsub")
    guest_prefix="""local function _campaign_guest(raw)
 assert(#raw==1048576)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_GUEST_RAM frame=1 bytes=%d hex=%s',#raw,hex))
end
"""
    expected=expected.replace('local function _campaign_emit(name)',guest_prefix+'local function _campaign_emit(name)').replace('Exactly the six original PNG sinks, controls untouched','Exactly six original PNG sinks; physical inputs untouched').replace('::PNG_sink_only','::native_output_sinks_only')
    wrapper=(ROOT/'mk2ks_guarded_campaign_guest_ram_v4006.lua').read_text()
    need(wrapper==expected,'Complete wrapper equals original with only six RGB and one initialized guest sink adaptations')
    need((ROOT/capture.LUA).read_text()=="-- Original zoning physical controls; actual Start700 is supplied by the host.\ndofile('mk2ks_guarded_campaign_guest_ram_v4006.lua')\n"+DEADLINE.replace("-- Only the host observation deadline changes. Exit before MAME's -str\n-- fallback, which otherwise writes an automatic PNG (video.cpp). This does\n-- not supply inputs, alter the game clock, health, roster, AI or a victory.\n",'').replace('Declared finite observation window only','Declared finite host observation window only')+"dofile('mk2ks_mileena_campaign_trace_v3848.lua')\n",'Exact host deadline/read-only observer; no game-state assistance')
    driver=ring.source_boundary()
    need(driver.count('screen:snapshot(')==6 and driver.count("local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()") == 1 and driver.count('local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)')==1,'Actual original frame-one full guest read and every output sink accounted for')
    return driver

def ram_guest(folder,pins,wanted,text,proof_override=None):
    p=folder/'guest_memory_proof.json';proof=json.loads(p.read_text())if proof_override is None else proof_override
    meta=json.loads((folder/'result.json').read_text());digest=hashlib.sha256(wanted).hexdigest().upper()
    need(len(wanted)==1048576 and digest=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821','Independently reconstructed entire3836 initialized guest')
    need(proof==dict(schema=1,frame=1,bytes=1048576,sha256=digest,everyActualByteComparedInRAM=True,
      executableSHA256=meta['executable_sha256'],payloadSHA256=meta['payload_sha256'],captureSourceSHA256=sha(capture.__file__),
      transportSourceSHA256=sha(ROOT/'mk2ks_guarded_campaign_guest_ram_v4006.lua'),guestDumpFilesWritten=0),
      'Actual RAM whole-byte comparison proof, source/executable/payload bound')
    need(meta['ramGuestSHA256']==digest and meta['nativeGuestBytesVerifiedInRAM']==1048576 and meta['guestDumpFilesWritten']==0 and not list(folder.rglob('guest*.bin')),'Native RAM digest/size and no persisted guest copy')
    lines=text.splitlines();header=f'MK2_CAMPAIGN_GUEST_RAM_DIGEST frame=1 bytes=1048576 sha256={digest}'
    need([s for s in lines if s.startswith('MK2_CAMPAIGN_GUEST_RAM')]==[header]and not any('hex='in s for s in lines),'Exactly one actual digest, no raw guest/RGB hex persisted')
    at=lines.index(header)
    need(any(s.startswith('MK2_NAT_CAMPAIGN_BOOT frame=1 ')for s in lines[:at])and any(s.startswith('MK2_NAT_CAMPAIGN_MORPH_ROM frame=1 ')for s in lines[at+1:]),'Native first-frame read stays between original BOOT and original ROM instruction checks')
    pins[str(p)]=sha(p)
    return wanted

def adapt_guest_transport(source):
    before="    guest_path=folder/'guest_maincpu.bin'\n    guest=guest_path.read_bytes()"
    after="    guest=ram_guest_checked(folder,current_inputs,current_source.expected()[0],text,errors)"
    need(source.count(before)==1,'Unique original guest-file read')
    source=source.replace(before,after)
    before="    current_inputs[str(guest_path)]=hashlib.sha256(guest).hexdigest().upper()\n"
    need(source.count(before)==1,'Unique original ordinary guest-file pin')
    return source.replace(before,'')

def ram_guest_checked(folder,pins,wanted,text,errors):
    # Keep the original verifier's accumulating-error behavior for actual
    # text faults, without accepting a failed transport proof as success.
    try:return ram_guest(folder,pins,wanted,text)
    except ValueError as error:
        errors.append(str(error))
        return wanted

def make_native(expected):
    source=inspect.getsource(ring.make_verifier)
    before='    namespace=dict(vars(old));namespace.update'
    need(source.count(before)==1,'Keep whole original factory and complete independent boss-input algorithm')
    source=source.replace(before,'    source=adapt_guest_transport(source)\n'+before)
    namespace=dict(vars(ring));namespace['adapt_guest_transport']=adapt_guest_transport
    exec(compile(source,__file__+'::original_ring_factory_ram_guest_sink_only','exec'),namespace)
    native=namespace['make_verifier'](expected)
    native.__globals__.update(NAME=NAME,matched=matched,ram_guest_checked=ram_guest_checked)
    return native

def matched(folder,pins):
    meta=json.loads((folder/'result.json').read_text())
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text())
    frozen=json.loads((folder/'source_snapshot_paths.json').read_text())
    need(meta['candidate']==NAME and meta['exit_code']==0 and meta['human_slot']==2 and meta['cpu_slot']==1 and
      meta['assistance']=='none'and not meta['cheats_enabled']and meta['snapshot_schema']==2 and
      meta['raw_audio_files_written']==meta['new_builds_or_rom_copies']==meta['rawRasterFilesWritten']==0 and
      before==meta['input_hashes'],'Terminal actual P2 input-only3680 capture, no audio/raster/build copies')
    need(meta['executable_sha256']==build['executable_sha256']=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
      meta['payload_sha256']==build['payload_sha256']=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24'and
      all(before.get(str(Path(p).resolve()))==h for p,h in build['input_hashes'].items()),'Exact executable/payload/all compiled inputs')
    for p,h in before.items():
        need(sha(p)==h,'Executed input unchanged');pins[p]=h
        if Path(p).suffix in('.lua','.py','.ps1','.json'):
            dest=Path(frozen[p]).resolve()
            need(dest.is_relative_to(folder.resolve())and sha(dest)==h,'Exact frozen hierarchy source');pins[str(dest)]=h
        if Path(p).suffix=='.lua':
            need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(p).read_text()),'No guest-state/AI/health/CPU assistance')
    transport_boundary()
    need(meta['seconds']==6000 and meta['observer_limit_seconds']==5900 and meta['player']=='sonya'and meta['strategy']=='zoning'and meta['boot_frame']==700,
      'Original zoning inputs, genuine physical Start700, finite host observation only')
    original=ROOT/'mk2ks_guarded_campaign_ram_v3743.lua';pins[str(original)]=sha(original)
    need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav')),'No new raster/PCM files')

def change(text,tag,frame,key,new):
    pattern=rf'^(MK2_NAT_CAMPAIGN_{tag} frame={frame} [^\r\n]*?\b{key}=)([^\s]+)'
    result,count=re.subn(pattern,lambda m:m[1]+str(new),text,count=1,flags=re.M)
    need(count==1 and result!=text,'Non-vacuous actual-row corruption')
    return result

def verify(fighter):
    policy=knife if fighter=='kano'else ring
    need(fighter=='sonya','This is the unfinished actual Sonya P2 context only')
    folder=ROOT/f'audit_v4009_{fighter}_zoning700_p2_campaign'
    need(folder.is_dir()and(folder/'result.json').is_file(),'Existing terminal actual capture required')
    prior_expected=data.old.expected_current()
    payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=data.check(prior_expected[2],(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,prior_expected[0],json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    expected=(guest,prior_expected[1],payload,prior_expected[3],prior_expected[4])
    native=make_native(expected)
    # Preserve the generated whole3515/3491 algorithm and its declared
    # stage16 input replay; replace only its matched-build provenance handler.
    native.__globals__.update(NAME=NAME,matched=matched)
    positive=native(folder)
    need(positive['passed'],'Whole original actual P2 campaign gate: '+repr(positive['errors']))
    text=(folder/'run.log').read_text();rows=knife.old.parse(text,2,fighter)
    guest_faults=[]
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    for key,value in(('sha256','0'*64),('bytes',1048575),('everyActualByteComparedInRAM',False),('captureSourceSHA256','0'*64),('transportSourceSHA256','0'*64),('guestDumpFilesWritten',1)):
        bad=dict(proof);bad[key]=value
        try:ram_guest(folder,{},guest,text,proof_override=bad)
        except ValueError as error:guest_faults.append(dict(key=key,rejectedBy=str(error)))
        else:raise ValueError('False RAM guest proof accepted '+key)
        need(ram_guest(folder,{},guest,text)==guest,'Exact positive guest proof restored')
    header=next(s for s in text.splitlines()if s.startswith('MK2_CAMPAIGN_GUEST_RAM_DIGEST '))
    for label,damaged in(('missing_guest_digest',text.replace(header+'\n','',1)),('wrong_guest_digest',text.replace(header,header.replace(proof['sha256'],'0'*64),1))):
        result=native(folder,text_override=damaged)
        need(not result['passed']and any('Exactly one actual digest'in s for s in result['errors']),'Actual full algorithm rejects wrong guest digest '+label)
        need(native(folder)==positive,'Positive campaign restored after RAM digest fault')
        guest_faults.append(dict(key=label,rejectedBy='Exactly one actual digest'))
    # Different physical strategy: zoning chronology is not a valid oracle.
    # Keep the whole independent campaign/special/damage/ending algorithm.
    eaten=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_MILEENA_CAMPAIGN_EATEN_TASK ')]
    removed=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_MILEENA_CAMPAIGN_DISAPPEAR ')]
    cache_result=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_MILEENA_CAMPAIGN_RESULT ')]
    need(len(eaten)==len(removed)and len(cache_result)==1 and cache_result[0]['global_cache_stores']=='0'and
         not any(line.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')for line in text.splitlines()),'Every actual swallowing sequence retired and no global cache stores through full terminal')
    for first,last in zip(eaten,removed):
        need(first['id']==last['id']=='18'and first['a8']==last['a8']==last['a0']and first['a13']==last['a13']and
             first['pc']=='FF9E7D80'and last['pc']=='FF838F70'and last['a9']=='FFD61620'and int(last['frame'])-int(first['frame'])==56,'Original true Sonya victim task, consumed own stream and actual native removal')
    deadline=re.findall(r'^MK2_CAMPAIGN_HOST_DEADLINE seconds=([\d.]+) limit=(\d+) assistance=none writes=0$',text,re.M)
    if deadline:
        need(len(deadline)==1 and deadline[0][1]=='5900'and 5900<=float(deadline[0][0])<5900.03,
          'Exactly one actual finite host exit, never an injected game victory')
    else:
        need(positive['unassisted_clear_proven'],'Without host deadline the original own ending must have completed and exited naturally')
    trials=[]
    def reject(label,damaged,error):
        result=native(folder,text_override=damaged)
        need(not result['passed']and any(error in message for message in result['errors']),
          'Specific same-path actual fault rejection '+label)
        restored=native(folder)
        need(restored==positive,'Exact positive restored after every actual fault')
        trials.append(label)
    first=lambda tag:next(r for r in rows if r['tag']==tag)
    r=first('LIVE');reject('proxy_Liu_live_ID',change(text,'LIVE',r['frame'],'human','0:0'),'True live human ID')
    r=first('SELECT_ID');reject('wrong_confirmed_roster',change(text,'SELECT_ID',r['frame'],'roster',0),'selection check retains own true ID')
    r=next(r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before'])
    reject('unoriginal_health_writer',change(text,'HEALTH',r['frame'],'pc','FFF00000'),'exact original writer')
    reject('negative_collision_health',change(text,'HEALTH',r['frame'],'after',-1),'collision never heals')
    r=first('WIN');reject('wrong_winner_table_PC',change(text,'WIN',r['frame'],'pc','FFF00000'),'winner-table call')
    reject('fabricated_win_zero_health',change(text,'WIN',r['frame'],'health','0,0'),'Native winning health')
    r=first('ROM');reject('changed_native_schedule',change(text,'ROM',r['frame'],'ids',r['ids'].replace('18','0',1)),'Original-derived true-ID schedule')
    r=first('SPECIAL');reject('wrong_move_actor_register',change(text,'SPECIAL',r['frame'],'a8','01000000'),'special instruction fetch')
    reject('wrong_native_move_entry_PC',change(text,'SPECIAL',r['frame'],'pc','FFF00000'),'special instruction fetch')
    fields={r['frame']for r in rows if r['tag']=='BOSS_FIELD'}
    attack=next((r for r in rows if r['tag']=='INPUT'and r['frame']in fields and r['button']in('High_Punch','Low_Punch')),None)
    if attack:
        original=next(line for line in text.splitlines()if line.startswith(f"MK2_NAT_CAMPAIGN_INPUT frame={attack['frame']} ")and f"button={attack['button']} "in line)
        reject('missing_actual_boss_attack_input',text.replace(original+'\n','',1),'independently replayed native state')
    if any(r['tag']=='ENDING_COMPLETED'for r in rows):
        r=first('ENDING_COMPLETED')
        reject('missing_own_ending_picture_page',change(text,'ENDING_COMPLETED',r['frame'],'pictures','0,0'),'Both own native picture/story pages')
        reject('wrong_ending_return_roster',change(text,'ENDING_COMPLETED',r['frame'],'roster',f'0,{17 if fighter=="kano"else 18}'),'return to attract roster')
    pins=positive['inputHashes']
    for file in folder.rglob('*'):
        if file.is_file():pins[str(file)]=sha(file)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py'and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    need(all(sha(p)==h for p,h in pins.items()),'All source/proof bytes unchanged')
    positive.update(actual3836P2WholeCampaignAlgorithmRetained=True,actualRowCounterexamplesRejected=trials,
      captureMemoryOnlyResourceContractAccepted=True,actualAutomaticRasterFilesWritten=0,
      actualNativeInitializedGuestBytesComparedInRAM=1048576,actualGuestDumpFilesWritten=0,actualRAMGuestFaultsRejected=guest_faults,
      actualFiniteHostDeadlineReached=bool(deadline),
      actualNativeSwallowingSequences=len(eaten),globalCacheOverruns=0,differentPhysicalStrategyNotComparedToZoningChronology=True,
      endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False)
    return positive

def run(fighters):
    cases=[verify(fighter)for fighter in fighters]
    return dict(passed=True,cases=cases,currentBothP2NaturalClearAccepted=set(fighters)=={'kano','sonya'}and all(c['unassisted_clear_proven']for c in cases),
      endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),action='append')
    args=parser.parse_args()
    try:report=run(args.fighter or('sonya',))
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes');(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    summary={k:v for k,v in report.items()if k!='cases'}
    summary['cases']=[{k:v for k,v in c.items()if k not in('inputHashes','uppercutAssignmentFrames')}for c in report.get('cases',[])]
    print(json.dumps(summary,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
