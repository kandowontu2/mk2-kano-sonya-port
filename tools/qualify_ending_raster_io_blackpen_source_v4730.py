"""Whole4721 preflight with the actual original pen_t declaration checked.

The first source preflight failed only its uint16_t-vs-pen_t literal check;
no native launch or pixel/IO acceptance resulted. Preserve that source.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/qualify_ending_raster_io_source_v4721.py').read_text()
changes=[('audit_v4722_ending_raster_io_source_checked','audit_v4732_ending_raster_io_blackpen_source_checked'),
 ('uint16_t blackpen = screen.palette().black_pen();','pen_t blackpen = screen.palette().black_pen();'),
 ('import run_ending_raster_io_campaign_ram_v4723 as capture','import run_ending_raster_io_blackpen_campaign_ram_v4731 as capture'),
 ("    files.update(map(Path,old['inputHashes']));files.update(ROOT/p for p in TRANSITIVE_LUA)",
  "    files.add(ROOT/'tools/qualify_ending_raster_io_source_v4721.py');files.add(ROOT/'tools/run_ending_raster_io_campaign_ram_v4723.py')\n    files.update(map(Path,old['inputHashes']));files.update(ROOT/p for p in TRANSITIVE_LUA)")]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after)
exec(compile(text,__file__+'::whole4721_actual_native_pen_t_source','exec'),globals())
