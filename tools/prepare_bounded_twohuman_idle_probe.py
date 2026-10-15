"""Reuse only physical selection and scalar actor sampling; no dense recorder."""
import json
import verify_native_source_sync as sync

ROOT = sync.ROOT

def main():
    pins = sync.verify()
    source = ROOT / 'mk2ks_special_shadow_v5131.lua'
    original = source.read_text()
    prefix = original.split('for _,address in ipairs({spec[2]', 1)[0]
    route = original[original.index('local function route(start,target)'):original.index('emu.register_frame_done(function()', original.index('local function route(start,target)'))]
    begin = original.index('emu.register_frame(function()')
    callback = original[begin:original.index(' if ready then', begin)]
    tail = r'''
 if frame>=3000 then log('FAILED','reason=ready_timeout');manager.machine:exit();return end
 if ready then
  assert(pair_live(a,b),'Native owned pair remains selected')
  if frame-ready>=120 then log('IDLE_TERMINAL','fields=120');manager.machine:exit();return end
  part(1,a);part(2,b)
 end
end)
local idle_fifo= p:install_read_tap(0xff804410,0xff80441f,'bounded idle actual FIFO',function(at)
 if not ready or (frame-ready)%8~=0 or at~=0xff804410 or regs.PC.value~=0xff804420 then return end
 for slot=1,2 do
  local a=sample(slot)
  if a and a.actor==regs.A0.value then
   log('IDLE_FIFO',string.format('slot=%d id=%d pose=%08X source=%08X size=%08X xy=%08X command=%08X y=%d floor=%d action=%04X',
    slot,a.id,a.pose,regs.A11.value,regs.A9.value,regs.A10.value,regs.A12.value,a.y,a.floor,a.action))
  end
 end
end)
emu.register_stop(function()assert(idle_fifo);log('STOP','ready='..tostring(ready)..' raw_media=none')end)
'''
    lua = prefix + route + callback + tail
    for banned in (':write_', ':snapshot(', ':pixels(', 'install_write_tap'):
        assert banned not in lua, banned
    out = ROOT / 'audit_bounded_twohuman_idle_preparation'
    out.mkdir(exist_ok=False)
    target = out / 'prepared_observer.lua'
    target.write_text(lua)
    runner = (ROOT / 'tools/run_bounded_native_uppercut_probe.ps1').read_text()
    runner = runner.replace('$taskRoot=Split-Path $PSScriptRoot -Parent', '$taskRoot="'+str(ROOT)+'"')
    runner = runner.replace('audit_bounded_native_uppercut_runtime', 'audit_bounded_twohuman_sonya_kitana_idle_runtime')
    runner = runner.replace('audit_bounded_native_uppercut_owners_bound_preparation', out.name)
    runner = runner.replace('92F2EBD73A57733ED7638FE90D78F57B10CD238742BB6F02C49BE0123323DE94',sync.sha(target))
    runner = runner.replace("$env:MK2KS_TEST_FIGHTER='kano'", "$env:MK2KS_HUMAN_SPECIAL_MOVE='ring'\n$env:MK2KS_HUMAN_SPECIAL_SIDE='1'\n$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'")
    (out / 'run.ps1').write_text(runner)
    (out / 'report.json').write_text(json.dumps(dict(prepared=True,launched=False,acceptance=False,
        sourceSha=sync.sha(source),observerSha=sync.sha(target),sourceSync=pins,maximumReadyFields=120),indent=2))
    print(json.dumps(dict(prepared=True, observerSha=sync.sha(target))))

if __name__ == '__main__':main()
