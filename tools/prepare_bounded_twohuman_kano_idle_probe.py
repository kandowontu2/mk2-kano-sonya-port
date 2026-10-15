"""Same immutable neutral observer; only ordinary selected fighter changes."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    previous=root/'audit_bounded_twohuman_idle_opaque_preparation'
    target=root/'audit_bounded_twohuman_kano_idle_preparation';target.mkdir(exist_ok=False)
    lua=(previous/'prepared_observer.lua').read_text()
    (target/'prepared_observer.lua').write_text(lua)
    runner=(previous/'run.ps1').read_text()
    assert runner.count("MK2KS_HUMAN_SPECIAL_MOVE='ring'")==1
    runner=runner.replace("MK2KS_HUMAN_SPECIAL_MOVE='ring'","MK2KS_HUMAN_SPECIAL_MOVE='knife'")
    runner=runner.replace(previous.name,target.name)
    runner=runner.replace('audit_bounded_twohuman_sonya_kitana_idle_opaque_runtime','audit_bounded_twohuman_kano_kitana_idle_opaque_runtime')
    (target/'run.ps1').write_text(runner)
    (target/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target/'prepared_observer.lua'))))
    print('Prepared neutral Kano/Kitana control')

if __name__=='__main__':main()
