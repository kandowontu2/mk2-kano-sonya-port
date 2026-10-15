"""Actual installed parser: full original special controller byte-identical."""
import inspect
from pathlib import Path
import qualify_native_kano_laser_ground_ram as prior

source=inspect.getsource(prior.main)
changes=[
    ("ROOT/'mk2ks_native_kano_laser_ground_parse.lua'","ROOT/'mk2ks_native_kano_laser_special_shadow_parse.lua'"),
    ("ROOT/'mk2ks_native_kano_laser_ground_ram.lua'","ROOT/'mk2ks_native_kano_laser_special_shadow.lua'"),
    ("ROOT/'mk2ks_ground_shadow_v815_probe.lua'","ROOT/'mk2ks_special_shadow_v5131.lua'"),
    ('MK2_GR_PARSE_PHYSICAL','MK2_SS_PARSE_PHYSICAL'),
    ("        need(original.count('io.open(output..')==3 and original.count('screen:snapshot(file)')==1,'Original exact evidence sink counts')\n"
     "        adapted=original.replace('io.open(output..','_ground_ram_open(output..').replace('screen:snapshot(file)','_ground_ram_rgb(file,frame)')\n"
     "        need(text.endswith(adapted),'Entire actual physical controller/DMA/timing/ownership observer byte-identical except four sinks')",
     "        need(text==original,'Entire actual physical/controller/body/shadow/source observer byte-identical, no command changes')"),
    ('wholePhysicalGroundByteIdentical=True,changedBinarySinks=3,changedPNGSinks=1,','wholePhysicalSpecialShadowByteIdentical=True,totalSampleChannels=19,'),
    ('wholePhysicalGroundUnchanged=True','wholePhysicalSpecialShadowUnchanged=True'),
    ('paths=[Path(__file__),','paths=[Path(__file__),Path(prior.__file__),')]
for before,after in changes:
    prior.need(before in source,'Exact whole original native parser boundary: '+before)
    source=source.replace(before,after)
scope=dict(vars(prior),prior=prior,__file__=__file__,OUT=prior.ROOT/'audit_native_kano_laser_special_shadow_source')
exec(compile(source,__file__+'::whole_actual_native_parser_and_identity','exec'),scope)
if __name__=='__main__':scope['main']()
