"""All twenty descriptor sources, full native action/follow-through pixel model."""
import inspect
import prepare_bounded_kung_lao_split_pixels as previous

def main():
    source=inspect.getsource(previous.main)
    changes={'audit_bounded_kung_lao_split_pixels_preparation':'audit_bounded_kung_lao_split_all_pixels_preparation',
        'audit_bounded_kung_lao_split_descriptors_checked':'audit_bounded_kung_lao_split_all_descriptors_checked',
        'assert len(sources)==12':'assert len(sources)==20',
        "'kung_lao_split_pixels_runtime'":"'kung_lao_split_all_pixels_runtime'"}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::all_ten_frames_pixels','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
