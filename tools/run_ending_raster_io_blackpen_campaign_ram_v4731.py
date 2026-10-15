"""Fresh whole4723 capture with actual pen_t source preflight and unused leaves."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_ending_raster_io_campaign_ram_v4723.py').read_text()
changes=[('qualify_ending_raster_io_source_v4721','qualify_ending_raster_io_blackpen_source_v4730'),
 ('audit_v4724_','audit_v4733_'),('audit_v4725_','audit_v4734_')]
for before,after in changes:
    assert text.count(before)>=1,before
    text=text.replace(before,after)
exec(compile(text,__file__+'::whole4723_actual_black_pen_type_preflight','exec'),globals())
