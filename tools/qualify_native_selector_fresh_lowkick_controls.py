"""Actual corrected-control history, not all interruption or port acceptance."""
import json
import re
import traceback
from pathlib import Path

import capture_native_selector_sonya_cpu_air_approach as air
import qualify_native_selector_existing_sonya_travel_phases as source
import verify_native_source_sync as sync

ROOT = sync.ROOT
OUT = ROOT / 'audit_native_selector_fresh_lowkick_controls_checked'
CAPTURE = ROOT / 'audit_native_selector_lowkick_after_host_exit_bound_capture_checked/report.json'
ledger = air.previous.base.choices.native_state


def gate(text, guest):
    source.source_gate(text, guest)
    whole = ledger.gate(text, guest)
    choices = air.previous.base.choices.choices_gate(text, guest, whole['schedule'])
    fields = ledger.original.pair.rows(text, 'FIELD')
    by = {r['frame']: r for r in fields}
    inputs = ledger.rows(text, 'MK2_CPU_PAIR_LOWKICK_INPUT')
    cold = ledger.rows(text, 'MK2_P2CPU_COLD_LIVE')
    sync.need(len(cold) == 1 and cold[0]['human_id'] == '17' and cold[0]['cpu_id'] == '18',
              'Actual true-identity cold admission, not a proxy name')
    first = int(cold[0]['frame'])
    sync.need(len(fields) == len(by) == len(inputs) and {int(r['frame']) for r in inputs} == set(by),
              'One corrected physical command per actual live callback')
    toward_count = kick_count = 0
    for row in inputs:
        frame = int(row['frame'])
        r = by[frame]
        vx = r['vvx'] if r['vvx'] < 0x80000000 else r['vvx'] - 0x100000000
        clean = (r['vypos'] == r['vfloor'] and r['vvy'] == r['vgravity'] == r['vtrail'] == 0
                 and r['vflags'] & 0x1c == 0 and r['vbody'] & 12 == 0
                 and (vx == 0 or r['vaction'] == 0x303 and abs(vx) <= 0x30000))
        eligible = r['vhp'] > 0 and r['hp'] > 0 and clean
        gap = abs(r['x'] - r['vxpos'])
        toward = eligible and gap > 70
        kicking = eligible and (frame - first) % 18 < 3
        sync.need(row['policy'] == 'walk_lowkick' and row['writes'] == '0' and row['assistance'] == 'none'
                  and row['cpu_slot'] == '2' and row['human_slot'] == '1'
                  and tuple(int(row[k]) for k in ('eligible','gap','toward','kicking')) ==
                  (int(eligible), gap, int(toward), int(kicking)),
                  'Every command follows real readiness/spacing and original corrected cadence')
        toward_count += toward
        kick_count += kicking
    sync.need(toward_count > 0 and kick_count > 0 and any(r['vaction'] == 0x303 and r['vvx'] for r in fields),
              'Actual walking and corrected kick-command branch exercised')
    bind = ledger.rows(text, 'MK2_LOWKICK_BIND')
    sync.need(bind == [dict(count='1',controller='original_physical_P1',inputs='walk_lowkick',writes='0',assistance='none')],
              'Exactly one actual original physical controller')
    return dict(wholeNativeHealthState=whole, allActuallyObservedCPUChoices=choices,
                actualLiveCallbacks=len(inputs), towardCommands=toward_count, lowKickCommands=kick_count,
                actualHumanActionFields={str(k): sum(r['vaction'] == k for r in fields) for k in sorted({r['vaction'] for r in fields})},
                actualCorrectedControlPolicySourceBound=True, wholePhysicalPortBytesAccepted=False,
                individualKickAttackInstructionsAccepted=False, privateVoiceInterruptionAccepted=False,
                fullPortAcceptance=False)


def execute(prepared):
    sync.need(not OUT.exists(), 'Fresh actual corrected-control evidence')
    proof = json.loads(CAPTURE.read_text())
    key = prepared.SCOPE['KEY']
    handle = prepared.NATIVE_HANDLES[key]
    sync.need(proof['passed'] and handle['process'].poll() == 0 and handle['identity'] == proof['actualNativeIdentity'],
              'Same actual native terminal, no replay')
    pins = dict(proof['inputHashes'])
    sync.need(all(sync.sha(p) == h for p,h in pins.items()), 'Whole unchanged actual capture inventory')
    text = prepared.RAM_CASES[key][1]
    result = gate(text, prepared.STATE['guest'])
    def change(tag, key, value, **where):
        line = next(s for s in text.splitlines() if s.startswith(tag + ' ') and
                    all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k) == str(v) for k,v in where.items()))
        bad, count = re.subn(r'\b' + key + r'=\S+', key + '=' + str(value), line, count=1)
        sync.need(count == 1 and bad != line, 'Effective actual-record fault')
        return text.replace(line, bad, 1)
    command = next(r for r in ledger.rows(text,'MK2_CPU_PAIR_LOWKICK_INPUT') if r['kicking'] == '1')
    dose = ledger.rows(text,'MK2_CPU_ROUND_HEALTH')[0]
    faults = []
    for label, bad in (
        ('actual_kick_command',change('MK2_CPU_PAIR_LOWKICK_INPUT','kicking',0,frame=command['frame'])),
        ('actual_spacing',change('MK2_CPU_PAIR_LOWKICK_INPUT','gap',-1,frame=command['frame'])),
        ('actual_readiness',change('MK2_CPU_PAIR_LOWKICK_INPUT','eligible',0,frame=command['frame'])),
        ('actual_human_identity',change('MK2_CPU_PAIR_FIELD','vid',1,frame=command['frame'])),
        ('actual_cpu_identity',change('MK2_CPU_PAIR_FIELD','id',17,frame=command['frame'])),
        ('actual_native_health_instruction',change('MK2_CPU_ROUND_HEALTH','op0','FFFF',frame=dose['frame'],slot=dose['slot'])),
        ('duplicate_controller',text + next(s+'\n' for s in text.splitlines() if s.startswith('MK2_LOWKICK_BIND '))),
        ('missing_actual_command',text.replace(next(s+'\n' for s in text.splitlines() if
            s.startswith('MK2_CPU_PAIR_LOWKICK_INPUT ') and 'frame='+command['frame']+' ' in s),'',1)),
    ):
        try:
            gate(bad, prepared.STATE['guest'])
        except (AssertionError,ValueError,KeyError,IndexError) as error:
            faults.append(dict(kind=label,rejectedBy=str(error)))
        else:
            raise AssertionError('Effective corrected-control fault admitted: ' + label)
    sync.need(len(faults) == 8 and gate(text, prepared.STATE['guest']) == result,
              'All eight faults reject and complete positive restores')
    for p in (Path(__file__),Path(source.__file__),CAPTURE):
        pins[str(p.resolve())] = sync.sha(p)
    sync.need(all(sync.sha(p) == h for p,h in pins.items()), 'Final fresh whole-file inventory')
    report = dict(passed=True, goalStatus='active', actualNativeIdentity=handle['identity'],nativeExit=0,
                  actualCorrectedControls=result, effectiveFaultRejections=faults,inputHashes=pins,
                  fullPortAcceptance=False, publicPlayableChanged=False,newNativeGames=0,
                  newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,callbacks=result['actualLiveCallbacks'],
                          lowKickCommands=result['lowKickCommands'],faults=len(faults),fullPortAcceptance=False)),flush=True)
    return report


def safe_execute(prepared):
    try:
        return execute(prepared)
    except Exception as error:
        sync.need(not OUT.exists(), 'Preserve original corrected-control rejection')
        OUT.mkdir()
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        return None
