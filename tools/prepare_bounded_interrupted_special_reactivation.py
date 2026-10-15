"""Physical second command after complete ordinary followup, no state writes."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_interrupted_followup_complete_preparation'
    out=sync.ROOT/'audit_bounded_interrupted_special_reactivation_preparation';assert not out.exists();out.mkdir()
    commands={
        'bicycle':"pulse(side,backward,repeat_age,0,3);pulse(side,backward,repeat_age,6,3);pulse(side,'Down',repeat_age,12,3);pulse(side,'High Kick',repeat_age,13,3)",
        'square':"pulse(side,forward,repeat_age,0,3);pulse(side,backward,repeat_age,5,3);pulse(side,'High Punch',repeat_age,6,3)",
        'ball':"pulse(side,'Low Kick',repeat_age,0,84)",
    }
    for move,sequence in commands.items():
        original=old/f'{move}.lua';source=original.read_text()
        assert source.count('frame-ready>=520')==1;source=source.replace('frame-ready>=520','frame-ready>=800')
        marker='   local age=frame-command\n';assert source.count(marker)==1
        source=source.replace(marker,marker+'   local repeat_age=age-460\n   '+sequence+'\n')
        target=out/f'{move}.lua';target.write_text(source)
        for side in (1,2):
            runner=(old/f'run_{move}_p{side}.ps1').read_text()
            for before,after in {old.name:out.name,
                f'audit_bounded_interrupted_{move}_p{side}_complete_runtime':f'audit_bounded_interrupted_{move}_p{side}_reactivation_runtime',
                sync.sha(original):sync.sha(target)}.items():
                assert runner.count(before)==1;runner=runner.replace(before,after)
            (out/f'run_{move}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,secondPhysicalCommandAge=460,maximumReadyFields=800,rawMedia=False)))

if __name__=='__main__':main()
