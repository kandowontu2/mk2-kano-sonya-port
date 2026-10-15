"""Before native boot: whole ending pipeline and actual-source raster clocks.

Source/schema checks only. No fabricated native clock/pixel positive, native
ending video acceptance, skipped actual field or replaced control policy.
"""
import ast,hashlib,inspect,json,re,subprocess,sys
from pathlib import Path
import qualify_ending_display_latch_source_v4647 as previous
import ending_raster_clock_model_v4709 as model
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4711_ending_raster_clock_source_checked'
OBSERVER='mk2ks_ending_raster_clock_ram_v4706.lua'
LUA={'kano':'mk2ks_kano_ending_raster_clock_campaign_ram_v4707.lua',
     'sonya':'mk2ks_sonya_ending_raster_clock_campaign_ram_v4708.lua'}
TRANSITIVE_LUA=tuple(sorted(set(previous.TRANSITIVE_LUA+(OBSERVER,)+tuple(LUA.values()))))

def observer_source(adapter=None):
    adapter=(ROOT/OBSERVER).read_text()if adapter is None else adapter
    need(adapter==(ROOT/OBSERVER).read_text(),'Only exact declared immutable raster-clock adapter')
    parent=previous.previous.previous
    executed,ram=parent.observer_source((ROOT/parent.OBSERVER).read_text())
    addition=adapter.split('local addition=[=[\n',1)[1].split('\n]=]',1)[0]
    pattern=r'\bonce\(\s*('+parent.TOKEN+r')\s*,\s*('+parent.TOKEN+r')\s*\)'
    changes=[tuple(parent.literal(t)for t in match.groups())for match in re.finditer(pattern,addition)]
    need(len(changes)==7,'Exactly seven whole-source hardware/clock/seed/finish adapters')
    need(changes[0][1].startswith(previous.previous.SCANOUT+'\n '),
         'Identical original4613 actual hardware scanout metadata retained')
    for before,after in changes:
        need(executed.count(before)==1,'Only actual unique full original observer boundary')
        executed=executed.replace(before,after,1)
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',executed),
         'Whole generated raster observer strictly read-only, RAM-only, no control/guest mutation')
    for token in("raster_clock('before');event=event+1", "raster_clock('field')", "raster_clock('begin')",
                  "raster_clock('finish')",'screen:frame_number()','screen:time_until_pos(last)',
                  'screen.scan_period','screen.frame_period','0xc00001d0','0xc00001e0','0xc0000070'):
        need(token in executed,'Actual source-bound clock hook/time/geometry '+token)
    for token in('FLOOR_CPU','FLOOR_DMA','FLOOR_GFX','FLOOR_PRE_FRAME','FLOOR_FLIP','FLOOR_LATCH',
                  'FLOOR_HELD','FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT','FLOOR_SNAP'):
        need(token in executed,'Every full original native raster gate retained')
    return executed,ram

def source_boundary(fighter):
    need(fighter in LUA,'Only original true P2 native contexts')
    parent=previous.previous.previous.kano if fighter=='kano'else previous.previous.previous.sonya
    physical=parent.source_boundary()
    expected="-- Existing accepted controller unchanged; only a read-only raster observer.\n"+f"dofile('{parent.LUA}')\ndofile('{OBSERVER}')\n"
    need((ROOT/LUA[fighter]).read_text()==expected,'Whole unchanged accepted controller plus exactly one read-only observer')
    executed,ram=observer_source()
    return dict(passed=True,fighter=fighter,physicalSlot=2,physicalInputsExactlyUnchanged=True,
                originalControllerProof=physical,executedObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),
                originalRAMTransportSHA256=hashlib.sha256(ram.encode()).hexdigest().upper(),
                continuousModelSHA256=model.MODEL_SOURCE_SHA256,nativeEndingVideoAccepted=False)

renderer_window=previous.renderer_window

