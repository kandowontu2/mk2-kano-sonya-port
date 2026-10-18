"""Stage generated native head data and roster roots into the current candidate."""
from pathlib import Path
import shutil
PORT=Path(__file__).resolve().parent
DEST=PORT.parent/'baseline/mk2-rebuild-main/srcp'
assert DEST.is_dir()
for folder,name in (('generated_heads','KSHDART.ASM'),('generated_decap','KSDCART.ASM'),('generated_roster_roots','KSROOT.ASM')):
    shutil.copyfile(PORT/folder/name,DEST/name)
print('Staged authored head data and native roster roots; no executable payload imported.')
for name in ('KSDRAIN.ASM','KSDRART.ASM'):
    shutil.copyfile(PORT/'generated_drain'/name,DEST/name)
shutil.copyfile(PORT/'generated_torso/KSTRART.ASM',DEST/'KSTRART.ASM')
shutil.copyfile(PORT/'generated_projectiles/KSPJROOT.ASM',DEST/'KSPJROOT.ASM')
shutil.copyfile(PORT/'asm/KSPROJ.ASM',DEST/'KSPROJ.ASM')
shutil.copyfile(PORT/'generated_reactions/KSSHRED.ASM',DEST/'KSSHRED.ASM')
shutil.copyfile(PORT/'generated_nut/KSNUTART.ASM',DEST/'KSNUTART.ASM')
shutil.copyfile(PORT/'generated_impale/KSIMART.ASM',DEST/'KSIMART.ASM')
for name in ('KANOMOV.ASM','SONYAMOV.ASM','KSBLADE.ASM','KSBIKE.ASM',
             'KSCHOKE.ASM','KSLEG.ASM','KSFATAL.ASM','KSKISS.ASM',
             'KSLASER.ASM','KSBUBBLE.ASM','KSFRIEND.ASM'):
    shutil.copyfile(PORT/'asm'/name,DEST/name)
