"""Independently assemble native attract additions; no runtime acceptance."""
import copy
import gzip
import hashlib
import json
import struct
from pathlib import Path
import stock_slideshow_row40_context as prior

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
STAGE = ROOT / 'source_native_attract_bios'
OUT = ROOT / 'audit_native_attract_bios_source'
ROSTER = tuple(range(12)) + (17, 18)
STORIES = (
 ('CAPTURED BY SHAO KAHN,|THE BLACK DRAGON LEADER|IS HELD IN OUTWORLD.|HE SEES THE TOURNAMENT|AS A CHANCE TO ESCAPE.|',
  "NOW HE MUST FACE THE|WARRIORS OF A WORLD|RULED BY BRUTE FORCE.|WITH EARTH IN DANGER,|KANO HAS HIS OWN PLAN:|SURVIVE THE CONTEST|AND LEAVE WITH THE|EMPEROR'S RICHES."),
 ("AFTER SHANG TSUNG'S|DEFEAT, SONYA PURSUES|KANO INTO OUTWORLD.|TAKEN BY SHAO KAHN,|SHE REFUSES TO GIVE IN.|",
  'HER SIGNAL HAS DRAWN|JAX TO THE DARK REALM.|TOGETHER THEY MUST|ESCAPE THE EMPEROR|AND STOP HIS INVASION.|SONYA ENTERS THE|CONTEST TO SAVE HER|TEAM AND DEFEND EARTH.'))

def addr(byte): return 0xff800000 + byte * 8
def offset(bit): return (bit - 0xff800000) // 8
def u32(raw, at): return struct.unpack_from('<I', raw, at)[0]

def source_check():
    old = {n:(ROOT / 'source_stock_slideshow_row40' / n).read_text()
           for n in ('midtunit_m.cpp', 'midtunit.cpp', 'midtunit.h')}
    new = {n:(STAGE / n).read_text() for n in old}
    marker = '\t// Native attract biographies and CPU demonstrations share the biography\n'
    start = new['midtunit_m.cpp'].index(marker)
    end = new['midtunit_m.cpp'].index('\n}\n\n\nvoid midtunit_state::init_mk2ks_native_selector()', start)
    addition = new['midtunit_m.cpp'][start:end]
    text = new['midtunit_m.cpp'][:start-1] + new['midtunit_m.cpp'][end+1:]
    changes = (
      ('\tsave_item(NAME(m_mk2ks_battle_id));', '\tsave_item(NAME(m_mk2ks_battle_id));\n\tsave_item(NAME(m_mk2ks_battle_mode));'),
      ('\tm_mk2ks_battle_id[slot] = 0;', '\tm_mk2ks_battle_id[slot] = 0;\n\tm_mk2ks_battle_mode[slot] = 0;'),
      ('\t\tif (space.read_word(0x010601d0) != 2)', '\t\tuint16_t const mode = space.read_word(0x010601d0);\n\t\tif ((mode != 1 && mode != 2) || mode != m_mk2ks_battle_mode[slot] ||\n\t\t\t(mode == 1 && space.read_word(0x01061990) != 0))'),
      ('\t\t\t\t\tuint32_t const health[2] = { 0x010602f0, 0x01060ec0 };', '\t\t\t\t\tuint32_t const health[2] = { 0x010602f0, 0x01060ec0 };\n\t\t\t\t\tuint16_t const launch_mode = space.read_word(0x010601d0);'),
      ('\t\t\t\t\t\t\tspace.read_word(0x010601d0) != 2 || read32(actors[slot]) != actor || read32(mains[slot]) != main ||', '\t\t\t\t\t\t\t(launch_mode != 1 && launch_mode != 2) ||\n\t\t\t\t\t\t\t(launch_mode == 1 && space.read_word(0x01061990) != 0) ||\n\t\t\t\t\t\t\tread32(actors[slot]) != actor || read32(mains[slot]) != main ||'),
      ('\t\t\t\t\t\tm_mk2ks_battle_id[slot] = launch_id;', '\t\t\t\t\t\tm_mk2ks_battle_id[slot] = launch_id;\n\t\t\t\t\t\tm_mk2ks_battle_mode[slot] = launch_mode;'))
    expected = old['midtunit_m.cpp']
    for a,b in changes:
        need(expected.count(a) == 1, 'Unique exact host audio delta')
        expected = expected.replace(a,b,1)
    need(text == expected, 'Entire previous implementation unchanged except appended native code and six host mode ownership deltas')
    need(new['midtunit.cpp'] == old['midtunit.cpp'], 'Machine/sample/DCS configuration unchanged')
    a = '\tuint16_t m_mk2ks_battle_id[2] = {};'
    need(new['midtunit.h'] == old['midtunit.h'].replace(a,a+'\n\tuint16_t m_mk2ks_battle_mode[2] = {};',1), 'Only saved host audio mode added to header')
    for stories in STORIES:
        for story in stories:
            need('"' + story.replace('|','\\\\n') + '"' in addition, 'Exact independently authored native biography text')
            lines = story.rstrip('|').split('|')
            need(max(map(len,lines)) <= 23 and len(lines) <= 8, 'Native biography width and row capacity')
    return {n:sha(STAGE/n) for n in old}, addition

