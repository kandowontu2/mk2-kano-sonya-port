"""Current native Jax head-clap earned-command, state and table qualification.

The entire original1036 earned-control/state/lookup algorithm is retained.
Legacy sparse PNG checks are not substituted for full scenes: the separate
4020 integer replay verifies every field, palette, CPU/DMA/shift and scanout.
Normal Dead Pool only; no all-finishers/audio/arena/ending acceptance.
"""
import copy,hashlib,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import run_jax_clap_native_scene_v4020 as capture
import verify_jax_clap_positions_v1036 as old
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4027_jax_clap_earned_checked'
CASES=tuple(f'audit_v4021_jax_clap_{f}_p{s}_native_scene_ram'for f in('kano','sonya')for s in(1,2))

def make_gate(guest):
    source=inspect.getsource(old.verify)
    boundary="        count=struct.unpack_from('<I',payload,0x160008)[0]"
    need(source.count(boundary)==1,'Unique end of original complete earned-state algorithm')
    source=source[:source.index(boundary)]
    need(source.count('heads.PAYLOAD')==2,'Two original payload provenance checks retained')
    source=source.replace('heads.PAYLOAD','PAYLOAD')
    changes={
      "name,side=result['player'],result['victim_slot']":"name,side=result['fighter'],result['side']",
      "result['killer']=='jax' and result['command']=='fff_lp_release' and result['target_gap']==64":"capture_source_boundary()",
      "result['cheats_enabled'] is False":"'-nocheat' in json.loads((directory/'process.json').read_text())['command']",
      "stops[0]['frame']=='5198'":"int(stops[0]['frame'])==start+750",
      "(directory/'guest_maincpu.bin').read_bytes()==guest":"ram_guest_bound(directory,text,guest)",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'One declared current provenance/RAM/host-deadline adaptation '+before);source=source.replace(before,after)
    source+="""        cases[case]=dict(victim=name,side=side,actualOrigin=start,nativeWrapAge=188,realCollisionDamage=322,nativeFullRounds=2,originalControlAndLookupAccepted=True)
        for filename in ('run.log','result.json','buffer_digests.json','visible_digests.json','continuous_scene_records.json','palette_checks.json'):
            pins[str(directory/filename)]=digest(directory/filename)
    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases,inputHashes=pins,fullPortAcceptance=False)
"""
    namespace=dict(vars(old));namespace.update(CANDIDATE=capture.NAME,CASES=CASES,PAYLOAD='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24',expected_guest=lambda:(guest,None),capture_source_boundary=capture_source_boundary,ram_guest_bound=ram_guest_bound)
    exec(compile(source,__file__+'::complete1036_earned_state_only_current_RAM','exec'),namespace)
    return namespace['verify']

def capture_source_boundary():
    text=Path(capture.__file__).read_text()
    need(text.count("MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='fff_lp_release',MK2KS_STOCK_GAP='64'")==1,'Exact physical Jax release-LP scenario')
    need("'-nocheat'"in text and "'-noautoframeskip','-frameskip','0'"in text and ':write_'not in capture.OBSERVER.read_text(),'Native physical execution; no guest/health/AI writes')
    observer=capture.OBSERVER.read_text()
    need("dofile('mk2ks_stock_extended_earned_ram_v3958.lua')"in observer and "exact('local action_entry=0xff8bdfe0','local action_entry=0xff8c7820')"in observer and 'a.id==11 and victim.id==identity' in observer,'Original1021 physical driver plus read-only actual Jax origin')
    return True

def ram_guest_bound(folder,text,guest):
    records=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_TOMB_RAM_BUFFER_CHECKED ')and 'file=guest_maincpu.bin 'in line]
    meta=json.loads((folder/'result.json').read_text());wanted=hashlib.sha256(guest).hexdigest().upper()
    return len(records)==1 and records[0]['bytes']=='1048576'and records[0]['sha256']==meta['ramGuestSHA256']==wanted and meta['rawRasterVRAMAudioROMCopiesWritten']==0 and not list(folder.rglob('guest*.bin'))

def source_contract(guest):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo,hi=(0xff8c7820-0xff800000)//8,(0xff8c8100-0xff800000)//8
    wanted=bytearray(original[lo:hi]);operand=(0xff8c7b50-0xff8c7820)//8
    need(struct.unpack_from('<I',wanted,operand)[0]==0xff8c7ff0,'Original Jax victim-position operand')
    struct.pack_into('<I',wanted,operand,0xfffdb000)
    need(guest[lo:hi]==wanted,'Entire original Jax head-clap task unchanged except true19-row position table')
    at=(0xff8c7ff0-0xff800000)//8
    need(guest[0xfb600:0xfb644]==original[at:at+68]and struct.unpack_from('<2I',guest,0xfb644)==(0x0005ffa0,0x0004ffa0),'All seventeen stock victim rows exact and correct own Kano/Sonya floor offsets')
    for side,base in((1,0xff878d90),(2,0xff878d30)):
        for offset in(0,16,32):
            # Native A11 cursor observed after its word load/postincrement.
            at=(base+offset-16-0xff800000)//8
            need(guest[at:at+2]==original[at:at+2],'Original slot-specific direction history word unchanged')
    return True

def run():
    need(not OUT.exists(),'Fresh immutable state report')
    report=json.loads((capture.OUT/'report.json').read_text());need(report['passed']and len(report['cases'])==4,'All four actual continuous native scene captures required')
    base,_,payload,_,_=capture.data.old.expected_current()
    guest,_=capture.data.check(payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    capture_source_boundary();source_contract(guest);gate=make_gate(guest)
    texts={case:(ROOT/case/'run.log').read_text()for case in CASES};positive=gate(texts=texts)
    need(positive['passed'],'Whole original Jax earned-state grammar '+repr(positive['errors']))
    faults=[]
    def fault(case,tag,key,new):
        source=texts[case];line=next(s for s in source.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_'+tag+' '))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+str(new),line,count=1);need(n==1 and changed!=line,'Actual non-vacuous state fault')
        damaged=dict(texts);damaged[case]=source.replace(line,changed,1)
        negative=gate(texts=damaged);need(not negative['passed'],'Actual earned-state fault rejected '+key)
        need(gate(texts=texts)==positive,'Exact original positive restored after actual state fault')
        faults.append(dict(context=case,tag=tag,key=key,rejectedBy=negative['errors']))
    for case in CASES:
        for tag,key,new in(('FIRST_LIVE','ids','11,1'),('ACTION','address','FF8C6040'),('ACTION','damage','321'),('WRAP','age','187'),('WRAP','pc','FFF00000'),('RESULT','wins','3'),('APPROACH','gap','100'),('HEALTH','pc','FFF00000')):fault(case,tag,key,new)
    pins=positive['inputHashes'];pins.update({str(Path(__file__).resolve()):sha(__file__),str(capture.OUT/'report.json'):sha(capture.OUT/'report.json'),str(capture.OBSERVER):sha(capture.OBSERVER),str(Path(capture.__file__).resolve()):sha(capture.__file__)})
    for p,h in pins.items():need(sha(p)==h,'All actual capture/state bytes unchanged')
    return dict(passed=True,candidate=capture.NAME,actualContexts=4,originalCompleteEarnedStateAlgorithmRetained=True,actualRowCounterexamplesRejected=faults,actualStateFaultsRejected=len(faults),sourceBoundOriginalJaxTaskAccepted=True,cases=positive['cases'],inputHashes=pins,scope=__doc__,allStockFatalitiesAccepted=False,allArenasAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualRowCounterexamplesRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
