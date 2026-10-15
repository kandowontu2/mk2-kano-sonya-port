"""Freeze the actually executing failed observer before a corrected wrapper."""
import gzip
import hashlib
import json
from pathlib import Path
from capture_native_secondary_kano_reference import ROOT,OUT,census,sha,need

def main():
    record=OUT/'raster_observer_failure.json'
    need(not record.exists(),'Do not overwrite actual failed reference evidence')
    process=json.loads((OUT/'process.json').read_text())
    live=next((item for item in census()if item['ProcessId']==process['pid']),None)
    need(live==process['actualWindowsIdentity'],'The same original native PID/parent/path/creation remains live')
    stderr=(OUT/'stderr.log').read_text()
    need("mk3_native_secondary_kano_reference.lua:156: bad argument #4 to 'format' (number expected, got nil)"in stderr,
         'Actual executed old-emulator raster dimension compatibility failure')
    paths=[ROOT/'mk3_native_secondary_kano_reference.lua',ROOT/'tools/capture_native_secondary_kano_reference.py',
           ROOT/'tools/native_process_census_v6647.py',Path(__file__)]
    pins={str(path.resolve()):sha(path)for path in paths}
    with gzip.open(OUT/'failed_executed_observer_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({str(path.resolve()):dict(sha256=pins[str(path.resolve())],text=path.read_text())for path in paths},stream)
    report=dict(passed=True,failedNativeRunAccepted=False,actualNativeIdentity=live,
                actualRepeatedRasterErrorLines=stderr.count('[LUA ERROR]'),
                stderrSnapshotSHA256=hashlib.sha256(stderr.encode()).hexdigest().upper(),
                originalNativeHandleStillLive=True,terminatedOrRestarted=False,inputHashes=pins,
                reason='Old original-game emulator returns only raster bytes from pixels(); dimension return values are nil.',
                gameSourceChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,goalStatus='active')
    record.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(preserved=True,nativePID=live['ProcessId'],nativeStillLive=True,errorLines=report['actualRepeatedRasterErrorLines'])))

if __name__=='__main__':main()