def expected_guest(base=None):
    if base is None: base = prior.expected()
    guest = bytearray(base)
    for a,b in ((0xf3780,0xf390c),(0xf6e40,0xf7000),(0xf7300,0xf7600),
                (0xf6730,0xf6830),(0xf49d8,0xf49e0)):
        need(base[a:b] == b'\xff'*(b-a), 'Every allocated native storage byte was genuinely unused')
    expected_hooks = {0xff84a3b0:'a005a01c0601',0xff84a540:'084c400bfdff',
      0xff84a7d0:'004d000b1c00',0xff8278d0:'a005a01c0601',
      0xff827970:'80195f0de0ea',0xff8475e0:'80195f0de0ea'}
    for bit,raw in expected_hooks.items():
        need(base[offset(bit):offset(bit)+6] == bytes.fromhex(raw), 'Entire stolen native hook prefix preserved before patch')
    need(u32(base,offset(0xff84a5f0)) == 0xff84a900, 'Original biography text table operand')
    def put32(at,value): struct.pack_into('<I',guest,at,value)
    def put16(at,value): struct.pack_into('<H',guest,at,value)
    def puttext(at,header,text):
        raw = header + text.encode('ascii') + b'\0'
        need(len(raw) <= 256, 'Complete native text including header and terminator fits')
        guest[at:at+len(raw)] = raw
    source_table = offset(0xff84a900)
    guest[0xf3780:0xf3810] = base[source_table:source_table+144]
    guest[0xf3810:0xf3864] = bytes(84)
    locations = ((0xf7300,0xf7400),(0xf7500,0xf6730))
    for i,label in enumerate(('KANO','SONYA')):
        name = 0xf3870 + i*64
        header = offset(u32(base,source_table+8*12))
        puttext(name,base[header:header+24],label)
        put32(0xf3780+(17+i)*12,addr(name))
        for j,story in enumerate(STORIES[i]):
            header = offset(u32(base,source_table+8*12+(j+1)*4))
            puttext(locations[i][j],base[header:header+24],story.replace('|','\\n'))
            put32(0xf3780+(17+i)*12+(j+1)*4,addr(locations[i][j]))
        put32(0xf4900+(54+i)*4,u32(base,0xf4860+(17+i)*4))
    for i,value in enumerate(ROSTER): put16(0xf38f0+i*2,value)
    put32(offset(0xff84a5f0),addr(0xf3780))
    cursor = 0xf6e40
    entries, labels, fixups = {}, {}, []
    def emit(*words):
        nonlocal cursor
        for word in words: put16(cursor,word);cursor += 2
    def branch(op,target):
        emit(op)
        if isinstance(target,str): fixups.append((cursor,target));emit(0,0)
        else:emit(target & 0xffff,target >> 16)
    def label(name): labels[name] = addr(cursor)
    entries[0xff84a3b0] = addr(cursor)
    emit(0x05a0,0x1ca0,0x0106,0x1020,0x0b40,0xfff4);branch(0xc280,'rotate_ready')
    emit(0x0b40,0xfff3);branch(0xca80,'rotate_kano')
    emit(0x0b40,0xffed);branch(0xca80,'rotate_ready')
    emit(0x5600);branch(0xc080,'rotate_ready')
    label('rotate_kano');emit(0x09c0,17)
    label('rotate_ready');branch(0xc080,0xff84a430)
    entries[0xff84a540] = addr(cursor)
    emit(0x4c08,0x0b40,0xffee);branch(0xca80,'picture_kano')
    emit(0x0b40,0xffed);branch(0xca80,'picture_sonya')
    emit(0x0b40,0xfffd);branch(0xcb80,0xff84a5a0);branch(0xc080,0xff84a580)
    label('picture_kano');emit(0x09c8,54);branch(0xc080,0xff84a5a0)
    label('picture_sonya');emit(0x09c8,55);branch(0xc080,0xff84a5a0)
    entries[0xff84a7d0] = addr(cursor)
    emit(0x0b48,0xffee);branch(0xca80,'voice_kano')
    emit(0x0b48,0xffed);branch(0xca80,'voice_sonya')
    emit(0x4d00,0x0b00,0x001c,0x0d5f,0x2430,0xffa1);branch(0xc080,0xff84a830)
    label('voice_kano');emit(0x09c0,0xfffc);branch(0xc080,'voice_mute')
    label('voice_sonya');emit(0x09c0,0xfffb)
    label('voice_mute');emit(0x05b3,0x1990,0x0106);branch(0xcb80,0xff84a830)
    emit(0x0580,0x1030,0x01d0);branch(0xc080,0xff84a830)
    entries[0xff8278d0] = addr(cursor)
    emit(0x05a0,0x1ca0,0x0106,0x0b40,0xfff4);branch(0xc280,'demo_ready')
    emit(0x0b40,0xffee);branch(0xca80,'demo_ready')
    emit(0x0b40,0xffed);branch(0xca80,'demo_ready')
    emit(0x1820);label('demo_ready');branch(0xc080,0xff827940)
    for hook,resume in ((0xff827970,0xff8279c0),(0xff8475e0,0xff847630)):
        entries[hook] = addr(cursor)
        emit(0x19c0,0x0d5f,0xeae0,0xff80,0x1420,0x2480,0x0b20,
             addr(0xf38f0)&0xffff,addr(0xf38f0)>>16,0x8400);branch(0xc080,resume)
    need(cursor <= 0xf7000, 'All six native trampolines within reserved code hole')
    for at,name in fixups: put32(at,labels[name])
    for hook,target in entries.items():
        struct.pack_into('<HI',guest,offset(hook),0xc080,target)
    return bytes(guest), dict(entries=entries,codeStart=0xf6e40,codeEnd=cursor)

