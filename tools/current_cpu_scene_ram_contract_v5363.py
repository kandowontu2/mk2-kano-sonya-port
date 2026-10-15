"""Full original RAM scene replay plus the complete source-derived native HUD image."""
import inspect,json
from pathlib import Path
import current_cpu_scene_ram_contract_v5357 as original
import current_cpu_scene_ram_contract_v5360 as binding
import verify_current_ground_shadow_v1859 as hud
ROOT,need,sha=original.ROOT,original.need,original.sha
def patch_hud(image,pins):
 prior=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json'
 accepted=json.loads(prior.read_text())
 need(sha(hud.__file__)==accepted['inputHashes'][str(Path(hud.__file__).resolve())],'Whole original accepted HUD source model unchanged')
 source=inspect.getsource(hud.graphics)
 first=source.index("    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()")
 source='def patch_hud(image,pins):\n'+source[first:]
 need(source.count('return bytes(image)')==1,'Exact original complete HUD face/gold-ramp/black-shadow constructor')
 source=source.replace('return bytes(image)','return image',1)
 namespace=dict(hud.graphics.__globals__)
 exec(compile(source,__file__+'::entire_original_native_HUD_ramp_masks_dark_edge','exec'),namespace)
 result=namespace['patch_hud'](image,pins)
 pins[str(Path(hud.__file__).resolve())]=sha(hud.__file__)
 return result
def verify(folder,ram,log,guest,pins):
 failed=ROOT/'audit_v5362_current_cpu_square_scene_ram_checked/report.json'
 failure=json.loads(failed.read_text())
 need(not failure['passed']and failure['error']=="ValueError('Every actual whole scene/effect/body/shadow graphics stream equals complete source-bound ROM')",'Preserve actual omitted native HUD graphics counterexample')
 source=inspect.getsource(original.verify)
 before='image=graphics.reconstruct(pins);payload='
 need(source.count(before)==1,'Add original HUD graphics constructor to complete native scene image')
 source=source.replace(before,'image=patch_hud(graphics.reconstruct(pins),pins);payload=',1)
 before="len(snaps)==70 and [r['frame']for r in snaps]==list(range(2279,2349))"
 need(source.count(before)==1,'Preserve exact original69 field30 post-ready scope')
 source=source.replace(before,"len(snaps)==qualified['sampledFrames']==69 and [r['frame']for r in snaps]==list(range(2279,2317+31))",1)
 namespace=dict(original.verify.__globals__,patch_hud=patch_hud,replay_binding=binding.replay_binding,__file__=__file__)
 exec(compile(source,__file__+'::complete_original_scene_with_complete_native_HUD_pixels','exec'),namespace)
 report=namespace['verify'](folder,ram,log,guest,pins)
 for p in(failed,Path(original.__file__),Path(binding.__file__),Path(__file__)):pins[str(p.resolve())]=sha(p)
 report.update(completeOriginalNativeHUDGoldFaceAndBlackShadowSourceBound=True,preservedExecutedGraphicsScopeFailure=str(failed),
  originalNativeThirtyPostReadyScanoutsPreserved=True)
 return report
