"""Unversioned launcher aliases must invoke actual current native checker."""
import json
import subprocess
import verify_native_source_sync as sync

def main():
    source=sync.verify()
    out=sync.ROOT/'audit_current_launcher_routing/report.json'
    assert not out.exists()
    results={}
    for name in ('PLAY_LATEST_KANO_SONYA.cmd','PLAY_MK2_KANO_SONYA.cmd'):
        path=sync.ROOT/name
        text=path.read_text()
        assert 'PLAY_CURRENT_NATIVE_CHECKED.cmd' in text
        assert 'diagnostic_native_cpu_finisher_spacing' not in text
        assert 'PLAY_CURRENT_V6508_CHECKED.cmd' not in text
        run=subprocess.run(['cmd.exe','/d','/c',str(path),'--check'],cwd=sync.ROOT,
                           capture_output=True,text=True,timeout=30)
        assert run.returncode==0 and not run.stderr.strip()
        assert 'all 23 sound files match' in run.stdout
        assert 'no checksum warning' in run.stdout
        results[name]=dict(sha256=sync.sha(path),exitCode=run.returncode,output=run.stdout)
    report=dict(passed=True,sourceSync=source,aliases=results,
                currentBuild=sync.BUILD.name,normalGameplayLaunched=False,
                newBuilds=0,newROMCopies=0,releaseZIPChanged=False,
                fullPortAcceptance=False,
                scope='Both unversioned root CMD aliases now route checked current native EXE/ROM/all23sound assets. Original old launcher bytes and report pins preserved explicitly. No new full gameplay or release acceptance.')
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,currentNativeLaunchAliases=2,newBuilds=0,fullPortAcceptance=False)))

if __name__=='__main__':main()
