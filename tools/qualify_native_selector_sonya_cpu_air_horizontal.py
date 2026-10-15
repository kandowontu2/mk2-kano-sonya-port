"""Replay both real fighters' complete contact/release horizontal word journal.

No game restart or gameplay writes. Original native memory-to-memory copies
read the independently replayed other actor, not the observed destination.
Register stores bind every source/destination/field-width operand. Every
32-bit instruction retains its two real 16-bit callbacks and whole low-word
pre-value. Scope is this actual contact and recovery, not all arenas.
"""
import copy, hashlib, json, struct, traceback
from collections import Counter
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_contact_recovery as contact
import qualify_native_selector_sonya_cpu_air_channels_assets as audio
import qualify_native_selector_sonya_horizontal_operands_gateway as gateway

ROOT, need, sha = contact.ROOT, contact.need, contact.sha
OUT = ROOT/'audit_native_selector_sonya_cpu_air_horizontal_checked'
FIRST, LAST = 2731, 2813
EXPECTED = {
    ('1','FF8040B0'):166, ('2','FF8040B0'):166,
    ('2','FF8285B0'):114, ('1','FF8285D0'):114,
    ('1','FF83CE90'):50, ('1','FFF9D270'):50,
    ('1','FF83CCD0'):25, ('2','FF83CCD0'):6,
    ('1','FF80F700'):12, ('2','FF80F700'):10,
    ('2','FFF9DE50'):4, ('1','FFF9DE70'):4,
}
REG = {0xff83ccd0:(0xb048,0x90,16), 0xff80f700:(0xb228,0x40,32),
       0xff8285b0:(0xb2e9,0x40,32), 0xff8285d0:(0xb2c8,0x40,32),
       0xfff9de50:(0xb208,0x40,32), 0xfff9de70:(0xb20a,0x40,32)}
COPY = {0xff83ce90:(0xbb00,0x80,0x80), 0xfff9d270:(0xbb0a,0x40,0x40)}


def records(text):
    capture = contact.control.capture
    fields = contact.data(text)['fields']
    stores = capture.previous.base.choices.native_state.rows(text,'MK2_SONYA_HORIZONTAL_STORE')
    return dict(fields=[r for r in fields if FIRST <= r['frame'] <= LAST+1],
                stores=[r for r in stores if FIRST <= int(r['frame']) <= LAST])


