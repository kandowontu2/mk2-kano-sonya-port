"""Repair stale latest alias; actual current CMD ROM/voice validation outside ROOT.

Normal gameplay launch was already qualified through the same canonical CMD.
This checks the new alias/argument forwarding without starting a second match
or changing saved settings. Historical versioned launchers stay available.
"""
import datetime,json,os,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6322_current_latest_launcher_checked'


def main():
 need(not OUT.exists(),'Fresh immutable launcher-alias evidence')
 latest=ROOT/'PLAY_LATEST_TEST_BUILD.cmd';canonical=ROOT/'PLAY_MK2_KANO_SONYA.cmd';versioned=ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd'
 old=ROOT/'launcher_history_v6318/PLAY_LATEST_TEST_BUILD.cmd'
 need(sha(old)=='54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784',
      'Exact recoverable original retired-folder alias preserved')
 need('diagnostic_v737_native_babality_performers'in old.read_text()and not(ROOT/'diagnostic_v737_native_babality_performers/PLAY_TEST_BUILD.cmd').exists(),
      'Authoritative old latest alias pointed to retired missing target')
 need('call "%~dp0PLAY_MK2_KANO_SONYA.cmd" %*'in latest.read_text()and
      'PLAY_CURRENT_V5219_CHECKED.cmd'in canonical.read_text()and'diagnostic_v5219_current_payload_rom_metadata'in versioned.read_text(),
      'Repaired exact latest->canonical->current checked launch route, arguments retained')
 pins={str(p):sha(p)for p in(latest,canonical,versioned,old,ROOT/'PLAY_CURRENT_V1250_TEST_BUILD.cmd',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',
                              ROOT/'tools/check_current_playtest_v5975.ps1',Path(__file__),ROOT/current.NAME/'build-info.json',
                              ROOT/current.NAME/'mkport_candidate.exe',ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata')}
 settings=[p for directory in('play_v5219_checked/cfg','play_v5219_checked/nvram')for p in(ROOT/directory).rglob('*')if p.is_file()]
 before={str(p):sha(p)for p in settings}
 outside=Path('C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port')
 command=[os.environ['ComSpec'],'/d','/c',str(latest),'-verifyroms']
 check=subprocess.run(command,cwd=outside,capture_output=True,text=True)
 need(check.returncode==0 and not check.stderr.strip()and
      'Checked v5219 executable, ROM payload and all sixteen voice assets.'in check.stdout and
      'romset mk2ks [mk2] is good'in check.stdout and'1 romsets found, 1 were OK.'in check.stdout,
      'Actual complete alias invocation validates current matched EXE/payload/all voices and native ROM set')
 after_files=[p for directory in('play_v5219_checked/cfg','play_v5219_checked/nvram')for p in(ROOT/directory).rglob('*')if p.is_file()]
 need(before=={str(p):sha(p)for p in after_files},'Current saved settings unchanged by read-only alias verification')
 need(all(sha(p)==h for p,h in pins.items()),'Alias/current/historical game and launcher bytes unchanged during test')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),currentCheckedCandidate=current.NAME,
             command=command,workingDirectory=str(outside),exitCode=check.returncode,stdout=check.stdout,stderr=check.stderr,
             repairedLatestAliasVerified=True,oldAliasRecoverableAt=str(old),versionedHistoricalLaunchersUnchanged=True,
             actualCurrentNativeROMValidationPassed=True,actualSixteenVoiceAssetsValidated=True,savedSettingsUnchanged=True,
             noInteractiveMatchStarted=True,normalCurrentCMDGameplayRegressionReference=str(ROOT/'audit_v6266_current_cmd_special_matrix_checked/report.json'),
             newBuilds=0,newZIPs=0,goalStatus='active',fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Exact small launcher verification report compressed')
 print(json.dumps(dict(passed=True,current=current.NAME,latestAliasVerified=True,savedSettingsUnchanged=True,newBuilds=0)),flush=True)


if __name__=='__main__':main()
