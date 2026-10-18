# Published native development snapshot

Repository: https://github.com/kandowontu2/mk2-kano-sonya-port

Commit `1fea6aa3b3137ccd4d8388c4a84a6a0094072a99` was pushed to main and
confirmed by `git ls-remote origin HEAD`.

`native-rom/` contains the121 byte-exact files from the qualified development
IPS package (7,089,916 uncompressed bytes), including59 own ASM modules and
the diff to40 original source files. All staged native files were compared
byte-for-byte before committing. `.gitattributes` disables line-ending
conversion for this tree so the published FILES.json hashes remain meaningful.

The root README now leads with the native stock-MAME/ASM/IPS implementation,
marks it unfinished, and explicitly separates the withdrawn custom-driver
history. The old README was retained as `docs/WITHDRAWN_DRIVER_README.md`.
No final release was created. This snapshot does not include full original
game source, proprietary tools, complete ROM archives or emulator binaries.

The separate local evidence/video/controller work remains development work;
do not infer that every local diagnostic was included in this121-file export.
Publication is not proof of a completed Kano campaign or full-port acceptance.
