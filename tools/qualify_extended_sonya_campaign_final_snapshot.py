"""Account explicitly for MAME's timed-terminal screenshot, retain state gates."""
from pathlib import Path
import verify_native_source_sync as sync
parent=Path(__file__).with_name('qualify_extended_sonya_campaign_timed_terminal.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))"
assert wrapper.count(marker)==1
namespace=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),namespace)
source=namespace['source']
source=source.replace('audit_extended_sonya_campaign_timed_terminal_checked','audit_extended_sonya_campaign_final_snapshot_checked')
gate="        assert not any(p.suffix.lower() in ('.bin','.png','.wav') for p in folder.rglob('*') if p.is_file())"
assert source.count(gate)==1
source=source.replace(gate,"""        media=[p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() in ('.bin','.png','.wav')]
        assert media==[folder/'snap'/'mk2ks'/'0000.png']
        assert media[0].stat().st_size==58249
        snapshot=dict(path=str(media[0]),SHA256=sync.sha(media[0]),bytes=58249,
            cause='Native video_manager timed execution exit automatically saves final screenshot',
            manualReview='Sonya versus Kung Lao, correct name/body/floor shadow, no selection portraits; finite terminal sample only')
""")
source=source.replace('report=dict(passed=True,results=results,','report=dict(passed=True,results=results,terminalSnapshot=snapshot,videoSourceSHA256=sync.sha(sync.ROOT/\'mame-mkp/src/emu/video.cpp\'),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=namespace['prior']))
