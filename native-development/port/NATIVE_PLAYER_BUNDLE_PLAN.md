# Minimal native player bundle preparation

Current player checkpoint: V3 adds the native first-boot CMOS acknowledgment
instructions. development_patches/MK2KS_NATIVE_PLAYTEST_WITH_STOCK_MAME_V3.zip
is98,257,403 bytes, SHA256
7C6EDA1CB0662512F14012FE55F966D54BA1DF7144E1E1871E8B0E9BBB9D58DE.
All33 member/hash checks, exact-ROM clean patch reproduction and468 unit tests
pass. A fresh V3 configuration reaches native attract mode through physical
High Punch acknowledgment and completes3600 fields, exit0/no Lua/fatal error.
PLAYER_HEADLESS_ATTRACT_ACK.json now binds that test to V3. No emulator remains;
all temporary files are removed. Verified superseded V2 was deleted to avoid
another94MiB duplicate; source/history and rebuild inputs remain. Older
version-specific receipts below are historical, not current artifact claims.

Fresh V3 combat follow-up: two separate9000-field runs reconstruct the exact
ROM in temporary player folders, use the hash-identical stock executable and
-noreadconfig, and select both added characters using physical inputs only.
PLAYER_HEADLESS_COMBAT.json and PLAYER_HEADLESS_COMBAT_MIRROR.json preserve
their frozen controllers, state traces, package/executable hashes and logs.
Both exit0 with no Lua/fatal errors. The acceptance gate requires600+ fields
with both human states1, locked selection, actual object identities17/18 in
the requested sides, damage to both sides, and no missing-animation marker.
It rejects CPU/proxy/unlocked/no-damage/short cases in unit tests.470 complete
unit cases pass. The first receipt's scope text predates the combat-specific
wording and conservatively says startup-only; its preserved combat trace and
explicit combat object establish the finite result, not a broad completion
claim. The frozen controller itself contains its normal physical startup
High Punch acknowledgment despite the older first receipt's false explicit
acknowledgment-profile flag; that flag must not be read as absence of input.
This is finite clean-player selection/combat evidence, not every move,
interactive rendering/audio, campaign or final release acceptance. Temporary
ROMs/executable links/settings are removed and no emulator remains.

The current local player artifact is now
development_patches/MK2KS_NATIVE_PLAYTEST_WITH_STOCK_MAME_V2.zip,
98,257,174 bytes, SHA256
7D3517D9882286AD2FFAB8C0E8CD83267DC4E4557457D936FA3ACA87C3EEF7C2.
Its PLAY.cmd explicitly uses -noreadconfig, retaining isolated cfg/nvram/snap
paths while ignoring unrelated default MAME INI settings. Stock MAME accepts
the option in a hidden -showconfig check; no interactive game was launched.
All33 member hashes and clean-folder exact-ROM patch reproduction pass;
466 unit tests pass. The earlier ZIP below is superseded. This launcher-only
player override does not alter native ROM bytes or final release approval.

Fresh-folder headless follow-up: qualify_player_headless_boot.py extracts the
actual V2 patch/player inputs, verifies their ZIP member hashes, reproduces
the exact tested ROM, and hard-links the hash-identical official executable
instead of copying316MiB. With the same isolated launch paths and
-noreadconfig plus explicit headless test options, stock MAME exits0 after
600 observed fields with changing CPU PCs and no Lua/fatal error. The
observer only reads native state; no input or game-memory forcing is used.
Temporary patched ROM, executable link, settings and observer are removed.
PLAYER_HEADLESS_BOOT.json preserves package/emulator binding, frozen observer,
observations and log. This proves short startup, NOT interactive rendering,
combat, audio output, campaign completion or final release acceptance.

First-boot follow-up: an unattended3600-field fresh-config run stayed in
native CMOS startup; PLAYER_HEADLESS_ATTRACT_NO_INPUT.json retains this failed
attract gate. DIAGDTST.ASM powercmos/cmosret/ctmp1 explicitly waits for a
button-state change after initializing invalid CMOS. A second fresh-config
run uses only physical P1 High Punch pulses after field1000 until attract
mode1 is observed. It reaches attract and completes3600 fields, exit0 with
no Lua/fatal error; PLAYER_HEADLESS_ATTRACT_ACK.json retains the exact observer,
state/PC samples, package/emulator hashes and log. No guest-memory writes,
coins, starts, selected characters or forced game state are used.
Player instructions must explain the native first-boot prompt: press an attack
button (tested P1 High Punch) to acknowledge initialized CMOS, then insert
coin/start normally. No prefilled NVRAM or bypass patch should be shipped.
The initial failed invocation predated retained failure reporting and cleaned
its temporary folder; its explicit repeat now preserves the failed observation
in JSON. Neither fresh startup test certifies interactive rendering or combat.

Local playtest checkpoint (2026-10-18): the minimal player bundle now exists
as development_patches/MK2KS_NATIVE_PLAYTEST_WITH_STOCK_MAME.zip (98,257,167
bytes), SHA256
30F7E0FBF9D91FF2EACB246EAFF404485F7E0D308D64076798BA148D25474D18.
PLAYER_PLAYTEST_QUALIFICATION.json records its isolated patcher reproduction
of the exact tested ROM and removal of the temporary ROM. Independent tests
re-read all 33 ZIP members, all member hashes, the ZIP hash, 14 IPS files and
unfinished/source-split instructions. The complete local unit suite passes
460 cases. No MAME window, gameplay replay or new audiovisual acceptance is
implied by these packaging tests. This is not a public/final release.

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
Plan it as a separate source asset alongside the binary player download.
It has now been downloaded and verified, as recorded below. Preserve upstream notices and complete the
source/redistribution review before publishing, not merely a vague source
promise. The local distribution JSON now records the source as present and
hash-verified, while releaseApproved remains false.

Update: fetch_stock_mame_source.py has now obtained the exact159028505-byte
official asset and verified the pinned SHA256. It was not executed or extracted,
and no extra source tree was created. STOCK_MAME_SOURCE_0289.json records the
actual asset proof; a fresh distribution audit marks it present/hash-verified.
This closes asset availability, not final redistribution or release approval.

Open: earned Kano campaign/video, final audiovisual/release acceptance,
final release-manifest/patcher/player-document validation, and corresponding
emulator source asset/redistribution review. No native game or ROM bytes changed.