def execute(guest,start,counter=0,a0=0,a8=0,mute=0,rng=1):
    """Small ISA test over emitted words, not the implementation's C++ branches."""
    pc = u32(guest,offset(start)+2)
    regs = {0:a0,8:a8,19:0}
    zero,lower = False,False
    calls,ports = [],[]
    for step in range(80):
        at = offset(pc)
        if not 0xf6e40 <= at < 0xf7000: return dict(pc=pc,a0=regs[0],a8=regs[8],calls=calls,ports=ports)
        word = struct.unpack_from('<H',guest,at)[0];pc += 16
        def arg():
            nonlocal pc
            value = struct.unpack_from('<H',guest,offset(pc))[0];pc += 16;return value
        def arg32(): return arg() | (arg()<<16)
        if word in (0xc080,0xc280,0xca80,0xcb80):
            target=arg32()
            if word==0xc080 or (word==0xc280 and lower) or (word==0xca80 and zero) or (word==0xcb80 and not zero):pc=target
        elif word in (0x05a0,0x05b3):
            address=arg32();need(address in (0x01061ca0,0x01061990),'Expected passive native read')
            r=0 if word==0x05a0 else 19;regs[r]=counter if r==0 else mute;zero=regs[r]==0
        elif word in (0x1020,0x1420):regs[0]=(regs[0]+(1 if word==0x1020 else -1))&0xffff
        elif word in (0x0b40,0x0b48):
            value=arg()^0xffff;r=word&15;zero=regs[r]==value;lower=regs[r]<=value
        elif word==0x5600:regs[0]=0
        elif word in (0x09c0,0x09c8):regs[word&15]=arg()
        elif word==0x4c08:regs[8]=regs[0]
        elif word==0x4d00:regs[0]=regs[8]
        elif word==0x0b00:regs[0]+=arg()
        elif word==0x0d5f:
            target=arg32();calls.append((target,regs[0]))
            if target==0xff80eae0:
                need(regs[0]==14 and 1<=rng<=14,'Unchanged native random call, legal count14');regs[0]=rng
        elif word==0x0580:ports.append((arg32(),regs[0]))
        elif word==0x1820:regs[0]=1
        elif word==0x19c0:regs[0]=14
        elif word==0x2480:regs[0]<<=4
        elif word==0x0b20:regs[0]+=arg32()
        elif word==0x8400:regs[0]=struct.unpack_from('<H',guest,offset(regs[0]))[0]
        else:raise ValueError('Unexpected emitted native opcode '+hex(word))
    raise ValueError('Native trampoline does not return')

