"""Stop only the exact own superseded native test after a qualified real win.

Keep its source, genuine losses, terminal failure and explicit cancellation
receipt. This is neither a game-engine crash nor a native campaign clear.
"""
import datetime,json,subprocess
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as old
ROOT,need,sha=old.ROOT,old.need,old.sha


def run():
 report_path=ROOT/'audit_v5686_sonya_p2_subzero_ring_retries_checked/report.json'
 report=json.loads(report_path.read_text())
 need(report['passed']and report['actualSubZeroAdvanceAccepted']and
  report['native']['actualFinalMatchOwnRoundWins']==2 and
  len(report['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  len(report['actualContext8TaskAndActionFaultsRejected'])==8 and
  all(sha(p)==h for p,h in report['inputHashes'].items()),'Real completed new strategy and19effective faults first')
 parent=json.loads((ROOT/'audit_v5681_subzero_sonya_p2_progress/progress.json').read_text())
 manifest=json.loads((old.OUT/'process.json').read_text())
 need(not(old.OUT/'result.json').exists(),'Only a currently nonterminal superseded test')
 query=f"Get-CimInstance Win32_Process -Filter 'ProcessId={manifest['pid']}' | Select-Object ProcessId,Name,CommandLine,@{{Name='createdUnix';Expression={{([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}}}} | ConvertTo-Json -Compress"
 actual=json.loads(subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout)
 expected=next(p for p in parent['observedLiveProcesses']if p['ProcessId']==manifest['pid'])
 need(actual==expected and actual['Name']=='mkport_candidate.exe'and str(ROOT/old.LUA)in actual['CommandLine'],
  'Exact Name/creation/command native process, never a reused PID or user game')
 path=old.OUT/'host_cancellation_reason.json'
 need(not path.exists(),'Fresh immutable explicit cancellation explanation')
 receipt=dict(observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),action='deliberate_host_cancellation_of_superseded_test',
  targetActualProcess=actual,qualifiedReplacementProof=str(report_path),qualifiedReplacementSHA256=sha(report_path),
  reason='Old close-guard Sub-Zero test repeatedly lost; actual finite Ring retry comparison won the final match2-0 and advanced to stage8 with19effective native/input/owner faults rejected. Stop obsolete own test and retain its terminal failure.',
  engineCrashAccepted=False,campaignClearAccepted=False,source=str(__file__),sourceSHA256=sha(__file__))
 path.write_text(json.dumps(receipt,indent=2)+'\n')
 command=f"$mk2Target=Get-CimInstance Win32_Process -Filter 'ProcessId={actual['ProcessId']}'; if ($null -eq $mk2Target -or $mk2Target.Name -ne 'mkport_candidate.exe' -or [Math]::Abs(([DateTimeOffset]$mk2Target.CreationDate).ToUnixTimeMilliseconds()/1000-{actual['createdUnix']}) -gt 0.001) {{ throw 'Exact native creation changed' }}; Stop-Process -Id $mk2Target.ProcessId -ErrorAction Stop"
 subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True,check=True)
 print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':run()
