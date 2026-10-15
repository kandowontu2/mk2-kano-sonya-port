# MK2 Kano/Sonya — native combat identity milestone (v37)

Historical milestone, superseded by [native selector/ladder v38](STATUS_2026-09-04_NATIVE_SELECTOR.md). The installed executable and current test evidence are documented there.

The overall native-character port is **not complete**. This build fixes canonical combat identity, native HUD/victory naming, Sonya's gender-dependent behavior, and the first-hit crash exposed by using real roster IDs. Native CSS/ladder integration, P2 selection, and complete character-specific moves remain open.

## Installed build

- Workspace: `C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port`
- Executable: `mame-mkp\mkport.exe`
- Executable SHA-256: `0AADD5B178D5243296975D8F2989F9B4E39283DE4998DBA5C1F84AB9651221F2`
- Animation payload remains the verified v36 `mk2ks.mdata`: SHA-256 `52F04600688052C5D3FA8FC1294961A271F03B80AB1C50B8132B72DF296CEB4A`.
- Launcher: `C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\PLAY_MK2_KANO_SONYA.cmd`
- The CMD forwards to this workspace and its `-verifyroms` check passes. Build and `git diff --check` pass.
- This requires the custom executable; it is not a standalone ROM for unmodified MAME.

## What changed

The canonical P1 variable now holds `11h` for Kano / `12h` for Sonya before the game's HUD and fighter construction. The native constructor copies that ID into the live object and uses its own palette/ground-height entries. The old video-loop and animation-root writes forcing the live ID have been removed, as has the first-HUD position correction.

New native tables contain independent HUD frames and correctly placed name entries, native-font KANO WINS / SONYA WINS text scripts, entrance alignment, and damage-scaling entries. The host-side HUD replacement function was deleted; MKII now draws the added names through its normal display list and DMA path. Original stock table entries are preserved. P2 name-table entries are prepared but P2 custom selection is not implemented.

Using the actual roster ID exposed a previously hidden crash: the native damage-scaling table ended at ID `10h`. Kano/Sonya indexed adjacent machine instructions as callback pointers and trapped on the first hit. The added entries now use normal human-fighter damage handling.

Sonya is included in the native female predicates for the finish prompt, hit voice and related reaction. The branches retain all existing female fighters; no temporary identity alias is used. New winner-announcer entries use the game's explicit skip value until custom voice samples exist, instead of announcing Liu or reading random instructions as sound commands.

## Verification — 32 accepted cases

All tests below use real controller input, isolated config/NVRAM, and no gameplay RAM pinning or diagnostic roster writes. Custom cases check both canonical and live identity. No stalls, CPU traps, selector portrait leaks, or HUD-name mismatches occurred in the accepted cases.

| Check | Result and evidence |
| --- | --- |
| Six confirmation buttons, both fighters | 12 passes, `regression_native_accepted_{kano,sonya}_{hp,hk,lp,lk,block,block2}`. Kano/Sonya: 1,737/1,647 HUD-visible fields per case, zero identity/name/leak errors. |
| Timer expiry, both fighters | 2 passes, `regression_native_verified_{kano,sonya}_timeout`. 906 HUD-visible fields each, actual roster IDs retained. |
| Recovery, next-round reset and post-defeat release | 2 passes, `regression_native_accepted_{kano,sonya}_lifecycle`. 2/1 recoveries, one native next-round reset each, correct ground anchors, zero identity/position errors. |
| Ordinary animation dispatch | 2 passes, `regression_native_final_{kano,sonya}_move0`: 20 basic checks per fighter, 2,227 combat frames each. |
| Four shortcut special paths, both fighters | 8 passes, `regression_native_final_{kano,sonya}_move{1,2,3,4}`: 2,227 combat frames each, zero canonical/live-ID errors, stalls or traps. This does not certify complete move semantics. |
| Two-player P1 wins | 2 passes, `regression_native_final_{kano,sonya}_win`. Two native win-script reads each; 2,346 HUD-visible fields. Screenshots `snap/mk2ks/0020.png` show their own poses and names, without selector overlays. |
| Sonya's native defeat prompt | 1 pass, `regression_native_final_sonya_loss`: real-input defeat selects sound `15h`, message `2`; screenshot `snap/mk2ks/0019.png` shows FINISH HER. |
| Stock victory control | 1 pass, `regression_native_final_stock_win`. The same blue text phase is visible in Liu's native victory screenshot, confirming the custom names preserve native palette behavior. |
| Stock selector-exit control | 1 pass, `regression_native_accepted_reptile_lp`, no portrait leaks. |
| Repeated Sonya/Reptile navigation and visuals | 1 pass, `regression_native_verified_navigation`: 10 checks, matching 1,064 border pixels and 66 number pixels, two blink colors, animated pose and zero backdrop shift. |

The names displayed in combat and victory were visually inspected. Blue victory lettering at the captured phase also appears in the unchanged stock Liu control; it is native behavior.

## Test corrections, not hidden game fixes

The stronger observers initially reported identity errors while inspecting freed memory. At CONTINUE, MKII clears its live P1 pointer and reuses the old allocation for text while the previous HUD fades. The test now follows the authoritative P1 pointer, requiring the explicit native loss/continue state before accepting an absent actor. It also permits the observed one-field publication delay during next-round construction, bounded to two fields after a real native HUD-table read with full health and the native setup mode. A missing actor elsewhere still fails. No object-ID pin was restored to make these checks pass.

Finish-prompt parameters are checked at the native write, not one frame later after the process has repurposed those fields. Earlier failed v37 first-hit cases are genuine crashes; earlier final/verified lifecycle failures are separately documented observer defects. The accepted case paths above are the final evidence.

## Remaining work

- Replace the CSS input bridge and ladder display replacement with native roster integration. The new canonical identity is committed at combat setup, not yet throughout selection/ladder.
- P2 custom selection, mirrors and complete two-cursor behavior.
- Independent character-specific special commands, behavior, timing, damage and hitboxes. Current shortcut paths still use shared MKII combat routines with imported animations.
- Custom voice samples/announcements, finishers, AI roster participation, later ladder progression, endings and complete continue/post-match behavior.
- Complete animation coverage; v36's missing mappings and frame-count mismatches still need review.

`NATIVE_ROSTER_FOLLOWUP.md` records native addresses, runtime storage allocations, reproduced failures and next-step details. The full user goal remains active.
