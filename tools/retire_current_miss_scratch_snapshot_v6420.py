"""Retire one unpinned legacy choice screenshot; preserve actual disclosure.

The read-only3303 observer made a PNG outside the continuous Ring window.
It is not a RAM target or input to either accepted miss checker. Do not
overwrite the executed collector's raw-files claim; record the discrepancy.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6421_current_miss_scratch_snapshot_retired'
TARGET=ROOT/'audit_v6413_current_cpu_ring_miss_render_ram/snap/native_square_choice_2994.png'

def need(value,message):
 if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def main():
 need(not OUT.exists(),'Fresh precise scratch retirement record')
 exact=Path('C:/Users/kando/Documents/Codex/2026-08-29/i-ha/work/mk2port/audit_v6413_current_cpu_ring_miss_render_ram/snap/native_square_choice_2994.png')
 need(TARGET.resolve()==exact.resolve() and TARGET.is_relative_to(ROOT) and TARGET.is_file() and
      not TARGET.lstat().st_file_attributes&0x400,'Resolved single exact scratch screenshot, no recursive/broad/reparse target')
 render=json.loads((ROOT/'audit_v6415_current_cpu_ring_miss_render_checked/report.json').read_text())
 phase=json.loads((ROOT/'audit_v6417_current_cpu_ring_miss_phase_checked/report.json').read_text())
 pins={**render['inputHashes'],**phase['inputHashes']}
 need(render['passed'] and phase['passed'] and str(TARGET.resolve())not in pins and
      all(sha(p)==h for p,h in pins.items()),'Scratch PNG is not pinned/used by the actual accepted miss evidence')
 state=json.loads((ROOT/'audit_v6413_current_cpu_ring_miss_render_ram/native_terminal.json').read_text())
 need(state['exitCode']==0 and state['naturalTerminal'] and not state['observationErrors'],'Same actual native process naturally terminal')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' } | Select-Object ProcessId | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'No live emulator before own scratch-file retirement')
 source=ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua'
 need("if kind=='square'then manager.machine.screens[':screen']:snapshot('native_square_choice_'..frame..'.png')end"in source.read_text(),'Exact unchanged legacy observer explains the unexpected source of PNG')
 OUT.mkdir()
 observed=dict(path=str(TARGET.resolve()),bytes=TARGET.stat().st_size,sha256=sha(TARGET),
  sourceObserver=str(source),sourceObserverSHA256=sha(source),actualFrame=2994,
  outsideAcceptedMissRenderWindow=True,usedByAcceptedMissChecks=False,
  executedCollectorRawFilesCountClaimWasIncorrect=True,rawScratchScreenshotsActuallyWritten=1,
  recovery='Digest only; this scratch PNG is not retained or recoverable from this folder.',
  noNativeReruns=True,protectedPins=len(pins))
 (OUT/'observed_before_retirement.json').write_text(json.dumps(observed,indent=2)+'\n')
 removed=subprocess.run(['powershell','-NoProfile','-Command',"Remove-Item -LiteralPath 'C:\\Users\\kando\\Documents\\Codex\\2026-08-29\\i-ha\\work\\mk2port\\audit_v6413_current_cpu_ring_miss_render_ram\\snap\\native_square_choice_2994.png' -Force"],capture_output=True,text=True)
 need(removed.returncode==0 and not TARGET.exists(),'Exact own scratch PNG retired, no other file targeted')
 need(all(sha(p)==h for p,h in pins.items()),'All accepted source/guest/build/trace/model bytes unchanged after scratch retirement')
 path=OUT/'report.json';path.write_text(json.dumps(dict(passed=True,removed=[observed],deletedFiles=1,
  deletedLogicalBytes=observed['bytes'],protectedInputsUnchanged=True,newBuilds=0,newNativeBoots=0,
  goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
 for p in OUT.iterdir():
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact retirement disclosure losslessly compressed')
 print(json.dumps(dict(passed=True,deletedScratchPNGBytes=observed['bytes'],allAcceptedEvidenceUnchanged=True)),flush=True)

if __name__=='__main__':main()
