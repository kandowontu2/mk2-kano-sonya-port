"""Every ten-frame custom split draw, independent FIFO/DMA/palette/pixels."""
import inspect,sys
import qualify_bounded_kung_lao_split_pixels as previous

def main(side):
    source=inspect.getsource(previous.main)
    changes={'audit_bounded_kung_lao_split_pixels_p':'audit_bounded_kung_lao_split_all_pixels_p',
        'audit_bounded_kung_lao_split_descriptors_checked':'audit_bounded_kung_lao_split_all_descriptors_checked',
        'kung_lao_split_pixels_runtime':'kung_lao_split_all_pixels_runtime',
        'assert sum(expected.values())==126':'assert sum(expected.values())==(354 if side==1 else 352)'}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::all_ten_frames_pixels','exec'),namespace);namespace['main'](side)

if __name__=='__main__':main(int(sys.argv[1]))
