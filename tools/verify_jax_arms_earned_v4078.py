"""Current3836 earned Jax arm-rip command/state/prop-palette/table proof.

Entire1074 original earned-state and actual palette-router algorithm retained.
Legacy sparse PNG and native graphics dumps are not fabricated: separate4074
continuous native CPU/DMA/shift/scanout replay covers every actual field.
No all-arenas/alternate-costume/audio/ending or full-port acceptance.
"""
import hashlib,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import run_jax_arms_native_scene_v4074 as capture
import verify_native_arm_palette_v1074 as old
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4079_jax_arms_earned_checked'
CASES=tuple(f'audit_v4075_jax_arms_{f}_p{s}_native_scene_ram'for f in('kano','sonya')for s in(1,2))

def source_boundary():
    runner=Path(capture.__file__).read_text();wrapper=capture.OBSERVER.read_text()
    need(runner.count("MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='bbbb_lp',MK2KS_STOCK_GAP='96'")==1,'Actual original Jax BBBB LP physical scenario')
    need("'-nocheat'"in runner and "'-noautoframeskip','-frameskip','0'"in runner,'Actual native unassisted/no-skipped-fields execution')
    previous=(ROOT/'mk2ks_jax_clap_native_scene_ram_v4019.lua').read_text()
    # Compare the complete base observer transport, with four explicit names
    # and the native action entry changed. Extra1073 taps are read-only only.
    start=wrapper.index('-- Keep only the original three read-only prop-palette taps.')
    end=wrapper.index('local previous={}',start)
    taps=wrapper[start:end];rest=wrapper[:start]+wrapper[end:]
    for before,after in(('real Jax earned head-clap finisher.','real Jax earned arm-rip finisher.'),("local move='jax_clap'","local move='jax_arms'"),
                         ('local action_entry=0xff8c7820','local action_entry=0xff8be240'),('Jax head-clap does not use','Jax arm-rip does not use'),
                         ('MK2_JAX_CLAP_NATIVE_SCENE_WRAPPER','MK2_JAX_ARMS_NATIVE_SCENE_WRAPPER'),('Jax_clap_window_RAM_sinks','Jax_arms_window_RAM_sinks')):
        need(previous.count(before)==1,'Unique declared actual arm-rip observer adaptation');previous=previous.replace(before,after)
    need(rest==previous,'Complete original native observer/RAM transport retained')
    palette=(ROOT/'mk2ks_arm_palette_trace_v1073.lua').read_text();marker="local p=manager.machine.devices[':maincpu'].spaces.program"
    need(palette.count(marker)==1 and "palettesource=palettesource:sub(first)"in taps and "palettesource:find('dofile',1,true)"in taps,'Exact only-read-only suffix loaded, never controlled-alt/retired1046 branch')
    suffix=palette[palette.index(marker):]
    need(not re.search(r':write_|set_value|clear_value|\.value\s*=(?!=)|snapshot\(|io\.open|dofile',suffix),'Original1073 actual palette taps read-only; no guest/register/pixel writes')
    return True

