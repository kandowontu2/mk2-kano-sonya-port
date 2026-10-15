"""Count actor rows separately from the physical input transcript."""
import inspect
import qualify_bounded_twohuman_p2_hit_voice as previous

def main():
    source=inspect.getsource(previous.main)
    before='assert len(fields)==842';assert source.count(before)==1
    source=source.replace(before,"assert sum(tag=='MK2_HSPECIAL_FIELD' for tag,r in rows)==842")
    source=source.replace("'voice_state_check.json'","'voice_state_actor_count_check.json'")
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::actor_count','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
