"""Qualify either actual true-character native random-drop slot from original code.

The legacy1731 input/earned-health/parser/action/retirement contract is retained
whole. Its single old Sonyap2 fixture restriction is replaced only when the
actual current guest and original unpressed RNG/269callback drop prove it.
No prescribed RNG, altered controls, held/drop normalization, or game writes.
"""
import hashlib
import inspect
import re
from pathlib import Path

import native_stage_variant_checks_v1731 as legacy
from verify_current_tomb_drop_physics_v3618 import phase_contract

ROOT=Path(__file__).resolve().parent.parent
need=legacy.need


def records(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()
            if line.startswith('MK2_STAGE_PROVENANCE_'+tag+' ')]


def qualify_drop(log,fighter,side,arena,case,guest):
    need(fighter in ('kano','sonya')and side in(1,2)and arena==1 and case=='positive',
         'Explicit bounded true-character Tomb drop context')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(hashlib.sha256(original).hexdigest().upper()==
         '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Unchanged original native MK2 program')
    need(guest is not None and len(guest)==1048576,'Actual whole initialized current guest required')
    for first,last in((0xff8eaf00,0xff8eb490),(0xff876650,0xff876b40),
                       (0xff80e980,0xff80ecf0),(0xff82b800,0xff82bca0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==original[lo:hi],'Exact original native Tomb/RNG/fall/retirement code')
    fields=legacy.rows(log,'FIELD');need(fields,'Actual physical action fields')
    origin=int(fields[0]['frame']);victim=fields[0]['victim'];main=fields[0]['victim_main']
    victim_id=18 if fighter=='kano'else 17
    need(int(fields[0]['victim_id'])==victim_id,'Actual own native victim identity')
    entries=('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0',
             'FF8EB200','FF8EB290','FF876650','FF8EB3C0','FF8EB400')
    branch=[r for r in records(log,'BRANCH')if int(r['frame'])>=origin and r['entry']in entries]
    need([r['entry']for r in branch]==list(entries[:9]),'Exact original native random-drop branch chronology')
    first=int(branch[0]['frame']);random=int(branch[3]['a0'],16)
    need(branch[2]['a0']=='00000032'and 0<=random<50 and
         len({r['frame']for r in branch[:4]})==1 and
         [int(r['frame'])for r in branch[4:]]==[first,first+128,first+240,first+240,first+268]and
         all(r['io0']=='FFFFFFFF'and r['a8']==r['actor']==victim and
             r['a13']==r['main']==main for r in branch),
         'Actual original5-percent unpressed-control gate and owned task/phase timing')
    need(tuple(branch[7][k]for k in('a0','a1','a2','a3'))==
         ('00000000','00020000','00008000','00000FFF'),'Exact original fall parameters')
    callbacks={int(r['frame']):r for r in records(log,'FIELD')if
               origin<int(r['frame'])<=first+269}
    need(all(r['actor']==victim and r['main']==main and int(r['id'])==victim_id
             for r in callbacks.values()),'Actual victim callback ownership throughout drop')
    floor=220-({17:134,18:135}[victim_id])
    phase=phase_contract(callbacks,first,floor)
    return dict(actualNativeRandomValue=random,trueVictim=victim_id,phase=phase,
                actualOriginalGuestBranchQualified=True)


# This exact source transformation retains the complete legacy health/input/
# distance/parser/action/field801/cleanup gates, including the old fixture path
# when a complete independently qualified current guest was not supplied.
source=inspect.getsource(legacy.check_log)
signature="def check_log(log, fighter, side, arena, case='positive', certified_drop_log=None):"
need(source.count(signature)==1,'Exact original contract signature')
source=source.replace(signature,signature.replace('certified_drop_log=None)',
                                                 'certified_drop_log=None, guest=None)'))
needle="""        if not held:
            need((fighter,side,arena,case)==('sonya',2,1,'positive') and
                 certified_drop_log is not None and log==certified_drop_log,
                 'Non-held Tomb requires exact source-bound original random-drop chronology')"""
replacement="""        if not held:
            if guest is not None:
                qualify_drop(log,fighter,side,arena,case,guest)
            else:
                need((fighter,side,arena,case)==('sonya',2,1,'positive') and
                     certified_drop_log is not None and log==certified_drop_log,
                     'Non-held Tomb requires exact source-bound original random-drop chronology')"""
need(source.count(needle)==1,'Exact old single-fixture restriction identified')
source=source.replace(needle,replacement)
scope=dict(legacy.__dict__);scope.update(qualify_drop=qualify_drop)
exec(compile(source,'<native1731_full_contract_plus_source_qualified_current_drop>','exec'),scope)
check_log=scope['check_log']
EXECUTED_CONTRACT_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
