"""Fresh qualifier correction: source faults confined to added reviewed block."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_native_subzero_bodies_v4923.py')
text=prior.read_text()
for before,after in (
 ("need(text.count(before)==1,'Unique actual source fault anchor')","need(block.count(before)==1,'Unique actual source fault anchor')"),
 ('source_gate(text.replace(before,after,1),base_text)','source_gate(text.replace(block,block.replace(before,after,1),1),base_text)'),
 ("('wrong_native_pixel',asset['fighters'][0]['parts'][0]['pixelOffset'],'<B',0)",
  "('wrong_native_pixel',asset['fighters'][0]['parts'][0]['pixelOffset'],'<B',payload[asset['fighters'][0]['parts'][0]['pixelOffset']]^1)"),
 ('audit_v4924_native_subzero_bodies_source_checked','audit_v4931_native_subzero_bodies_source_checked'),
 ('SOURCE,BASE,Path(__file__).resolve(),ASSET','SOURCE,BASE,Path(__file__).resolve(),prior,ASSET'),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::corrected_qualifier4923','exec'),globals())
