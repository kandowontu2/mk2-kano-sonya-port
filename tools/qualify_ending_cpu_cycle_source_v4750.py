"""Whole original source gates plus source-defined CPU-cycle timing.

The complete actual Kano clock/IO ledger is required as metadata evidence.
It never substitutes for the complete RAM-only source-timed VRAM/RGB replay
or original native bit faults. Physical controls and the guest are unchanged.
"""
import ast,copy,hashlib,inspect,json,re,subprocess,sys
from pathlib import Path
import qualify_ending_raster_clock_source_v4710 as previous
import ending_raster_cpu_cycle_model_v4740 as model
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4751_ending_cpu_cycle_source_checked'
OBSERVER='mk2ks_ending_raster_io_ram_v4719.lua'
LUA={'kano':'mk2ks_kano_ending_raster_io_campaign_ram_v4728.lua',
     'sonya':'mk2ks_sonya_ending_raster_io_campaign_ram_v4729.lua'}
TRANSITIVE_LUA=tuple(sorted(set(previous.TRANSITIVE_LUA+(OBSERVER,)+tuple(LUA.values()))))

def observer_source(adapter=None):
    adapter=(ROOT/OBSERVER).read_text()if adapter is None else adapter
    need(adapter==(ROOT/OBSERVER).read_text(),'Only exact new immutable explicit-register adapter')
    executed,ram=previous.observer_source()
    grammar=previous.previous.previous.previous
    addition=adapter.split('local addition=[=[\n',1)[1].split('\n]=]',1)[0]
    pattern=r'\bonce\(\s*('+grammar.TOKEN+r')\s*,\s*('+grammar.TOKEN+r')\s*\)'
    changes=[tuple(grammar.literal(t)for t in m.groups())for m in re.finditer(pattern,addition)]
    need(len(changes)==1,'One read-only I/O observation addition, whole prior observer retained')
    before,after=changes[0];need(executed.count(before)==1,'Exact original renderer anchor')
    executed=executed.replace(before,after,1)
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',executed),
         'Whole new observer strictly read-only, RAM-only, no register/data/control changes')
    for token in("[0xc0000080]='control'","[0xc00001b0]='tap'","[0xc00001e0]='dpyadr'",
                  "log('FLOOR_RASTER_IO'",'next_event(),at,register,p:read_u16(at),data,mask,cpu.PC.value'):
        need(token in executed,'Actual native pre-store source/clock/PC/data/before register witness '+token)
    need(executed.count("log('FLOOR_RASTER_IO'")==1 and 'FLOOR_RASTER_IO'in model.Model.OPERATIONS,
         'Exactly one real IO observer and explicit register operation admitted by full model')
    return executed,ram

scope=dict(vars(previous),__file__=__file__,OBSERVER=OBSERVER,LUA=LUA,model=model,observer_source=observer_source)
exec(compile(inspect.getsource(previous.source_boundary),__file__+'::whole4710_original_physical_boundary','exec'),scope)
source_boundary=scope['source_boundary'];renderer_window=previous.renderer_window

