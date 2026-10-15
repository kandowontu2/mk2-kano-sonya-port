"""Fresh profiles with actual native leg-area RGB magnification; no sprite editing."""
from pathlib import Path
prior=Path(__file__).with_name('run_native_subzero_dma_pcm_v4966.py')
text=prior.read_text()
for before,after in(('audit_v4967_subzero_','audit_v4970_subzero_'),('audit_v4968_subzero_','audit_v4971_subzero_')):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
# Change the generated host collector only; actual controller/native inputs stay exact.
anchor="exec(compile(text,str(Path(__file__).resolve())+'::actual_native_DMA','exec'),globals())"
assert text.count(anchor)==1
extension='''
before="png=io.BytesIO();Image.frombytes('RGB',(400,254),raw,'raw','BGRX').save(png,format='PNG')"
after="""native_image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')
      png=io.BytesIO();native_image.save(png,format='PNG')
      if len(scenes)==3:
       detail=io.BytesIO();native_image.crop((24,130,108,185)).resize((336,220),Image.Resampling.NEAREST).save(detail,format='PNG')
       print('MK2_NATIVE_SUBZERO_DETAIL_DATAURL data:image/png;base64,'+base64.b64encode(detail.getvalue()).decode(),flush=True)
       pixel_rows=[]
       for y in range(130,185):
        actual=[native_image.getpixel((x,y))for x in range(24,108)]
        pixel_rows.append(dict(y=y,blackPixels=sum(c==(0,0,0)for c in actual),sha256=hashlib.sha256(bytes(v for c in actual for v in c)).hexdigest().upper()))
       (folder/'leg_area_pixel_rows.json').write_text(json.dumps(dict(frame=int(fields['frame']),bounds=[24,130,108,185],rows=pixel_rows,rawMediaFilesWritten=0),indent=2)+'\\n')"""
assert text.count(before)==1
text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::actual_native_DMA_detail','exec'),globals())
'''
text=text.replace(anchor,extension,1)
exec(compile(text,str(Path(__file__).resolve())+'::RAM_only_magnification','exec'),globals())
