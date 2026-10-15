"""Same native display, complete source-defined initialized HUD/projectile GFX.

Keep the original ROM-only graphics mismatch. Native init copies independent
payload headers into zero graphics storage and generates stock-ramp name art.
Use the original full name algorithm and exact compiled copy ranges; never
seed expected graphics from native target buffers or waive mismatched streams.
"""
import inspect
import json
import struct
import traceback
from pathlib import Path
from types import SimpleNamespace
import qualify_native_selector_walkin_knife_display_ram as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_walkin_knife_display_initialized_checked'
FAILURE=original.OUT/'failure.json'
NAME_MODEL=ROOT/'tools/launch_ground_native_names.py'


def runtime_graphics(state,pins):
    name_source=NAME_MODEL.read_text()
    start=name_source.index('def reconstruct(pins):')
    stop=name_source.index('\nsource=base.source',start)
    source=name_source[start:stop]
    before=' gfx=base.reconstruct(pins)'
    need(source.count(before)==1,'Reuse the whole original native HUD reconstruction, only current ROM-lane source binding')
    source=source.replace(before,' gfx=bytearray(compiledgfx)',1)
    name=original.capture.previous.original.previous.choices.current.startup.NAME
    scope=dict(ROOT=ROOT,need=need,sha=sha,struct=struct,compiledgfx=state['gfx32'],
               base=SimpleNamespace(current=SimpleNamespace(NAME=name)))
    exec(compile(source,str(NAME_MODEL)+'::whole_original_names_current_compiled_graphics','exec'),scope)
    image=scope['reconstruct'](pins)
    path=ROOT/name/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    code=path.read_text();payload=state['payload']
    copies=[]
    for header,magic,source_at,destination in (
        (0x1c0000,b'KFX1',0x1c4000,0x1e04000),
        (0x1c1000,b'KPI1',0x1e6000,0x1e50000),
        (0x1c2000,b'KPJ1',0x1f4000,0x1e60000),
        (0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        need(payload[header:header+4]==magic,'Exact current native graphics header '+magic.decode())
        start,count,dest=struct.unpack_from('<III',payload,header+4)
        need(start==source_at and dest==destination and 0<count and start+count<=len(payload) and
             dest+count<=len(image) and not any(image[dest:dest+count]),
             'Source-defined bounded native graphics copy into independently empty storage')
        image[dest:dest+count]=payload[start:start+count]
        copies.append(dict(magic=magic.decode(),source=start,bytes=count,destination=dest))
    for fragment in ('std::copy_n(donor + effect_source, effect_bytes, gfx + effect_destination);',
                     'std::copy_n(donor + 0x1e6000, impact_bytes, gfx + 0x1e50000);',
                     'std::copy_n(donor + 0x1f4000, 6356, gfx + 0x1e60000);'):
        need(fragment in code,'Exact actual compiled runtime projectile graphics copy '+fragment)
    need('"KBL1"' in code and '0x1e08000' in code,'Compiled separate original native Blade graphics allocation')
    for p in (NAME_MODEL,path):
        key=str(p.resolve());digest=sha(p);need(key not in pins or pins[key]==digest,'Original name/current init source unchanged');pins[key]=digest
    return image


def execute(state):
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error']==
         "ValueError('Every actually used packed graphics byte equals independent current ROM/payload model')",
         'Actual ROM-only GFX oracle rejection retained; no new game or target fitting')
    source=inspect.getsource(original.execute)
    source=original.once(source,'    display=capture.DISPLAY',
        '    display=capture.DISPLAY\n    image=runtime_graphics(state,pins)')
    source=original.once(source,"raw==state['gfx32'][first:first+len(raw)]","raw==image[first:first+len(raw)]")
    source=original.once(source,'sources=(Path(__file__).resolve(),',
        'sources=(Path(original_source).resolve(),failure_path.resolve(),Path(__file__).resolve(),')
    scope=dict(vars(original),OUT=OUT,__file__=__file__,runtime_graphics=runtime_graphics,
               original_source=original.__file__,failure_path=FAILURE)
    exec(compile(source,__file__+'::whole_original_renderer_complete_native_graphics_init','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual initialized-renderer rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
