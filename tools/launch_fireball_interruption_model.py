"""Whole physical/body/owner/audio contract for real original Liu fireballs.

Native airborne fireball reaction does not assign uppercut action503. Bind
the original selected reaction, native fling constants, every collision and
actual projectile parent/victim ownership instead of admitting arbitrary hurt.
"""
import collections,struct
import launch_interruption_model_v6689 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def stock_floor(guest,identity):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    at=lambda a:(a-0xff800000)//8
    anchors=struct.unpack_from('<17H',stock,at(0xff908010))
    ptr=struct.unpack_from('<I',guest,at(0xff907f70))[0]
    current=struct.unpack_from('<19H',guest,at(ptr))
    need(identity==1 and current[:17]==anchors and current[17:]==(134,135) and anchors[1]==anchors[4]==133,
         'Every original floor parameter retained; real Liu1 shares the source Kitana133 anchor, not Sub-Zero131')
    return 216-anchors[identity]

def projectile_gate(carrier):
    guest=carrier['guest'];stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();at=lambda a:(a-0xff800000)//8
    for lo,hi in ((0xff835b70,0xff835bd0),(0xff8de490,0xff8de750),(0xff8f3760,0xff8f37f0)):
        need(guest[at(lo):at(hi)]==stock[at(lo):at(hi)],'Whole explicit original box comparisons/fireball reaction/descriptor interval unchanged')
    need(struct.unpack_from('<9H',guest,at(0xff8f3760))==(52,20,45,30,0x1110,0x1605,0,0,1), 'Entire original high-fireball rectangle, reaction17 and22HP descriptor')
    need(struct.unpack_from('<11H',guest,at(0xff8de620))==(0x09e0,0x8000,3,0x09e1,0,0xfffa,0x09c2,0x7000,0x18a3,0x09c9,15),
         'Original selected airborne fireball fling VX3.5/VY-6/gravity7000/animation15, not uppercut503')
    fields={(int(r['frame']),int(r['slot'])):r for r in previous.rows(carrier['text'],'MK2_HSPECIAL_FIELD')}
    records=previous.rows(carrier['text'],'MK2_FIREBALL_COUNTER_EVENT');groups=collections.defaultdict(list)
    addresses={'collision':0xff835440,'rectangles':0xff835b70,'contact':0xff835e50,'miss':0xff835e70}
    need(records,'Actual native collision records retained')
    side=carrier['side'];contacts=[]
    for r in records:
        address=addresses[r['kind']];f=int(r['frame']);own,opponent=fields[f,side],fields[f,3-side]
        need(r['writes']=='0' and r['assistance']=='none' and int(r['at'],16)==address and int(r['pc'],16)==address+16 and
             r['mask']=='FFFF' and int(r['opcode'],16)==struct.unpack_from('<H',guest,at(address))[0], 'Every actual native collision instruction/register inventory source bound')
        if r['id']=='1':
            need(r['a8']==r['mainActor'] and r['parentActor']==opponent['actor'] and r['victimActor']==own['actor'] and
                 r['victimMain']==own['main'] and r['a8'] not in (own['actor'],opponent['actor']) and
                 r['a13'] not in (own['main'],opponent['main']), 'Actual original Liu projectile child, parent fighter and real own victim, never a proxy or human punch')
        else:
            need(r['id']==own['id'] and r['a8']==r['mainActor']==own['actor'] and r['a13']==own['main'] and
                 r['victimActor']==opponent['actor'] and r['victimMain']==opponent['main'], 'All own collision attempts remain owned true-ID native attacks')
        groups[f,r['a8'],r['a13']].append(r)
    for (f,actor,main),group in groups.items():
        need([r['kind'] for r in group] in (['collision','rectangles','miss'],['collision','rectangles','contact']), 'Every real collision has full rectangle comparison and actual hit/miss outcome')
        entry,rect,end=group
        def xy(key):
            value=int(rect[key],16)
            return previous.physical.short(value),previous.physical.short(value>>16)
        victim_min,victim_max,attack_min,attack_max=map(xy,('a2','a3','a4','a5'))
        intersects=all(victim_min[i]<=attack_max[i] and victim_max[i]>=attack_min[i] for i in (0,1))
        need(intersects==(end['kind']=='contact'), 'Every actual native hit/miss agrees with unchanged signed original CMPXY rectangle instructions')
        if end['id']=='1':
            need(entry['a0']=='FF8F3760' and end['kind'] in ('contact','miss'), 'Every original high-fireball descriptor and full branch outcome')
            if end['kind']=='contact':
                need(end['a7']=='FF8DE490' and int(end['a10'],16)==22, 'Actual source-selected original high-fireball reaction and22HP, not fitted damage')
                contacts.append(dict(frame=f,child=actor,childMain=main,parentActor=end['parentActor'],victimActor=end['victimActor'],
                                     victimMain=end['victimMain'],nativeReaction=end['a7'],damage=22))
    health=[r for r in previous.rows(carrier['text'],'MK2_INTERRUPT_HEALTH') if int(r['slot'])==side and int(r['after'])<int(r['before'])]
    need(len(contacts)==len(health)==2 and [(c['frame'],c['child'],c['childMain']) for c in contacts]==
         [(int(r['frame']),r['a8'],r['a13']) for r in health], 'Both actual child-owned contacts exactly account for all genuine incoming health stores')
    return dict(passed=True,completeNativeCollisionRecords=len(records),completeHitMissBranches=len(groups),actualStockProjectileContacts=contacts,
                opaqueField250NotAcceptedAsParentMain=True,scope='Every observed original/native collision; not all possible hitboxes or arenas')

