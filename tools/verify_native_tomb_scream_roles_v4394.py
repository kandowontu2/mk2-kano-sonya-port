"""Qualify actual native victim voice routing, including both Main roles.

Base32/34 selection is proven from the original Main+20 load/shift code and
its observed A2/A1 operands, not by accepting a wider unowned code range.
Sonya18 takes the genuine existing female extension to base38. No writes.
"""
import hashlib,re
from pathlib import Path
import run_jax_arms_native_audio_routes_v4212 as native
ROOT,need=native.ROOT,native.need

def qualify_scream(log,fighter,side,guest,scream):
    own=17 if fighter=='kano' else 18
    need(fighter in ('kano','sonya') and side in (1,2),'Actual added mirror identity/side')
    need(len(guest)==1048576 and hashlib.sha256(guest).hexdigest().upper()==
      '938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821','Entire actual3836 native guest')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(hashlib.sha256(original).hexdigest().upper()==
      '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Original native source')
    def code(first,last):return guest[(first-0xff800000)//8:(last-0xff800000)//8]
    need(code(0xffa11fd0,0xffa12020)==bytes.fromhex('4018e1093836343220c0'),
      'Exact native two variants and packed32343638 selector')
    need(code(0xffa12220,0xffa12430)==bytes.fromhex(
      '02b5f001420bfbff14ca420bfaff11ca80c00002ffff420bfeff08caa2b52000420bfeff01ca0125012d05c00126012d02c00127012d5f0de0ea80ff2014204010c0'),
      'Exact current native female extension, original Main+20 load, role shift, RNG and add dispatch')
    lo,hi=(0xffa122d0-0xff800000)//8,(0xffa12430-0xff800000)//8
    need(guest[lo:hi]==original[lo:hi],'All original generic male Main-role/female-byte/RNG dispatch instructions')
    rows=native.rows(log,'ROUTE')
    branch=[r for r in rows if r['frame']==scream['frame'] and r['a8']==scream['a8'] and r['return_pc']=='FF8EB2C0']
    entries=['FFA11FD0','FFA12220','FFA123B0' if own==18 else 'FFA122D0','FFA123D0','FFA12530']
    need([r['entry'] for r in branch]==entries,'Exact native Tomb late scream call/gender/role/random/dispatch sequence')
    need(branch[0]==scream and all(int(r['id'])==own and r['owner']==r['a8']==scream['a8'] and
      r['a13']==scream['a13'] and r['writes']=='0' and r['assistance']=='none' for r in branch),
      'Every actual scream stage owns the real mirror victim actor/Main, no fabricated dispatch')
    need(all(float(a['seconds'])<float(b['seconds']) for a,b in zip(branch,branch[1:])),
      'Native instruction route order')
    fields=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines()
      if line.startswith('MK2_STAGE_FIELD ') and 'frame='+scream['frame']+' ' in line]
    need(len(fields)==1 and fields[0]['victim']==scream['a8'] and fields[0]['victim_main']==scream['a13'] and
      int(fields[0]['victim_id'])==own,'Actual original full-field victim actor/Main corroborates native voice task')
    selector,gender,variant,dispatch=branch[1:]
    need(selector['a0']=='00000002' and selector['a1']==gender['a1']=='32343638' and
      int(gender['a2'],16)==own and gender['a0']==variant['a0']=='00000002',
      'Observed native packed selector and genuine victim ID entering gender routing')
    role=int(variant['a2'],16)
    if own==17:
        need(role in (1,2) and role==3-side,'Observed original Main+20 role register matches actual mirror victim slot')
        base=0x32 if role==1 else 0x34
    else:
        need(role==18,'Female extension retains actual18 register into byte selection')
        base=0x38
    need(int(variant['a1'],16)==base and int(dispatch['a1'],16)==base and
      int(dispatch['a0'],16) in (base,base+1) and int(dispatch['a2'],16)==role,
      'Exact source-selected role/gender byte plus one native RNG variant, not any arbitrary male code')
    return dict(passed=True,fighter=fighter,winnerSide=side,victimActor=scream['a8'],victimMain=scream['a13'],
      actualRoleRegister=role,sourceSelectedBase=base,actualDispatchCode=int(dispatch['a0'],16),
      nativeReturnPC='FF8EB2C0',routes=branch)

def faults(log,fighter,side,guest):
    scream=next(r for r in native.rows(log,'ROUTE') if r['entry']=='FFA11FD0')
    accepted=qualify_scream(log,fighter,side,guest,scream)
    mutations=[('FFA123D0','a2','00000000'),('FFA123D0','a1','00000036'),
      ('FFA12530','a0','00000036'),('FFA12530','a1','00000036'),
      ('FFA12530','owner','00000000'),('FFA12530','a13','00000000'),
      ('FFA12530','id','1'),('FFA12530','return_pc','00000000')]
    rejected={}
    for entry,key,value in mutations:
        lines=log.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('MK2_MAUDIO_ROUTE ') and
          'entry='+entry+' ' in s and 'frame='+scream['frame']+' ' in s and 'return_pc=FF8EB2C0' in s)
        lines[i]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,lines[i],count=1)
        try:qualify_scream('\n'.join(lines)+'\n',fighter,side,guest,scream)
        except Exception as error:rejected[entry+':'+key]=str(error)
        else:raise ValueError('Actual native scream role/owner/source fault accepted: '+entry+':'+key)
    need(len(rejected)==8 and qualify_scream(log,fighter,side,guest,scream)==accepted,
      'Every actual native scream routing fault rejected, original restored')
    return rejected
