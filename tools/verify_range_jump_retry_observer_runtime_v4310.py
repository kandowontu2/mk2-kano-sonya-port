"""Actual native slot/Main reuse and jump/kick/throw stores with repaired observers.

Native positive-health events only. All logged CPU throws must pair with their
actual owned victim clear; this does not certify events outside observer guards,
all arenas, all move pixels/audio, a tower clear or a complete port.
"""
import collections,hashlib,json,re,struct,subprocess,traceback
from pathlib import Path
import verify_shang_jump_retry_prefix_v4306 as physical
ROOT,need,sha=physical.ROOT,physical.need,physical.sha
FOLDER=physical.FOLDER
OUT=ROOT/'audit_v4311_range_jump_retry_observer_runtime_checked'
off=lambda a:(a-0xff800000)//8

def check(text,guest,native):
    for first,last in ((0xff842710,0xff8429f0),(0xff8b6e80,0xff8b6ff0),(0xff831300,0xff8313e0),(0xff871ed0,0xff871f50)):
        need(guest[off(first):off(last)]==native[off(first):off(last)],'Original native capture/throw/jump/air-kick dispatch code unchanged')
    for first,last,words in ((0xff831320,0xff831360,(0x09c0,0x0308,0xb00d,0x01f0)),
                             (0xff871f10,0xff871f50,(0x09c0,0x0200,0xb00d,0x01f0)),
                             (0xff8b6f60,0xff8b6fa0,(0x09c0,0x0507,0xb00d,0x01f0))):
        need(guest[off(first):off(last)]==struct.pack('<4H',*words),'Exact original native action setter and Main store signature')
    physical.replay(text);rows=physical.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='RANGE_FIELD'}
    bindings={};by_binding={};gaps=collections.Counter()
    for f in fields.values():
        for who,side in (('human',2),('cpu',1)):
            main=f[who+'_main'];bindings.setdefault(main,side)
            if bindings[main]!=side:gaps[who]+=1
        by_binding[f['frame']]=dict(bindings)
    reused_actions=[]
    actions=[r for r in rows if r['tag'] in ('RANGE_ACTION','RANGE_CPU_ACTION')]
    for r in actions:
        f=fields.get(r['frame'])
        if f is None:continue
        side=1 if r['tag']=='RANGE_CPU_ACTION' else 2
        if by_binding[r['frame']][r['main']]!=side:reused_actions.append(r)
    roles=collections.Counter(r['tag'] for r in reused_actions)
    need(roles['RANGE_ACTION']>0 and roles['RANGE_CPU_ACTION']>0,
         'Actual native stores on both roles after Main address opposite-side reuse, not model-only admission')
    throws=[r for r in actions if r['tag']=='RANGE_CPU_ACTION' and int(r['after'])==0x507]
    clears=[r for r in actions if r['tag']=='RANGE_ACTION' and r['pc']=='FF8428A0']
    pairs=[]
    for r in throws:
        f=fields.get(r['frame']);need(f is not None,'Logged native throw has actual same-field pair state')
        paired=[c for c in clears if c['frame']==r['frame'] and c['actor']==f['human_actor'] and c['main']==f['human_main']]
        need(len(paired)==1 and paired[0]['after']=='0','Every actual logged CPU throw has exactly one original owned victim clear')
        pairs.append(dict(actualNativeCpuThrow=r,actualOwnedVictimClear=paired[0],actualField=f,
          humanMainReusedFromCpu=by_binding[r['frame']][f['human_main']]!=2,
          cpuMainReusedFromHuman=by_binding[r['frame']][f['cpu_main']]!=1))
    need(pairs and any(p['humanMainReusedFromCpu'] or p['cpuMainReusedFromHuman'] for p in pairs),
         'Actual repaired paired throw/capture after native role reuse')
    jumps=[r for r in actions if r['tag']=='RANGE_ACTION' and int(r['after'])==0x308]
    kicks=[r for r in actions if r['tag']=='RANGE_ACTION' and int(r['after'])==0x200]
    return dict(actualCompleteNativeRangeFields=len(fields),actualOriginalHuman308JumpStores=len(jumps),
      actualOriginalHuman200AirKickStores=len(kicks),actualOriginalCpu507ThrowStores=len(throws),
      actualLoggedThrowCapturePairs=len(pairs),actualNativeOppositeRoleReuseFields=dict(gaps),
      actualNativeStoresAfterOppositeRoleReuse=dict(roles),actualNativeReuseStoreExamples=reused_actions[:12],
      actualNativeThrowCapturePairs=pairs,allLoggedPositiveHealthThrowsHaveOwnedVictimClear=True,
      nativeObserverRepairRuntimeProven=True,unobservedEventsOutsideGuardsAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable native observer repair proof')
    physical.capture.source.source_boundary()
    meta=json.loads((FOLDER/'result.json').read_text())
    need(meta['exit_code']==0 and meta['assistance']=='none' and not meta['cheats_enabled'],'Actual terminal unassisted run')
    text=(FOLDER/'run.log').read_text();guest=physical.capture.expected();native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['sha256']==hashlib.sha256(guest).hexdigest().upper() and
         proof['captureSourceSHA256']==sha(physical.capture.__file__) and proof['transportSourceSHA256']==sha(ROOT/physical.capture.LUA),
         'Every actual initialized guest byte and executed source bound in RAM')
    positive=check(text,guest,native);rows=physical.parse(text);faults=[]
    example=positive['actualNativeThrowCapturePairs'][0]['actualOwnedVictimClear']
    line=next(l for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION ') and
      dict(re.findall(r'(\w+)=([^\s]+)',l))=={k:str(v) for k,v in example.items() if k!='tag'})
    cases=[('missing_actual_victim_clear',text.replace(line+'\n','',1),guest)]
    for key,value in (('pc','FFF00000'),('owner','01000000'),('main','01000000'),('after','1')):
        damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Actual non-vacuous native observer fault')
        cases.append((key,text.replace(line,damaged,1),guest))
    for label,address in (('native_jump_opcode',0xff831320),('native_air_kick_opcode',0xff871f10),('native_throw_opcode',0xff8b6f60)):
        bad=bytearray(guest);bad[off(address)]^=1;cases.append((label,text,bytes(bad)))
    for label,damaged,binary in cases:
        try:check(damaged,binary,native)
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native observer fault accepted '+label)
        need(check(text,guest,native)==positive,'Exact actual positive native/source restored')
    pins=dict(meta['input_hashes'])
    for p in (Path(__file__),Path(physical.__file__),FOLDER/'run.log',FOLDER/'result.json',FOLDER/'guest_memory_proof.json',ROOT/'audit_v4277_mileena_observer_slot_reuse_source_checked/report.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All executed source and actual native evidence unchanged')
    return dict(passed=True,actualNativeObserverRepair=positive,actualNativeFaultsRejected=faults,inputHashes=pins,
      naturalTowerClearAccepted=False,completeMoveRasterAndAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable output')
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress report before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualNativeObserverRepair')},indent=2),flush=True)
    if report['passed']:
        print(json.dumps({k:v for k,v in report['actualNativeObserverRepair'].items() if k not in ('actualNativeThrowCapturePairs','actualNativeReuseStoreExamples')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
