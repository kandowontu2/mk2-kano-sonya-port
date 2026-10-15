"""Correct one manual high-word transcription, not any native game bytes.

Canonical palette record is FFFE2800, so its complemented comparison operand
is 0001D7FF, not0100D7FF. Preserve the prior explicit-word rejection.
"""
from pathlib import Path
import qualify_native_selector_sonya_death_raw_pool_owned_reset as previous

ROOT=previous.ROOT
WORD_SOURCE=Path(previous.__file__)
WORD_FAILURE=previous.OUT/'failure.json'
helper=WORD_SOURCE.read_text()
before='0x0b60,0xd7ff,0x0100,0xcb80'
previous.failed.need(helper.count(before)==1,'One erroneous manually transcribed palette operand high word')
helper=helper.replace(before,'0x0b60,0xd7ff,0x0001,0xcb80',1)
helper=helper[helper.index('def hook_gate(guest):'):helper.index('\n\nsource=SOURCE.read_text()')]
namespace=dict(vars(previous))
exec(compile(helper,__file__+'::canonical_complemented_palette_operand','exec'),namespace)
source=previous.source
source=source.replace("OUT=ROOT/'audit_native_selector_sonya_death_raw_pool_owned_reset_checked'",
                      "OUT=ROOT/'audit_native_selector_sonya_death_raw_pool_palette_word_checked'",1)
before='for p in (Path(__file__),SOURCE,FAILURE,previous.OUT/'
previous.failed.need(source.count(before)==1,'Complete predecessor source/failure pins')
source=source.replace(before,'for p in (Path(__file__),WORD_SOURCE,WORD_FAILURE,SOURCE,FAILURE,previous.OUT/',1)
scope=dict(previous.scope,__file__=__file__,WORD_SOURCE=WORD_SOURCE,WORD_FAILURE=WORD_FAILURE,hook_gate=namespace['hook_gate'])
exec(compile(source,__file__+'::same_whole_native_pool_gate_correct_palette_word','exec'),scope)
OUT,gate,execute,safe_execute=(scope[k] for k in ('OUT','gate','execute','safe_execute'))