def main():
    need(not OUT.exists(),'Fresh immutable before-boot raster source proof')
    contexts=[source_boundary(f)for f in LUA]
    old_path=ROOT/'audit_v4648_ending_display_actual_metadata_source_checked/report.json'
    old=json.loads(old_path.read_text());need(old['passed']and all(sha(p)==h for p,h in old['inputHashes'].items()),
         'All original whole controls/transport/metadata/hardware/source faults remain unchanged')
    cause_path=ROOT/'audit_v4703_actual_ending_clear_raster_cause_checked/report.json'
    cause=json.loads(cause_path.read_text());need(cause['passed']and cause['singleFieldSourceTimingCauseAccepted'],
         'Actual independently proven partial-update counterexample, never called complete video')
    need(all(sha(p)==h for p,h in cause['inputHashes'].items()),'Every actual cause/source byte unchanged')
    cpu=(ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp').read_text()
    need(cpu.index('screen().update_partial(vcount);')<cpu.index('dpyadr = ((dpyadr & 0xfffc) - (IOREG(REG_DPYCTL) & 0x03fc))')and
         'IOREG(REG_DPYADR) = IOREG(REG_DPYSTRT);'in cpu and 'if (vcount == vsblnk)'in cpu,
         'Original actual partial-update before decrement and native274display latch')
    lua=(ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp').read_text()
    for token in('screen_dev_type["frame_number"] = &screen_device::frame_number;',
                  'screen_dev_type["scan_period"] = sol::property','screen_dev_type["frame_period"] = sol::property',
                  'return sdev.time_until_pos(vpos).as_double();'):
        need(token in lua,'Actual native screen time/period/frame bindings, no guessed deadline')
    executed,ram=observer_source();faults=[];adapter=(ROOT/OBSERVER).read_text()
    for label,before,after in(('wrong_scanline','0xc00001d0','0xc00001b0'),('wrong_DP YADR'.replace(' ',''),'0xc00001e0','0xc0000090'),
      ('wrong_vertical_total','0xc0000070','0xc0000060'),('omitted_operation_clock',"raster_clock('before');event=event+1",'event=event+1'),
      ('omitted_finish_clock',"raster_clock('finish')",'-- removed finish clock'),
      ('same_beam_cycle_ambiguity','screen:frame_number()','0'),
      ('guessed_vblank_deadline','screen:time_until_pos(last)','0.00006325')):
        changed=adapter.replace(before,after,1);need(changed!=adapter,'Non-vacuous actual raster observer source fault')
        try:observer_source(changed)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Source raster counterexample accepted '+label)
        observer_source(adapter)
    import run_ending_raster_clock_campaign_ram_v4712 as capture
    for fighter in LUA:
        generated=capture.collector(fighter)
        need(generated.__globals__['model']is model and
             Path(generated.__globals__['source'].__file__).resolve()==Path(__file__).resolve()and
             'errors'in generated.__code__.co_varnames and 'scene_errors'in generated.__code__.co_varnames,
             'Actual generated whole collector uses exact clock model/source and distinct error locals')
    need(model.Model.line.__globals__['parse']is model.parse and model.Model.__init__.__globals__['Scanline']is model.Scanline and
         model.Model.replay_events.__globals__['Scanline']is model.Scanline,
         'Actual entire generated model uses strict clock parser and source-timed surface')
    files={Path(__file__).resolve(),Path(model.__file__).resolve(),Path(capture.__file__).resolve(),old_path,cause_path}
    files.update(map(Path,old['inputHashes']));files.update(ROOT/p for p in TRANSITIVE_LUA)
    for module in tuple(sys.modules.values()):
        p=getattr(module,'__file__',None)
        if p and Path(p).resolve().is_relative_to(ROOT/'tools'):files.add(Path(p).resolve())
    for path in files:
        if path.suffix=='.py':ast.parse(path.read_text(),filename=str(path))
    report=dict(passed=True,contexts=contexts,wholeOriginalNativePipelineRetained=True,
                nativeClockObservationsAccepted=False,fullEndingRendererVideoAccepted=False,fullPortAcceptance=False,
                observerSourceFaultsRejected=faults,inputHashes={str(p.resolve()):sha(p)for p in files},
                rawMediaFilesWritten=0,newBuilds=0,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','contexts')},indent=2),flush=True)

if __name__=='__main__':main()
