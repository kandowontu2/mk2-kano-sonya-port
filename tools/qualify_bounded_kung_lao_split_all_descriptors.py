"""All ten split poses, every actual custom-source draw through follow-through."""
import inspect
import qualify_bounded_kung_lao_split_descriptors as previous

def main():
    source=inspect.getsource(previous.main)
    changes={'audit_bounded_kung_lao_split_descriptors_checked':'audit_bounded_kung_lao_split_all_descriptors_checked',
        'audit_bounded_kung_lao_split_descriptor_lists_runtime':'audit_bounded_kung_lao_split_all_descriptors_runtime',
        'list(range(6))':'list(range(10))',
        'len(source_sets[17])==len(source_sets[18])==6':'len(source_sets[17])==len(source_sets[18])==10',
        'audit_bounded_kung_lao_split_draw_census_checked':'audit_bounded_kung_lao_split_followthrough_palette_checked',
        'kung_lao_split_draw_census_runtime':'kung_lao_split_followthrough_palette_runtime'}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    before="                    if r['source'] in all_sources:draws.append(r)";assert source.count(before)==1
    source=source.replace(before,"                    if r['source'].startswith('0F'):assert r['source'] in all_sources\n"+before)
    before="            specs={r['source']:r for r in descriptors[ident]};accepted=gate(draws,ident,specs,side);faults=[]"
    assert source.count(before)==1
    source=source.replace(before,before+"\n            assert {r['source'] for r in draws}==set(specs)")
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::all_ten_split_frames','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
