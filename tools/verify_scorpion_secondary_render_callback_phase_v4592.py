"""Qualify actual557-field renderer window using its own callback phase.

Keep every original state/render/palette/pixel/source/negative gate. The old
collector's last gate compared renderer frame_done retirement to the next
MACHINE_NOTIFY_FRAME state observation. No replay target, missing field or
pixel mismatch is ignored; no actual capture or executed source is edited.
Not independent art aesthetics, all arenas/alternate palettes/audio/full port.
"""
import copy,json,re,subprocess
from pathlib import Path
import run_current_scorpion_secondary_state_v4549 as state
import scorpion_secondary_native_scene_model_v4581 as model
ROOT,need,sha=state.ROOT,state.need,state.sha
CASE=ROOT/'audit_v4584_scorpion_secondary_kano_p1_native_scene_ram'
OUT=ROOT/'audit_v4593_scorpion_secondary_render_callback_phase_checked'

def rows(text,prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith(prefix+' ')]

def contract(text,meta,records,visible):
    native=state.contract(text,'kano',1)
    need(meta['exit_code']==0 and meta['guestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
      meta['completeGuestBytesComparedInRAM']==1048576 and meta['nativeRGBFramesDigested']==62 and
      not meta['sceneErrors']and meta['rawMediaGuestROMOrBuildFilesWritten']==0 and not meta['cheatsEnabled']and meta['assistance']=='none',
      'All original actual native terminal/guest/controller/RAM transport and every pipeline field exact')
    retired=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_RETIRED');begin=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_BEGIN')
    terminal=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_RESULT');fields=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_STATE')
    need(len(retired)==len(begin)==len(terminal)==1,'One original actual renderer activation/retirement/terminal')
    first=int(begin[0]['frame']);end=int(retired[0]['frame'])
    need(first==native['actualNativeActivation'] and begin[0]['entry']=='FF8BBFE0' and begin[0]['id']=='10'and
      retired[0]['p1']==retired[0]['p2']=='00000000'and retired[0]['victim_health']=='0'and
      end+1==native['actualNativeRetirement'] and int(terminal[0]['retired'])==end,
      'Actual same instruction window; frame_done both-pointer retirement precedes next frame state sample by one callback phase')
    expected=list(range(first+1,end+31))
    need([r['frame']for r in records]==expected and [int(r['frame'])for r in fields]==list(range(first,end+31))and
      meta['exactNativeSceneFields']==len(records)==len(visible)==int(terminal[0]['snapshots']),
      'Every actual renderer field, exactly thirty later renderer fields after actual retirement; no gap or arbitrary trim')
    need(all(r['exactVRAMWords']==512*512 and r['exactRGBPixels']==400*254 and
      v['file']==f"display_{r['frame']}.png"and v['rgbSHA256']==r['rgbSHA256']for r,v in zip(records,visible)),
      'Every complete native VRAM and actual visible RGB comparison target remains exact')
    need(len(meta['nativeRasterFaults'])==2 and {r['kind']for r in meta['nativeRasterFaults']}=={'VRAM target bit','visible RGB bit'},
      'Original actual first-frame VRAM/RGB counterexamples retained')
    lookup={int(r['frame']):r for r in fields}
    need(lookup[end-1]['p1']!='00000000'and lookup[end-1]['p2']!='00000000'and
      all(r['p1']==r['p2']=='00000000'for r in fields if int(r['frame'])>=end),
      'Genuine renderer both-pointer transition and every later physical state remains cleared')
    lines=text.splitlines()
    def index(prefix,frame):
        found=[i for i,line in enumerate(lines)if line.startswith(prefix+' ')and f'frame={frame} 'in line]
        need(len(found)==1,'One actual ordered callback event');return found[0]
    need(index('MK2_SSECOND_FIELD',end)<index('MK2_NAT_CAMPAIGN_FLOOR_RETIRED',end)<
      index('MK2_NAT_CAMPAIGN_FLOOR_SNAP',end)<index('MK2_SSECOND_FIELD',end+1)<
      index('MK2_SSECOND_RETIRED',end+1)<index('MK2_NAT_CAMPAIGN_FLOOR_STATE',end+1),
      'Actual logged callback ordering, never guessing equivalent field numbers')
    queues=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_QUEUE');dispatch=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_QUEUE_DISPATCH')
    shadows=rows(text,'MK2_NAT_CAMPAIGN_SHADOW_COMPONENT')
    need(queues and dispatch and shadows and {r['id']for r in queues}=={'17','10'} and
      all(r['id']==r['roster']and r['owner']==r['actor']for r in queues),
      'Actual true Kano17/Scorpion10 owned body FIFO, palette dispatch and compressed floor-shadow components')
    original_actor={r['actor']for r in queues}
    need(not any(int(r['frame'])>=end and r['actor']in original_actor for r in
      rows(text,'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE')),'No retired physical body actor republished in native FIFO')
    return dict(native=native,rendererRetirement=end,stateRetirement=end+1,completeFields=len(records),
      postRetirementFields=sum(r['frame']>end for r in records),trueOwnedQueues=len(queues),
      sourcePaletteDispatches=len(dispatch),nativeCompressedShadowComponents=len(shadows))

