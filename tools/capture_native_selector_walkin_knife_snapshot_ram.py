"""Additional genuinely absent current rendered snapshot; physical route intact.

Do not reinterpret or replace the original screen:pixels capture. Its entire
source/FIFO/VRAM passes remain accepted and RGB rejection remains failed.
Same complete capture bytecode with separate RAM/handle/transport bindings.
"""
import json
from pathlib import Path
from types import FunctionType
import capture_native_selector_walkin_knife_display_ram as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_native_selector_walkin_knife_snapshot_ram'
OUT=ROOT/'audit_native_selector_walkin_knife_snapshot_capture_checked'
LUA=ROOT/'mk2ks_native_selector_walkin_knife_snapshot_ram.lua'
KEY='original_sonya_walkin_kano_CPU_complete_Knife_current_snapshot'
PARENT=ROOT/'audit_native_selector_walkin_knife_vram_checked/report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={}
DISPLAY=dict(buffers={},headers={},gfx={},rgb={},rgbHeaders={})
scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
    RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
    DISPLAY=DISPLAY,SCOPE=None,__file__=__file__)
for name in ('normalize','prepare','execute','safe_execute'):
    function=getattr(original,name)
    need(not function.__closure__,'No hidden alternate recorder bindings')
    scope[name]=FunctionType(function.__code__,scope,name,function.__defaults__)
    need(scope[name].__code__ is function.__code__,'Whole original capture bytecode unchanged')


def run(state,preflight=False):
    receipt=json.loads(PARENT.read_text())
    need(receipt['passed'] and not receipt['displayedRGBPixelsAccepted'] and
         original.NATIVE_HANDLES[original.KEY]['process'].poll()==0,
         'Original terminal source/VRAM accepted; current snapshot is genuinely absent, never a timeout replay')
    old=original.LUA.read_text().replace('\r\n','\n')
    before='local rgb,w,h=screen:pixels();assert(w==400 and h==254 and #rgb==406400)'
    after='local video=manager.machine.video;local rgb=video:snapshot_pixels();local w,h=video:snapshot_size();assert(w==400 and h==254 and #rgb==406400)'
    need(old.count(before)==1 and LUA.read_text().replace('\r\n','\n')==
         '-- Source-correct current rendered snapshot target, no persistent media.\n'+old.replace(before,after),
         'Exactly one original passive pixel API binding changes; driver/FIFO/timing/VRAM/sound unchanged')
    engine=(ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp').read_text()
    video=(ROOT/'mame-mkp/src/emu/video.cpp').read_text()
    screen=(ROOT/'mame-mkp/src/emu/screen.cpp').read_text()
    need('video_type["snapshot_pixels"] =' in engine and 'vm.pixels(ptr);' in engine and
         'video_type["snapshot_size"] =' in engine and 'return std::make_tuple(width, height);' in engine,
         'Exact current pixel/dimension native API returns')
    need('void video_manager::pixels(u32 *buffer)\n{\n\tcreate_snapshot_bitmap(nullptr);' in video and
         'render_primitive_list &primlist = m_snap_target->get_primitives();' in video and
         'm_curtexture = m_curbitmap;\n\t\t\t\tm_curbitmap = 1 - m_curbitmap;' in screen,
         'Actual rendered snapshot primitives differ from post-swap m_curbitmap raw screen API')
    return scope['safe_execute'](state,preflight)