def actual_phase_control():
    path=ROOT/'audit_v4713_kano_p2_ending_raster_clock_ram/run.log';rows=[]
    # Read only closed real lines from the complete first observed field.
    # Do not pin an actively growing log or infer a stopped native process.
    with path.open()as stream:
        for line in stream:
            if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK frame=56296 '):
                need(line.endswith('\n'),'Actual complete native clock record');rows.append(line.rstrip())
                if 'reason=finish 'in line:break
    need(len(rows)==4,'Actual complete first-field four-clock prefix from existing native run')
    _,seed=model.parse(rows[0]);_,before=model.parse(rows[1]);_,disabled=model.parse(rows[2]);_,finished=model.parse(rows[3])
    need(seed['reason']=='begin'and seed['vcount']==273 and
         abs(seed['next_vblank']-seed['seconds']-seed['frame_period'])<1e-9 and
         before['vcount']==274 and before['dpyadr']!=seed['start']and
         disabled['control']==0x6810 and not disabled['control']&0x8000 and
         finished['vcount']==273 and finished['control']==0xf010,
         'Actual prior CPU273 notifier, future blank deadline, unexplained IO/control-change counterexample retained')
    clock=model.Scanline((13,17));clock.advance(None,seed)
    need(clock.completed==0 and not clock.finished,'Actual notifier metadata only; no fake VRAM or native pixel positive')
    faults=[]
    for key,value in(('sequence',2),('epoch',2),('vcount',272),('human_slot',1),('fighter','sonya'),
                      ('writes',1),('assistance','forced'),('next_vblank',seed['next_vblank']-seed['frame_period'])):
        bad=dict(seed);bad[key]=value;need(bad!=seed,'Real non-vacuous actual notifier metadata fault')
        try:model.Scanline((13,17)).advance(None,bad)
        except ValueError as error:faults.append(dict(kind=key,rejectedBy=str(error)))
        else:raise ValueError('Actual malformed notifier metadata admitted '+key)
        restored=model.Scanline((13,17));restored.advance(None,seed)
        need(restored.completed==0 and restored.state==clock.state,'Same actual metadata-only positive restored')
    return dict(actualNativeFirstFieldClocks=rows,actualSourceBoundNotifierPhaseAccepted=True,
                actualNotifierMetadataFaultsRejected=faults,newNativeExplicitDisplayIOWitnessesAccepted=False,
                nativePixelPositivesFabricated=False,fullEndingRendererVideoAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable CPU-cycle source preflight')
    inherited=ROOT/'audit_v4732_ending_raster_io_blackpen_source_checked/report.json'
    inherited_proof=json.loads(inherited.read_text())
    timing=ROOT/'audit_v4743_actual_cpu_cycle_raster_boundary_checked/report.json'
    timing_proof=json.loads(timing.read_text())
    ledger=ROOT/'audit_v4749_kano_complete_cpu_cycle_ending_terminal_ledger_checked/report.json'
    ledger_proof=json.loads(ledger.read_text())
    need(inherited_proof['passed']and timing_proof['passed']and ledger_proof['passed']and
         timing_proof['actualFieldsMetadataAccepted']==14 and
         ledger_proof['completeActualMetadataFields']==3040 and
         len(ledger_proof['actualMetadataFaultsRejected'])==27 and len(ledger_proof['actualTerminalFaultsRejected'])==8 and
         not ledger_proof['fullEndingVRAMRGBPixelsAccepted'],
         'Original entire IO/source proof, actual CPU timing counterexample and complete actual metadata ledger, not fabricated pixels')
    for proof in(inherited_proof,timing_proof,ledger_proof):
        need(all(sha(p)==h for p,h in proof['inputHashes'].items()),'Every frozen original and actual native timing/source byte unchanged')
    old_model=(ROOT/'tools/ending_raster_io_model_v4720.py').read_text()
    new_model=Path(model.__file__).read_text()
    body=lambda value:value.split('"""',2)[2]
    before="phase>=self.phase and first-1e-9<=row['seconds']<first+row['scan_period']+1e-9"
    after="phase>=self.phase and first-CPU_CYCLE_SECONDS-1e-9<=row['seconds']<first+row['scan_period']+1e-9"
    need(old_model.count(before)==1 and body(new_model)==body(old_model).replace('IO_KEYS=','CPU_CYCLE_SECONDS=8/50000000\nIO_KEYS=',1).replace(before,after,1),
         'Complete original single-base VRAM/RGB/IO model unchanged except actual source-defined early CPU cycle')
    ops=(ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx').read_text()
    table=(ROOT/'mame-mkp/src/devices/cpu/tms34010/34010tbl.hxx').read_text()
    core=(ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp').read_text()
    for token in('WFIELD##F(PARAM_LONG(),R##REG(DSTREG(op)))','move0_ra_a','move0_ra_b','move1_ra_a','move1_ra_b'):
        need(token in ops,'Actual native absolute destination/source-register handler '+token)
    for block,field in(('0500','0'),('0700','1')):
        section=table.split('// 0x'+block,1)[1].split('// 0x',1)[0]
        handlers=re.findall(r'&tms34010_device::(\w+)',section)
        need(len(handlers)==16 and handlers[8:10]==['move'+field+'_ra_a','move'+field+'_ra_b'],
             'Actual opcode0580/0780 absolute register store dispatch table, not arbitrary unchanged ROM')
    need('(this->*s_opcode_table[op >> 4])(op);'in core and 'm_pc += 4 << 3;'in core and
         '#define DSTREG(O)       ((O) & 0x0f)'in core,
         'Original opcode index,32bit absolute operand advance and source register bits')

    contexts=[source_boundary(f)for f in LUA];phase=actual_phase_control()
    old_path=ROOT/'audit_v4711_ending_raster_clock_source_checked/report.json';old=json.loads(old_path.read_text())
    need(old['passed']and all(sha(p)==h for p,h in old['inputHashes'].items()),'All whole original source/controls/transport/faults unchanged')
    cpu=(ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp').read_text()
    screen=(ROOT/'mame-mkp/src/emu/screen.cpp').read_text()
    need('IOREG(offset) = data;'in cpu and 'IOREG(REG_DPYADR) = IOREG(REG_DPYSTRT);'in cpu and
         cpu.index('screen().update_partial(vcount);')<cpu.index('dpyadr = ((dpyadr & 0xfffc)'),
         'Original full CPU IO stores, native blank latch and partial-before-DUDATE source')
    begin=screen.index('TIMER_CALLBACK_MEMBER(screen_device::vblank_begin)')
    need(screen.index('m_vblank_start_time = machine().time();',begin)<screen.index('machine().video().frame_update();',begin)and
         'if (targetdelta <= curdelta + m_pixeltime / 2)'in screen and 'targetdelta += m_frame_period;'in screen,
         'Actual screen blank start resets before notifier; time_until_pos reports the next full field')
    palette=(ROOT/'mame-mkp/src/lib/util/palette.cpp').read_text();interface=(ROOT/'mame-mkp/src/emu/dipalette.cpp').read_text()
    need('m_adjusted_color[numcolors * numgroups + 0] = rgb_t::black();'in palette and
         'm_black_pen = m_palette->black_entry();'in interface and
         'pen_t blackpen = screen.palette().black_pen();'in cpu,
         'Original disabled IND16 callback uses permanently black palette pen, not a guessed RGB buffer')
    executed,ram=observer_source();adapter=(ROOT/OBSERVER).read_text();faults=[]
    for label,before,after in(('wrong_control_register','0xc0000080','0xc0000090'),('wrong_tap_register','0xc00001b0','0xc00001d0'),
      ('wrong_address_register','0xc00001e0','0xc0000090'),('missing_before_value','p:read_u16(at)','0'),
      ('missing_actual_clock','next_event(),at,register','event,at,register'),('fabricated_native_store','ensure_base()','ensure_base();p:write_u16(at,data)')):
        bad=adapter.replace(before,after,1);need(bad!=adapter,'Actual non-vacuous IO observer source fault')
        try:observer_source(bad)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual bad IO observation source admitted '+label)
        observer_source(adapter)
    import run_ending_cpu_cycle_campaign_ram_v4752 as capture
    for fighter in LUA:
        generated=capture.collector(fighter)
        need(generated.__globals__['model']is model and
             Path(generated.__globals__['source'].__file__).resolve()==Path(__file__).resolve()and
             'errors'in generated.__code__.co_varnames and 'scene_errors'in generated.__code__.co_varnames,
             'Actual whole generated collector bound to IO model/source with distinct error locals')
    need(model.Model.line.__globals__['parse']is model.parse and model.Model.__init__.__globals__['Scanline']is model.Scanline,
         'Actual full generated model uses complete clock/IO parser and actual state machine')
    files={Path(__file__).resolve(),Path(model.__file__).resolve(),Path(capture.__file__).resolve(),old_path,
           ROOT/'mame-mkp/src/emu/dipalette.cpp',ROOT/'mame-mkp/src/lib/util/palette.cpp'}
    files.update([inherited,timing,ledger,ROOT/'tools/qualify_ending_raster_io_source_v4721.py',
                  ROOT/'tools/qualify_ending_raster_io_blackpen_source_v4730.py',
                  ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx',
                  ROOT/'mame-mkp/src/devices/cpu/tms34010/34010tbl.hxx'])
    for proof in(inherited_proof,timing_proof,ledger_proof):files.update(map(Path,proof['inputHashes']))
    files.update(map(Path,old['inputHashes']));files.update(ROOT/p for p in TRANSITIVE_LUA)
    files.add(ROOT/'audit_v4713_kano_p2_ending_raster_clock_ram/input_hashes_before.json')
    for module in tuple(sys.modules.values()):
        p=getattr(module,'__file__',None)
        if p and Path(p).resolve().is_relative_to(ROOT/'tools'):files.add(Path(p).resolve())
    for path in files:
        if path.suffix=='.py':ast.parse(path.read_text(),filename=str(path))
    report=dict(passed=True,contexts=contexts,actualNotifierPhaseControl=phase,observerSourceFaultsRejected=faults,
      wholeOriginalNativeOneBasePipelineRetained=True,explicitDisplayIOObservationsAccepted=True,
      actualSourceDefinedCPUClockBoundaryQualified=True,wholeKanoMetadataLedgerAccepted=True,
      originalNativeIOStoreInstructionSemanticsQualified=True,all27MetadataAnd8TerminalFaultsRetained=True,
      fullEndingRendererVideoAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaFilesWritten=0,
      inputHashes={str(p.resolve()):sha(p)for p in files},scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','contexts')},indent=2),flush=True)

if __name__=='__main__':main()
