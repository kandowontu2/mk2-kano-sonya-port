"""Preserve5485; native palette bank arithmetic needs at least16-bit indices.

NumPy2.5 correctly rejects adding native512 bank to uint8 sprite pens. Promote
only that intermediate integer arithmetic; every strict original pixel/FIFO/
palette/whole-scanout gate remains. Native preview JPEGs are stdout/RAM only.
"""
import json
from pathlib import Path
import current_reptile_victims_ram_v5467 as canonical5467

failed=canonical5467.ROOT/'audit_v5485_current_reptile_victims_progress/progress.json'
status=json.loads(failed.read_text())
canonical5467.need(not status['passed']and status['error']=="OverflowError('Python integer 512 out of bounds for uint8')",
                  'Preserved exact native palette-bank arithmetic checker overflow')
base=Path(__file__).with_name('current_reptile_victims_ram_v5483.py')
source=base.read_text()
before="    exec(compile(source,__file__+'.whole5480_exact_shared_native_scene_metadata','exec'),scope)"
after='''    narrow="(int(d['palette'],16)+indices)&0x7fff"
    wide="(int(d['palette'],16)+indices.astype(np.uint32))&0x7fff"
    need(source.count(narrow)==1,'One actual native palette-bank integer-width correction')
    source=source.replace(narrow,wide)
    positive="    return dict(passed=True,targets=out,effectiveActualScanoutRAMFaults=faults)"
    preview="""    side=re.search(r'^MK2_REPTILE_V879_ACTION .*?side=(\\\\d)',log,re.M)
    if side and side[1]=='1':
        import base64
        from io import BytesIO
        from PIL import Image
        encoded=BytesIO();Image.fromarray(images[out[1]['filename']]).save(encoded,format='JPEG',quality=80)
        print('MK2_CURRENT_REPTILE_VISUAL_PREVIEW '+fighter+' '+base64.b64encode(encoded.getvalue()).decode(),flush=True)
    return dict(passed=True,targets=out,effectiveActualScanoutRAMFaults=faults)"""
    need(source.count(positive)==1,'Only actual already-qualified displayed image preview, no file dump')
    source=source.replace(positive,preview)
'''+before
canonical5467.need(source.count(before)==1,'Exact entire shared-metadata verifier adaptation boundary')
source=source.replace(before,after)
changes={
 'audit_v5484_current_reptile_victims_ram':'audit_v5487_current_reptile_victims_ram',
 'audit_v5485_current_reptile_victims_progress':'audit_v5488_current_reptile_victims_progress',
 "ROOT/'audit_v5482_current_reptile_victims_progress/progress.json')":
 "ROOT/'audit_v5482_current_reptile_victims_progress/progress.json',ROOT/'tools/current_reptile_victims_ram_v5483.py',ROOT/'audit_v5485_current_reptile_victims_progress/progress.json')",
}
for before,after in changes.items():
    canonical5467.need(source.count(before)==1,'Exact fresh palette-width-only qualifier adaptation: '+before)
    source=source.replace(before,after)
exec(compile(source,__file__+'.whole5483_exact_native_uint32_palette_bank_arithmetic','exec'),globals())
