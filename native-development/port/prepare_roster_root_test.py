"""Compile/link the candidate roster-root library without mutating old evidence.

This is an object/link test. Final gameplay MUST link all original and new
objects together; never paste this test image into a differently linked game.
"""
from pathlib import Path
HERE=Path(__file__).resolve().parent
BUILD=HERE.parent/'baseline/mk2-rebuild-main'
SRC=BUILD/'srcw'
def main():
    for src,name in [(HERE/'generated_templates_candidate/KANOANI.ASM','KNCAND.ASM'),
                     (HERE/'generated_templates_candidate/SONYAANI.ASM','SNCAND.ASM'),
                     (HERE/'generated_roster_roots/KSROOT.ASM','KSROOT.ASM')]:
        (SRC/name).write_bytes(src.read_bytes())
    link=(SRC/'PORT.CMD').read_text()
    assert 'KANOMOV.OBJ' in link and 'KSNAV.OBJ' in link
    link=link.replace('PORT.OUT','ROOT.OUT').replace('PORT.MAP','ROOT.MAP')
    link=link.replace('KANOANI.OBJ','KNCAND.OBJ').replace('SONYAANI.OBJ','SNCAND.OBJ')
    link=link.replace('MEMORY { ROM: org=0xffe00000, len=0x80000 }',
                      'KSROOT.OBJ\nMEMORY { ROM: org=0xffe00000, len=0x80000 RAM: org=0x01100000, len=0x1000 }')
    link=link.replace('SECTIONS { .text: {} > ROM .data: {} > ROM }',
                      'SECTIONS { .text: {} > ROM .data: {} > ROM .bss: {} > RAM }')
    (SRC/'ROOT.CMD').write_text(link)
    print('Prepared independent root-library test; real game objects not yet changed')
if __name__=='__main__':main()
