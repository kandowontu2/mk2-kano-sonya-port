"""Defer host exit to frame-done so final298 draw field is visibly checked."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_all_pixels_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_pixels_final_flush_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    before="  log('BOUNDED_TERMINAL','reason=native_common_completion_followthrough raw_media=none')\n  manager.machine:exit()"
    assert text.count(before)==1
    text='local bounded_split_exit_pending=false\n'+text.replace(before,"  log('BOUNDED_TERMINAL','reason=native_common_completion_followthrough raw_media=none')\n  bounded_split_exit_pending=true")
    before='frame-ready>=1 and frame-ready<=299';assert text.count(before)==2
    text=text.replace(before,'frame-ready>=1 and frame-ready<=298')
    for before,after in [('frame-action_start>299','frame-action_start>298'),('frame-ready>299','frame-ready>298')]:
        assert text.count(before)>=1;text=text.replace(before,after)
    text+='\nemu.register_frame_done(function()if bounded_split_exit_pending then manager.machine:exit()end end)\n'
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace('kung_lao_split_all_pixels_runtime','kung_lao_split_pixels_final_flush_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),nativeDrawFields=298,hostExitFrameDoneAtAge=299,acceptance=False)))

if __name__=='__main__':main()
