"""Passive bounded native selection-navigation RAM sheet, no disk images."""
def _send_navigation():
    from pathlib import Path

    path=Path('tools/read_native_anchor_ui_remote.py')
    source=path.read_text()
    boundary='\n_send_anchor_ui()'
    assert source.count(boundary)==1
    source=source.split(boundary)[0]
    before="{'delayed':27800,'standard':12004}"
    assert source.count(before)==1
    source=source.replace(before,"{'navigation':42340}",1)
    scope={}
    exec(compile(source,str(path)+'::navigation_rasters_only','exec'),scope)
    scope['_send_anchor_ui']()

_send_navigation()