def source_contract(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();allowed=set()
    for index,(table,operand)in enumerate(zip(old.TABLES,old.OPERANDS)):
        at=0xfba00+index*0x50;address=(operand-0xff800000)//8;source=(table-0xff800000)//8
        need(struct.unpack_from('<I',guest,address)[0]==0xff800000+at*8 and guest[at:at+68]==stock[source:source+68]and
             struct.unpack_from('<2I',guest,at+68)==old.ADDED[index],'Whole17 stock arm-rip rows exact and two actual own rows '+str(index))
        allowed.update(range(address,address+4))
    at=(0xff8bed50-0xff800000)//8
    need(guest[at:at+6]==struct.pack('<HI',0xc080,0xfffde000)and guest[0xfbc00:0xfbc60]==old.palette_router(),'Exact original native prop-palette extension and48-word register/stack-preserving router')
    allowed.update(range(at,at+6))
    for first,last in((0xff8be240,0xff8bf820),(0xff9a64e0,0xff9a6e50)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(all(guest[i]==stock[i]or i in allowed for i in range(lo,hi)),'Entire original Jax/body/detached-arm native tasks only declared own data/router operands differ')
    return True

def ram_guest(folder,text,guest):
    records=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_TOMB_RAM_BUFFER_CHECKED ')and 'file=guest_maincpu.bin 'in s]
    meta=json.loads((folder/'result.json').read_text());wanted=hashlib.sha256(guest).hexdigest().upper()
    return len(records)==1 and records[0]['bytes']=='1048576'and records[0]['sha256']==meta['ramGuestSHA256']==wanted and meta['rawRasterVRAMAudioROMCopiesWritten']==0 and not list(folder.rglob('guest*.bin'))

def make_gate(guest):
    source=inspect.getsource(old.verify)
    boundary="        need((directory/'native_arm_rip_gfx.bin').read_bytes()==graphics"
    need(source.count(boundary)==1,'Original complete earned-state/palette/table boundary');source=source[:source.index(boundary)]
    changes={
      'guest,graphics,assets=reconstruct()':'guest,graphics,assets=actual_guest,None,None',
      "name=result['player'];side=result['victim_slot']":"name=result['fighter'];side=result['side']",
      "result['executable_sha256']":"result['input_hashes'][str((ROOT/CANDIDATE/'mkport_candidate.exe').resolve())]",
      "result['payload_sha256']":"result['input_hashes'][str((ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').resolve())]",
      "not result['cheats_enabled'] and result['killer']=='jax' and result['command']=='bbbb_lp' and result['target_gap']==96":"source_boundary()and '-nocheat' in json.loads((directory/'process.json').read_text())['command']",
      "stops[0]['frame']=='5198'":"int(stops[0]['frame'])==start+750",
      "(directory/'guest_maincpu.bin').read_bytes()==guest":"ram_guest(directory,text,guest)",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'One declared actual current provenance/RAM/deadline adaptation');source=source.replace(before,after)
    source+="""        writers={'FF836700','FF825930'if side==1 else'FF825960','FF9DECE0'if side==1 else'FF9DED10','FF9DEF40'if side==1 else'FF9DEF70'}
        need(all(r['pc']in writers for r in items('HEALTH')),'All native health writes remain original '+case)
        need(len(items('WIN'))==2 and live[0]['own']==action['actor']and action['mode']=='2','Actual two original WIN reads and true Jax ownership '+case)
        cases[case]=dict(victim=name,side=side,origin=start,nativeWrapAge=147,realCollisionDamage=322,nativeRounds=2,actualPropPaletteConsumers=2,actualOwnedTableConsumers=6)
        for filename in ('run.log','result.json','buffer_digests.json','visible_digests.json','continuous_scene_records.json','palette_checks.json'):
            pins[str(directory/filename)]=digest(directory/filename)
    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases,inputHashes=pins,fullPortAcceptance=False)
"""
    namespace=dict(vars(old));namespace.update(CANDIDATE=capture.NAME,CASES=CASES,actual_guest=guest,source_boundary=source_boundary,ram_guest=ram_guest)
    exec(compile(source,__file__+'::complete_original1074_earned_normal_palette_state','exec'),namespace)
    return namespace['verify']

def run():
    need(not OUT.exists(),'Fresh immutable original earned-state proof')
    scene=json.loads((capture.OUT/'report.json').read_text());need(scene['passed']and len(scene['cases'])==4,'All four actual complete continuous native body/arm captures, no legacy PNG substitution')
    base,_,prior,_,_=capture.data.old.expected_current();payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=capture.data.check(prior,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    source_boundary();source_contract(guest);gate=make_gate(guest)
    texts={case:(ROOT/case/'run.log').read_text()for case in CASES};positive=gate(texts=texts);need(positive['passed'],'Complete original arm-rip state/table/prop palette '+repr(positive['errors']))
    faults=[]
    for case in CASES:
        trials=[('FIRST_LIVE','ids','11,1'),('ACTION','address','FF8C7820'),('ACTION','variant','1'),('ACTION','damage','321'),('WRAP','age','146'),
                ('WRAP','pc','FFF00000'),('RESULT','wins','3'),('APPROACH','gap','64'),('HEALTH','pc','FFF00000'),('TABLE_RETURN','value','00000000')]
        for tag,key,new in trials:
            line=next(s for s in texts[case].splitlines()if s.startswith('MK2_STOCK_HEAD_V921_'+tag+' '))
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(n==1 and changed!=line,'Non-vacuous actual original state fault')
            damaged=dict(texts);damaged[case]=texts[case].replace(line,changed,1)
            negative=gate(texts=damaged);need(not negative['passed'],'Actual original arm-rip state fault rejected '+key)
            need(gate(texts=texts)==positive,'Original positive restored after each native state fault');faults.append(dict(context=case,tag=tag,key=key,rejectedBy=negative['errors']))
        for key,new in(('preserved','0'),('victim','01000000'),('flags','0040')):
            line=next(s for s in texts[case].splitlines()if s.startswith('MK2_ARM_PALETTE_V1073_STOCK_FALLBACK '))
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(n==1 and changed!=line,'Non-vacuous actual native prop route fault')
            damaged=dict(texts);damaged[case]=texts[case].replace(line,changed,1)
            negative=gate(texts=damaged);need(not negative['passed'],'Actual native prop register/owner/normal palette fault rejected '+key)
            need(gate(texts=texts)==positive,'Original positive restored after each native prop fault');faults.append(dict(context=case,tag='STOCK_FALLBACK',key=key,rejectedBy=negative['errors']))
    pins=positive['inputHashes'];pins.update({str(Path(__file__).resolve()):sha(__file__),str(Path(old.__file__)):sha(old.__file__),str(capture.OBSERVER):sha(capture.OBSERVER),str(capture.OUT/'report.json'):sha(capture.OUT/'report.json'),str(Path(capture.__file__)):sha(capture.__file__)})
    for p,h in pins.items():need(sha(p)==h,'All actual execution/state/continuous scene bytes unchanged')
    return dict(passed=True,actualContexts=4,originalCompleteEarnedStateAndPropPaletteAlgorithmRetained=True,actualNativeStateAndPropFaultsRejected=len(faults),
        actualRowCounterexamplesRejected=faults,cases=positive['cases'],inputHashes=pins,scope=__doc__,allArenasAccepted=False,alternateCostumesAccepted=False,allFinisherAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable original-state report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualRowCounterexamplesRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
