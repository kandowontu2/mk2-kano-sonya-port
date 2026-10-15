"""Entire original815/811 ground and native shadow model over current RAM.

Only file-backed inputs are replaced by exact actual same-run buffers.
Every native source stream additionally matches reconstructed compiled ROMs.
"""
import inspect
import inspect_current_ground_shadow_v811 as original
import verify_current_ui_ground_v816 as contract
import verify_move_phase_shadow_v5089 as graphics
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def reconstruct(pins):
 source=inspect.getsource(graphics.reconstruct)
 scope=dict(vars(graphics),native=current)
 exec(compile(source,__file__+'::whole_original_compiled_ROM_lane_reconstruction','exec'),scope)
 return scope['reconstruct'](pins)

source=inspect.getsource(original.inspect)
changes=[
 ('def inspect(folder):','def inspect(carrier):'),
 ("    folder=Path(folder)\n    log=(folder/'run.log').read_text(encoding='utf-8-sig')","    log=carrier['text']"),
 ("    buffers={r['key']:r for r in rows(log,'GFX')}","    buffers=carrier['gfx']"),
 ("        image=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))","        image=carrier['images'][snap['file']]"),
 ("        words=np.fromfile(folder/snap['vram_file'],dtype='<u2').reshape(512,512)","        words=np.frombuffer(carrier['raw'][snap['vram_file']],dtype='<u2').reshape(512,512)"),
 ("(folder/snap['palette_file']).read_bytes()","carrier['raw'][snap['palette_file']]"),
 ("np.fromfile(folder/snap['palette_file'],dtype='<u4')","np.frombuffer(carrier['raw'][snap['palette_file']],dtype='<u4')"),
 ("np.fromfile(folder/pre[frame-1]['file'],dtype='<u2')","np.frombuffer(carrier['raw'][pre[frame-1]['file']],dtype='<u2')"),
]
for before,after in changes:
 need(source.count(before)==1,'Only actual RAM source binding changed '+before[:75]);source=source.replace(before,after,1)
scope=dict(vars(original));exec(compile(source,__file__+'::entire_original_mobility_raster_shadow_contract_RAM','exec'),scope)
inspect_ground=scope['inspect']

def check(carrier):
 value=inspect_ground(carrier);contract.check_ground(value,carrier['fighter'],carrier['side'])
 return value
