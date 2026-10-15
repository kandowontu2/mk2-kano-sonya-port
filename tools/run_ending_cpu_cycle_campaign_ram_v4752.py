"""Fresh whole native RAM renderer after complete real clock/IO diagnosis.

One source-defined early CPU clock boundary only; identical physical native
campaign controls/guest/whole renderer/bit faults/ending+300attract retained.
Require actual prior terminal and complete character-specific native ledger.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_ending_raster_clock_campaign_ram_v4712.py').read_text()
changes=[('ending_raster_clock_model_v4709','ending_raster_cpu_cycle_model_v4740'),
 ('qualify_ending_raster_clock_source_v4710','qualify_ending_cpu_cycle_source_v4750'),
 ('audit_v4713_{fighter}_p2_ending_raster_clock_ram','audit_v4753_{fighter}_p2_ending_cpu_cycle_ram'),
 ('audit_v4714_{args.fighter}_p2_ending_raster_clock_checked','audit_v4754_{args.fighter}_p2_ending_cpu_cycle_checked'),
 ('    report=whole_run(fighter)',
  "    prior=ROOT/f'audit_v4733_{fighter}_p2_ending_raster_io_ram'\n    terminal=ROOT/f'audit_v4734_{fighter}_p2_ending_raster_io_checked/report.json'\n    ledger=ROOT/f'audit_v4749_{fighter}_complete_cpu_cycle_ending_terminal_ledger_checked/report.json'\n    need(terminal.exists()and not json.loads(terminal.read_text())['passed']and json.loads((prior/'result.json').read_text())['exit_code']==0,'Prior real native terminal0/checker failure, never timeout restart')\n    proof=json.loads(ledger.read_text());need(proof['passed']and proof['actualAttractFields']==300 and not proof['fullEndingVRAMRGBPixelsAccepted']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual complete original character-specific hardware ledger/source pins required, metadata never replaces native pixels')\n    report=whole_run(fighter)"),
 ("actualRasterClocks=sum(r['actualRasterClocks']for r in records),scope=__doc__)",
  "actualRasterClocks=sum(r['actualRasterClocks']for r in records),\n                  actualOriginalDisplayIOStores=records[-1]['actualDisplayIOStoresAtSnapshot'],\n                  actualNativeDisabledVisiblePixels=sum(r['sourceTimedBlankPixels']for r in records),\n                  originalSourceDefinedEarlyCPUCycleSeconds=model.CPU_CYCLE_SECONDS,scope=__doc__)")]
for before,after in changes:
    assert text.count(before)>=1,before
    text=text.replace(before,after)
exec(compile(text,__file__+'::whole4712_actual_source_bound_CPU_cycle','exec'),globals())
