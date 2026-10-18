"""Fetch the exact official corresponding source asset without executing/extracting it."""
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request
from audit_stock_mame_distribution import SOURCE_SHA, file_digest
from inspect_normal_runtime import PORT

SIZE=159028505
URL='https://github.com/mamedev/mame/releases/download/mame0289/mame0289s.exe'


def check_chunk(total,chunk):
    assert 0<=total<=SIZE and total+len(chunk)<=SIZE,'Source asset exceeds pinned size'
    return total+len(chunk)


def main():
    folder=(PORT.parents[1].parent/'mame0289').resolve();assert folder.is_dir()
    target=folder/'mame0289s.exe'
    reused=target.exists()
    if reused:
        assert target.is_file() and target.stat().st_size==SIZE and file_digest(target)==SOURCE_SHA
    else:
        partial=folder/'mame0289s.exe.partial'
        assert not partial.exists(),'Inspect an existing partial download before retrying'
        digest=hashlib.sha256();total=0;started=time.monotonic();created=False
        try:
            with partial.open('xb') as output:
                created=True
                request=urllib.request.Request(URL,headers={'User-Agent':'MK2KS-native-source-preparation'})
                with urllib.request.urlopen(request,timeout=30) as response:
                    while True:
                        assert time.monotonic()-started<300,'Source download exceeded bounded runtime'
                        chunk=response.read(65536)
                        if not chunk:break
                        total=check_chunk(total,chunk)
                        output.write(chunk);digest.update(chunk)
            assert total==SIZE and digest.hexdigest().upper()==SOURCE_SHA,'Official source hash/size mismatch'
            # Exclusive publication: do not replace a file created concurrently.
            os.link(partial,target)
        finally:
            if created and partial.exists():partial.unlink()
        assert file_digest(target)==SOURCE_SHA
    report=dict(scope='Pinned official corresponding MAME source asset, not executed or extracted',
        file=str(target),bytes=SIZE,SHA256=SOURCE_SHA,url=URL,reused=reused,
        completeAssetVerified=True,executed=False,extracted=False,releasePublished=False)
    (PORT/'STOCK_MAME_SOURCE_0289.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Official MAME source asset verified:',SIZE,'bytes;',SOURCE_SHA,'; not executed/extracted.')


if __name__=='__main__':main()
