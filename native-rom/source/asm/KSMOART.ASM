; Authored own morph intermediate DATA, acceptance tracked separately.
        .include mainequ.asm
        .data
        .def ks_kano_morph_palette
ks_kano_morph_palette
        .word 65
        .word 00000h,07b73h,07b2ch,07713h,07b02h,07ab0h,076a7h,06e85h
        .word 0628eh,0724dh,06a43h,06a2bh,065eah,05e23h,05de7h,04e2ch
        .word 04dc3h,059a9h,04da4h,045a3h,04161h,05505h,04525h,03941h
        .word 038e4h,02d48h,02d03h,02ce2h,01cc5h,028a2h,018a3h,014a4h
        .word 01084h,07425h,06024h,04823h,04402h,03022h,03402h,01c62h
        .word 01c01h,01083h,01063h,00c63h,00c63h,00c42h,00842h,00c41h
        .word 01001h,00842h,00842h,00821h,00421h,00421h,00421h,00421h
        .word 00021h,00420h,00400h,00000h,00000h,00000h,00000h,00000h
        .word 0
        .def ks_sonya_morph_palette
ks_sonya_morph_palette
        .word 65
        .word 00000h,07fffh,07fffh,07f97h,07f47h,07bdeh,0779ah,0739ch
        .word 06b5bh,07f12h,07f03h,07ad0h,07ac6h,06318h,06ea7h,052d8h
        .word 03adah,0766eh,0764ah,06668h,06640h,06e0bh,06207h,065c9h
        .word 05dc9h,0524fh,055e2h,051c5h,04dc0h,03a56h,03dcbh,02a57h
        .word 021d4h,05588h,04d46h,04580h,04545h,03963h,03522h,0216eh
        .word 02128h,038e4h,030e3h,028e2h,024a2h,018e9h,018c3h,01483h
        .word 01861h,00cech,00ca9h,00c64h,00c62h,00842h,00842h,00422h
        .word 00421h,00420h,00421h,00400h,00000h,00000h,00000h,00000h
        .word 0
        .def ks_mo_kano_frame0,ks_mo_kano_pose0
ks_mo_kano_frame0
        .word 78,129,39,-2
        .long 00713c9d0h
        .word 06000h
        .long ks_kano_morph_palette
ks_mo_kano_pose0
        .long ks_mo_kano_frame0,0
        .def ks_mo_kano_frame1,ks_mo_kano_pose1
ks_mo_kano_frame1
        .word 78,128,39,-3
        .long 00714b5a8h
        .word 06000h
        .long ks_kano_morph_palette
ks_mo_kano_pose1
        .long ks_mo_kano_frame1,0
        .def ks_mo_kano_frame2,ks_mo_kano_pose2
ks_mo_kano_frame2
        .word 82,131,41,0
        .long 007159fa8h
        .word 06000h
        .long ks_kano_morph_palette
ks_mo_kano_pose2
        .long ks_mo_kano_frame2,0
        .def ks_mo_sonya_frame0,ks_mo_sonya_pose0
ks_mo_sonya_frame0
        .word 78,132,39,0
        .long 007169b70h
        .word 06000h
        .long ks_sonya_morph_palette
ks_mo_sonya_pose0
        .long ks_mo_sonya_frame0,0
        .def ks_mo_sonya_frame1,ks_mo_sonya_pose1
ks_mo_sonya_frame1
        .word 79,132,39,0
        .long 007178cc0h
        .word 06000h
        .long ks_sonya_morph_palette
ks_mo_sonya_pose1
        .long ks_mo_sonya_frame1,0
        .def ks_mo_sonya_frame2,ks_mo_sonya_pose2
ks_mo_sonya_frame2
        .word 78,132,39,0
        .long 007188128h
        .word 06000h
        .long ks_sonya_morph_palette
ks_mo_sonya_pose2
        .long ks_mo_sonya_frame2,0
