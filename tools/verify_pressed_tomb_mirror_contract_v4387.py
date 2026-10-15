"""Original full earned1731 gates plus independently source-qualified button drop.

The existing unpressed/RNG contract is preserved unchanged. This separate
pressed case requires the exact original both-Down branch code, all actual
physical input fields, native IO bits/register ownership/PCs and the complete
original269callback signed motion/landing cadence. No inferred activation.
"""
import copy,hashlib,inspect,struct
import verify_tomb_mirror_contract_v4344 as old
native=old.native
ROOT,need=old.ROOT,old.need

def qualify_pressed_drop(log,fighter,side,arena,case,guest):
    need(fighter in('kano','sonya')and side in(1,2)and arena==1 and case=='positive','Exact true mirror pressed Tomb context')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
      'Original native MK2 program unchanged')
    need(guest is not None and len(guest)==1048576,'Entire actual initialized native guest required')
    for first,last in ((0xff8eaf00,0xff8eb490),(0xff876650,0xff876b40),(0xff80e980,0xff80ecf0),(0xff82b800,0xff82bca0),
      (0xff83cc20,0xff83cd50)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==original[lo:hi],'Every original Tomb/branch/RNG/fall/retirement code byte')
    lo=(0xff8eb0d0-0xff800000)//8
    need(guest[lo:lo+32]==struct.pack('<16H',0x07a0,0,0x0160,0x03e0,0x1fc0,0xca02,0x1ec0,0xcb06,
      0x09c0,0x32,0x0d5f,0xec20,0xff80,0xc925,0x09c0,0x80),
      'Exact native IN0/NOT/bit1/bit9/direct drop versus original RNG instruction bytes')
    fields=native.legacy.rows(log,'FIELD');need(fields,'Actual native action fields')
    origin=int(fields[0]['frame']);victim=fields[0]['victim'];main=fields[0]['victim_main']
    own=17 if fighter=='kano'else 18
    need(int(fields[0]['victim_id'])==own,'Real mirror victim identity')
    inputs=native.legacy.rows(log,'INPUT');downs=[r for r in inputs if r['button']=='Down'and origin+32<=int(r['frame'])<origin+64]
    need(len(downs)==64 and {(int(r['frame']),int(r['slot']))for r in downs}==
      {(f,n)for f in range(origin+32,origin+64)for n in(1,2)},'Every actual physical both-Down field, neither missing nor duplicated')
    marked=native.legacy.rows(log,'DROP_INPUT');results=native.legacy.rows(log,'DROP_RESULT')
    need(len(marked)==32 and [int(r['age'])for r in marked]==list(range(32,64))and
      [int(r['frame'])for r in marked]==list(range(origin+32,origin+64))and
      [int(r['pressed_fields'])for r in marked]==list(range(1,33))and
      all(int(r['origin'])==origin for r in marked)and len(results)==1 and results[0]['pressed_fields']=='32',
      'Exactly declared32physical both-Down callbacks after real stage activation')
    entries=('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0','FF8EB400')
    branches=[r for r in native.records(log,'BRANCH')if int(r['frame'])>=origin and r['entry']in entries]
    need([r['entry']for r in branches]==['FF8EB0D0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0'],
      'Exact native both-Down direct drop, no RNG or held branch substituted')
    first=int(branches[0]['frame'])
    need(origin+32<=first<origin+64 and [int(r['frame'])for r in branches]==[first,first,first+128,first+240,first+240,first+268],
      'Complete actual original direct-drop dispatch/phase chronology')
    # Different physical-slot scheduler orders do not share a prescribed
    # origin+44 arrival. Qualify the actual original 64pixel upward store,
    # caller operands and immediate branch in the same native victim task.
    floor=220-{17:134,18:135}[own];ceiling=floor-259
    stores=[r for r in native.records(log,'MOTION')if int(r['frame'])>=origin and r['pc']=='FF83CD20']
    need(len(stores)==1,'One actual original ceiling-adjustment writer, not a sampled arrival guess')
    store=stores[0]
    need(int(store['frame'])==first and store['offset']=='B0'and int(store['at'],16)==int(victim,16)+0xb0 and
      int(store['before'],16)&0xffff==(ceiling+64)&0xffff and int(store['value'],16)&0xffff==ceiling&0xffff and
      int(store['mask'],16)==0xffff and store['actor']==store['a8']==victim and store['main']==store['a13']==main and
      int(store['id'])==own and store['mode']=='2'and branches[0]['a0']=='00000000'and
      branches[0]['a1']=='FFFFFFC0'and int(branches[0]['a2'],16)==ceiling&0xffffffff,
      'Exact native ceiling y-minus64 writer and source caller registers qualify physical-slot arrival')
    need([r['io0']for r in branches]==['FFFFFDFD','FFFFFDFD','FFFFFFFF','FFFFFFFF','FFFFFFFF','FFFFFFFF']and
      branches[1]['a0']=='00000202'and all(int(r['pc'],16)==int(r['entry'],16)+16 and
      r['a8']==r['actor']==victim and r['a13']==r['main']==main for r in branches),
      'Actual both-Down IO bits and NOT operand, source-entry PC and owned native victim task')
    need(tuple(branches[4][k]for k in ('a0','a1','a2','a3'))==('00000000','00020000','00008000','00000FFF'),
      'Every original native fall-helper argument')
    callbacks={int(r['frame']):r for r in native.records(log,'FIELD')if origin<int(r['frame'])<=first+269}
    need(all(r['actor']==victim and r['main']==main and int(r['id'])==own for r in callbacks.values()),
      'Every actual victim callback belongs to its real mirror actor/Main')
    phase=native.phase_contract(callbacks,first,floor)
    return dict(passed=True,trueVictim=own,actualPhysicalDownFields=32,actualBothDownBranchFrame=first,
      nativeRNGNotInvokedForThisBranch=True,phase=phase,actualOriginalPressedGuestBranchQualified=True,
      actualNativeCeilingWriter=store,actualNativeCeilingArrivalOffset=first-origin)