def semantics(guest):
    for i,value in enumerate(ROSTER):
        result=execute(guest,0xff84a3b0,counter=value)
        need(result['a0']==ROSTER[(i+1)%14] and result['pc']==0xff84a430,'Entire native fourteen-character biography rotation')
        result=execute(guest,0xff8278d0,counter=value)
        need(result['a0']==value and result['pc']==0xff827940,'Real attract P1 ID never proxied')
        for hook in (0xff827970,0xff8475e0):
            need(execute(guest,hook,rng=i+1)['a0']==value,'Every actual RNG result maps to legal real roster')
        pic=execute(guest,0xff84a540,a0=value)
        expected=54 if value==17 else 55 if value==18 else value
        need(pic['a0']==value and pic['a8']==expected and pic['pc']==(0xff84a580 if value==2 else 0xff84a5a0), 'ID preserved independently of native biography picture index')
        for mute in (0,1):
            voice=execute(guest,0xff84a7d0,a8=value,mute=mute)
            need(voice['pc']==0xff84a830,'Original voice task resumes its own wait/cleanup')
            if value<12:need(voice['calls']==[(0xffa12430,value+28)] and not voice['ports'],'Original stock announcer unchanged')
            else:need(not voice['calls'] and voice['ports']==([] if mute else [(0x01d01030,0xfffc if value==17 else 0xfffb)]),'Correct real name and original native mute gate')
    for value in (12,13,14,15,16,19,0xffff):
        need(execute(guest,0xff8278d0,counter=value)['a0']==1,'Original invalid demo fallback retained only for invalid IDs')
    need(tuple(struct.unpack_from('<14H',guest,0xf38f0))==ROSTER,'Typed ordinary roster excludes secret/boss IDs')

def main():
    need(not OUT.exists(),'Fresh immutable source proof')
    sources,addition=source_check()
    base=prior.expected();guest,assembly=expected_guest(base);semantics(guest)
    faults=[]
    for label,at,value in (('proxy Kano',0xf38f0+24,1),('boss RNG row',0xf38f0+26,12),
                          ('wrong own portrait',offset(0xff84a540)+2,addr(0xf6e40)),
                          ('wrong real announcer',0xf6e40+140,0)):
        bad=bytearray(guest);struct.pack_into('<H',bad,at,value&0xffff)
        try:semantics(bad)
        except (ValueError,struct.error) as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Mutated native attract code unexpectedly accepted: '+label)
    need(guest[0xf4900:0xf49d8]==base[0xf4900:0xf49d8], 'Entire forty-one stock pictures and four K/S ending pointers unchanged')
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__)):sha(prior.__file__),
          str(ROOT/prior.NAME/'build-info.json'):sha(ROOT/prior.NAME/'build-info.json')}
    for name in sources:pins[str(STAGE/name)]=sha(STAGE/name)
    result=dict(passed=True,sourceOnlyAccepted=True,nativeFixAccepted=False,fullPortAcceptance=False,
      stagedSourceHashes=sources,proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
      expectedGuestChangedBytes=sum(a!=b for a,b in zip(base,guest)),nativeCodeBytes=assembly['codeEnd']-assembly['codeStart'],
      actualRecordFaultsRejected=faults,assembly=assembly,roster=ROSTER,inputHashes=pins,
      scope='Native biographies, real-ID CPU demos, original RNG call with typed14 roster, scene-owned/mute-respecting startup audio. Runtime not yet tested.',
      publicBuildPromoted=False,goalStatus='active')
    OUT.mkdir()
    with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump({k:dict(sha256=sha(k),text=Path(k).read_text()) for k in pins if str(k).endswith(('.cpp','.h','.py'))},f)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','sourceOnlyAccepted','proposedGuestSHA256','expectedGuestChangedBytes','nativeCodeBytes','nativeFixAccepted')}))

if __name__=='__main__': main()