def main():
    need(not OUT.exists(),'Fresh immutable phase qualification')
    text=(CASE/'run.log').read_text();meta=json.loads((CASE/'result.json').read_text())
    records=json.loads((CASE/'native_scene_records.json').read_text());visible=json.loads((CASE/'native_scene_visible_digests.json').read_text())
    pins=dict(meta['input_hashes'])
    def pin(path):pins[str(Path(path).resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Every actually executed source/game/input unchanged')
    positive=contract(text,meta,records,visible)
    # The host observer has no effect on any of the original62 scanouts.
    old=ROOT/'audit_v4552_scorpion_secondary_kano_p1_native_state_ram/native_rgb_digests.json'
    need(json.loads(old.read_text())==json.loads((CASE/'native_rgb_digests.json').read_text()),'All62 prior actual native controller RGB digests exactly unchanged')
    pin(old)
    guest=state.source.current.expected();payload=(ROOT/state.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    graphic_pins={};graphics=model.sources(payload,graphic_pins);pins.update(graphic_pins)
    gfx=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_GFX')
    need(gfx and all(model.digest(graphics[int(r['first']):int(r['first'])+int(r['bytes'])])==r['data_sha256']for r in gfx),
      'Every observed native source stream, including full independent original KTR1 upload, matches exactly')
    faults=[]
    mutations=[('missing_actual_render_field',lambda:(text,meta,records[:10]+records[11:],visible)),
      ('wrong_retirement_phase',lambda:(text.replace('MK2_NAT_CAMPAIGN_FLOOR_RETIRED frame=3691 ','MK2_NAT_CAMPAIGN_FLOOR_RETIRED frame=3692 ',1),meta,records,visible)),
      ('shortened_post_retirement_window',lambda:(text,meta,records[:-1],visible[:-1])),
      ('native_guest_mismatch',lambda:(text,dict(meta,guestSHA256='0'*64),records,visible)),
      ('hidden_actual_render_error',lambda:(text,dict(meta,sceneErrors=[{'error':'actual failure'}]),records,visible)),
      ('missing_native_pixel_counterexample',lambda:(text,dict(meta,nativeRasterFaults=meta['nativeRasterFaults'][:1]),records,visible))]
    for label,mutate in mutations:
        try:contract(*mutate())
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted real callback/field/meta fault: '+label)
        need(contract(text,meta,records,visible)==positive,'Entire unchanged actual positive restored after fault')
    # Bind the source explaining callback ordering, not just observed numbers.
    video=ROOT/'mame-mkp/src/emu/video.cpp';lua=ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp'
    code=video.read_text();lo=code.index('void video_manager::frame_update(');hi=code.index('void video_manager::',lo+10);code=code[lo:hi]
    need(code.index('emulator_info::frame_hook()')<code.index('machine().call_notifiers(MACHINE_NOTIFY_FRAME)'),
      'Original frame-done Lua hook runs before ordinary frame notifier')
    need('return execute_function("LUA_ON_FRAME_DONE");'in lua.read_text(),'Actual Lua frame hook invokes recorded frame_done callback')
    pin(video);pin(lua);pin(__file__)
    for p in CASE.rglob('*'):
        if p.is_file():pin(p)
    report=dict(passed=True,candidate=state.NAME,fighter='kano',physicalVictimSlot=1,identity=17,
      capture=str(CASE),actualNativeCallbackPhase=positive,actualPhaseFaultsRejected=faults,
      actualPixelFaultsRejected=meta['nativeRasterFaults'],everyOriginalControllerRGBDigestUnchanged=True,
      exactObservedGraphicsStreams=len(gfx),exactRGBPixels=len(records)*400*254,exactVRAMWords=len(records)*512*512,
      completeNativeRendererWindowAccepted=True,independentArtAllArenaAlternateGroundAudioAccepted=False,
      fullPortAcceptance=False,priorFrozenCollectorFinalGateFailure='Mixed frame_done and subsequent frame-notifier retirement labels, despite every captured target passing.',
      oldExecutedSourcesAndCaptureUnchanged=True,inputHashes=pins,scope=__doc__)
    need(all(sha(p)==h for p,h in pins.items()),'Every source/capture/public input unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
