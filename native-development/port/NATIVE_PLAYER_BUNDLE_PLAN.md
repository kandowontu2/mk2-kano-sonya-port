# Minimal native player bundle preparation

`audit_stock_mame_distribution.py` verifies the local official0.289 x64
installer against GitHub release metadata SHA256
A1AA7912168C9D1B05E611906BC21B8B9BE3935822AEAD36D12A1DA363150B7D.
It streams each selected member through7-Zip without extracting files and
compares the existing runtime/font/COPYING/eight docs/legal files byte-for-byte.
All11 members pass. The tested mame.exe is the official installer member,
SHA256AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3;
this is stronger provenance than merely naming a file stock MAME.

Official release/source metadata:
https://github.com/mamedev/mame/releases/tag/mame0289
https://api.github.com/repos/mamedev/mame/releases/tags/mame0289
License information: https://docs.mamedev.org/license.html

The planned player patch payload contains14 IPS files plus manifest, patcher,
IPS codec, two CMD launch/patch scripts, movelist and instructions (21 files).
Do not carry over the developer121-file FILES.json into this smaller layout;
generate a matching player-file manifest. Player instructions must be adapted
to the split player/source layout, not falsely claim source/asm is inside.
Readable59-module native ASM/40-file source diff remain in the separate native
source package and public GitHub source tree. Do not include complete game
ROMs, test dumps, raw recordings, debug symbols, old builds or developer tools
in the player ZIP. No final ZIP has been created by this planning/audit script.

The official corresponding MAME source asset is mame0289s.exe,159028505 bytes,
SHA2566243EAC3A80DF6BE602BF0AF7889305691737BC26C2DED1433EC11B7C6A3C7B9.
Plan it as a separate source asset alongside the binary player download;
it has not been downloaded yet. Preserve upstream notices and complete the
source/redistribution review before publishing, not merely a vague source
promise. The local JSON records correspondingSourceAsset.presentAndHashVerified=false
and releaseApproved=false.

Open: earned Kano campaign/video, final audiovisual/release acceptance,
final release-manifest/patcher/player-document validation, and corresponding
emulator source asset/redistribution review. No native game or ROM bytes changed.
