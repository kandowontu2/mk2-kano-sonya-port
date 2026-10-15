"""Extend host exit only; preserve all physical command and followup inputs."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_interrupted_move_followup_preparation'
    out=sync.ROOT/'audit_bounded_interrupted_followup_complete_preparation';assert not out.exists();out.mkdir()
    hashes={}
    for move in ('bicycle','square','ball'):
        original=old/f'{move}.lua';source=original.read_text()
        assert source.count('frame-ready>=420')==1
        source=source.replace('frame-ready>=420','frame-ready>=520')
        target=out/f'{move}.lua';target.write_text(source);hashes[move]=sync.sha(target)
        for side in (1,2):
            runner=(old/f'run_{move}_p{side}.ps1').read_text()
            for before,after in {old.name:out.name,
                f'audit_bounded_interrupted_{move}_p{side}_followup_runtime':f'audit_bounded_interrupted_{move}_p{side}_complete_runtime',
                sync.sha(original):sync.sha(target)}.items():
                assert runner.count(before)==1;runner=runner.replace(before,after)
            (out/f'run_{move}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=hashes,onlyHostExitExtended=True,rawMedia=False)))

if __name__=='__main__':main()
