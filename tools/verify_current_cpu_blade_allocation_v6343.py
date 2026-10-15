"""Original blade lifetime plus every later Main write, including native knife.

Observer's two corrections separate completed blade context from later child.
Original pool/attach/pose/list/retire/reuse model remains unchanged. Later
round zero-fill and knife publish/clear transactions are independently bound
to actual source operands and full qualified knife child/health/state trace.
"""
import inspect,json,struct
from pathlib import Path
import verify_current_cpu_blade_allocation_v6333 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6344_current_cpu_blade_allocation_checked'


def later_parent_gate(text,guest,result):
 old=prior.old
 ctx=result['contexts'][0];main=ctx['main'];actor=ctx['parent'];end=ctx['nativeRetirement']
 rows=old.rows(text,'LATER_PARENT_STORE')
 need(len(rows)==8 and all(r['context']==1 and r['frame']>end and r['actor']==actor and r['main']==main and
      r['at']in(main+0x190,main+0x1a0)and r['mask']==65535 and r['writes']==0 and r['assistance']=='none'for r in rows),
      'Every later original Main write retained separately from retired blade')
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 zero=[r for r in rows if r['pc']==0xff83a100]
 need(len(zero)==4 and [r['frame']for r in zero]==[2346]*4 and
      [r['at']for r in zero]==[main+0x190,main+0x190,main+0x1a0,main+0x1a0],
      'Entire native round-reset zero-fill, including both byte passes')
 for r in zero:
  offset=(r['pc']-32-0xff800000)//8
  need(r['before']==r['data']==r['merged']==0 and (r['op0'],r['op1'])==(0x0388,0x8c20)and
       r['a0']in(r['at'],r['at']+8)and guest[offset:offset+4]==original[offset:offset+4]==struct.pack('<HH',r['op0'],r['op1']),
       'Source-bound later zero-fill cannot reattach the retired blade')
 knife=[r for r in rows if r['pc']!=0xff83a100]
 child=prior.phase.model.knife.one([r for r in prior.phase.model.knife.overlap.rows(text,'CHILD')if r['frame']==2445],
                                 'Actual already-qualified native knife child entry')
 obj=child['a8'];need(obj!=ctx['object'] and old.pool(obj) and child['shot_owner']==actor and child['main_owner']==obj,
                     'Later actual owned knife object is not the retired blade')
 need([r['frame']for r in knife]==[2445]*4 and [r['at']for r in knife]==[main+0x190,main+0x1a0]*2,
      'Entire later knife attachment and immediate original detach')
 value=0
 for i,r in enumerate(knife):
  offset=(r['pc']-32-0xff800000)//8
  want_pc=0xff8b6530 if i<2 else 0xff83f050
  want_words=(0xb34d if i<2 else 0xb20d,0x0190)
  need(r['pc']==want_pc and(r['op0'],r['op1'])==want_words and
       guest[offset:offset+4]==original[offset:offset+4]==struct.pack('<HH',*want_words)and
       r['before']==value and r['a8']==actor and r['a13']==main and r['a10']==obj,
       'Later knife Main-field transaction uses original instructions and actual distinct child')
  shift=r['at']-(main+0x190)
  want=obj if i<2 else 0
  need(r['data']==(want>>shift)&65535 and (r['a0']==child['gravity']if i<2 else r['a0']==0),
       'Native child process/attachment operands, then native zero clear')
  value=((value&~(65535<<shift))|(r['data']<<shift))&0xffffffff
  need(r['merged']==value,'Each later native knife half-store merged without normalization')
 need(value==0 and ctx['nativeRetirement']==1909,'Knife cannot overwrite earlier blade retirement')
 return dict(retainedLaterMainStores=len(rows),roundZeroFillStores=len(zero),knifeStores=len(knife),
             knifeObject=obj,knifePublishFrame=2445,bladeRetirementUnchanged=1909)


def allocation_gate():
 base=prior.allocation_gate()
 def gate(text,guest):
  result=base(text,guest)
  result['laterParentWrites']=later_parent_gate(text,guest,result)
  return result
 return gate


def main():
 extraPins=[ROOT/'tools/verify_current_cpu_blade_allocation_v6333.py',ROOT/'tools/verify_current_cpu_blade_allocation_v6338.py',
            ROOT/'tools/capture_current_cpu_blade_allocation_v6341.py',ROOT/'audit_v6339_current_cpu_blade_allocation_checked/failure.json']
 source=inspect.getsource(prior.main)
 before='for path in(PARENT,baseline,';need(source.count(before)==1,'Preserve source of original complete gate and failed observer result')
 source=source.replace(before,'for path in(*extraPins,PARENT,baseline,',1)
 before="  ('constructor_owner',mutate('CREATE','owner','01000000')),"
 need(source.count(before)==1,'Additional later-parent faults, original full matrix unchanged')
 source=source.replace(before,"  ('later_round_zero',mutate('LATER_PARENT_STORE','merged','01000000',{'frame':2346})),\n  ('later_knife_object',mutate('LATER_PARENT_STORE','a10','01031B00',{'frame':2445})),\n  ('later_knife_opcode',mutate('LATER_PARENT_STORE','op0','FFFF',{'frame':2445})),\n  ('later_knife_clear',mutate('LATER_PARENT_STORE','data','0001',{'frame':2445,'pc':'FF83F050'})),\n  ('overwritten_blade_retirement',mutate('CONTEXT_RESULT','detached','2445')),\n"+before,1)
 scope=dict(prior.__dict__,__file__=__file__,CASE=ROOT/'audit_v6342_current_cpu_blade_allocation_ram',OUT=OUT,
            allocation_gate=allocation_gate,extraPins=extraPins)
 exec(compile(source,__file__+'::whole_original_positive_fault_matrix_and_later_native_owners','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
