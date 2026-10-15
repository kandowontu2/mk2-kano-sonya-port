"""Preserve first checker rejection; use all19 actual terminal Lua errors.

The earlier14 count was a live stderr snapshot, not final evidence. Ownership
math, all snapshots, source timing and fault gates remain unchanged.
"""
import json
from pathlib import Path
import qualify_native_selector_sonya_voice_owner_eof as original

failure=original.OUT/'failure.json'
original.need(json.loads(failure.read_text())['error']==
    "AssertionError('Exact actual missing-input errors preserved and excluded from gameplay acceptance')",
    'Original live-count checker rejection preserved')
source=Path(original.__file__).read_text()
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_errors_checked'"),
    ("errors.count(marker)==14", "errors.count(marker)==19"),
    ("actualOriginalLuaErrors=14", "actualOriginalLuaErrors=19"),
    ("for p in (Path(__file__),CAPTURE,", "for p in (Path(__file__),Path(original.__file__),failure,CAPTURE,")):
    original.need(source.count(before)==1,'Only exact actual terminal-error count and failure preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_owner_eof_actual_terminal_stderr_inventory','exec'))
