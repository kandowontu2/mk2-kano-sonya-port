"""New native own-body cold ROM/GFX and physical freeze; RGB RAM-only."""
from pathlib import Path
prior=Path(__file__).with_name('run_earned_subzero_victims_v4871.py')
text=prior.read_text()
for before,after in (
 ('import run_native_subzero_offset_regression_v4856 as native','import native_subzero_body_context_v4932 as native'),
 ('mk2ks_earned_subzero_victims_v4870.lua','mk2ks_native_subzero_body_probe_v4933.lua'),
 ('audit_v4872_subzero_','audit_v4935_subzero_'),('audit_v4873_subzero_','audit_v4936_subzero_'),
 ("MK2KS_STOCK_COMMAND='fdf_hp'","MK2KS_STOCK_COMMAND='ffd_hk'"),
 ('ROOT/LUA,ROOT/\'mk2ks_stock_fatality_v1021.lua\',Path(__file__).resolve()',
  'ROOT/LUA,ROOT/\'mk2ks_stock_fatality_v1021.lua\',prior,Path(__file__).resolve(),Path(native.__file__).resolve()'),
 ('guest_proof=None','guest_proof=None;gfx_proof=None;rgb_proof=None'),
 ("if line.startswith('MK2_EARNED_SUBZERO_GUEST '):", """if line.startswith('MK2_EARNED_SUBZERO_GFX '):
                    fields=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
                    need(gfx_proof is None and fields==dict(frame='1',bytes='11944') and raw==native.expected_gfx(),
                         'Every actual initialized owned graphics byte compared independently in RAM')
                    gfx_proof=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),everyActualByteComparedInRAM=True)
                    (folder/'gfx_memory_proof.json').write_text(json.dumps(gfx_proof,indent=2)+'\\n')
                    log.write('MK2_EARNED_SUBZERO_GFX_DIGEST frame=1 bytes=11944 sha256='+gfx_proof['sha256']+'\\n')
                elif line.startswith('MK2_EARNED_SUBZERO_RGB '):
                    fields=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
                    need(rgb_proof is None and len(raw)==400*254*4,'Actual single native RGB field in RAM')
                    from PIL import Image
                    rgba=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')
                    # Small actual native scene transmitted in RAM for visual inspection; no media files.
                    import base64,io
                    preview=io.BytesIO();rgba.save(preview,format='PNG')
                    print('MK2_NATIVE_SUBZERO_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(preview.getvalue()).decode(),flush=True)
                    rgb_proof=dict(frame=int(fields['frame']),width=400,height=254,bytes=len(raw),
                                   sha256=hashlib.sha256(raw).hexdigest().upper(),rawMediaFilesWritten=0,visualAcceptance=False)
                    (folder/'rgb_memory_proof.json').write_text(json.dumps(rgb_proof,indent=2)+'\\n')
                    log.write('MK2_EARNED_SUBZERO_RGB_DIGEST frame='+fields['frame']+' sha256='+rgb_proof['sha256']+'\\n')
                elif line.startswith('MK2_EARNED_SUBZERO_GUEST '):"""),
 ("nativeCacheOverrunObserved='CACHE_OVERWRITE 'in log,rawMediaGuestFilesWritten=0,fullPortAcceptance=False)",
  "nativeCacheOverrunObserved='CACHE_OVERWRITE 'in log,rawMediaGuestFilesWritten=0,fullPortAcceptance=False,gfxEveryActualByteComparedInRAM=bool(gfx_proof),actualRGBField=rgb_proof,fullShatterAccepted=False,artAccepted=False)"),
 ('need(code==0 and guest_proof and not re.search','need(code==0 and guest_proof and gfx_proof and rgb_proof and not re.search'),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::actual_owned_native_body','exec'),globals())
