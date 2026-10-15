"""Entire existing terminal-first RAM collector, genuine Kano P2 stage advance."""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_launch_interruption_v6681 as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
source = inspect.getsource(previous.run)
edits = [
    ('audit_v6682_launch_interrupt_', 'audit_launch_stage_advance_'),
    ("MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay)",
     "MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay),MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='2',MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat',MK2KS_TEST_BOOT_FRAME='600'"),
    ("'-snapsize','400x254','-str','100'", "'-snapsize','400x254','-str','310'"),
    ("carrier['rgb'].append(head)", "carrier['rgb'].append(head);carrier.setdefault('rgbFrames',[]).append(dict(header=dict(head),pixels=raw))"),
    ('Path(__file__),Path(current.__file__)',
     "Path(__file__),Path(previous.__file__),ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua',ROOT/'mk2ks_single_continue_controls_v6579.lua',ROOT/'mk2ks_launch_ko_round.lua',ROOT/'mk2ks_launch_interrupt_v6680.lua',Path(current.__file__)"),
    ("MK2_INTERRUPT_ENTRY ',line)", "MK2_INTERRUPT_ENTRY |MK2_NAT_CAMPAIGN_(ADVANCE|WIN|WALK|JUMP|PUNCH|RECOVER|STAGE_RESULT|LOSS) ',line)"),
]
for before, after in edits:
    need(source.count(before) == 1, 'Exact complete terminal-first collector adaptation: ' + before)
    source = source.replace(before, after, 1)
scope = dict(vars(previous), __file__=__file__, previous=previous,
             LUA=ROOT/'mk2ks_launch_stage_advance.lua', LAST_CAPTURE=None)
exec(compile(source, __file__+'::whole_terminal_first_earned_stage_RAM_transport', 'exec'), scope)


if __name__ == '__main__':
    text = (ROOT/'mk2ks_launch_stage_advance.lua').read_text()
    need(not re.search(r'write_u\d+|write_i\d+|:write_|load_?state|\.value\s*=(?!=)', text),
         'Physical controls/passive observer only, no state or health assistance')
    try:
        scope['run']('ball', 2, 1)
    except Exception as error:
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
    if scope['LAST_CAPTURE']:
        code.interact(banner='Same-terminal earned stage advance; all source PCM/DAC/ROM and RGB retained in RAM.',
                      local=dict(capture=scope['LAST_CAPTURE']))
