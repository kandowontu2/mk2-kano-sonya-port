"""Read all ten split pose-pointer lists per character, including prone frames."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_descriptor_lists_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_all_descriptors_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text();before='for index=0,5 do';assert text.count(before)==1
    text=text.replace(before,'for index=0,9 do')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    runner=(old/'run.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace('kung_lao_split_descriptor_lists_runtime','kung_lao_split_all_descriptors_runtime')
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
