"""Fresh reference decoder: native count is16bits; color0 may be7FFF."""
from pathlib import Path
prior=Path(__file__).with_name('prepare_native_subzero_shatter_references_v4860.py')
text=prior.read_text()
before='palette=native.palette(program,palette_address)'
assert text.count(before)==1
text=text.replace(before,'palette=shatter_palette(program,palette_address)',1)
text=text.replace('art_reference_subzero_shatter_v4861','art_reference_subzero_shatter_v4863',1)
before='def main():\n'
after='''def shatter_palette(program,address):
    at=native.off(address)
    count=struct.unpack_from('<H',program,at)[0]
    need(count==64,'Actual original six-bit palette count, not color0/count32 alias')
    colors=[(0,0,0,0)]
    colors.extend((*ui.xrgb555(struct.unpack_from('<H',program,at+2+index*2)[0]),255)for index in range(1,count))
    return colors+[(255,0,255,255)]*(256-count)

def main():
'''
assert text.count(before)==1
text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::corrected_reference4860','exec'),globals())
