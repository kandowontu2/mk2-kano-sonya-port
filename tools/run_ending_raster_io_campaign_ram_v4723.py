"""Whole4712 native full ending campaign, explicit native IO and corrected phase.

Fresh leaves only, after the prior same-character run is actually terminal.
No restart for timeout, native controls changed, game fix or narrower window.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_ending_raster_clock_campaign_ram_v4712.py').read_text()
changes=[('ending_raster_clock_model_v4709','ending_raster_io_model_v4720'),
 ('qualify_ending_raster_clock_source_v4710','qualify_ending_raster_io_source_v4721'),
 ('audit_v4713_{fighter}_p2_ending_raster_clock_ram','audit_v4724_{fighter}_p2_ending_raster_io_ram'),
 ('audit_v4713_{args.fighter}_p2_ending_raster_clock_ram','audit_v4724_{args.fighter}_p2_ending_raster_io_ram'),
 ('audit_v4714_{args.fighter}_p2_ending_raster_clock_checked','audit_v4725_{args.fighter}_p2_ending_raster_io_checked'),
 ('    report=whole_run(fighter)',
  "    prior=ROOT/f'audit_v4713_{fighter}_p2_ending_raster_clock_ram'\n    terminal=ROOT/f'audit_v4714_{fighter}_p2_ending_raster_clock_checked/report.json'\n    need(terminal.exists()and not json.loads(terminal.read_text())['passed']and json.loads((prior/'result.json').read_text())['exit_code']==0,'Prior actual native terminal0 and real checker failure, never restart live/timeout')\n    report=whole_run(fighter)"),
 ("actualRasterClocks=sum(r['actualRasterClocks']for r in records),scope=__doc__)",
  "actualRasterClocks=sum(r['actualRasterClocks']for r in records),\n                  actualOriginalDisplayIOStores=records[-1]['actualDisplayIOStoresAtSnapshot'],\n                  actualNativeDisabledVisiblePixels=sum(r['sourceTimedBlankPixels']for r in records),scope=__doc__)")]
for before,after in changes:
    if 'audit_v4713_{args.fighter}'in before:
        assert text.count(before)==0 #4712 has no such leaf; record the absence explicitly.
        continue
    assert text.count(before)>=1,before
    text=text.replace(before,after)
exec(compile(text,__file__+'::whole4712_actual_native_IO_and_screen_phase','exec'),globals())
