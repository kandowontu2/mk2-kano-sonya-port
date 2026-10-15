"""Complete retained-run projectile interruption, native delivery and waveform.

Keep all original native health/body/recovery/audio and actual fault suites.
Only physical stock inputs and the source-defined projectile reaction differ.
"""
import inspect
import qualify_launch_interruption_v6691 as original
import launch_fireball_interruption_model as model
import qualify_ground_input_delivery_v6712 as delivery
ROOT,need,sha=model.ROOT,model.need,model.sha

def inputs(carrier,phase):
    actual=model.rows(carrier['text'],'MK2_INTERRUPT_INPUT');expected=[]
    for serial,cycle in enumerate(phase['wholePhysicalAndSourceBodyContract']['cycles'],1):
        onset=(55+carrier['delay']) if carrier['move']=='ball' else carrier['delay']-1
        toward='Left' if cycle['forward']=='Right' else 'Right'
        for age in range(9):
            frame=cycle['command']+onset+age
            common=dict(frame=str(frame),serial=str(serial),slot=str(3-carrier['side']),ground='1')
            if age<3 or 5<=age<8:expected.append(dict(common,button=toward))
            if 6<=age<9:expected.append(dict(common,button='High_Punch'))
    normalized=[{k:v for k,v in r.items() if k not in ('seconds','writes','assistance')} for r in actual]
    need(normalized==expected and all(r['writes']=='0' and r['assistance']=='none' for r in actual),
         'Every actual stock F,F,HP controller operation and both true physical facings')
    bits=delivery.delivered(carrier['text'])
    return dict(passed=True,physicalOpponentOperations=len(actual),realIN0IN2BitDelivery=bits,forcedGuestWrites=0,
                opaqueField250ProtocolLabelCorrection='parentMain in captured EVENT is the opaque native field250; it is not accepted as a parent task pointer')

source=inspect.getsource(original.qualify)
changes=[
 ('audit_v6692_launch_interruption_checked_','audit_launch_fireball_interruption_checked_'),
 ("   ('uppercut wrong opponent','UPPERCUT','id','17',dict(frame=cycle['uppercutEntry'])),\n",''),
 ('Path(__file__),Path(model.__file__)',"Path(__file__),Path(original.__file__),Path(delivery.__file__),ROOT/'tools/launch_interruption_model_v6689.py',ROOT/'mk2/mk2-maincpu.bin',Path(model.__file__)"),
 ("  else:raise ValueError('Actual semantic counterexample admitted '+label)","  else:raise ValueError('Actual semantic counterexample admitted '+label)\n  print('Rejected actual '+label,flush=True)"),
 (" for tag,key,value in [('MK2_MAUDIO_PACKET'", """ for cycle in phase['actualInterruptedCycles']:
  hit=cycle['hit']
  for label,key,value in [('wrong native projectile parent','parentActor','010350A0'),
                          ('wrong native projectile child','mainActor','01034E90'),
                          ('wrong native projectile victim task','victimMain','0106A370'),
                          ('wrong original native fireball reaction','a7','FF8DE760')]:
   reject(str(hit)+' '+label,'MK2_FIREBALL_COUNTER_EVENT',key,value,dict(frame=hit,kind='contact'),model.phase)
 for tag,key,value in [('MK2_MAUDIO_PACKET'"""),
]
for before,after in changes:
    need(source.count(before)==1,'Only actual projectile input/semantic fault adapter changed: '+before[:75]);source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,model=model,inputs=inputs,delivery=delivery)
exec(compile(source,__file__+'::whole_native_source_interruption_proof_real_fireball','exec'),scope)
qualify=scope['qualify']
