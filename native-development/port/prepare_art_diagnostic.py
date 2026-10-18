"""Build a native, source-only art scene without changing the baseline files."""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
BUILD=HERE.parent/'baseline/mk2-rebuild-main'
SRC=BUILD/'srcw'
def main():
    original=(SRC/'MKSEL.ASM').read_text()
    marker='\tcalla\tmulti_plane\t\t; player select background !!'
    assert original.count(marker)==1
    diagnostic=original.replace(marker,marker+'\n\t.ref ks_art_scene\n\tjauc ks_art_scene ; source-built asset diagnostic only')
    (SRC/'KSSEL.ASM').write_text(diagnostic)
    (SRC/'KSART.ASM').write_bytes((HERE/'diagnostics/KSART.ASM').read_bytes())
    link=(SRC/'MK2NEWW.CMD').read_text()
    assert len(re.findall(r'(?i)\bmksel\.obj\b',link))==1
    link=re.sub(r'(?i)\bmksel\.obj\b','KSSEL.OBJ',link)
    link=link.replace('-o mk2neww.out','-o ARTTEST.OUT').replace('-m mk2new.map','-m ARTTEST.MAP')
    marker='MEMORY        '
    assert link.count(marker)==1
    link=link.replace(marker,'KSART.OBJ\nKANOMOV.OBJ\nSONYAMOV.OBJ\nKSCMD.OBJ\nKANOART.OBJ\nSONYAART.OBJ\nKSANIM.OBJ\nKANOANI.OBJ\nSONYAANI.OBJ\n\n'+marker)
    (SRC/'ARTTEST.CMD').write_text(link)
    learn=(SRC/'rom/ff8w.lrn').read_text()
    assert '..\\MK2newW.OUT' in learn
    (SRC/'rom/ART.LRN').write_text(learn.replace('..\\MK2newW.OUT','..\\ARTTEST.OUT').replace('U12','A12'))
    print('Prepared alternate selection module and real full-game linker command; baseline sources unchanged')
if __name__=='__main__': main()
