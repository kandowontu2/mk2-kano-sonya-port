"""Entire interruption/source-output contract for genuine stock jump-kick hits.

Replace only the uppercut-specific attack/hurt and controller expectations.
Native damage writer, all identity/body/FIFO/recovery/owner/source-stop gates
remain. This finite proof does not claim complete collision-box choreography.
"""
import inspect
import qualify_launch_interruption_v6691 as original
import launch_interruption_model_v6689 as previous_model
ROOT,need,sha=original.ROOT,original.need,original.sha

class Model:
 pass
model=Model()
model.__dict__.update(vars(previous_model))
code=(ROOT/'tools/launch_interruption_model_v6686.py').read_text()
code=code[code.index('def phase(carrier):'):code.index('\ndef source_events(carrier,pins):')]
changes=[
 ('else45512','else 45512'),('else40720','else 40720'),
 ("uppercuts=rows(text,'MK2_INTERRUPT_UPPERCUT')","uppercuts=[r for r in rows(text,'MK2_HSPECIAL_FIELD')if r['slot']==str(3-side)and r['action']=='512'and r['frame']in{h['frame']for h in incoming}]"),
 ('Two source-owned real launches and two original opponent uppercut entries','Two source-owned real launches and two actual stock opponent air-kick fields at contact'),
 ("int(hit['before'])-int(hit['after'])==40","int(hit['before'])-int(hit['after'])==26"),
 ('One real40-point incoming hit interrupts each already launched cycle; native ledger explains cumulative HP','One real26-point incoming jump-kick hit interrupts each already launched cycle; full native HP ledger retained'),
 ("""need(uppercut['entry']=='FF870DC0'and uppercut['pc']=='FF870DD0'and uppercut['mask']=='FFFF'and
       int(uppercut['opcode'],16)==struct.unpack_from('<H',guest,(0xff870dc0-0xff800000)//8)[0]and
       uppercut['actor']==uppercut['owner']==opponent['actor']==hit['a8']and uppercut['main']==opponent['main']==hit['a13']and
       uppercut['id']=='8'and start<int(uppercut['frame'])<=at,
       'Actual unchanged original uppercut instruction and real physical opponent owns the incoming damage')""",
  """need(uppercut['actor']==uppercut['owner']==opponent['actor']==hit['a8']and uppercut['main']==opponent['main']==hit['a13']and
       uppercut['id']==uppercut['roster']=='8'and int(uppercut['frame'])==at and num(uppercut,'action')==0x200 and
       num(uppercut,'y')<num(uppercut,'floor')and num(uppercut,'gravity')==0x8000,
       'Actual unchanged original airborne kick state belongs to the true stock opponent at native collision contact')
  stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
  lo=(0xff830000-0xff800000)//8;hi=(0xff880000-0xff800000)//8
  need(guest[lo:hi]==stock[lo:hi],'Entire original collision, movement, hurt and stock attack kernel remains unchanged')"""),
 ("num(before[f,side],'gravity')==0x6000 and num(before[f,side],'vy')==0xfff40000","num(before[f,side],'gravity')==0x8000 and num(before[f,side],'vy')==0xfffa0000"),
 ('Native uppercut hurt task reaches original airborne503/gravity/launch vector','Native jump-kick hurt task reaches original airborne503/gravity/launch vector'),
 ("uppercutEntry=int(uppercut['frame'])","kickObservedFrame=int(uppercut['frame'])"),
]
for before,after in changes:
 need(code.count(before)==1,'Exact whole phase kick-route adaptation: '+before);code=code.replace(before,after,1)
scope=dict(vars(previous_model))
exec(compile(code,__file__+'::whole_phase_actual_stock_jump_kick','exec'),scope)
model.phase=scope['phase']


def inputs(carrier,phase):
 actual=model.rows(carrier['text'],'MK2_INTERRUPT_INPUT');expected=[]
 for i,c in enumerate(phase['wholePhysicalAndSourceBodyContract']['cycles'],1):
  common=dict(serial=str(i),slot=str(3-carrier['side']),jump='1')
  onset=c['command']+{'ball':80,'square':2,'bicycle':9}[carrier['move']]
  toward='Left'if c['forward']=='Right'else'Right'
  for f in range(onset,onset+3):
   for button in('Up',toward):expected.append(dict(common,frame=str(f),button=button))
  for f in range(onset+carrier['delay']+4,onset+carrier['delay']+8):expected.append(dict(common,frame=str(f),button='High_Kick'))
 normalized=[{k:v for k,v in r.items()if k not in('seconds','writes','assistance')}for r in actual]
 need(normalized==expected and all(r['writes']=='0'and r['assistance']=='none'for r in actual),'Complete actual forward-jump and four-field High Kick controller schedule')
 io=model.rows(carrier['text'],'MK2_INTERRUPT_IO')
 need(io and all(r['at']=='01D00000'and r['mask']=='FFFF'and r['writes']=='0'and r['assistance']=='none'for r in io),'Every actual read-only native IO record retained')
 return dict(passed=True,physicalOpponentOperations=len(actual),actualNativePortReads=len(io),forcedGuestWrites=0,fullInputBitIsolationAccepted=False)

source=inspect.getsource(original.qualify)
for before,after in [
 ('audit_v6692_launch_interruption_checked_','audit_v6697_launch_jump_interruption_checked_'),
 ("('uppercut wrong opponent','UPPERCUT','id','17',dict(frame=cycle['uppercutEntry'])),",''),
 ("Path(__file__),Path(model.__file__)","Path(__file__),Path(original.__file__),Path(model.__file__)"),
]:
 need(source.count(before)==1,'Exact same-terminal qualifier jump-route scope/pins');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,model=model,inputs=inputs)
exec(compile(source,__file__+'::whole_same_RAM_qualifier_jump_route','exec'),scope)
qualify=scope['qualify']