contract_source=old.contract_source
before='qualify_drop(log,fighter,side,arena,case,guest)'
need(contract_source.count(before)==1,'One original source-qualified non-held branch call, all other full1731 gates retained')
contract_source=contract_source.replace(before,'qualify_pressed_drop(log,fighter,side,arena,case,guest)')
scope=dict(old.scope);scope.update(qualify_pressed_drop=qualify_pressed_drop)
exec(compile(contract_source,'<entire1731_full_true_mirror_contract_with_exact_pressed_branch>','exec'),scope)
full_check_log=scope['check_log']

def check_log(log,fighter,side,arena,case='positive',certified_drop_log=None,guest=None):
    checked=full_check_log(log,fighter,side,arena,case,certified_drop_log,guest)
    qualify_pressed_drop(log,fighter,side,arena,case,guest)
    return checked

fault_source=inspect.getsource(old.actual_faults)
fault_scope=dict(old.__dict__);fault_scope.update(check_log=check_log)
exec(compile(fault_source,'<entire4344_actual_faults_pressed_native_context>','exec'),fault_scope)
actual_faults=fault_scope['actual_faults']
CONTRACT_SHA256=hashlib.sha256(contract_source.encode()).hexdigest().upper()

def pressed_phase_faults(log,fighter,side,guest):
    accepted=qualify_pressed_drop(log,fighter,side,1,'positive',guest)
    first=accepted['actualBothDownBranchFrame'];floor=accepted['phase']['floor']
    rows={int(r['frame']):r for r in native.records(log,'FIELD')}
    rejected=[]
    for name,frame,key,base in (('hold position',first+2,'y',10),('slow descent velocity',first+130,'vy',16),
      ('fall gravity',first+242,'gravity',16),('native floor landing',first+269,'y',10)):
        changed=copy.deepcopy(rows);value=int(changed[frame][key],base)+1
        changed[frame][key]=f'{value:08X}'if base==16 else str(value)
        try:native.phase_contract(changed,first,floor)
        except Exception as error:rejected.append(dict(name=name,frame=frame,rejectedBy=str(error)))
        else:raise ValueError('Changed actual native pressed drop phase accepted: '+name)
    need(len(rejected)==4 and qualify_pressed_drop(log,fighter,side,1,'positive',guest)==accepted,'All actual phase faults rejected and original restored')
    return rejected
