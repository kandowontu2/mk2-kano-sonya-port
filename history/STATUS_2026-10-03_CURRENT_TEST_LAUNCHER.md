# Current test launcher available; full port still incomplete

Supersedes the launcher-specific state in the earlier same-day checkpoint.
The six full sampled native secondary rendering cases and52 fresh human
activation/contact/block/miss/recovery cases remain as recorded in v1242.
Candidate1219, executable, payload and game sources have not changed.

PLAY_CURRENT_V1219_TEST_BUILD.cmd now launches that exact current candidate,
using a SHA256 check of both EXE and payload before startup. It clears all
diagnostic-only environment flags and uses isolated play/cfg/nvram/snap paths.
It does not load a diagnostic input script or add selection hints. The older
v786/v737/production launchers and their settings are unchanged. This is a
development playtest launcher, not a final-release promotion.

The first actual CMD boot v1245 failed before starting the emulator because
Windows PowerShell launched from CMD could not resolve Get-FileHash in this
environment. The failed report/log and original launcher/checker/test source
snapshots are preserved. The successor v1246 uses the built-in .NET SHA256
implementation. v1247 ran the actual corrected CMD from another working
directory and completed an ordinary one-second emulator boot with exit0,
without diagnostic autoboot. This is not full interactive/video/audio or
campaign acceptance; current gameplay evidence remains the separate real-input
matches and human matrix. The launcher/checker inputs stayed unchanged during
that successful boot. No material data has been deleted; cleanup and the final
release ZIP remain open, along with the full remaining scope in v1242/status.
