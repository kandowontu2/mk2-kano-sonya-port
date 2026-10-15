"""Finite recorded hit/recovery regression; not complete move/port acceptance."""
import copy
import json
import traceback

import qualify_native_selector_fresh_lowkick_controls as controls
import verify_native_source_sync as sync

OUT = sync.ROOT / 'audit_native_selector_fresh_lowkick_recovery_checked'


def episode(fields, flags, health):
    by = {r['frame']: r for r in fields}
    sync.need(all(f in by for f in range(1911, 1961)), 'Complete contiguous hit/recovery observations')
    for f in range(1911, 1955):
        r = by[f]
        sync.need((r['vid'], r['id'], r['vactor'], r['vmain']) ==
                  (17, 18, 0x01034e90, 0x0106a370), 'Real Kano actor and Sonya victim throughout')
        sync.need(r['vaction'] == (0x104 if f <= 1934 else 0x60c)
                  and r['vbody'] == 0x16 and r['vflags'] == 0x11,
                  'Actual complete attack and retraction state interval')
    expected_intro = [0xff00f560, 0xff00f5c0, 0xff00f600, 0xff00f640, 0xff00f680]
    sync.need([by[f]['vpose'] for f in range(1911, 1916)] == expected_intro
              and all(by[f]['vpose'] == 0xff00f6c0 for f in range(1916, 1935)),
              'Recorded own low-kick intro and contact hold poses')
    expected_reverse = [p for p in reversed(expected_intro) for _ in range(4)]
    sync.need([by[f]['vpose'] for f in range(1935, 1955)] == expected_reverse,
              'Recorded five-pose four-field reverse sequence')
    damage = [r for r in health if r['frame'] == '1916' and r['slot'] == '2']
    sync.need(len(damage) == 1, 'One actual contact health store')
    d = damage[0]
    sync.need(tuple(d[k] for k in ('before','after','pc','a8','a13','op0','op1','op2','ids','writes','assistance')) ==
              ('161','135','FF836700','01034E90','0106A370','CF01','5621','8026','17,18','0','none'),
              'Actual native damage instruction and real attack ownership')
    sync.need(by[1916]['hp'] == 161 and by[1917]['hp'] == 135, 'Health store brackets actual fields')
    for kind, before, after, pc, op, offset in (
        ('action','060C','0000','FF83EDD0','B00D','01F0'),
        ('body','0016','0012','FF83EEB0','B088','0160'),
        ('flags','0011','0001','FF83EFC0','B08D','0210'),
    ):
        sync.need(any(r['frame']=='1954' and r['slot']=='1' and r['kind']==kind
                      and tuple(r[k] for k in ('before','after','pc','op0','op1','actor','main','id')) ==
                      (before,after,pc,op,offset,'01034E90','0106A370','17') for r in flags),
                  'Actual native cleanup store: ' + kind)
    for f in (1955,1956):
        r = by[f]
        sync.need((r['vaction'],r['vbody'],r['vflags']) == (0x303,0x12,1)
                  and r['vypos']==r['vfloor'] and r['vvy']==r['vgravity']==r['vtrail']==0,
                  'Actual grounded ordinary walking after cleanup')
    sync.need(all((by[f]['vbody'],by[f]['vflags'])==(0x12,1) for f in (1957,1958,1959))
              and (by[1960]['vbody'],by[1960]['vflags'])==(0x1a,5)
              and by[1960]['vhp'] < by[1959]['vhp'], 'Later hurt is separate from completed kick recovery')
    return dict(hitFrame=1916, health=[161,135], retractionFields=20, cleanupFrame=1954,
                groundedWalkingFrame=1955, separateLaterHurtFrame=1960,
                directAttackEntryTapAccepted=False, directCollisionTapAccepted=False,
                contactHoldTimingDerivedFromSource=False, privateVoiceInterruptionAccepted=False,
                wholeRenderedPixelsAccepted=False, fullPortAcceptance=False)


def execute(prepared):
    sync.need(not OUT.exists(), 'Fresh bounded recovery evidence')
    capture = json.loads(controls.CAPTURE.read_text())
    key = prepared.SCOPE['KEY']
    handle = prepared.NATIVE_HANDLES[key]
    sync.need(handle['process'].poll()==0 and capture['passed']
              and handle['identity']==capture['actualNativeIdentity'], 'Same actual terminal; no replay')
    pins = capture['inputHashes']
    sync.need(all(sync.sha(p)==h for p,h in pins.items()), 'All actual capture inputs unchanged')
    text = prepared.RAM_CASES[key][1]
    whole = controls.gate(text, prepared.STATE['guest'])
    fields = [r for r in controls.ledger.original.pair.rows(text,'FIELD') if 1911<=r['frame']<=1960]
    flags = [r for r in controls.ledger.rows(text,'MK2_CPU_PAIR_FLAG') if 1910<=int(r['frame'])<=1960]
    health = [r for r in controls.ledger.rows(text,'MK2_CPU_ROUND_HEALTH') if 1910<=int(r['frame'])<=1960]
    result = episode(fields,flags,health)
    faults = []
    for label, collection, selector, field, value in (
        ('wrong_actual_actor',0,lambda r:r['frame']==1916,'vid',1),
        ('wrong_hit_pose',0,lambda r:r['frame']==1916,'vpose',0),
        ('missing_retraction',0,lambda r:r['frame']==1940,'vaction',0),
        ('retained_attack_flags',0,lambda r:r['frame']==1955,'vflags',0x11),
        ('wrong_damage_owner',2,lambda r:r['frame']=='1916' and r['slot']=='2','a8','010350A0'),
        ('wrong_cleanup_opcode',1,lambda r:r['frame']=='1954' and r['kind']=='body' and r['before']=='0016','op0','FFFF'),
        ('misclassified_later_hurt',0,lambda r:r['frame']==1960,'vflags',1),
    ):
        bad = copy.deepcopy([fields,flags,health])
        row = next(r for r in bad[collection] if selector(r))
        sync.need(row[field]!=value, 'Effective fault')
        row[field]=value
        try:
            episode(*bad)
        except AssertionError as error:
            faults.append(dict(name=label,rejected=True,reason=str(error)))
        else:
            raise AssertionError('Fault accepted: '+label)
    sync.need(episode(fields,flags,health)==result, 'Full positive restored')
    sync.need(all(sync.sha(p)==h for p,h in pins.items()), 'All whole pins remain unchanged')
    report = dict(passed=True, actualNativeIdentity=capture['actualNativeIdentity'],
                  wholeNativeAndControls=whole, boundedRecordedRecovery=result,
                  effectiveFaults=faults, wholePinsVerified=len(pins), inputHashes=pins,
                  limitations='Finite observed hit/recovery only. No direct attack-entry/contact tap or source-derived contact-hold timing. No voice-interruption, pixel/audio or full-port acceptance.')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main(prepared):
    try:
        return execute(prepared)
    except BaseException:
        OUT.mkdir(exist_ok=True)
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n')
        raise
