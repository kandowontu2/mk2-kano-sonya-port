"""Whole original recovery gate, recognizing the real original close elbow.

Do not drop walk/jump/punch, native damage, ownership, body or FIFO checks.
The retained standing-jab-only rejection stays false and unchanged.
This adds only the measured six-field close-elbow path and its native contact.
"""
import inspect,struct
import qualify_ground_input_delivery_v6712 as previous
model=previous.model
ROOT,need,sha=model.ROOT,model.need,model.sha

def close_punch(by,side,followup,rows,guest):
    # Original native routine: action114, animation22, five startup fields,
    # native common strike helper, then action60B at contact/recovery.
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo=(0xff873a70-0xff800000)//8;hi=(0xff873bb0-0xff800000)//8
    need(guest[lo:hi]==original[lo:hi], 'Whole original close-elbow action/animation/startup/contact interval unchanged')
    need(struct.unpack_from('<7H',guest,lo)==(0x09c1,0x114,0x09c9,0x22,0x18aa,0x09cb,0xf), 'Original exact action114/animation22/five-field strike startup')
    start=followup+114;hit=start+6
    need(all(model.num(by[f,side],'action')==0x114 and model.num(by[f,side],'y')==model.num(by[f,side],'floor') and
             all(model.num(by[f,side],k)==0 for k in ('vx','vy','gravity')) for f in range(start,hit)), 'Every real six-field grounded close-punch startup')
    need(model.num(by[hit,side],'action')==0x60b and len({by[f,side]['pose'] for f in range(start,hit+1)})>=3,
         'Original close elbow advances owned poses and reaches native60B contact/recovery')
    stores=[r for r in rows['MK2_HSPECIAL_HEALTH'] if int(r['frame'])==hit]
    need(len(stores)==1 and int(stores[0]['slot'])==3-side and int(stores[0]['before'])-int(stores[0]['after'])==24,
         'Actual stock target receives the complete native24HP close-elbow contact')
    return True

code=model.source
code=code[code.index('def physical_gate():'):code.index('\ndef phase(carrier):')]
before=" scope=dict(physical.__dict__,native=current,floor_source=floor_source)"
after=""" before=\"any(num(by[f,side],'action')==0x101 for f in range(followup+112,followup+140))\"
 need(source.count(before)==1,'Only original standing-jab follow-up predicate extended')
 source=source.replace(before,\"(any(num(by[f,side],'action')==0x101 for f in range(followup+112,followup+140))or close_punch(by,side,followup,rows,guest))\",1)
 scope=dict(physical.__dict__,native=current,floor_source=floor_source,close_punch=close_punch)"""
need(code.count(before)==1,'Whole previously corrected physical gate retained')
code=code.replace(before,after,1)
scope=dict(vars(model),close_punch=close_punch)
exec(compile(code,__file__+'::whole_native_recovery_add_original_close_elbow','exec'),scope)
phase_code=model.source
phase_code=phase_code[phase_code.index('def phase(carrier):'):phase_code.index(" health=rows(text,'MK2_INTERRUPT_HEALTH')")]+" return whole\n"
exec(compile(phase_code,__file__+'::whole_physical_body_contract_without_incoming_claim','exec'),scope)
phase=scope['phase']

# Reuse the entire input+physical qualifier with its four actual input faults.
source=inspect.getsource(previous.qualify)
first=source.index(" code=(ROOT/'tools/launch_interruption_model_v6686.py').read_text()")
last=source.index(" need(physical['twoRealSpecialCyclesAndCleanupVerified']",first)
source=source[:first]+" physical=phase(carrier)\n"+source[last:]
source=source.replace("ROOT/'audit_v6713_ground_input_delivery_checked'","ROOT/'audit_native_close_recovery_checked'",1)
source=source.replace('Path(__file__),Path(model.__file__)',"Path(__file__),ROOT/'tools/qualify_ground_input_delivery_v6712.py',ROOT/'audit_native_input_delivery_address_correction/report.json',Path(model.__file__)",1)
scope=dict(vars(previous),__file__=__file__,phase=phase)
exec(compile(source,__file__+'::whole_same_RAM_input_and_native_close_recovery_qualifier','exec'),scope)
qualify=scope['qualify']
