"""Actual natural CPU hit interrupts Kano low kick; finite state regression."""
import copy
import json
import traceback
import qualify_native_selector_fresh_lowkick_controls as controls
import verify_native_source_sync as sync

OUT = sync.ROOT / 'audit_native_selector_fresh_lowkick_interruption_checked'


def gate(fields, flags, health):
    by = {r['frame']:r for r in fields}
    sync.need(set(by)==set(range(2128,2159)), 'Complete contiguous interruption/recovery fields')
    for r in fields:
        sync.need((r['vid'],r['id'],r['vactor'],r['vmain']) == (17,18,0x01034e90,0x0106a370)
                  and r['writes']==0 and r['assistance']=='none', 'Actual true actors; passive observations')
    for f,p in ((2129,0xff00f560),(2130,0xff00f5c0)):
        r=by[f]
        sync.need((r['vaction'],r['vbody'],r['vflags'],r['vhp'],r['vpose'])==(0x104,0x16,0x11,59,p),
                  'Actual two own low-kick frames before incoming hit')
    damage=[r for r in health if r['frame']=='2130' and r['slot']=='1']
    sync.need(len(damage)==1 and tuple(damage[0][k] for k in
              ('before','after','pc','a8','a13','op0','op1','op2','ids','writes','assistance')) ==
              ('59','39','FF836700','010350A0','0106BF30','CF01','5621','8026','17,18','0','none'),
              'Actual natural Sonya CPU incoming damage instruction')
    for f in range(2131,2155):
        r=by[f]
        sync.need((r['vaction'],r['vbody'],r['vflags'],r['vhp'])==(0x503,0x1a,0x15,39),
                  'Whole observed native hurt interval replaces low kick')
    for frame,kind,before,after,pc,op,offset in (
        ('2130','action','0104','0503','FF8E1450','B00D','01F0'),
        ('2154','action','0503','0000','FF83EDD0','B00D','01F0'),
        ('2154','body','001A','0012','FF83EEB0','B088','0160'),
        ('2154','flags','0015','0001','FF83EFC0','B08D','0210'),
    ):
        sync.need(any(tuple(r[k] for k in ('frame','kind','before','after','pc','op0','op1','slot','actor','main','id')) ==
                      (frame,kind,before,after,pc,op,offset,'1','01034E90','0106A370','17') for r in flags),
                  'Actual native interruption/cleanup store: '+kind+' '+frame)
    for f in range(2155,2159):
        r=by[f]
        sync.need((r['vaction'],r['vbody'],r['vflags'],r['vhp'])==(0,0x12,1,39)
                  and r['vypos']==r['vfloor'] and r['vvy']==r['vgravity']==r['vtrail']==0,
                  'Grounded clean state after native hurt recovery')
    return dict(incomingDamageFrame=2130,health=[59,39],hurtFields=24,cleanupFrame=2154,
                cleanGroundedFrame=2155,privateVoiceInterruptionAccepted=False,
                wholeRenderedPixelsAccepted=False,allMovesInterruptionsAccepted=False,fullPortAcceptance=False)


def main(prepared):
    try:
        sync.need(not OUT.exists(), 'Fresh immutable interruption proof')
        proof=json.loads(controls.CAPTURE.read_text()); key=prepared.SCOPE['KEY']
        h=prepared.NATIVE_HANDLES[key]
        sync.need(proof['passed'] and h['process'].poll()==0 and h['identity']==proof['actualNativeIdentity'],
                  'Same real completed process, no replay')
        pins=dict(proof['inputHashes'])
        for p in (__file__,controls.__file__): pins[str(sync.ROOT / 'tools' / __import__('pathlib').Path(p).name)]=sync.sha(p)
        sync.need(all(sync.sha(p)==v for p,v in pins.items()), 'Whole input inventory intact')
        text=prepared.RAM_CASES[key][1]
        whole=controls.gate(text,prepared.STATE['guest'])
        fields=[r for r in controls.ledger.original.pair.rows(text,'FIELD') if 2128<=r['frame']<=2158]
        flags=[r for r in controls.ledger.rows(text,'MK2_CPU_PAIR_FLAG') if 2128<=int(r['frame'])<=2158]
        health=[r for r in controls.ledger.rows(text,'MK2_CPU_ROUND_HEALTH') if 2128<=int(r['frame'])<=2158]
        positive=gate(fields,flags,health); faults=[]
        for label,index,selector,field,value in (
            ('wrong_kick_actor',0,lambda r:r['frame']==2129,'vid',1),
            ('kick_not_interrupted',0,lambda r:r['frame']==2131,'vaction',0x104),
            ('missing_hurt_health',0,lambda r:r['frame']==2132,'vhp',59),
            ('dangling_attack_flag',0,lambda r:r['frame']==2155,'vflags',0x11),
            ('wrong_cpu_damage_owner',2,lambda r:r['frame']=='2130' and r['slot']=='1','a8','01034E90'),
            ('wrong_native_interruption_opcode',1,lambda r:r['frame']=='2130' and r['kind']=='action','op0','FFFF'),
            ('wrong_cleanup_opcode',1,lambda r:r['frame']=='2154' and r['kind']=='body','op0','FFFF'),
        ):
            bad=copy.deepcopy([fields,flags,health]); row=next(r for r in bad[index] if selector(r))
            sync.need(row[field]!=value,'Effective fault'); row[field]=value
            try: gate(*bad)
            except AssertionError as error: faults.append(dict(name=label,rejected=True,reason=str(error)))
            else: raise AssertionError('Accepted fault: '+label)
        sync.need(gate(fields,flags,health)==positive and all(sync.sha(p)==v for p,v in pins.items()),
                  'Full positive restored and all whole pins intact')
        report=dict(passed=True,actualNativeIdentity=proof['actualNativeIdentity'],wholeNativeAndControls=whole,
                    boundedNaturalHitInterruption=positive,effectiveFaults=faults,inputHashes=pins,
                    limitations='One natural ordinary-hit interruption. Not active-private-voice interruption, full visual/audio, all moves or full port acceptance.')
        OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n'); return report
    except BaseException:
        OUT.mkdir(exist_ok=True); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n')
        raise
