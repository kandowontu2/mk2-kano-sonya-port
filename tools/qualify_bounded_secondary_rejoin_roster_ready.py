"""Strict error-free native rejoin gates, no rendering claim from scalar retry."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_secondary_rejoin.py')
source=prior.read_text()
source=source.replace('audit_bounded_secondary_rejoin_checked','audit_bounded_secondary_rejoin_roster_ready_checked')
source=source.replace('audit_bounded_secondary_rejoin_delayed_{fighter}', 'audit_bounded_secondary_rejoin_roster_ready_{fighter}')
source=source.replace("terminal['rawMedia']=='bounded_two_png'","terminal['rawMedia']=='none'")
begin=source.index('    images={}\n');end=source.index('    results[fighter]=',begin)
source=source[:begin]+"    assert not list((folder/'snap').rglob('*.png'))\n    assert len(rows['REJOIN_MARKER'])==2\n"+source[end:]
source=source.replace('images=images,','markerReceipts=rows[\'REJOIN_MARKER\'],')
source=source.replace('Native selection and next arena with correct Kano/Sonya versus Kitana bodies/names; no prior laser/orb/debris/selector overlays observed in next-match sample. Finite raster samples, not every transition field.',
    'No images in this retry. Native selection/new-match identities and owner gates qualify independently; earlier visual samples are separate finite observations, not full clearing proof.')
source=source.replace('four inspected transition rasters.','text-only mechanics, no new rendered evidence.')
source=source.replace('reviewedPNGs=4','reviewedPNGs=0')
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
