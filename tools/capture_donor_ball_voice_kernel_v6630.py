"""Same native full-ROM source collector, complete launch voice kernel."""
import inspect
import capture_donor_ball_source_v6624 as original
OUT=original.ROOT/'audit_v6629_donor_ball_voice_kernel'
source=inspect.getsource(original.main)
before="lua=ROOT/'mk3_cannonball_startup_source_v6622.lua'"
original.need(source.count(before)==1,'Only source inspection leaf changes')
source=source.replace(before,"lua=ROOT/'mk3_cannonball_voice_kernel_v6628.lua'",1)
before="[exe,lua,rom,Path(__file__)]"
original.need(source.count(before)==1,'Original and wrapper executed-source pins')
source=source.replace(before,"[exe,lua,rom,Path(__file__),Path(original.__file__),ROOT/'mk3_cannonball_startup_source_v6622.lua']",1)
namespace=dict(original.__dict__,__file__=__file__,OUT=OUT,original=original)
exec(compile(source,__file__+'::native_donor_voice_kernel','exec'),namespace)
if __name__=='__main__':namespace['main']()