def source(guest):
    need(hashlib.sha256(guest).hexdigest().upper()==contact.control.source.GUEST,
         'Whole independently cold-bound current guest, no opcode substitution')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    boundary=gateway.boundary_source(guest,stock)
    for lo,hi in ((0xff804000,0xff804110),(0xff83cc20,0xff83cd50),
                  (0xff83ce60,0xff83cef0),(0xff80f6b0,0xff80f740),
                  (0xff828570,0xff8285f0)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Whole original integration/push/displacement/copy routines')
    for pc,(op,offset,width) in REG.items():
        need(struct.unpack_from('<2H',guest,(pc-32-0xff800000)//8)==(op,offset),
             'Exact real register-to-offset instruction')
    for pc,words in COPY.items():
        need(struct.unpack_from('<3H',guest,(pc-48-0xff800000)//8)==words,
             'Exact real memory-to-memory instruction and both offsets')
    need(struct.unpack_from('<2H',guest,(0xff8040b0-32-0xff800000)//8)==(0x0983,0x00c0),
         'Exact MMTM A3 and original A8/A9 register list')
    ops=(ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx').read_text()
    need('int32_t data = RFIELD##F(R##REG(SRCREG(op))+o1);' in ops and
         'WFIELD##F(R##REG(DSTREG(op))+o2,data);' in ops and
         'WFIELD##F(R##REG(DSTREG(op))+o,R##REG(SRCREG(op)));' in ops,
         'Original native MOVE field-width, source-before-destination semantics')
    return boundary


def gate(data,guest):
    fields=data['fields']; stores=data['stores']; by={r['frame']:r for r in fields}
    need(len(fields)==LAST-FIRST+2 and len(by)==len(fields) and
         set(by)==set(range(FIRST,LAST+2)), 'Every complete physical callback through next field')
    need(len(stores)==721 and dict(Counter((r['slot'],r['pc']) for r in stores))==EXPECTED,
         'All721 actual horizontal stores, both actors and every source site')
    need([int(r['frame']) for r in stores]==sorted(int(r['frame']) for r in stores),
         'Actual native journal order retained')
    actors={1:0x01034e90,2:0x010350a0}; mains={1:0x0106a370,2:0x0106bf30}
    sites=Counter(); instructions=0; copies=0; snapshots=0
    for frame in range(FIRST,LAST+1):
        f=by[frame]; following=by[frame+1]
        need((f['actor'],f['main'],f['owner'],f['id'],f['vactor'],f['vmain'],f['vowner'],f['vid'])==
             (actors[2],mains[2],actors[2],18,actors[1],mains[1],actors[1],17) and
             f['writes']==0 and f['assistance']=='none', 'Real CPU Sonya and human Kano, no assistance')
        values={actors[1]:dict(x=f['vxraw'],vx=f['vvx']),
                actors[2]:dict(x=f['xraw'],vx=f['vx'])}
        rows=[r for r in stores if int(r['frame'])==frame]; index=0
        while index<len(rows):
            r=rows[index]; slot=int(r['slot']); actor=actors[slot]; kind=r['kind']
            need(kind in ('x','vx') and (int(r['actor'],16),int(r['owner'],16),int(r['main'],16),int(r['id']))==
                 (actor,actor,mains[slot],16+slot) and r['writes']=='0' and r['assistance']=='none',
                 'Every store remains owned by its genuine physical actor')
            regs={n:int(r['a'+str(n)],16) for n in range(15)}
            status=int(r['status'],16); pc=int(r['pc'],16)
            base=actor+(0x80 if kind=='x' else 0x40)
            if pc==0xff8040b0:
                width=32; target=regs[3]; value=regs[9]; src=9; dst=3
                need(kind=='x' and target==base and value==(values[actor]['x']+values[actor]['vx'])&0xffffffff,
                     'Actual MMTM updated A3 and independently integrated X+VX source A9')
            elif pc in REG:
                op,offset,width=REG[pc]; src=(op>>5)&15; dst=op&15
                target=(regs[dst]+offset)&0xffffffff; value=regs[src]
                field=1 if op&0x200 else 0
                actual=(status>>(6 if field else 0))&31
                need((actual or 32)==width and not op&16,
                     'Actual native field width and A-register bank')
                need(target==base+(16 if width==16 else 0), 'Actual register/offset destination')
            else:
                need(pc in COPY,'No unaccounted native source site')
                op,off1,off2=COPY[pc]; src=(op>>5)&15; dst=op&15; width=32
                target=(regs[dst]+off2)&0xffffffff; source_at=(regs[src]+off1)&0xffffffff
                field=1 if op&0x200 else 0
                need(((status>>(6 if field else 0))&31)==0 and not op&16,
                     'Actual32-bit memory copy native field width and bank')
                need(target==base and regs[src] in values and source_at==regs[src]+(0x80 if kind=='x' else 0x40),
                     'Actual source and destination actor pointers, not inferred destination data')
                value=values[regs[src]][kind]; copies+=1
            halves=2 if width==32 else 1
            need(index+halves<=len(rows),'Both real halves of each32-bit instruction present')
            for half in range(halves):
                w=rows[index+half]; at=int(w['at'],16); bit=at-base
                need(at==target+half*16 and bit in (0,16) and
                     all(w[k]==r[k] for k in ('frame','slot','kind','pc','actor','owner','main','id','action','status',
                                            *('a'+str(n) for n in range(15)))),
                     'Adjacent native low/high callbacks retain all actual instruction operands')
                current=values[actor][kind]; before=int(w['before'],16)
                need((bit!=0 or before==current) and (before&65535)==((current>>bit)&65535) and
                     int(w['xraw'],16)==values[actor]['x'] and int(w['vx'],16)==values[actor]['vx'],
                     'Whole low pre-value and every high pre-word agree with ordered replay')
                mask=int(w['mask'],16); word=int(w['data'],16)
                # 16-bit offset stores address the upper physical X word,
                # but consume the LOW16 of their source register.
                source_bit=half*16
                need(mask==65535 and word==((value>>source_bit)&65535),
                     'Every data word equals independently observed native source operand')
                values[actor][kind]=(current&~(mask<<bit))|((word&mask)<<bit)
                sites[w['pc']]+=1
            instructions+=1; index+=halves
        need(values=={actors[1]:dict(x=following['vxraw'],vx=following['vvx']),
                      actors[2]:dict(x=following['xraw'],vx=following['vx'])},
             'Every native masked write explains both actors next complete physical field')
        snapshots+=2
    return dict(passed=True,first=FIRST,last=LAST,actualWordStores=sum(sites.values()),
        fullNativeInstructions=instructions,memoryCopyInstructions=copies,
        physicalNextFieldComparisons=snapshots,sourceSites=dict(sites),
        releasedHorizontalPushReplayAccepted=True,wholePreValuesAccepted=True,
        everySourceDestinationAndWidthAccepted=True,allContactsArenasAccepted=False,
        directContactInstructionTapAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable actual paired horizontal qualification')
    capture=contact.control.capture; held=capture.NATIVE_HANDLES[capture.KEY]
    parent=contact.OUT/'report.json'; channel=audio.OUT/'report.json'
    receipt=json.loads(parent.read_text()); channels=json.loads(channel.read_text())
    need(held['process'].poll()==0 and held['identity']['ProcessId']==50372 and
         receipt['passed'] and channels['passed'] and
         receipt['actualNativeIdentity']==channels['actualNativeIdentity']==held['identity'],
         'Same retained actual50372 terminal capture, not a new game')
    pins={}
    for report in (receipt,channels):
        for p,h in report['inputHashes'].items():
            need(p not in pins or pins[p]==h,'No original input pin replaced'); pins[p]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every complete original source/capture pin intact')
    _,text,_=capture.RAM_CASES[capture.KEY]; data=records(text)
    source_proof=source(state['guest']); positive=gate(data,state['guest']); faults=[]
    def trial(label,key,value,pc=None):
        bad=copy.deepcopy(data)
        row=next(r for r in bad['stores'] if pc is None or r['pc']==pc)
        need(row[key]!=value,'Effective actual operand fault'); row[key]=value
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError,KeyError) as error:
            faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual horizontal source fault accepted: '+label)
    for label,key,value,pc in (
        ('integrated_X','a9','00000000','FF8040B0'),
        ('MMTM_destination','a3','01000000','FF8040B0'),
        ('copy_X_source','a8','01000000','FF83CE90'),
        ('copy_X_destination','a0','01000000','FF83CE90'),
        ('copy_VX_source','a8','01000000','FFF9D270'),
        ('copy_VX_destination','a10','01000000','FFF9D270'),
        ('copy_width','status','00200430','FFF9D270'),
        ('human_requested_VX','a6','00000001','FF8285D0'),
        ('CPU_requested_VX','a7','00000001','FF8285B0'),
        ('paired_velocity','a0','00000001','FFF9DE50'),
        ('offset_X_source','a2','00000000','FF83CCD0'),
        ('offset_X_width','status','00200000','FF83CCD0'),
        ('whole_pre_value','before','00008000','FF8040B0'),
        ('word_mask','mask','0000FFFE','FF8040B0'),
        ('actor_owner','owner','01000000','FFF9D270'),
        ('data_word','data','00000001','FF8040B0')):
        trial(label,key,value,pc)
    for label,alter in (
        ('missing_real_high_half',lambda d:d['stores'].pop(1)),
        ('duplicate_real_word',lambda d:d['stores'].insert(1,copy.deepcopy(d['stores'][0]))),
        ('next_physical_X',lambda d:d['fields'][1].update(vxraw=d['fields'][1]['vxraw']^1))):
        bad=copy.deepcopy(data); alter(bad)
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError,KeyError) as error:
            faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual journal fault accepted: '+label)
    need(gate(data,state['guest'])==positive,'Whole untouched two-actor positive restored')
    for p in (Path(__file__),parent,channel,Path(contact.__file__),Path(audio.__file__),Path(gateway.__file__),
              ROOT/'audit_native_selector_sonya_cpu_air_sealed.json',
              ROOT/'mk2/mk2-maincpu.bin',ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'):
        key=str(p.resolve()); h=sha(p)
        need(key not in pins or pins[key]==h,'Executed source and old evidence immutable'); pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All complete pins unchanged after effective faults')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        pairedHorizontal=positive,exactNativeBoundary=source_proof,effectiveFaultsRejected=faults,
        inputHashes=pins,requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],
        allContactsArenasAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS721 actual both-actor x/vx stores through contact/release/recovery;19 effective faults',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual horizontal rejection')
        OUT.mkdir(); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
