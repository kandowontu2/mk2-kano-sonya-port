"""Whole original source gates plus actual notifier phase and explicit IO.

The old live/terminal native prefix is diagnostic metadata only. It provides
an actual ordinary-notifier timing positive, not fabricated VRAM/pixels or
complete-ending acceptance. New native display-register witnesses are pending.
"""
import ast,copy,hashlib,inspect,json,re,subprocess,sys
from pathlib import Path
import qualify_ending_raster_clock_source_v4710 as previous
import ending_raster_io_model_v4720 as model
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4722_ending_raster_io_source_checked'
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
    need(not OUT.exists(),'Fresh immutable actual IO/timing source preflight')
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
         'uint16_t blackpen = screen.palette().black_pen();'in cpu,
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
    import run_ending_raster_io_campaign_ram_v4723 as capture
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
    files.update(map(Path,old['inputHashes']));files.update(ROOT/p for p in TRANSITIVE_LUA)
    files.add(ROOT/'audit_v4713_kano_p2_ending_raster_clock_ram/input_hashes_before.json')
    for module in tuple(sys.modules.values()):
        p=getattr(module,'__file__',None)
        if p and Path(p).resolve().is_relative_to(ROOT/'tools'):files.add(Path(p).resolve())
    for path in files:
        if path.suffix=='.py':ast.parse(path.read_text(),filename=str(path))
    report=dict(passed=True,contexts=contexts,actualNotifierPhaseControl=phase,observerSourceFaultsRejected=faults,
      wholeOriginalNativeOneBasePipelineRetained=True,explicitDisplayIOObservationsAccepted=False,
      fullEndingRendererVideoAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaFilesWritten=0,
      inputHashes={str(p.resolve()):sha(p)for p in files},scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','contexts')},indent=2),flush=True)

if __name__=='__main__':main()