source=previous.source
changes=[
 ("'ids={side:identity,3-side:8}'","'ids={side:identity,3-side:1}'"),
 ('floors[3-side]==floor_source.subzero_floor(guest)','floors[3-side]==stock_floor(guest,1)'),
 ('native=current,floor_source=floor_source','native=current,floor_source=floor_source,stock_floor=stock_floor'),
 ("uppercuts=rows(text,'MK2_INTERRUPT_UPPERCUT')","uppercuts=[r for r in rows(text,'MK2_FIREBALL_COUNTER_EVENT')if r['kind']=='contact'and r['id']=='1']"),
 ('Two source-owned real launches and two original opponent uppercut entries','Two source-owned real launches and two original projectile contacts'),
 ("int(hit['before'])-int(hit['after'])==40","int(hit['before'])-int(hit['after'])==22"),
 ('One real40-point incoming hit interrupts each already launched cycle; native ledger explains cumulative HP','One real22HP incoming fireball hit interrupts each already launched cycle; full native ledger explains cumulative HP'),
 ("""need(uppercut['entry']=='FF870DC0'and uppercut['pc']=='FF870DD0'and uppercut['mask']=='FFFF'and
       int(uppercut['opcode'],16)==struct.unpack_from('<H',guest,(0xff870dc0-0xff800000)//8)[0]and
       uppercut['actor']==uppercut['owner']==opponent['actor']==hit['a8']and uppercut['main']==opponent['main']==hit['a13']and
       uppercut['id']=='8'and start<int(uppercut['frame'])<=at,
       'Actual unchanged original uppercut instruction and real physical opponent owns the incoming damage')""",
  """need(uppercut['id']=='1'and uppercut['a8']==uppercut['mainActor']==hit['a8']and uppercut['a13']==hit['a13']and
       uppercut['parentActor']==opponent['actor']and uppercut['victimActor']==own['actor']and uppercut['victimMain']==own['main']and
       int(uppercut['frame'])==at and uppercut['a7']=='FF8DE490',
       'Actual original projectile child/parent/victim/reaction and native incoming HP source')"""),
 ("num(before[f,side],'action')==0x503 and num(before[f,side],'gravity')==0x6000 and num(before[f,side],'vy')==0xfff40000",
  "num(before[f,side],'action')==(0x20b if move=='ball'else 0x204)and num(before[f,side],'body')&8==8 and num(before[f,side],'flags')&4==4 and num(before[f,side],'gravity')==0x7000 and num(before[f,side],'vy')==0xfffa0000"),
 ('Native uppercut hurt task reaches original airborne503/gravity/launch vector','Native original airborne fireball reaction preserves launch action and applies source-defined compact hurt body/7000 gravity/-6 vector'),
 ("uppercutEntry=int(uppercut['frame'])","projectileContact=int(uppercut['frame'])"),
 ('completeOwnershipFields=len(owner_rows),completeBattleChannelFields=len(channel_rows),',
  'completeOwnershipFields=len(owner_rows),completeBattleChannelFields=len(channel_rows),nativeProjectileContacts=projectile_gate(carrier),'),
]
for before,after in changes:
    need(source.count(before)==1,'Only exact native projectile route/floor/reaction adaptation: '+before[:70]);source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_original_contract_actual_Liu_projectile_interruption','exec'),globals())
