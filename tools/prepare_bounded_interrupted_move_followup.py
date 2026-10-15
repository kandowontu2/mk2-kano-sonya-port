"""Physical walk/jump/punch after actual interruption, both selected slots."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    out=sync.ROOT/'audit_bounded_interrupted_move_followup_preparation';assert not out.exists();out.mkdir()
    cases={
        'bicycle':('audit_bounded_twohuman_hit_voice_state_preparation',lambda side:'run.ps1'),
        'square':('audit_bounded_twohuman_square_rise_counter_preparation',lambda side:f'run_p{side}.ps1'),
        'ball':('audit_bounded_kano_ball_guard_counter_preparation',lambda side:f'run_p{side}.ps1'),
    }
    hashes={}
    for move,(name,runnername) in cases.items():
        old=sync.ROOT/name;original=old/'prepared_observer.lua';source=original.read_text()
        before='   local age=frame-command\n';assert source.count(before)==1
        source=source.replace(before,before+"   pulse(side,forward,age,260,10);pulse(side,'Up',age,290,4);pulse(side,'High Punch',age,360,4)\n")
        target=out/f'{move}.lua';target.write_text(source);hashes[move]=sync.sha(target)
        for side in (1,2):
            runner=(old/runnername(side)).read_text()
            before=f'{name}/prepared_observer.lua';assert runner.count(before)==1
            runner=runner.replace(before,f'{out.name}/{move}.lua').replace(sync.sha(original),sync.sha(target))
            before=next(line.split("'")[1] for line in runner.splitlines() if line.startswith('$taskCase=Join-Path'))
            runner=runner.replace(before,f'audit_bounded_interrupted_{move}_p{side}_followup_runtime')
            runner=runner.replace("MK2KS_HUMAN_SPECIAL_SIDE='1'",f"MK2KS_HUMAN_SPECIAL_SIDE='{side}'")
            (out/f'run_{move}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=hashes,rawMedia=False,physicalFollowup='walk260 jump290 HP360')))

if __name__=='__main__':main()
