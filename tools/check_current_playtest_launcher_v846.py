"""Actual current named CMD boot smoke check; not a release or full gameplay test."""
import hashlib
import json
import subprocess
from pathlib import Path
from verify_native_candidate_v798 import ROOT,NAME,EXE,PAYLOAD


def main():
    out=ROOT/'audit_v846_current_playtest_launcher'
    if out.exists():raise ValueError('Refusing to overwrite evidence')
    wrapper=ROOT/'PLAY_CURRENT_V786_TEST_BUILD.cmd'
    inner=ROOT/NAME/'PLAY_TEST_BUILD.cmd'
    for path,wanted in((ROOT/NAME/'mkport_candidate.exe',EXE),(ROOT/NAME/'roms/mk2ks/mk2ks.mdata',PAYLOAD)):
        if hashlib.sha256(path.read_bytes()).hexdigest().upper()!=wanted:raise ValueError('Wrong actual current build')
    source=inner.read_text();outer=wrapper.read_text()
    assert NAME+'\\PLAY_TEST_BUILD.cmd'in outer
    assert NAME+'\\roms;roms'in source and '-samplepath "samples"'in source and '-nocheat'in source
    assert all('set '+prefix in source for prefix in('MK2KS_','MK2_TRACE_','MK2_RANGE_','MK2_P2_'))
    # A different working directory specifically checks %~dp0/CD resolution.
    command='"'+str(wrapper)+'" -video none -sound none -str 3 -nothrottle -skip_gameinfo'
    # cmd has its own quote grammar, not Python's list2cmdline/C-runtime
    # backslash escaping. Preserve its /s /c outer quotes explicitly.
    process=subprocess.run(r'C:\Windows\System32\cmd.exe /d /s /c "'+command+'"',cwd=str(ROOT.parent),
                           capture_output=True,text=True,timeout=60)
    passed=process.returncode==0 and 'Average speed:'in process.stdout
    out.mkdir();(out/'run.log').write_text(process.stdout+process.stderr)
    paths=(Path(__file__),wrapper,inner,ROOT/NAME/'mkport_candidate.exe',ROOT/NAME/'roms/mk2ks/mk2ks.mdata',
           ROOT/'PLAY_LATEST_TEST_BUILD.cmd',ROOT/'PLAY_MK2_KANO_SONYA.cmd')
    report={'passed':passed,'exit_code':process.returncode,'candidate':NAME,'command':command,
            'scope':'actual named current CMD boot from different cwd; no GUI, match or full-release claim',
            'inputHashes':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in paths},
            'fullPortAcceptance':False,'release_promoted':False}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:value for k,value in report.items()if k!='inputHashes'},indent=2))
    if not passed:raise SystemExit(1)


if __name__=='__main__':main()
