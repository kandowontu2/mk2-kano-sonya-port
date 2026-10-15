"""Native-only mixer control for the identical physical hit replay."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_voice_hit_pcm_window_preparation'
    out=sync.ROOT/'audit_bounded_voice_hit_pcm_disabled_preparation';assert not out.exists()
    observer=old/'prepared_observer.lua';runner=(old/'run.ps1').read_text()
    before='audit_bounded_voice_hit_pcm_window_runtime';assert runner.count(before)==1
    runner=runner.replace(before,'audit_bounded_voice_hit_pcm_disabled_runtime')
    assert runner.count("'-samples'")==1
    runner=runner.replace("'-samples'","'-nosamples'")
    out.mkdir();(out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),onlySamplesOptionChanged=True,acceptance=False)))

if __name__=='__main__':main()
