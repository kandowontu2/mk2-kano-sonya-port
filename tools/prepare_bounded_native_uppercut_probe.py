"""Prepare, but never launch, a scalar-only natural-input diagnostic.

This is not acceptance evidence. No snapshots, PCM, scanout or retained pixels.
The cold selection prefix is preserved except for removal of snapshot calls.
"""
import json
from pathlib import Path
import verify_native_source_sync as sync

ROOT = sync.ROOT
OUT = ROOT / 'audit_bounded_native_uppercut_preparation'
SOURCE = ROOT / 'mk2ks_physical_p2_cpu_continuation_v3300.lua'
TAIL = r'''
-- Bounded scalar-only probe. CPU decisions and all guest state remain native.
assert(human=='kano','This distinct policy is the physical Kano uppercut probe')
local bounded_fields,bounded_presses=0,0
local function bounded_actor(slot)
    local ap=slot==1 and 0x01060220 or 0x01060df0
    local mp=slot==1 and 0x01060260 or 0x01060e30
    local a,m=selection_p:read_u32(ap),selection_p:read_u32(mp)
    if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then return nil end
    return {a=a,m=m,id=selection_p:read_u16(a+0x1f0),
        x=selection_p:read_i16(a+0x90),y=selection_p:read_i16(a+0xb0),
        floor=selection_p:read_i16(m+0x200),action=selection_p:read_u16(m+0x1f0),
        vy=selection_p:read_u32(a+0x60),gravity=selection_p:read_u32(a+0x20),
        flags=selection_p:read_u16(m+0x210),body=selection_p:read_u16(a+0x160),
        hp=selection_p:read_u16(slot==1 and 0x010602f0 or 0x01060ec0)}
end
emu.register_frame(function()
    if not first_live then
        if selection_frame>=2400 then print('MK2_BOUNDED_STOP reason=no_live_pair');manager.machine:exit() end
        return
    end
    local age=selection_frame-first_live
    if age>=1800 then print('MK2_BOUNDED_STOP reason=field_limit');manager.machine:exit();return end
    local a,b=bounded_actor(1),bounded_actor(2)
    if not a or not b then return end
    bounded_fields=bounded_fields+1
    local press='none'
    local ordinary=selection_p:read_u16(0x010601d0)==2 and
        selection_p:read_u16(0x010601f0)==1 and selection_p:read_u16(0x01060dc0)==0 and
        a.id==17 and a.hp>0 and b.hp>0 and a.y==a.floor and a.vy==0 and a.gravity==0 and
        (a.flags&0x1c)==0 and (a.body&0xc)==0 and (a.action==0 or a.action==0x0303)
    if ordinary then
        if math.abs(a.x-b.x)<120 and age%36<4 then
            high['P1 Down']:set_value(1);high['P1 High Punch']:set_value(1)
            bounded_presses=bounded_presses+1;press='down_highpunch'
        elseif math.abs(a.x-b.x)>50 then
            press=a.x<b.x and 'Right' or 'Left';high['P1 '..press]:set_value(1)
        end
    end
    print(string.format('MK2_BOUNDED_FIELD frame=%d mode=%d p1id=%d p2id=%d hp1=%d hp2=%d action1=%04X action2=%04X x1=%d x2=%d y1=%d floor1=%d press=%s writes=0',
        selection_frame,selection_p:read_u16(0x010601d0),a.id,b.id,a.hp,b.hp,a.action,b.action,a.x,b.x,a.y,a.floor,press))
end)
emu.register_stop(function()
    print(string.format('MK2_BOUNDED_RESULT fields=%d presses=%d writes=0 raw_media=none',bounded_fields,bounded_presses))
end)
'''

def main():
    pins = sync.verify()
    original = SOURCE.read_text()
    marker = "local p=manager.machine.devices[':maincpu'].spaces.program"
    assert original.count(marker) == 1
    prefix = original.split(marker, 1)[0]
    lines = prefix.splitlines()
    snapshots = [line for line in lines if ':snapshot(' in line]
    assert len(snapshots) == 3
    prefix = '\n'.join(line for line in lines if ':snapshot(' not in line)+'\n'
    prepared = prefix+TAIL
    for forbidden in (':write_', ':snapshot(', 'install_write_tap', 'getenv(\'MK2KS_DIAGNOSTIC'):
        assert forbidden not in prepared
    assert '1800' in TAIL and '2400' in TAIL
    OUT.mkdir(exist_ok=False)
    target = OUT / 'prepared_observer.lua'
    target.write_text(prepared, encoding='utf-8')
    report = dict(prepared=True, launched=False, acceptance=False,
        source=str(SOURCE), sourceSha256=sync.sha(SOURCE), observer=str(target),
        observerSha256=sync.sha(target), removedSnapshotCalls=3,
        maximumLiveFields=1800, maximumPreLiveFrames=2400,
        rawMedia='none', retainedFramePixels=False,
        sourceSync=pins, missing='Runtime syntax/control/resource checks and private-cue interruption evidence')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('prepared','launched','acceptance','observerSha256','maximumLiveFields')}))

if __name__=='__main__':
    main()
