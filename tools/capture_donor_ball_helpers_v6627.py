"""Same original whole-ROM native source collector, extra donor callees."""
import inspect
import capture_donor_ball_source_v6624 as original
OUT=original.ROOT/'audit_v6626_donor_ball_startup_helpers'
source=inspect.getsource(original.main)
before="lua=ROOT/'mk3_cannonball_startup_source_v6622.lua'"
original.need(source.count(before)==1,'Only source probe leaf changes')
source=source.replace(before,"lua=ROOT/'mk3_cannonball_startup_helpers_v6625.lua'",1)
before="[exe,lua,rom,Path(__file__)]"
original.need(source.count(before)==1,'Preserve both original and wrapper source pins')
source=source.replace(before,"[exe,lua,rom,Path(__file__),Path(original.__file__),ROOT/'mk3_cannonball_startup_source_v6622.lua']",1)
namespace=dict(original.__dict__,__file__=__file__,OUT=OUT,original=original)
exec(compile(source,__file__+'::whole_native_donor_callee_source_capture','exec'),namespace)
if __name__=='__main__':namespace['main']()
