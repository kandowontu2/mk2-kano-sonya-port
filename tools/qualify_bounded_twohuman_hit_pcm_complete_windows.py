"""Only windows starting after observed cleanup; overlapping update unproven."""
import inspect
import qualify_bounded_twohuman_hit_pcm as previous

def main():
    gate=inspect.getsource(previous.gate)
    before="if Decimal(a['seconds'])>cleared]";assert gate.count(before)==1
    gate=gate.replace(before,"if Decimal(a['seconds'])-Decimal('.02')>=cleared]")
    before="<Decimal('.02')";assert gate.count(before)==1
    gate=gate.replace(before,"<Decimal('.04')")
    gate=gate.replace('firstNativeOnlyUpdateSeconds=','firstCompleteNativeOnlyWindowEndSeconds=')
    source=inspect.getsource(previous.main)
    source=source.replace("'audit_bounded_twohuman_hit_pcm_checked'","'audit_bounded_twohuman_hit_pcm_complete_windows_checked'")
    before="if Decimal(r['seconds'])>cleared)";assert source.count(before)==1
    source=source.replace(before,"if Decimal(r['seconds'])-Decimal('.02')>=cleared)")
    source=source.replace('first_post_cleanup_difference','first_complete_post_cleanup_window_difference')
    source=source.replace('intraUpdateSampleBoundaryAccepted=False','intraUpdateSampleBoundaryAccepted=False,overlappingFirstPostClearUpdateAccepted=False')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate+'\n'+source,__file__+'::complete_output_windows','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
